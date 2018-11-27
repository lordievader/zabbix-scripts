#!/usr/bin/env python3
""" Description: Pulls urls and ports from /etc/zabbix/urls.txt
                 for Zabbix to monitor.
Author:      Olivier van der Toorn <oliviervdtoorn@gmail.com>"""
import json


def main():
    """Reads /etc/zabbix/ports.txt for ports to monitor.
    """
    urls = []
    try:
        with open('/etc/zabbix/ports.txt', 'r') as url_file:
            lines = url_file.readlines()

        for line in lines:
            line = line.replace('\n', '')
            try:
                port = line

            except ValueError:
                pass

            urls.append({
                '{#PORT}': port
            })

    except (FileNotFoundError, PermissionError):
        pass

    data = {'data': urls}
    print(json.dumps(data, sort_keys=True, indent=4))


if __name__ == '__main__':
    main()
