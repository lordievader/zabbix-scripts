#!/usr/bin/env python3
"""Author:      Olivier van der Toorn <oliviervdtoorn@gmail.com>
Description:    Collection of tests for the Zabbix discovery scripts.
"""
import json
from zabbix_scripts import discover_unbound


with open('tests/unbound-control.txt', 'r') as unbound_file:
    UNBOUND_CONTROL = unbound_file.read()


def test_discover_unbound(mocker):
    """Tests the discover unbound function.
    """
    mocker.patch.object(
        discover_unbound.subprocess, 'getoutput',
        return_value=UNBOUND_CONTROL)
    output = {
        "data": [
            {
                "{#NAME}": "thread0.num.queries",
                "{#KEY}": "thread0numqueries",
            },
        ],
    }
    assert discover_unbound.main() == json.dumps(
        output, sort_keys=True, indent=4)
