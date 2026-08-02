FROM debian:bookworm-slim

COPY . /workdir

WORKDIR /workdir

# Normalize build scripts and build-system metadata to Unix LF endings.
# This protects the Linux build from Windows CRLF checkout conversion.
RUN find /workdir -type f \
        \( \
            -name "*.sh" \
            -o -name "*.ac" \
            -o -name "*.am" \
            -o -name "*.m4" \
            -o -name "*.in" \
            -o -name "*.cmake" \
            -o -name "CMakeLists.txt" \
            -o -name "Makefile" \
            -o -name "Makefile.*" \
        \) \
        -exec sed -i 's/\r$//' {} +

RUN set -eux; \
    mkdir -p /docker_persistent; \
    sed -i '2i set -o pipefail' /workdir/install.sh; \
    sed -i \
        '/^[[:space:]]*python3 -m pip install pymodbus==2\.5\.3[[:space:]]*$/d' \
        /workdir/background_installer.sh; \
    ./install.sh docker; \
    test -x /workdir/start_openplc.sh; \
    test -x /workdir/.venv/bin/python3; \
    test -f /workdir/webserver/webserver.py; \
    test -x /workdir/webserver/iec2c; \
    /workdir/.venv/bin/python3 -c \
        "import flask, pymodbus; print('Python dependencies verified')"; \
    touch /docker_persistent/mbconfig.cfg; \
    touch /docker_persistent/persistent.file; \
    mkdir -p /docker_persistent/st_files; \
    cp /workdir/webserver/openplc.db \
        /docker_persistent/openplc.db; \
    mv /workdir/webserver/openplc.db \
        /workdir/webserver/openplc_default.db; \
    cp /workdir/webserver/dnp3.cfg \
        /docker_persistent/dnp3.cfg; \
    mv /workdir/webserver/dnp3.cfg \
        /workdir/webserver/dnp3_default.cfg; \
    cp -r /workdir/webserver/st_files/. \
        /docker_persistent/st_files/; \
    mv /workdir/webserver/st_files \
        /workdir/webserver/st_files_default; \
    cp /workdir/webserver/active_program \
        /docker_persistent/active_program; \
    mv /workdir/webserver/active_program \
        /workdir/webserver/active_program_default; \
    ln -s /docker_persistent/mbconfig.cfg \
        /workdir/webserver/mbconfig.cfg; \
    ln -s /docker_persistent/persistent.file \
        /workdir/webserver/persistent.file; \
    ln -s /docker_persistent/openplc.db \
        /workdir/webserver/openplc.db; \
    ln -s /docker_persistent/dnp3.cfg \
        /workdir/webserver/dnp3.cfg; \
    ln -s /docker_persistent/st_files \
        /workdir/webserver/st_files; \
    ln -s /docker_persistent/active_program \
        /workdir/webserver/active_program

VOLUME ["/docker_persistent"]

ENTRYPOINT ["/workdir/start_openplc.sh"]