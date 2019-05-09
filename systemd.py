#!/usr/bin/env python3
"""Script to monitor Systemd services.
"""
import subprocess
import argparse


def check_service(service_name):
    """Checks the status of a systemd service.
    """
    command = [
        'systemctl',
        'is-active',
        service_name,
    ]
    active = 1
    try:
        process = subprocess.run(
            command,
            stdout=subprocess.PIPE)
        output = str(process.stdout, 'utf-8')
        output = output.replace('\n', '')
        if output == 'active':
            active = 0

    except subprocess.CalledProcessError:
        active = 2

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
