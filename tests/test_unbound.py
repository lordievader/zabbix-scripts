#!/usr/bin/env python3
"""Author:      Olivier van der Toorn <oliviervdtoorn@gmail.com>
Description:    Collection of tests for the Zabbix discovery scripts.
"""
import json
from zabbix_scripts import unbound


with open('tests/unbound-control.txt', 'r') as unbound_file:
    UNBOUND_CONTROL = unbound_file.read()


def test_unbound(mocker):
    """Tests the unbound parser.
    """
    mocker.patch.object(
        unbound.subprocess, 'getoutput',
        return_value=UNBOUND_CONTROL)
    output = {
        'data': {
            'thread0numqueries': 345.0,
        },
    }
    assert unbound.main() == json.dumps(
        output, sort_keys=True, indent=4)
