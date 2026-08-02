# Troubleshooting Log

Copy this template for each issue.

---

## Issue

- Date and time:
- Step number:
- Expected behavior:
- Observed behavior:
- Exact error message:
- Initial hypothesis:
- Diagnostic commands performed:
- Root cause:
- Resolution:
- Evidence captured:
- Related Git commit:


---

## OpenPLC Runtime v3 Docker Build and Startup Failure

* **Date:** August 1, 2026
* **Affected steps:** Steps 13–17
* **Component:** OpenPLC Runtime v3 Docker environment
* **Final status:** Resolved

### Expected behavior

The OpenPLC Runtime v3 source should build into the Docker image `openplc-v3-local`. The `openplc-v3` container should then start successfully and expose:

* OpenPLC web interface at `http://127.0.0.1:8080`
* Modbus TCP at `127.0.0.1:1502`

### Initial observed behavior

The original Docker build appeared to complete and created the image. However, the container failed immediately when started with:

```text
OCI runtime create failed:
exec: "./start_openplc.sh":
stat ./start_openplc.sh: no such file or directory
```

Running:

```powershell
docker logs --tail 100 openplc-v3
```

returned no application logs because the container failed before the OpenPLC startup script could execute.

The initial `start_openplc.ps1` script also continued printing the expected dashboard and Modbus addresses after Docker had failed, which made the startup result appear more successful than it actually was.

### Diagnostics performed

The image was inspected by overriding its entry point:

```powershell
docker run --rm `
    --entrypoint /bin/bash `
    openplc-v3-local `
    -lc 'ls -la /workdir/start_openplc.sh || true; tail -n 150 /workdir/install_log.txt || true'
```

This confirmed that:

```text
/workdir/start_openplc.sh
```

did not exist.

Pipeline failure checking was then added to the Docker installation process so that failures inside the OpenPLC installer could no longer be hidden by its output being piped through `tee`.

After rebuilding with strict failure checking, the actual installation failure became visible during the MatIEC compiler stage:

```text
[MATIEC COMPILER]
configure.ac:72: error: '\' is already registered with AC_CONFIG_FILES.
autom4te: error: /usr/bin/m4 failed with exit status: 1
aclocal: error: /usr/bin/autom4te failed with exit status: 1
autoreconf: error: aclocal failed with exit status: 1
./background_installer.sh: line 124: ./configure: No such file or directory
make: *** No targets specified and no makefile found. Stop.
cp: cannot stat './iec2c': No such file or directory
Error compiling MatIEC
OpenPLC was NOT installed!
```

A separate nonfatal installer issue also appeared:

```text
/usr/bin/python3: No module named pip
```

The required Python packages had already been installed into OpenPLC’s virtual environment, so the failing system-Python PyModbus installation was redundant.

### Root cause

The primary root cause was Windows CRLF line-ending conversion in legacy OpenPLC and MatIEC build-system files.

MatIEC’s `configure.ac` uses Unix-style backslash line continuations inside `AC_CONFIG_FILES`. With CRLF line endings, the carriage-return character appears after the backslash. Autoconf therefore interprets the backslash as an actual configuration-file entry instead of a continuation character.

This caused `autoreconf` to fail, prevented MatIEC’s `configure` script and `iec2c` compiler from being generated, stopped the remainder of the OpenPLC installation, and prevented `start_openplc.sh` from being created.

Changing the base image from Debian Trixie to Debian Bookworm alone did not resolve the problem. The same MatIEC error occurred with Autoconf 2.71, confirming that the source-file line endings—not only the Autoconf version—were responsible.

The original Docker build had appeared successful because the archived OpenPLC installer piped its installation output through `tee` without reliable pipeline-failure propagation. The successful exit status from `tee` could hide the failed installation command.

### Resolution

The issue was resolved through the following changes:

1. Removed the Windows-converted OpenPLC Runtime source clone.

2. Recloned OpenPLC Runtime v3 with automatic CRLF conversion disabled:

```powershell
git clone `
    -c core.autocrlf=false `
    https://github.com/thiagoralves/OpenPLC_v3.git `
    OpenPLC_v3

git -C "OpenPLC_v3" config core.autocrlf false
git -C "OpenPLC_v3" config core.eol lf
```

3. Verified that `utils/matiec_src/configure.ac` contained zero carriage-return bytes.

4. Created a custom Dockerfile at:

```text
docker/OpenPLC_v3.Dockerfile
```

5. Added defensive CRLF-to-LF normalization inside the Docker image for Linux build files, including:

* `.sh`
* `.ac`
* `.am`
* `.m4`
* `.in`
* CMake files
* Makefiles

6. Enabled strict pipeline-failure detection so failed installer commands could not be hidden by `tee`.

7. Removed the redundant system-level command that attempted to install PyModbus through `/usr/bin/python3`.

8. Added build-time verification for critical OpenPLC artifacts:

```text
/workdir/start_openplc.sh
/workdir/.venv/bin/python3
/workdir/webserver/webserver.py
/workdir/webserver/iec2c
```

9. Changed the Docker entry point to the absolute path:

```text
/workdir/start_openplc.sh
```

10. Updated `scripts/start_openplc.ps1` to inspect Docker’s native exit code and stop with an error instead of printing success information after a failed container startup.

11. Removed the failed image and container, rebuilt the image from the LF-only source, and recreated the container.

### Successful verification

After applying the fixes:

* The Docker image built successfully.
* The MatIEC `iec2c` compiler was generated.
* `start_openplc.sh` existed and was executable.
* OpenPLC’s Python virtual environment and webserver files were present.
* The `openplc-v3` container remained in the `Up` state.
* Port 8080 accepted connections.
* The OpenPLC Runtime login page opened successfully at:

```text
http://127.0.0.1:8080
```

* The default `openplc` account successfully authenticated.
* The default password was changed immediately.
* Login was verified using the new password.
* The Runtime ports were bound only to localhost:

```text
127.0.0.1:8080 -> container port 8080
127.0.0.1:1502 -> container port 502
```

### Security and reproducibility outcome

The legacy Runtime remains isolated inside Docker and is not exposed on all Windows network interfaces. No OpenPLC password is stored in the repository, scripts, notes, screenshots, or report.

The custom Dockerfile, LF-only checkout instructions, startup scripts, source commit hash, and verification records are retained in the project so the working Runtime environment can be reproduced.

### Evidence files

Relevant diagnostic and verification files include:

```text
notes/openplc_failed_image_diagnostic.txt
notes/openplc_corrected_build.txt
notes/openplc_build_failure_summary.txt
notes/openplc_build_failure_tail.txt
notes/openplc_line_endings_before.txt
notes/openplc_line_endings_after.txt
notes/openplc_lf_build.txt
notes/openplc_lf_verification.txt
notes/openplc_image_metadata.txt
notes/openplc_container_metadata.txt
notes/runtime_commit.txt
notes/runtime_setup.md
docker/OpenPLC_v3.Dockerfile
scripts/start_openplc.ps1
screenshots/08_openplc_runtime_dashboard.png
screenshots/09_openplc_localhost_ports.png
```

Some diagnostic files may be omitted from Git if they contain only repetitive package-installation output. The concise troubleshooting record, final Dockerfile, verification results, and successful screenshots are the primary evidence.

### Related Git commit

```text
Set up isolated OpenPLC Runtime v3 environment
```
