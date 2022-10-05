#!/usr/bin/python3 -u
import yaml
from abc import ABC, abstractmethod
from itertools import count
import logging
import enum
from gi.repository import GLib
import dbus
import dbus.mainloop.glib
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


class TemperatureSensor(Sensor):
    """A temperature Sensor."""

    dbusBasepath = "com.victronenergy.temperature"
    _ids = count(0)

    def __init__(self, dbus, dev):
        """Initialise the class."""
        self._dbus = dbus
        self._dev = dev
        self._id = next(self._ids)
        self._temperature = 24.0
        self.scale = 1
        self.offset = 0

    def update(self):
        """Update the temperature reading of the sensor."""
        with open(self._dev, "r") as dev:
            self._temperature = dev.read() * self.scale + self.offset


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

    svc = VeDbusService('com.victronenergy.modem')

    svc.add_path('/Model', None)
    svc.add_path('/IMEI', None)
    svc.add_path('/NetworkName', None)
    svc.add_path('/NetworkType', None)
    svc.add_path('/SignalStrength', None)
    svc.add_path('/Roaming', None)
    svc.add_path('/Connected', None)
    svc.add_path('/IP', None)
    svc.add_path('/SimStatus', None)
    svc.add_path('/RegStatus', None)

    modem = Ads1115(svc, args.serial, rate)
    if not modem.start():
        return

    GLib.timeout_add(5000, modem.update)
    mainloop.run()

    quit(1)

try:
    main()
except KeyboardInterrupt:
    quit(1)

