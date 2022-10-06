#!/usr/bin/python3 -u
import yaml
from abc import ABC, abstractmethod
from itertools import count
import logging
import enum
from gi.repository import GLib
import dbus
import dbus.mainloop.glib
from velib_python.vedbus import VeDbusService
from velib_python.settingsdevice import SettingsDevice
logger = logging.getLogger(__name__)


VERSION = 0.1

ADS1115_RANGE = 4096
ADS1115_OFFSET = 0

class FluidType(enum):
    """Note that the FluidType enumeration is kept in sync with NMEA2000 definitions."""

    FUEL = 0
    FRESH_WATER = 1
    WASTE_WATER = 2
    LIVE_WELL = 3
    OIL = 4
    BLACK_WATER = 5  # Sewage


class Status(enum):
    """Enum to describe Sensor Status."""

    OK = 0
    DISCONNECTED = 1
    SHORT_CIRCUITED = 2
    REVERSE_POLARITY = 3
    UNKNOWN = 4


class TemperatureType(enum):
    """Enum for type of temperature sensor."""

    BATTERY = 0
    FRIDGE = 1
    GENERIC = 2


class Sensor(ABC):
    """Abstract Sensor Class."""

    @abstractmethod
    def update(self):
        """Update the sensor."""
        pass

TEMPERATURE_SENSOR_SETTINGS = 
class TemperatureSensor(Sensor):
    """A temperature Sensor."""

    dbusBasepath = "com.victronenergy.temperature."
    _ids = count(0)

    def __init__(self, dev):
        """Initialise the class."""
        self._dev = dev
        self._id = next(self._ids)
        self._temperature = 24.0
        self._status = Status.DISCONNECTED
        self._scale = 1
        self._offset = 0
        self._attach_to_dbus()

    def _attach_to_dbus(self):
        """Attach to dbus and create paths and callbacks.

        The dbus object will be com.victronenergy.temperature.<n>
        Paths
        /analogpinFunc
        /Temperature        degrees Celcius
        /Status             0=Ok; 1=Disconnected; 2=Short circuited; 3=Reverse polarity; 4=Unknown
        /Scale
        /Offset
        /TemperatureType    0=battery; 1=fridge; 2=generic
        """
        self._dbus = VeDbusService(f"{TemperatureSensor.dbusBasepath}{self.id}")
        # self._dbus.add_path("/analogpinFunc", 0)

        self._dbus.add_path("/Temperature", self._temperature)
        self._dbus.add_path("/Status", self._status)

        self._settings_base ={ 'scale': [f'/Settings/Devices/{self.id}/Scale', 1.0, 0.0, 1.0],
                               'offset': [f'/Settings/Devices/{self._id}/Offset', 0,0, ADS1115_RANGE]}
        self._settings = SettingsDevice(self._dbus.dbusconn, self._settings_base, eventCallback)

    def _setting_changed(self, setting, old, new):
        if setting == 'scale':
            logger.info(f"Scale setting Changed from {old} to {new}")
            self._scale = new
        elif setting == "offset":
            logger.info(f"Offset setting Changed from {old} to {new}")
            self._offset = new
    def _set_status(self, status):
            self._status = status
            self._dbus["/Status"] = self._status


    def update(self):
        """Update the temperature reading of the sensor."""
        try:
            with open(self._dev, "r") as dev:
                self._temperature = dev.read() * self._scale + self._offset
            self._dbus["/Temperature"] = self._temperature
            if self._status != Status.OK:
                self._set_status(Status.OK)
        except FileNotFoundError as err:
                self._set_status(Status.DISCONNECTED)


class SensorManager(Object):
    """Class to manage a fleet of sensors connected to the ADC channels."""

    def __init__(self, config_filename):
        """Initialise the SensorManager.

        Parse a config file instantiate the Sensors based on the file.
        """
        with open(config_filename, "r") as stream:
            self._config = yaml.safe_load(stream)


def quit(n):
    global start
    log.info('End. Run time %s' % str(datetime.now() - start))
    os._exit(n)

def main():
    global mainloop
    global start

    start = datetime.now()

    parser = ArgumentParser(description='dbus_ads1115', add_help=True)
    parser.add_argument('-d', '--debug', help='enable debug logging',
                        action='store_true')

    args = parser.parse_args()

    logging.basicConfig(format='%(levelname)-8s %(message)s',
                        level=(logging.DEBUG if args.debug else logging.INFO))

    logLevel = {
        0:  'NOTSET',
        10: 'DEBUG',
        20: 'INFO',
        30: 'WARNING',
        40: 'ERROR',
    }
    logger.info('Loglevel set to ' + logLevel[log.getEffectiveLevel()])

    logger.info(f'Starting dbus_ads1115 {VERSION}')

    dbus.mainloop.glib.threads_init()
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    mainloop = GLib.MainLoop()

    # TODO do stff
    if not modem.start():
        return

    GLib.timeout_add(5000, modem.update)
    mainloop.run()

    quit(1)

try:
    main()
except KeyboardInterrupt:
    quit(1)

