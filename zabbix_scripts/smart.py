#!/usr/bin/env python3
"""Description: Allow Zabbix to monitor smartvalues.
Author: Olivier van der Toorn <oliviervdtoorn@gmail.com>
"""
import sys
import subprocess
import re


def smartvalues(disk):
    """Retrieve the smartvalues for the given disk.

    :param disk: disk to check output for
    :type disk: str
    :return: smartctl output
    """
    command = ['sudo', 'smartctl', '-A', disk]
    output = subprocess.getoutput(" ".join(command))
    return output


def filter_output(attribute, output):
    """Filter the output, looking for the given attribute.

    :param attribute: string to look for
    :type attribute: str
    :param output: output from smartctl
    :type output: str
    :return: line containing attribute
    """
    for line in output.split('\n'):
        if attribute in line:
            break

    else:
        line = "0"

    return line


def main(*args):
    """Main function calls all the other functions.
    """
    if len(args) == 1:
        disk = args[0]
        return smartvalues(disk)

    elif len(args) == 2:
        disk = args[0]
        attribute = args[1]
        output = filter_output(
            attribute, smartvalues(disk))
        splitted_data = re.split(r'\s+', output.lstrip())
        if len(splitted_data) >= 10:
            value = int(splitted_data[9])

        else:
            value = 0

        return value

    return 0


def init():
    """Ensures 100% code coverage.
    """
    if __name__ == '__main__':
        value = main(*sys.argv[1:])
        print(value)
        return value


init()
