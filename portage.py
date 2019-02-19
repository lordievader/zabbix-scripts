#!/usr/bin/env python3
"""Script to monitor portage things.
"""
import subprocess
import argparse


def updates():
    """Counts how many packages can be updated.
    """
    packages = 0
    test = 'test -f "$(which eix)"'
    try:
        subprocess.check_call(test, shell=True)
        command = '$(which eix) --installed --upgrade -#'
        output = subprocess.getoutput(command)
        if output:
            packages = len(output.split('\n'))

    except subprocess.CalledProcessError:
        pass

    return packages


def main():
    """Main function.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('keyword', type=str, nargs=1)
    arguments = parser.parse_args()
    if arguments.keyword[0] == 'updates':
        data = updates()

    else:
        data = 0

    print(data)

if __name__ == "__main__":
    main()
