#!/usr/bin/env python3
"""Description: Allows Zabbix to monitor lvm values
Author:         Olivier van der Toorn <oliviervdtoorn@gmail.com>
"""
import sys
import subprocess
import json
import re
import pdb


def filter_digits(string):
    """Grabs the digits from the input string.

    :param string: input string
    :type string: str
    :return: digits from the input string
    """
    value = re.sub(r'[^0-9a-z,.]', '', string)
    if value == '':
        value = 0

    return value


def run_command(lvm, option):
    """Runs an lvm command with the specified options.
    """
    option = option
    command = [
        'sudo', lvm, '--unbuffered', '--noheadings', '--nosuffix',
        '--units', 'b', '--reportformat', 'json', '-o', option]
    process = subprocess.run(
        command,
        stdout=subprocess.PIPE)
    # output = filter_digits(str(process.stdout, 'utf-8'))
    output = process.stdout
    return output


def physical_volume():
    """Gathers the information for all physical volumes and
    spits it out as a json. Can be used as the source for dependent
    items.
    """
    options = ("pv_name,pv_free,pv_size")
    output = run_command('pvs', options)
    json_data = json.loads(output)
    data = {}
    for row in json_data['report'][0]['pv']:
        name = row['pv_name']
        del row['pv_name']
        data[name] = {k: v or 0 for k, v in row.items()}

    return json.dumps(data, sort_keys=True, indent=4)


def volume_group():
    """Gathers the information for all volume groups and spits it
    out as a json.
    """
    options = ("vg_name,lv_count,pv_count,vg_free,vg_size")
    output = run_command('vgs', options)
    json_data = json.loads(output)
    data = {}
    for row in json_data['report'][0]['vg']:
        name = row['vg_name']
        del row['vg_name']
        data[name] = {k: v or 0 for k, v in row.items()}

    return json.dumps(data, sort_keys=True, indent=4)


def logical_volume():
    """Gathers the information for all logical volumes and spits it out
    as a json.
    """
    options = ("lv_name,cache_dirty_blocks,cache_read_hits,"
               "cache_read_misses,cache_total_blocks,cache_write_hits,"
               "cache_write_misses,copy_percent,"
               "data_percent,lv_layout,lv_size")
    output = run_command('lvs', options)
    json_data = json.loads(output)
    data = {}
    for row in json_data['report'][0]['lv']:
        name = row['lv_name']
        del row['lv_name']
        data[name] = {k: v or 0 for k, v in row.items()}

    return json.dumps(data, sort_keys=True, indent=4)


def main(*switch):
    """Switches between the requested type.
    """
    output = ''
    if len(switch) == 1:
        if switch[0] == 'lv':
            output = logical_volume()

        elif switch[0] == 'vg':
            output = volume_group()

        elif switch[0] == 'pv':
            output = physical_volume()

    return output


if __name__ == '__main__':
    print(main(*sys.argv[1:]))
