# OpenPLC Temperature-Control Project

A software-only PLC/ICS exploratory project completed for **CPSec & CyFI Labs**. The project demonstrates Structured Text programming, OpenPLC deployment, Modbus TCP communication, Python-based sensor simulation, and end-to-end validation.

## Final result

- OpenPLC Editor installed and used successfully.
- OpenPLC Runtime v3 built and run in a localhost-only Docker container.
- A Boolean Structured Text exercise passed all four input combinations.
- A temperature controller was implemented with a 3°C hysteresis band.
- Python wrote simulated temperatures through Modbus TCP and read the fan output.
- The automated validation suite passed **9 of 9 tests**.

### Controller behavior

| Temperature | Fan behavior |
|---|---|
| `Temperature >= 30°C` | Turn fan **ON** |
| `Temperature <= 27°C` | Turn fan **OFF** |
| `27°C < Temperature < 30°C` | Preserve the previous fan state |

The separate ON and OFF thresholds prevent rapid switching when a temperature fluctuates near a single boundary.

## Why OpenPLC Runtime v3 was used

The assignment required deployment confirmation through **OpenPLC's web-based runtime interface**. Runtime v3 provides the browser dashboard, Programs upload page, compilation log, and running-status view used in this project.

Runtime v3 is not presented here as a current production platform. Its upstream repository was archived on April 4, 2026, is read-only, and describes v3 as end-of-life and replaced by Runtime v4. For this assignment, v3 was pinned to a specific commit and isolated in Docker with both host ports bound only to `127.0.0.1`.

Official v3 repository: <https://github.com/thiagoralves/OpenPLC_v3>

## Assignment walkthrough

The implementation follows the six tasks in the assignment paper.

### 1. Explore and set up OpenPLC

1. Recorded the Windows, virtualization, WSL, Git, Python, Docker, and VS Code environment.
2. Installed and opened OpenPLC Editor.
3. Cloned OpenPLC Runtime v3 at commit:

   ```text
   b5d41356dab4aeadca0dd7ca64ba542f870b595d
   ```

4. Built a custom Docker image named `openplc-v3-local`.
5. Diagnosed and fixed a Windows CRLF line-ending failure in MatIEC's Autoconf files.
6. Created the persistent Docker volume `openplc-v3-data`.
7. Started the container with localhost-only mappings:
   - Web interface: `127.0.0.1:8080`
   - Modbus TCP: `127.0.0.1:1502` -> container port `502`
8. Logged in through the Runtime dashboard and changed the default password.

Key evidence: `screenshots/01_...` through `screenshots/09_...`.

### 2. Learn PLC programming with Structured Text

1. Created the OpenPLC Editor project `plc/boolean_test`.
2. Added `TestInput`, `Enable`, and `TestOutput` Boolean variables.
3. Implemented:

   ```iecst
   TestOutput := TestInput AND Enable;
   ```

4. Configured a cyclic `MainTask` and `MainInstance`.
5. Simulated all four Boolean combinations.
6. Confirmed all four combinations produced the expected result.

Key evidence: `screenshots/10_...` through `screenshots/14_...` and `notes/boolean_test_results.md`.

### 3. Define the temperature-control scenario

1. Defined a simulated unsigned temperature input and Boolean fan output.
2. Mapped the variables as:

   | Variable | IEC location | Purpose |
   |---|---|---|
   | `Temperature` | `%MW0` | Simulated sensor reading |
   | `Fan` | `%QX0.0` | Cooling-fan output |

3. Selected 30°C as the fan-ON threshold and 27°C as the fan-OFF threshold.
4. Implemented the hysteresis logic:

   ```iecst
   IF Temperature >= 30 THEN
       Fan := TRUE;
   ELSIF Temperature <= 27 THEN
       Fan := FALSE;
   END_IF;
   ```

5. Simulated the controller in order to verify that 28°C retained OFF and 29°C retained ON.

Key evidence: `screenshots/15_...` through `screenshots/19_...` and `notes/temperature_control_design.md`.

### 4. Deploy and execute the PLC program

1. Created the complete Runtime v3 source file:

   ```text
   plc/exported/temperature_control_runtime.st
   ```

2. Opened the Runtime dashboard at `http://127.0.0.1:8080`.
3. Uploaded the `.st` file through the **Programs** page.
4. Waited for compilation to complete.
5. Confirmed the Runtime status changed to **Running**.

Key evidence: `screenshots/20_temperature_program_uploaded.png`, `screenshots/21_temperature_runtime_running.png`, and `notes/temperature_runtime_log.txt`.

### 5. Establish Modbus communication

1. Created a Python 3.11 virtual environment.
2. Installed PyModbus 3.11.1.
3. Used the following mapping:

   | PLC variable | Modbus area | PyModbus address |
   |---|---|---:|
   | `%MW0` Temperature | Holding register | `1024` |
   | `%QX0.0` Fan | Coil | `0` |

4. Connected to `127.0.0.1:1502` with device ID `1`.
5. Wrote a temperature to holding register `1024`.
6. Read the written temperature and fan coil.
7. Ran smoke tests at 20°C and 35°C:
   - 20°C -> fan OFF
   - 35°C -> fan ON

Key evidence: `client/modbus_smoke_test.py`, `screenshots/22_...` through `screenshots/24_...`, and `results/smoke_test_*.txt`.

