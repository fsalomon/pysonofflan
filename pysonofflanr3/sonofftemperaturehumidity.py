import asyncio
import logging
from typing import Callable, Awaitable, Dict

from pysonofflanr3 import SonoffSwitch
from pysonofflanr3 import SonoffLANModeClient


class SonoffTemperatureHumidity(SonoffSwitch):
    """Representation of a Sonoff TH10/TH16.

    Usage example when used as library:
    p = SonoffTemperatureHumidity("192.168.1.105")
    # print the device ID
    print(p.device_id)
    # change state of plug
    p.state = "ON"
    p.state = "OFF"
    # query and print current state of plug
    print(p.state)

    Errors reported by the device are raised as Exceptions,
    and should be handled by the user of the library.
    """

    # switch states
    SWITCH_STATE_TEMPERATURE = "TEMPERATURE"


    @property
    def state(self) -> str:
        """
        Retrieve the switch state

        :returns: one of
                  SWITCH_STATE_ON
                  SWITCH_STATE_OFF
                  SWITCH_STATE_UNKNOWN
        :rtype: str
        """

        try:
            deviceType = self.basic_info["deviceType"]
        except:  # noqa
            deviceType = ""

        try:
            state = self.params["switch"]
        except:  # noqa
            state = SonoffTemperatureHumidity.SWITCH_STATE_UNKNOWN

        if deviceType == "normal" and state == "off":
            return SonoffTemperatureHumidity.SWITCH_STATE_OFF
        elif deviceType == "normal" and state == "on":
            return SonoffTemperatureHumidity.SWITCH_STATE_ON
        elif deviceType == "temperature":
            return SonoffTemperatureHumidity.SWITCH_STATE_TEMPERATURE
        else:
            self.logger.debug("Unknown state %s / deviceType %s returned.", state, deviceType)
            return SonoffTemperatureHumidity.SWITCH_STATE_UNKNOWN


    @property
    def is_on(self) -> bool:
        """
        Returns whether device is on.
        :return: True if device is on, False otherwise
        """
        if "switch" in self.params and "deviceType" in self.basic_info:
            return self.params["switch"] == "on" and self.basic_info["deviceType"] == "normal"

        return False

    async def turn_on(self):
        """
        Turn the switch on.
        """
        self.logger.debug("Switch turn_on called.")
        self.update_params({"switch": "on", "mainSwitch": "on", "deviceType": "normal"})

    @property
    def is_off(self) -> bool:
        """
        Returns whether device is off.

        :return: True if device is off, False otherwise.
        :rtype: bool
        """
        if "switch" in self.params and "deviceType" in self.basic_info:
            return self.params["switch"] == "off" and self.basic_info["deviceType"] == "normal"

        return False

    async def turn_off(self):
        """
        Turn the switch off.
        """
        self.logger.debug("Switch turn_off called.")
        self.update_params({"switch": "off", "mainSwitch": "off", "deviceType": "normal"})

    async def set_heat_targets(self, low: int, high: int):
        """
        Set the target temperatures for heating.
        """
        self.logger.debug("Switch set_heat_targets %d/%d called.", low, high)
        self.update_params({"mainSwitch":"on","deviceType":"temperature","targets":[{"targetHigh":high,"reaction":{"switch":"off"}},{"targetLow":low,"reaction":{"switch":"on"}}]})


    async def set_cool_targets(self, low: int, high: int):
        """
        Set the target temperatures for cooling.
        """
        self.logger.debug("Switch set_cool_targets %d/%d called.", low, high)
        self.update_params({"mainSwitch":"on","deviceType":"temperature","targets":[{"targetHigh":high,"reaction":{"switch":"on"}},{"targetLow":low,"reaction":{"switch":"off"}}]})
