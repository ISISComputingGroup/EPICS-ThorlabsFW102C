import unittest

from utils.channel_access import ChannelAccess
from utils.ioc_launcher import get_default_ioc_dir
from utils.test_modes import TestModes
from utils.testing import get_running_lewis_and_ioc, skip_if_recsim

DEVICE_PREFIX = "TLFW102C_01"

POSITION = "POSITION"
TRIGGERMODE = "TRIGGERMODE"
SPEEDMODE = "SPEEDMODE"
SENSORMODE = "SENSORMODE"
ID = "ID"

IOCS = [
    {
        "name": DEVICE_PREFIX,
        "directory": get_default_ioc_dir("TLFW102C"),
        "macros": {},
        "emulator": "thorlabsfw102c",
    },
]

TEST_MODES = [TestModes.DEVSIM]


class Thorlabsfw102CTests(unittest.TestCase):
    """
    Tests for the _Device_ IOC.
    """

    def setUp(self):
        self._lewis, self._ioc = get_running_lewis_and_ioc('thorlabsfw102c', DEVICE_PREFIX)
        self.ca = ChannelAccess(device_prefix=DEVICE_PREFIX)
        self._lewis.backdoor_set_on_device('position', 1)
        self.ca.set_pv_value(f'{POSITION}.PROC', 1)
        self.ca.assert_that_pv_is('POSITION', 'Filter 1',
                                  timeout=5)  # ensure that position actually set.

    @skip_if_recsim("In rec sim this test fails")
    def test_GIVEN_move_THEN_filter_moves_to_position(self):
        self.ca.set_pv_value(f"{POSITION}:SP", "Filter 2")
        self.ca.assert_that_pv_is(f'{POSITION}:SP.RVAL', 2)
        self.ca.assert_that_pv_is_number(f'{POSITION}.RVAL', 2, 0, timeout=5)

    @skip_if_recsim("In rec sim this test fails")
    def test_GIVEN_trigger_mode_THEN_mode_is_set(self):
        self.ca.set_pv_value(f'{TRIGGERMODE}:SP', 'OUTPUT')
        self.ca.assert_that_pv_is(f'{TRIGGERMODE}:SP', 'OUTPUT')
        self.ca.assert_that_pv_is(f'{TRIGGERMODE}', 'OUTPUT')
        self.ca.set_pv_value(f'{TRIGGERMODE}:SP', 'INPUT')
        self.ca.assert_that_pv_is(f'{TRIGGERMODE}:SP', 'INPUT')
        self.ca.assert_that_pv_is(f'{TRIGGERMODE}', 'INPUT')

    @skip_if_recsim("In rec sim this test fails")
    def test_GIVEN_speed_mode_THEN_mode_is_set(self):
        self.ca.set_pv_value(f'{SPEEDMODE}:SP', 'FAST')
        self.ca.assert_that_pv_is(f'{SPEEDMODE}:SP', 'FAST')
        self.ca.assert_that_pv_is(f'{SPEEDMODE}', 'FAST')
        self.ca.set_pv_value(f'{SPEEDMODE}:SP', 'SLOW')
        self.ca.assert_that_pv_is(f'{SPEEDMODE}:SP', 'SLOW')
        self.ca.assert_that_pv_is(f'{SPEEDMODE}', 'SLOW')

    def test_GIVEN_sensor_mode_THEN_mode_is_set(self):
        self.ca.set_pv_value(f'{SENSORMODE}:SP', 'ACTIVE')
        self.ca.assert_that_pv_is(f'{SENSORMODE}:SP', 'ACTIVE')
        self.ca.assert_that_pv_is(f'{SENSORMODE}', 'ACTIVE')
        self.ca.set_pv_value(f'{SENSORMODE}:SP', 'OFF')
        self.ca.assert_that_pv_is(f'{SENSORMODE}:SP', 'OFF')
        self.ca.assert_that_pv_is(f'{SENSORMODE}', 'OFF')
