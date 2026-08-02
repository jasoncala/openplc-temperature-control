"""Perform a basic Modbus test against the OpenPLC controller."""

from __future__ import annotations

import argparse
import time

from pymodbus.client import ModbusTcpClient


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 1502
DEVICE_ID = 1

TEMPERATURE_REGISTER = 1024
FAN_COIL = 0


def validate_response(response: object, operation: str) -> None:
    """Raise an informative exception for an invalid response."""
    if response is None:
        raise RuntimeError(f"{operation} returned no response")

    is_error = getattr(response, "isError", None)

    if callable(is_error) and is_error():
        raise RuntimeError(f"{operation} failed: {response}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Test basic Modbus communication with OpenPLC."
    )
    parser.add_argument(
        "--host",
        default=DEFAULT_HOST,
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
    )
    parser.add_argument(
        "--temperature",
        type=int,
        required=True,
    )

    args = parser.parse_args()

    if not 0 <= args.temperature <= 65535:
        print(
            "ERROR: temperature must fit in an unsigned "
            "16-bit Modbus register"
        )
        return 1

    client = ModbusTcpClient(
        host=args.host,
        port=args.port,
        timeout=3,
    )

    try:
        if not client.connect():
            raise ConnectionError(
                f"Unable to connect to "
                f"{args.host}:{args.port}"
            )

        write_response = client.write_register(
            address=TEMPERATURE_REGISTER,
            value=args.temperature,
            device_id=DEVICE_ID,
        )
        validate_response(
            write_response,
            "Temperature write",
        )

        # Allow several PLC scan cycles to execute.
        time.sleep(0.5)

        temperature_response = client.read_holding_registers(
            address=TEMPERATURE_REGISTER,
            count=1,
            device_id=DEVICE_ID,
        )
        validate_response(
            temperature_response,
            "Temperature read",
        )

        fan_response = client.read_coils(
            address=FAN_COIL,
            count=1,
            device_id=DEVICE_ID,
        )
        validate_response(
            fan_response,
            "Fan read",
        )

        actual_temperature = int(
            temperature_response.registers[0]
        )
        actual_fan = bool(
            fan_response.bits[0]
        )

        print(f"Connected to: {args.host}:{args.port}")
        print(f"Temperature written: {args.temperature}")
        print(f"Temperature read: {actual_temperature}")
        print(
            f"Fan state: "
            f"{'ON' if actual_fan else 'OFF'}"
        )

        return 0

    except (
        ConnectionError,
        RuntimeError,
        OSError,
    ) as error:
        print(f"ERROR: {error}")
        return 1

    finally:
        client.close()


if __name__ == "__main__":
    raise SystemExit(main())