#!/usr/bin/env python3
"""Author:      Olivier van der Toorn <oliviervdtoorn@gmail.com>
Description:    Discovers the statistics exported by `unbound-control stats`.
"""
import subprocess
import re
import json


REGEX = re.compile(r'([A-Za-z0-9.]+[.][A-Za-z0-9]+)=(.*)')


def main():
    """Main function
    """
    command = 'sudo unbound-control stats'
    output = subprocess.getoutput(command)
    stats = {}
    if output:
        lines = output.split('\n')
        for line in lines:
            match = REGEX.match(line)
            if match:
                key = match.group(1).replace('.', '')
                value = float(match.group(2))
                stats[key] = value
    
    data = {'data': stats}
    return json.dumps(data, sort_keys=True, indent=4)


if __name__ == '__main__':
    print(main())  # pragma: no cover
