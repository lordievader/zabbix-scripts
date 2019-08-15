#!/usr/bin/env python3
"""Author:      Olivier van der Toorn <oliviervdtoorn@gmail.com>
Description:    Discovery script for key values used by the iostat.py script.
"""
import subprocess
import json
import yaml
import re
import pdb

strip = re.compile(r'\ .*$')

def blockdevices():
    """Enumerates the blockdevices returned by iostat.
    """
    devices = []
    try:
        output = subprocess.getoutput('iostat -N')
        for line in output.split('\n')[6:]:
            line = strip.sub('', line)
            if line:
                devices.append(
                    {
                        '{#BLOCK}': line
                    }
                )

    except subprocess.CalledProcessError:
        pass

    return devices


def main():
    devices = blockdevices()
    data = {'data': devices}
    return json.dumps(data, sort_keys=True, indent=4)

if __name__ == '__main__':
    print(main())
