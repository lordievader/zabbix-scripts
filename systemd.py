#!/usr/bin/env python3
"""Script to monitor Systemd services.
"""
import subprocess
import argparse


def check_service(service_name):
    """Checks the status of a systemd service.
    This function can return a value between 0 and 2.
    0: service is active
    1: service is not active
    2: service has failed
    3: service in unkown state
    255: an error in the process occured

    :return: int active
    """
    command = [
        'systemctl',
        'is-active',
        service_name,
    ]
    active = 255
    try:
        process = subprocess.run(
            command,
            stdout=subprocess.PIPE)
        output = str(process.stdout, 'utf-8')
        output = output.replace('\n', '')
        if output == 'active':
            active = 0

        elif output == 'in-active':
            active = 1

        elif output == 'failed':
            active = 2

        else:
            active = 3

    except subprocess.CalledProcessError:
        active = 255

    return active


def main():
    """Main function.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('service', type=str, nargs=1)
    arguments = parser.parse_args()
    service_name = arguments.service[0]
    service_name = service_name.replace('--at--', '@')
    service_name = service_name.replace('--backslash--', '\\')
    return check_service(service_name)


if __name__ == '__main__':
    print(main())
