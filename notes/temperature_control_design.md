# Temperature-Control Design

## Scenario

A Python Modbus client simulates a temperature sensor by writing an unsigned
16-bit temperature value to OpenPLC memory.

OpenPLC executes Structured Text logic that controls a Boolean cooling-fan
output.

## Control behavior

| Temperature condition | Fan action |
|---|---|
| Temperature >= 30°C | Turn fan ON |
| Temperature <= 27°C | Turn fan OFF |
| 27°C < Temperature < 30°C | Preserve previous fan state |

## Hysteresis

The fan-on and fan-off thresholds differ by 3°C.

This hysteresis prevents the fan from rapidly switching on and off if the
temperature fluctuates near one threshold.

## Variables

| Name | Type | IEC location | Purpose |
|---|---|---|---|
| `Temperature` | `UINT` | `%MW0` | Simulated sensor value |
| `Fan` | `BOOL` | `%QX0.0` | Cooling-fan control output |

## Initial condition

- Temperature: 20°C
- Fan: OFF

## Validation sequence

| Test | Temperature | Previous expected fan | Expected fan | Purpose | Result
|---:|---:|---|---|---| ---|
| 1 | 20 | OFF | OFF | Establish low state | PASS
| 2 | 27 | OFF | OFF | Exact off threshold | PASS
| 3 | 28 | OFF | OFF | Middle region retains OFF | PASS
| 4 | 30 | OFF | ON | Exact on threshold | PASS
| 5 | 29 | ON | ON | Middle region retains ON | PASS
| 6 | 27 | ON | OFF | Downward transition | PASS
| 7 | 40 | OFF | ON | Clearly high value | PASS
| 8 | 35 | ON | ON | Remains ON | PASS
| 9 | 27 | ON | OFF | Final shutdown | PASS