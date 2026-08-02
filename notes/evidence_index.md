# Evidence Index

| Figure | Screenshot file | What it proves | Planned report section |
|---:|---|---:|---|
| 1 | `01_windows_version.png` | Records the Windows edition, version, and OS build used for the experiment | Environment and platform |
| 2 | `02_virtualization_enabled.png` | Confirms the host CPU and that hardware virtualization is enabled for Docker | Environment and platform |
| 3 | `03_wsl_status.png` | Shows that WSL infrastructure is available without a user-facing Ubuntu installation | Environment and platform |
| 4 | `04_development_tool_versions.png` | Records the installed Git, Python, Docker CLI, and VS Code versions | Environment and platform |
| 5 | `05_docker_hello_world.png` | Demonstrates that Docker Desktop can successfully run a Linux container | Environment and platform |
| 6 | `06_openplc_editor_installed.png` | Confirms that the Windows OpenPLC Editor was installed and launched successfully | Environment and platform |
| 7 | `07_openplc_docker_image.png` | Confirms that the OpenPLC Runtime v3 Docker image was built successfully | Runtime installation |
| 8 | `08_openplc_runtime_dashboard.png` | Confirms successful authentication and access to the OpenPLC Runtime v3 dashboard | Runtime installation |
| 9 | `09_openplc_localhost_ports.png` | Shows that the Runtime web and Modbus ports are bound only to localhost | Runtime installation and security |
| 10 | `10_boolean_variables.png` | Shows the Boolean exercise variable declarations | Structured Text learning |
| 11 | `11_boolean_logic.png` | Shows the Boolean AND logic written in Structured Text | Structured Text learning |
| 12 | `12_boolean_task_configuration.png` | Shows the cyclic task and Boolean program instance | Structured Text learning |
| 13 | `13_boolean_simulation_false.png` | Demonstrates a Boolean combination correctly producing FALSE | Structured Text learning |
| 14 | `14_boolean_simulation_true.png` | Demonstrates TRUE AND TRUE correctly producing TRUE | Structured Text learning |
| 15 | `15_temperature_variables.png` | Shows the mapped temperature and fan variables | Controller implementation |
| 16 | `16_temperature_logic.png` | Shows the Structured Text hysteresis logic | Controller implementation |
| 17 | `17_temperature_task_configuration.png` | Shows the cyclic task and controller instance | Controller implementation |
| 18 | `18_hysteresis_retains_off.png` | Shows 28°C retaining the previous OFF state | Controller simulation |
| 19 | `19_hysteresis_retains_on.png` | Shows 29°C retaining the previous ON state | Controller simulation |
| 20 | `20_temperature_program_uploaded.png` | Shows the temperature-control program uploaded to Runtime v3 | PLC deployment |
| 21 | `21_temperature_runtime_running.png` | Confirms successful compilation and execution in OpenPLC Runtime | PLC deployment |
| 22 | `22_modbus_port_available.png` | Confirms that the local Modbus TCP endpoint is accepting connections | Modbus communication |
| 23 | `23_modbus_smoke_test_20.png` | Shows Python writing 20°C and reading the fan as OFF | Modbus communication |
| 24 | `24_modbus_smoke_test_35.png` | Shows Python writing 35°C and reading the fan as ON | Modbus communication |
| 25 | `25_validation_console.png` | Shows all nine automated tests passing with zero failures | Validation results |
| 26 | `26_validation_csv.png` | Shows the recorded expected and actual controller states | Validation results |
| 27 | `../results/validation_plot.png` | Visualizes temperature inputs, hysteresis thresholds, and actual fan state | Validation results |