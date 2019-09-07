#!/usr/bin/env python3
""" Description: Pulls the amount of clustermanagers from /etc/clustermanager
                 for Zabbix to monitor.
Author:      Olivier van der Toorn <o.i.vandertoorn@utwente.nl>"""
import json
import re


def main():
    """Reads /etc/clustermanager for measurements to monitor.
    """
    clustermanagers = []
    try:
        with open('/etc/clustermanager', 'r') as clustermanager_file:
            lines = clustermanager_file.readlines()

        for line in lines:
            line = line.replace('\n', '')
            match = re.match(r'([a-zA-Z0-9 ]+?) +([0-9]+)$', line)
            name = match.group(1)
            index = match.group(2)
            clustermanagers.append({
                '{#CMNAME}': name,
                '{#CMINDEX}': index
            })

    except (FileNotFoundError, PermissionError):
        pass

    data = {'data': clustermanagers}
    return json.dumps(data, sort_keys=True, indent=4)


if __name__ == '__main__':
    print(main())  # pragma: no cover
