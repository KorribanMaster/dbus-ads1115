import pytest
from pytest import MonkeyPatch
from dbus_ads1115.dbus_ads1115 import TemperatureSensor
# import dbus_ads1115.mock.mock_settings_device
# import dbus_ads1115.mock.mock_dbus_service
from .mock.mock_settings_device import MockSettingsDevice
from .mock.mock_dbus_service import MockDbusService
from unittest.mock import patch, mock_open

MOCK_DEV_FILENAME = "inX_input"


def mock_attach_to_dbus(cls, *args, **kwargs):
    _dbus = MockDbusService(
        f"{TemperatureSensor.dbusBasepath}device0_{cls._id}")

    _dbus.add_path("/Temperature", cls._temperature)
    _dbus.add_path("/Status", cls._status)
    return _dbus


def mock_attach_to_settings(cls, *args, **kwargs):
    return MockSettingsDevice(*args)


@pytest.fixture(scope="function")
def temperature_sensor(monkeypatch: MonkeyPatch) -> TemperatureSensor:
    monkeypatch.setattr(TemperatureSensor, "_attach_to_dbus",
                        mock_attach_to_dbus)
    monkeypatch.setattr(TemperatureSensor, "_attach_to_settings",
                        mock_attach_to_settings)
    temp_sensor = TemperatureSensor(MOCK_DEV_FILENAME)
    yield temp_sensor
    del temp_sensor


def test_temperature_sensor_counting(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(TemperatureSensor, "_attach_to_dbus",
                        mock_attach_to_dbus)
    monkeypatch.setattr(TemperatureSensor, "_attach_to_settings",
                        mock_attach_to_settings)
    sensor0 = TemperatureSensor(MOCK_DEV_FILENAME)
    sensor1 = TemperatureSensor(MOCK_DEV_FILENAME)
    assert sensor0._id == sensor1._id - 1


@pytest.mark.parametrize("data, expect", [('0', 0), ('4096', 4096)])
def test_sensor_update(temperature_sensor, data, expect):
    with patch("builtins.open", mock_open(read_data=data)) as mock_file:
        temperature_sensor.update()
        assert temperature_sensor._temperature == expect
        assert temperature_sensor._dbus["/Temperature"] == expect
        mock_file.assert_called_with(MOCK_DEV_FILENAME, "r")
    pass
