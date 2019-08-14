#!/usr/bin/env python3
"""Author:      Olivier van der Toorn <oliviervdtoorn@gmail.com>
Description:    Collection of tests for the Zabbix smart script.
"""
# pylint: disable=import-error,unused-import
from pytest_mock import mocker  # noqa: F401

import smart


# pylint: disable=line-too-long
MOCK_OUTPUT = """SMART Attributes Data Structure revision number: 16
Vendor Specific SMART Attributes with Thresholds:
ID# ATTRIBUTE_NAME          FLAG     VALUE WORST THRESH TYPE      UPDATED  WHEN_FAILED RAW_VALUE
  1 Raw_Read_Error_Rate     0x002f   200   200   051    Pre-fail  Always       -       0
  3 Spin_Up_Time            0x0027   171   171   021    Pre-fail  Always       -       6441
  4 Start_Stop_Count        0x0032   100   100   000    Old_age   Always       -       11
  5 Reallocated_Sector_Ct   0x0033   200   200   140    Pre-fail  Always       -       0
  7 Seek_Error_Rate         0x002e   200   200   000    Old_age   Always       -       0
  9 Power_On_Hours          0x0032   087   087   000    Old_age   Always       -       9661
 10 Spin_Retry_Count        0x0032   100   253   000    Old_age   Always       -       0
 11 Calibration_Retry_Count 0x0032   100   253   000    Old_age   Always       -       0
 12 Power_Cycle_Count       0x0032   100   100   000    Old_age   Always       -       10
192 Power-Off_Retract_Count 0x0032   200   200   000    Old_age   Always       -       4
193 Load_Cycle_Count        0x0032   155   155   000    Old_age   Always       -       137291
194 Temperature_Celsius     0x0022   113   099   000    Old_age   Always       -       37
196 Reallocated_Event_Count 0x0032   200   200   000    Old_age   Always       -       0
197 Current_Pending_Sector  0x0032   200   200   000    Old_age   Always       -       0
198 Offline_Uncorrectable   0x0030   200   200   000    Old_age   Offline      -       0
199 UDMA_CRC_Error_Count    0x0032   200   200   000    Old_age   Always       -       0
200 Multi_Zone_Error_Rate   0x0008   200   200   000    Old_age   Offline      -       0"""  # noqa: E501


def test_smart_no_arguments():
    """Tests if no arguments gives a zero.
    """
    assert smart.main() == 0


# pylint: disable=redefined-outer-name
def test_smart_single_argument(mocker):  # noqa: F811
    """Tests if a single argument gives string output (smart output).
    """
    mocker.patch.object(smart, 'smartvalues')
    smart.smartvalues.return_value = MOCK_OUTPUT
    assert isinstance(smart.main('/dev/sda'), str)


# pylint: disable=redefined-outer-name
def test_smart_two_arguments(mocker):  # noqa: F811
    """Tests the request of a value.
    """
    mocker.patch.object(smart, 'smartvalues')
    smart.smartvalues.return_value = MOCK_OUTPUT
    assert smart.main('/dev/sda', 'Power_On_Hours') != 0
