#!/usr/bin/python3
"""Author:      Olivier van der Toorn <oliviervdtoorn@gmail.com>
Description:    Discovery script for key values used in Synapse metrics.
"""
import json
import logging
import re
import urllib.request
import yaml
import zbxtoolkit
from tqdm import tqdm

KEYS_REGEX = re.compile(
    r'^([A-Za-z0-9_{}=\",.-]+) [0-9]+[.][0-9]+',
    re.MULTILINE)
WHITELIST = [
    'process_cpu_seconds_total',
    'process_resident_memory_bytes',
    'process_open_fds',
    'synapse_http_client_responses',
    'synapse_http_server_responses',
    'synapse_federation_client_sent_edus',
    'synapse_federation_client_sent_pdu_destinations',
    'synapse_federation_client_sent_queries',
    'synapse_federation_client_sent_transactions',
    'synapse_federation_server_received_edus',
    'synapse_federation_server_received_pdus',
    'synapse_federation_server_received_queries',
    'synapse_federation_transaction_queue_pending_',
    'synapse_storage_events_persisted_events',
    'synapse_notifier_listeners',
    'synapse_notifier_rooms',
    'synapse_http_server_response_ru_utime_seconds',
    'synapse_http_server_response_db_txn_duration_seconds',
    'synapse_replication_tcp_protocol_inbound_commands',
    'synapse_util_caches_cache:size',
]


def get_or_create(template_host, template_name, zapi=None):
    """Function to return the template or create a new one.

    :param template_host: technical name of the template
    :type template_host: str
    :param template_name: friendly name of the template
    :type template_name: str
    :param zapi: reference to the ZabbixAPI
    :type zapi: ZabbixAPI
    :returns: id of template
    """
    if zapi is None:
        zapi = zbxtoolkit.init()

    try:
        template = zbxtoolkit.template(template_name, zapi)

    except RuntimeError:
        logging.debug("creating template")
        template_group = zbxtoolkit.group('Templates', zapi)
        zbxtoolkit.template_create(
            template_group, template_host, template_name, zapi)
        template = zbxtoolkit.template(template_name, zapi)


    return template


def create_master_items(template, config, zapi=None):
    """Creates the base structure of the monitoring template.

    :param template: reference to the template
    :type template: dict
    :param config: configuration of synapse
    :type config: dict
    :param zapi: reference to the ZabbixAPI
    :type zapi: ZabbixAPI
    """
    try:
        application = zbxtoolkit.application(
            'Synapse::Metrics',
            {'templateids': template['templateid']},
            zapi
        )

    except RuntimeError:
        application = zbxtoolkit.application_create(
            'Synapse::Metrics',
            template,
            zapi)

    for name, address in config['synapse'].items():
        if name == 'hostname':
            continue

        params = {
            'delay': '1m',
            'hostid': template['templateid'],
            'name': f'Synapse: {name} metrics',
            'key_': f'synapse_{name}_ng',
            'type': 19,
            'url': f'http://{address}/_synapse/metrics/',
            'value_type': 4,
            'history': '1d',
            'applications': [
                application['applicationid'],
            ],
        }
        try:
            zapi.item.create(**params)  # TODO: port to zbxtoolkit

        except Exception as error:
            logging.error(error)


def gather(url):
    """Gathers a URL.

    :param url: URL to retrieve
    :type url: str
    """
    with urllib.request.urlopen(url) as response:
        html = response.read()

    return html


def parse(content):
    """Parses the content into keys only.

    :param content: content to parse
    :type content: string
    """
    html = str(content, 'utf-8')
    keys = re.findall(KEYS_REGEX, html)
    return keys


def create_slave_items(template, config, zapi=None):
    """Creates the items ready for monitoring.
    """
    try:
        application = zbxtoolkit.application(
            'Synapse::Metrics',
            {'templateids': template['templateid']},
            zapi
        )

    except RuntimeError:
        application = zbxtoolkit.application_create(
            'Synapse::Metrics',
            template,
            zapi)

    keys = {}
    for name, address in config['synapse'].items():
        if name != 'hostname':
            url = f'http://{address}/_synapse/metrics'
            logging.debug(f'gathering {url}')
            content = gather(url)
            if name in keys:
                keys[name].expand(parse(content))

            else:
                keys[name] = parse(content)

    for name, items in tqdm(keys.items()):
        master_item = zbxtoolkit.item(
            f'Synapse: {name} metrics',
            params={'templateid': template['templateid']},
            zapi=zapi)
        for key in tqdm(items):
            for item in WHITELIST:
                if item in key:
                    break

            else:
                continue

            key_ = re.sub(r'[{}"=,:]', '', key)
            key_ = f'{name}_{key_}'
            params = {
                #'delay': '1m',
                'hostid': template['templateid'],
                'name': f'Synapse: {name} {key}',
                'key_': key_,
                'type': 18,
                'value_type': '0',
                'history': '1d',
                'master_itemid': master_item['itemid'],
                'preprocessing': [
                    {
                        'type': '5',
                        'params': f'{key} ([0-9]+[.][0-9]+(e[+][0-9]+)*)\n\\1',
                        'error_handler': '0',
                        'error_handler_params': '',
                    },
                ],
                'applications': [
                    application['applicationid'],
                ],
            }
            zbxtoolkit.item_create(params, zapi)


def main():
    """Main function.
    """
    config = zbxtoolkit.read_config()
    zapi = zbxtoolkit.init(config)
    hostname = config['synapse']['hostname']
    _hostname = hostname.capitalize().replace('-', '')
    template_name = f'Templates::Hosts::{_hostname}::Synapse'
    template_host = f't_hosts_{hostname.replace("-", "")}_synapse'
    template = get_or_create(template_host, template_name, zapi)
    create_master_items(template, config, zapi)
    create_slave_items(template, config, zapi)


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s: %(levelname)8s - %(message)s',
        level='WARN')
    main()
