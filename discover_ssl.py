#!/usr/bin/env python3
""" Description: Pulls urls and ports from /etc/zabbix/urls.txt
                 for Zabbix to monitor.
Author:      Olivier van der Toorn <oliviervdtoorn@gmail.com>"""
import json


def main():
    """Reads /etc/zabbix/urls.txt for URLs to monitor.
    """
    urls = []
    try:
        with open('/etc/zabbix/urls.txt', 'r') as url_file:
            lines = url_file.readlines()

        for line in lines:
            line = line.replace('\n', '')
            try:
                url, port = line.split(':')

            except ValueError:
                url = line
                port = '443'

            urls.append({
                '{#URL}': url,
                '{#PORT}': port
            })

    except FileNotFoundError:
        pass

    data = {'data': urls}
    print(json.dumps(data, sort_keys=True, indent=4))


if __name__ == '__main__':
    main()
