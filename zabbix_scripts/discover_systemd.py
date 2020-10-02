#!/usr/bin/env python3
"""Author:      Olivier van der Toorn <olivier@snt.utwente.nl>
Description:    Zabbix discovery script for finding systemd services.
"""
import json
import subprocess
import re


def main():
    """Main discovery function.
    {#SERVICENAME} is a modified version to remove 'illegal' characters.
    """
    command = [
        'systemctl',
        '--type=service',
        '--no-legend',
        '--no-pager',
    ]
    try:
        process = subprocess.run(
            command,
            stdout=subprocess.PIPE)
        output = str(process.stdout, 'utf-8')

    except subprocess.CalledProcessError:
        output = ''

    services = []
    for line in output.split('\n'):
        if line:
            match = re.match(r'.*?([A-Za-z0-9]+[.]service).*', line)
            if match:
                name = match.group(1)
                name = name.replace('@', '--at--')
                name = name.replace('\\', '--backslash--')
                services.append({
                    '{#NAME}': name,
                    '{#SERVICENAME}': name,
                })

    data = {'data': services}
    return json.dumps(data, sort_keys=True, indent=4)


if __name__ == '__main__':
    print(main())  # pragma: no cover
