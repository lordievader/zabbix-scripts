#!/usr/bin/env python3
"""Test for the ovirt api.
"""
import logging
import json
import sys
import configparser

import ovirtsdk4 as sdk


def connect(cfg):
    """Sets up a connection to the ovirt api.

    :param cfg: configparser
    :type cfg: configparser.ConfigParser()
    :return: API connection
    """
    connection = sdk.Connection(
        url=cfg.get('ovirt', 'api_url'),
        username=cfg.get('ovirt', 'api_user'),
        password=cfg.get('ovirt', 'api_password'),
        ca_file=cfg.get('ovirt', 'api_ca_file'),
        debug=False,
        log=logging.getLogger(),
    )
    logging.debug('connected to the API')
    return connection


def retrieve_properties(virtual_machine):
    """Retrieves all the (string like) properties of a virtual machine.

    :param virtual_machine: a virtual machine to process
    :type virtual_machine: vm object as returned by the API
    :return: json parsed dictionary
    """
    properties = {}
    for attr in dir(virtual_machine):
        if attr.startswith('_') is False:
            value = getattr(virtual_machine, attr)
            properties[attr] = str(value)

    return json.dumps(properties, sort_keys=True, indent=4)


def discover(cfg, connection):
    """Discover all the running virtual machines on the ovirt instance.

    :param cfg: config parser
    :type cfg; configparser.ConfigParser
    :param connection: the connection to the ovirt api
    :type connection: sdk.Connection
    :return: list of machines
    """
    system_service = connection.system_service()
    vms_service = system_service.vms_service()
    virtual_machines = vms_service.list()

    machines = []
    for virtual_machine in virtual_machines:
        if virtual_machine.status.value != 'up':
            continue

        if virtual_machine.fqdn is not None:
            fqdn = virtual_machine.fqdn

        else:
            fqdn = "{0}.{1}".format(
                virtual_machine.name,
                cfg.get('ovirt', 'domain'))

        machine = {
            '{#VMNAME}': virtual_machine.name,
            '{#FQDN}': fqdn,
        }
        machines.append(machine)

    return machines


if __name__ == '__main__':
    cfg = configparser.ConfigParser()
    cfg.read('conf.ini')

    logging.basicConfig(level=cfg.get('ovirt', 'log_level'))
    connection = connect(cfg)
    machines = discover(cfg, connection)
    data = {'data': machines}
    connection.close()

    print(json.dumps(data, sort_keys=True, indent=4))
