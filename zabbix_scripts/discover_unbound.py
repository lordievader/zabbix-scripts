#!/usr/bin/env python3
"""Author:      Olivier van der Toorn <oliviervdtoorn@gmail.com>
Description:    Discovers the statistics exported by `unbound-control stats`.
"""
import subprocess
import re
import json


REGEX = re.compile(r'([A-Za-z0-9.]+[.][A-Za-z0-9]+)=.*')


def main():
    """Main function
    """
    command = 'sudo unbound-control stats'
    output = subprocess.getoutput(command)
    stats = []
    if output:
        lines = output.split('\n')
        for line in lines:
            match = REGEX.match(line)
            if match:
                name = match.group(1)
                key = name.replace('.', '')
                stats.append({
                    '{#NAME}': name,
                    '{#KEY}': key,
                })

    data = {'data': stats}
    return json.dumps(data, sort_keys=True, indent=4)


if __name__ == '__main__':
    print(main())  # pragma: no cover