### 6. Validate and document the results

1. Created `client/validate_controller.py`.
2. Reset the controller to a known low state.
3. Ran this ordered sequence:

   ```text
   20, 27, 28, 30, 29, 27, 40, 35, 27
   ```

4. Compared the actual fan output with an independent Python implementation of the expected hysteresis behavior.
5. Saved the results to `results/validation_results.csv`.
6. Generated `results/validation_plot.png`.
7. Confirmed **9 tests passed and 0 failed**.

Key evidence: `screenshots/25_validation_console.png`, `screenshots/26_validation_csv.png`, `results/validation_results.csv`, and `results/validation_plot.png`.

## Architecture

```text
Python / PyModbus client
        |
        | Modbus TCP 127.0.0.1:1502
        v
Docker port forwarding
        |
        | container port 502
        v
OpenPLC Runtime v3
        |
        | cyclic Structured Text program
        v
Temperature %MW0  --->  fan logic  --->  Fan %QX0.0

Browser dashboard: http://127.0.0.1:8080
```

## Repository structure

```text
client/       Python Modbus smoke test, validator, and plotting script
docker/       Custom Runtime v3 Dockerfile
notes/        Setup, design, mapping, evidence, and troubleshooting notes
plc/          OpenPLC Editor projects and exported PLC source
results/      Smoke-test output, validation CSV, console output, and plot
screenshots/  Numbered evidence screenshots
scripts/      PowerShell start, stop, and status helpers
report/       Final report files when added to the repository
```

## Reproduce the project

The commands below assume Windows PowerShell, Docker Desktop, Git, Python 3.11, and OpenPLC Editor are installed.

### 1. Clone this repository

```powershell
git clone https://github.com/jasoncala/openplc-temperature-control.git
Set-Location openplc-temperature-control
```

### 2. Clone the Runtime v3 source with LF line endings

The Runtime source is deliberately excluded from this repository.

```powershell
New-Item -ItemType Directory -Force -Path tools | Out-Null
Set-Location tools

git clone `
    -c core.autocrlf=false `
    https://github.com/thiagoralves/OpenPLC_v3.git `
    OpenPLC_v3

git -C OpenPLC_v3 checkout `
    b5d41356dab4aeadca0dd7ca64ba542f870b595d

git -C OpenPLC_v3 config core.autocrlf false
git -C OpenPLC_v3 config core.eol lf

Set-Location ..
```

### 3. Build the Runtime image

```powershell
docker build `
    --pull `
    --no-cache `
    -f "docker\OpenPLC_v3.Dockerfile" `
    -t openplc-v3-local `
    "tools\OpenPLC_v3"
```

Create the persistent volume once:

```powershell
docker volume create openplc-v3-data
```

### 4. Start and check OpenPLC

PowerShell's process-scoped execution-policy change must be repeated in each new PowerShell session.

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

.\scripts\start_openplc.ps1
.\scripts\status_openplc.ps1
```

Open the dashboard:

```powershell
Start-Process "http://127.0.0.1:8080"
```

On a newly initialized Runtime, change the default web password immediately.

### 5. Upload the PLC program

In the Runtime web interface:

1. Open **Programs**.
2. Upload `plc/exported/temperature_control_runtime.st`.
3. Confirm compilation succeeds.
4. Confirm the Runtime shows **Running**.

### 6. Create the Python environment

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install pymodbus==3.11.1 matplotlib
```

### 7. Run smoke tests

```powershell
python client\modbus_smoke_test.py --temperature 20
python client\modbus_smoke_test.py --temperature 35
```

Expected states:

```text
20°C -> OFF
35°C -> ON
```

### 8. Run automated validation

```powershell
python client\validate_controller.py
python client\plot_results.py
```

Expected summary:

```text
Tests completed: 9
Tests passed: 9
Tests failed: 0
```

## Important troubleshooting note

The original v3 build appeared to succeed but generated an unusable image without `/workdir/start_openplc.sh`. Strict error handling exposed a MatIEC Autoconf failure caused by Windows CRLF conversion in `configure.ac`. The final solution was to:

- clone the Runtime source with `core.autocrlf=false`;
- normalize Linux build files to LF inside the Dockerfile;
- use Debian Bookworm;
- enable pipeline failure propagation;
- remove a redundant system-Python PyModbus installation command; and
- verify the startup script, virtual environment, webserver, and `iec2c` compiler during the build.

The complete record is in `notes/troubleshooting_log.md`.

## Security and limitations

- Runtime v3 is archived and no longer maintained.
- The web and Modbus ports are bound only to `127.0.0.1`.
- The default web password was changed and is not stored in the repository.
- Modbus TCP traffic is not encrypted or authenticated; this project keeps it local.
- The system is a software simulation, not a safety-rated physical controller.
- The exact OpenPLC Editor version was not captured in the repository.

## Results files

- `results/validation_results.csv` - all nine expected and actual states
- `results/validation_console.txt` - validation console capture
- `results/validation_plot.png` - plotted test sequence and fan state
- `results/smoke_test_20.txt` - low-temperature smoke test
- `results/smoke_test_35.txt` - high-temperature smoke test

## Project outcome

The completed system demonstrates the full requested workflow: PLC programming in Structured Text, Runtime deployment through the OpenPLC web interface, Modbus TCP communication from Python, and repeatable validation of the controller's behavior.
