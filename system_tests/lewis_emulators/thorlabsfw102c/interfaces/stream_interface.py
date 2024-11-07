from lewis.adapters.stream import StreamInterface
from lewis.utils.command_builder import CmdBuilder

from ..device import TriggerMode, SpeedMode, SensorMode


class Thorlabsfw102CStreamInterface(StreamInterface):
    in_terminator = "\r"
    out_terminator = "\r"
    readtimeout = 5000

    def __init__(self):
        super(Thorlabsfw102CStreamInterface, self).__init__()
        # Commands that we expect via serial during normal operation
        self.commands = {
            CmdBuilder('get_id').escape("*idn?").build(),
            CmdBuilder(self.get_position).escape("pos?").eos().build(),
            CmdBuilder(self.set_position).escape("pos=").int().build(),
            CmdBuilder(self.get_trigger_mode).escape("trig?").eos().build(),
            CmdBuilder(self.set_trigger_mode).escape("trig=").int().build(),
            CmdBuilder(self.get_speed_mode).escape("speed?").eos().build(),
            CmdBuilder(self.set_speed_mode).escape("speed=").int().build(),
            CmdBuilder(self.get_sensor_mode).escape("sensors?").eos().build(),
            CmdBuilder(self.set_sensor_mode).escape("sensors=").int().build(),
        }

    def handle_error(self, request, error):
        """
        If command is not recognised print and error

        Args:
            request: requested string
            error: problem

        """
        print("An error occurred at request " + repr(request) + ": " + repr(error))
        return str(error)

    @staticmethod
    def get_version():
        return "TLFW102C_EMULATED"

    def get_id(self):
        return f'*idn?\r{self._device.idn}'

    def get_position(self):
        return f'pos?\r{self._device.position}'

    def set_position(self, new_position: int) -> str:
        self._device.position = new_position
        return f'pos={new_position}'

    def get_trigger_mode(self):
        return 'trig?\r' + ('0' if self._device.trigger_mode == TriggerMode.INPUT
                            else '1')

    def set_trigger_mode(self, new_mode: int) -> str:
        self._device.trigger_mode = TriggerMode(new_mode)
        return f'trig={new_mode}'

    def get_speed_mode(self):
        return 'speed?\r' + ('0' if self._device.speed_mode == SpeedMode.SLOW
                             else '1')

    def set_speed_mode(self, new_mode: int) -> str:
        self._device.speed_mode = SpeedMode(new_mode)
        return f'speed={new_mode}'

    def get_sensor_mode(self):
        return 'sensors?\r' + ('0' if self._device.sensor_mode == SensorMode.OFF
                               else '1')

    def set_sensor_mode(self, new_mode: int) -> str:
        self._device.sensor_mode = SensorMode(new_mode)
        return f'sensors={new_mode}'

    def catch_all(self, command):
        pass
