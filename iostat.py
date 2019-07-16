#!/usr/bin/env python3
"""Author:      Olivier van der Toorn <oliviervdtoorn@gmail.com>
Description:    Pusher of iostat data to Zabbix.
"""
import threading
import subprocess
import select
import queue
import signal
import sys
import time
import pdb
import re
import socket

import yaml
from pyzabbix import ZabbixMetric, ZabbixSender


whitespace = re.compile(r'\ +')
stats_queue = queue.Queue()
control_queue = queue.Queue()


def producer():
    """Reads values from the iostat process and pushes them to the queue.
    """
    command = ['iostat', '-Nxy', str(config['interval'])]
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        if control_queue.empty() is False:
            command = control_queue.get()
            if command == 'SIGINT':
                process.terminate()
                break

        if len(select.select([process.stdout], [], [], 0)[0]) > 0:
            line = str(process.stdout.readline(), 'utf-8').replace('\n', '')
            if line.count('Device') > 0:
                continue

            parts = whitespace.split(line)
            if len(parts) == 16:
                disk = parts[0]
                data = {}
                for key, value in config['keys'].items():
                    data[key] = parts[value]

                stats_queue.put((disk, data))

        else:
            time.sleep(1)

    control_queue.task_done()


def signal_handler(signum, frame):
    """Controls the SIGINT.
    """
    control_queue.put('SIGINT')
    control_queue.join()
    sys.exit()


def main():
    hostname = socket.gethostname()
    zabbix = ZabbixSender(zabbix_server=config['zabbix_server'])
    while True:
        packets = []
        while stats_queue.empty() is False:
            disk, data = stats_queue.get()
            packets.extend(
                [ZabbixMetric(hostname, f'iostat[{disk},{key}]', value)
                 for key, value in data.items()])

        if packets:
            result = zabbix.send(packets)
            print(packets, result)

        time.sleep(1)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    path = 'iostat.yml'
    with open(path, 'r') as config_file:
        config = yaml.load(config_file, Loader=yaml.Loader)

    t = threading.Thread(target=producer)
    t.daemon = True
    t.start()
    # del t

    main()
