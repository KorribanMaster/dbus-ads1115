# dbus-ads1115
Expansion for venus-os from victron to use the ads1115 adc
Planned Features to support the following sensors:

## Tank


com.victronenergy.temperature.device0_<n>

| Path           | Description                                                                      | Writable |
|:---------------|:---------------------------------------------------------------------------------|:---------|
| /analogpinFunc | uknown, probably belongs to settings                                             | ?        |
| /Level         | 0 to 100%                                                                        | No       |
| /Remaining     | m3                                                                               | No       |
| /Status        | 0=Ok; 1=Disconnected; 2=Short circuited; 3=Reverse polarity; 4=Unknown           | No       |
| /Capacity      | m3                                                                               | Yes      |
| /FluidType     | 0=Fuel; 1=Fresh water; 2=Waste water; 3=Live well; 4=Oil; 5=Black water (sewage) | Yes      |
| /Standard      | 0=European; 1=USA                                                                | Yes      |


Settings Bus

| Path                                 | Default | Min | Max  |
|:-------------------------------------|:--------|-----|:-----|
| /Settings/Devices/device0_<n>/Scale  | 1       | 0   | 1    |
| /Settings/Devices/device0_<n>/Offset | 0       | 0   | 4096 |
|                                      |         |     |      |

## Temperature

com.victronenergy.temperature.device0_<n>

| Path             | Description                                                            | Writable |
|:-----------------|:-----------------------------------------------------------------------|:---------|
| /analogpinfunc   | uknown, probably belongs to settings                                   | ?        |
| /Temperature     | degrees Celcius                                                        | No       |
| /Status          | 0=Ok; 1=Disconnected; 2=Short circuited; 3=Reverse polarity; 4=Unknown | No       |
| /TemperatureType | 0=battery; 1=fridge; 2=generic                                         | Yes      |


Settings Bus

| Path                                 | Default | Min | Max  |
|:-------------------------------------|:--------|-----|:-----|
| /Settings/Devices/device0_<n>/Scale  | 1       | 0   | 1    |
| /Settings/Devices/device0_<n>/Offset | 0       | 0   | 4096 |
|                                      |         |     |      |

## Current (DC/Mains)

TODO

## Voltage (DC/AC)

TODO


# Configuration

YAML file in ???
TODO

![Tests](https://github.com/KorribanMaster/dbus-ads1115/actions/workflows/tests.yml/badge.svg)

[![Built with Spacemacs](https://cdn.rawgit.com/syl20bnr/spacemacs/442d025779da2f62fc86c2082703697714db6514/assets/spacemacs-badge.svg)](http://spacemacs.org)
