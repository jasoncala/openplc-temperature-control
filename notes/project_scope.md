# Project Scope

## Required core system

The project simulates a temperature sensor whose value is sent from Python to
OpenPLC Runtime over Modbus TCP.

OpenPLC executes Structured Text control logic and controls a Boolean cooling
fan output.

## Core thresholds

- Temperature >= 30°C: Fan ON
- Temperature <= 27°C: Fan OFF
- 27°C < Temperature < 30°C: Preserve previous fan state

## Why hysteresis is used

The separate ON and OFF thresholds prevent rapid switching when a measured
temperature fluctuates around one threshold.

## Required project evidence

- OpenPLC Editor installed
- OpenPLC Runtime installed and running
- Basic Structured Text exercise
- Temperature controller design
- Successful PLC deployment
- Python Modbus register write
- Python Modbus coil read
- Multiple validation cases
- Screenshots and written documentation

## Optional extensions

- High-temperature alarm
- Validation plot
- Wireshark observation of local Modbus traffic
- Additional security discussion

Optional work will only begin after the core project passes validation.