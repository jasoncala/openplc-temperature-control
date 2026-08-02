# OpenPLC Runtime v3 Setup

## Runtime environment

- Host operating system: Windows
- Container engine: Docker Desktop
- Runtime: OpenPLC Runtime v3
- Docker image: `openplc-v3-local`
- Container name: `openplc-v3`
- Persistent volume: `openplc-v3-data`
- Runtime source commit: See `runtime_commit.txt`

## Custom build

The archived OpenPLC Runtime v3 source did not build correctly from its stock
Dockerfile on the Windows checkout.

The local build therefore uses:

- A repository checkout configured for Unix LF line endings
- A custom Dockerfile under `docker/OpenPLC_v3.Dockerfile`
- Explicit CRLF-to-LF normalization for Linux build files
- Strict pipeline failure detection
- Verification that the MatIEC compiler, Python environment, webserver, and
  startup script exist before the Docker image is accepted

The modified Dockerfile is part of this project's reproducible environment.

## Network exposure

- Web dashboard: `http://127.0.0.1:8080`
- Modbus TCP endpoint: `127.0.0.1:1502`
- Container-side Modbus port: `502`

The host ports are deliberately bound to `127.0.0.1`. The legacy runtime is
not published on all host network interfaces.

## Authentication

- Initial username: `openplc`
- Default password changed immediately: Yes
- New password stored in Git: No
- New password shown in screenshots: No
- Login verified after changing password: Yes

## Start Runtime

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\start_openplc.ps1