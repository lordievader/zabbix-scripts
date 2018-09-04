#!/usr/bin/env python3
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


def main():
    """Main function calls all the other functions.
    """
    if len(sys.argv) < 2:
        return

    elif len(sys.argv) < 3:
        disk = sys.argv[1]
        print(smartvalues(disk))

    else:
        disk = sys.argv[1]
        attribute = sys.argv[2]
        output = filter_output(
                attribute, smartvalues(disk))
        value = re.split(r'\s+', output)[9]
        print(value)


if __name__ == '__main__':
    main()
