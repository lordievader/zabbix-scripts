#!/usr/bin/env python3
""" Description: Allows Zabbix to discover files in a given directory.
Author:      Olivier van der Toorn <oliviervdtoorn@gmail.com>"""
import os
import sys
import json


def main():
    """Uses os to list files in a directory.
    """
    try:
        folder = sys.argv[1]

    except IndexError:
        folder = '/'

    files = [
        {
            '{#NAME}': _file,
            '{#PATH}': os.path.join(folder, _file)
        } for _file in os.listdir(folder)
        if os.path.isfile(
            os.path.join(folder, _file))]
    data = {'data': files}
    return json.dumps(data, sort_keys=True, indent=4)


if __name__ == '__main__':
    print(main())
