#!/usr/bin/env python3
import sys
import re
import urllib.request

SYNAPSE = "https://matrix.oliviervandertoorn.nl/_synapse/metrics"


def get_data():
    with urllib.request.urlopen(SYNAPSE) as f:
        data = f.read()
        lines = str(data, 'utf-8')

    return lines


def find_str(lines, string):
    return re.search(string, lines)


def main():
    if len(sys.argv) < 2:
        print(0)
        return

    string = sys.argv[1]
    lines = get_data()
    match = find_str(lines, r'{0}.+?(\d+.\d+)'.format(string))
    if match:
        print(match.group(1))


if __name__ == '__main__':
    main()
