from collections import OrderedDict
from .states import DefaultState
from lewis.devices import StateMachineDevice
from enum import Enum


class TriggerMode(Enum):
    INPUT = 0
    OUTPUT = 1


class SpeedMode(Enum):
    SLOW = 0
    FAST = 1


class SensorMode(Enum):
    OFF = 0
    ACTIVE = 1


# noinspection PyAttributeOutsideInit
class SimulatedThorlabsfw102C(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self._idn: str = 'Thorlabs FW102C (emulated), V0.0.0'
        self._position: int = 0
        self._trigger_mode: TriggerMode = TriggerMode.INPUT
        self._speed_mode: SpeedMode = SpeedMode.SLOW
        self._sensor_mode: SensorMode = SensorMode.OFF

    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([])

    @property
    def state(self):
        return self._csm.state

    @property
    def idn(self) -> str:
        return self._idn

    @property
    def position(self) -> int:
        return self._position
    
    @position.setter
    def position(self, new_position: int) -> None:
        if self.state == 'moving':
            raise RuntimeError("Can't set new position while moving.")

        if not (0 <= new_position <= 5):
            raise ValueError('Position is out of range [0, 5]')

        self._position = new_position

    @property
    def trigger_mode(self) -> TriggerMode:
        return self._trigger_mode
    
    @trigger_mode.setter
    def trigger_mode(self, new_mode: TriggerMode) -> None:
        prev_mode = self._trigger_mode
        # It's vaguely possible that the new_mode value may not be in the enum list
        # if not then maintain the old value.
        try:
            self._trigger_mode = TriggerMode(new_mode)
        except IndexError:
            self._trigger_mode = prev_mode

    @property
    def speed_mode(self) -> SpeedMode:
        return self._speed_mode
    
    @speed_mode.setter
    def speed_mode(self, new_mode: SpeedMode) -> None:
        prev_mode = self._speed_mode
        # It's vaguely possible that the new_mode value may not be in the enum list
        # if not then maintain the old value.
        try:
            self._speed_mode = SpeedMode(new_mode)
        except IndexError:
            self._speed_mode = prev_mode

    @property
    def sensor_mode(self) -> SensorMode:
        return self._sensor_mode
    
    @sensor_mode.setter
    def sensor_mode(self, new_mode: SensorMode) -> None:
        prev_mode = self._sensor_mode
        # It's vaguely possible that the new_mode value may not be in the enum list
        # if not then maintain the old value.
        try:
            self._sensor_mode = SensorMode(new_mode)
        except IndexError:
            self._sensor_mode = prev_mode
        self._sensor_mode = new_mode


