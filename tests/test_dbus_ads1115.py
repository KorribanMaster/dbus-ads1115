import pytest
import dbus
from unittest.mock import patch, mock_open
from dbus_ads1115.dbus_ads1115 import TemperatureSensor
import subprocess as sp
from gi.repository import GLib
import sys
from time import sleep
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../ext/velib_python'))
import settingsdevice

sys.path.append(
    os.path.join(os.path.dirname(__file__), '../ext/velib_python/test'))
from mock_settings_device import MockSettingsDevice

MOCK_DEV_FILENAME = "inX_input"


@pytest.fixture(scope="session")
def dbus_session(tmp_path_factory):
    global mainloop
    settingsfolder = tmp_path_factory.mktemp("settings")
    localsettings_process = sp.Popen([
        "python3",
        os.path.join(os.path.dirname(__file__),
                     '../ext/localsettings/localsettings.py'), "--path",
        settingsfolder
    ])
    sleep(5)
    dbus.mainloop.glib.threads_init()
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    mainloop = GLib.MainLoop()
    yield
    localsettings_process.kill()


@pytest.fixture(scope="module")
def temperature_sensor(dbus_session):
    temp_sensor = TemperatureSensor(MOCK_DEV_FILENAME)
    yield temp_sensor
    del temp_sensor


@patch.object(TemperatureSensor, "_attach_to_dbus")
def test_temperature_sensor_counting(dbus_session):
    sensor0 = TemperatureSensor(MOCK_DEV_FILENAME)
    sensor1 = TemperatureSensor(MOCK_DEV_FILENAME)
    assert sensor0._id == sensor1._id - 1


@pytest.mark.parametrize("data, expect", [('0', 0), ('4096' , 100)])
def test_sensor_update(temperature_sensor, dbus_session, data, expect):
    with patch("builtins.open", mock_open(read_data=data)) as mock_file:
        temperature_sensor.update()
        mock_file.assert_called_with(MOCK_DEV_FILENAME, "r")
    pass
