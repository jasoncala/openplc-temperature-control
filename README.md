# OpenPLC Temperature-Control Project

## Status

Work in progress.

## Project objective

Implement and validate a simulated temperature-control system using:

- OpenPLC Editor
- Structured Text
- OpenPLC Runtime v3
- Docker Desktop
- Modbus TCP
- Python and PyModbus

## Core behavior

- Fan turns ON when temperature is at or above 30°C.
- Fan turns OFF when temperature is at or below 27°C.
- Between 27°C and 30°C, the previous fan state is preserved.

## Repository organization

- `plc/` — OpenPLC projects and exported PLC source
- `client/` — Python Modbus client and validation scripts
- `results/` — CSV and generated result figures
- `screenshots/` — numbered project evidence
- `notes/` — environment, design, evidence, and troubleshooting notes
- `scripts/` — PowerShell helper scripts
- `report/` — final report source and PDF

## Security note

OpenPLC Runtime v3 is used only inside a localhost-bound Docker container.
It must not be exposed directly to the public Internet.