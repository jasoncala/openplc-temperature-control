# Modbus Address Map

## Endpoint

- Protocol: Modbus TCP
- Host: `127.0.0.1`
- Host port: `1502`
- Container port: `502`
- Device ID: `1`

## Variables

| Variable | IEC location | Modbus area | PyModbus address |
|---|---|---|---:|
| Temperature | `%MW0` | Holding register | 1024 |
| Fan | `%QX0.0` | Coil | 0 |

## Docker forwarding

Docker forwards:

- `127.0.0.1:1502` on Windows
- to port `502` inside the OpenPLC container

## Addressing

OpenPLC Runtime v3 maps `%MW0` to holding-register data address 1024.

OpenPLC maps `%QX0.0` to discrete output coil data address 0.

PyModbus accepts zero-based protocol addresses, so the Python client uses
exactly `1024` and `0`.