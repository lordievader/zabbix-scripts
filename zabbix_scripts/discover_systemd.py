#!/usr/bin/env python3
"""Author:      Olivier van der Toorn <olivier@snt.utwente.nl>
Description:    Zabbix discovery script for finding systemd services.
"""
import json
import subprocess


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
            line = line.split(' ')
            line = list(filter(None, line))
            name = line[0]
            name = name.replace('@', '--at--')
            name = name.replace('\\', '--backslash--')
            services.append({
                '{#NAME}': line[0],
                '{#SERVICENAME}': name,
            })
            # load = line[1]
            # active = line[2]
            # sub = line[3]
            # description = " ".join(line[4:])

    data = {'data': services}
    return json.dumps(data, sort_keys=True, indent=4)


if __name__ == '__main__':
    print(main())
