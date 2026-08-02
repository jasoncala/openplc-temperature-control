"""Validate the OpenPLC hysteresis temperature controller."""

from __future__ import annotations

import argparse
import csv
import time
from dataclasses import asdict, dataclass
from pathlib import Path

from pymodbus.client import ModbusTcpClient


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 1502
DEVICE_ID = 1

TEMPERATURE_REGISTER = 1024
FAN_COIL = 0

FAN_ON_THRESHOLD = 30
FAN_OFF_THRESHOLD = 27

POLL_INTERVAL_SECONDS = 0.1
POLL_TIMEOUT_SECONDS = 2.0

TEST_SEQUENCE = [
    (20, "Establish known low state"),
    (27, "Exact fan-off threshold"),
    (28, "Hysteresis region retains OFF"),
    (30, "Exact fan-on threshold"),
    (29, "Hysteresis region retains ON"),
    (27, "Downward transition"),
    (40, "Clearly high temperature"),
    (35, "Remain ON above threshold"),
    (27, "Final shutdown"),
]


@dataclass
class TestResult:
    """One PLC validation result."""

    test_number: int
    description: str
    temperature_written: int
    temperature_read: int
    previous_expected_fan: bool
    expected_fan: bool
    actual_fan: bool
    elapsed_seconds: float
    passed: bool


def validate_response(response: object, operation: str) -> None:
    """Raise an exception for an invalid Modbus response."""
    if response is None:
        raise RuntimeError(f"{operation} returned no response")

    is_error = getattr(response, "isError", None)

    if callable(is_error) and is_error():
        raise RuntimeError(f"{operation} failed: {response}")


def calculate_expected_fan(
    temperature: int,
    previous_state: bool,
) -> bool:
    """Apply the same hysteresis rules as the PLC."""
    if temperature >= FAN_ON_THRESHOLD:
        return True

    if temperature <= FAN_OFF_THRESHOLD:
        return False

    return previous_state


def read_controller_state(
    client: ModbusTcpClient,
) -> tuple[int, bool]:
    """Read the current PLC temperature and fan state."""
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

    return (
        int(temperature_response.registers[0]),
        bool(fan_response.bits[0]),
    )


def wait_for_expected_state(
    client: ModbusTcpClient,
    expected_temperature: int,
    expected_fan: bool,
) -> tuple[int, bool, float]:
    """Poll until expected state appears or timeout expires."""
    start_time = time.monotonic()

    actual_temperature = -1
    actual_fan = False

    while True:
        actual_temperature, actual_fan = (
            read_controller_state(client)
        )

        elapsed = time.monotonic() - start_time

        if (
            actual_temperature == expected_temperature
            and actual_fan == expected_fan
        ):
            return (
                actual_temperature,
                actual_fan,
                elapsed,
            )

        if elapsed >= POLL_TIMEOUT_SECONDS:
            return (
                actual_temperature,
                actual_fan,
                elapsed,
            )

        time.sleep(POLL_INTERVAL_SECONDS)


def write_csv(
    results: list[TestResult],
    output_file: Path,
) -> None:
    """Write the validation results to a CSV file."""
    if not results:
        raise RuntimeError(
            "No validation results were produced"
        )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_file.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=list(
                asdict(results[0]).keys()
            ),
        )
        writer.writeheader()

        for result in results:
            writer.writerow(
                asdict(result)
            )


def run_validation(
    host: str,
    port: int,
    output_file: Path,
) -> list[TestResult]:
    """Run the complete ordered validation sequence."""
    client = ModbusTcpClient(
        host=host,
        port=port,
        timeout=3,
    )

    if not client.connect():
        raise ConnectionError(
            f"Unable to connect to OpenPLC "
            f"at {host}:{port}"
        )

    results: list[TestResult] = []
    expected_fan = False

    try:
        # Establish a deterministic initial state.
        reset_response = client.write_register(
            address=TEMPERATURE_REGISTER,
            value=20,
            device_id=DEVICE_ID,
        )
        validate_response(
            reset_response,
            "Initial reset",
        )

        time.sleep(0.5)

        for test_number, test_case in enumerate(
            TEST_SEQUENCE,
            start=1,
        ):
            temperature, description = test_case

            previous_expected_fan = expected_fan

            expected_fan = calculate_expected_fan(
                temperature,
                previous_expected_fan,
            )

            write_response = client.write_register(
                address=TEMPERATURE_REGISTER,
                value=temperature,
                device_id=DEVICE_ID,
            )
            validate_response(
                write_response,
                "Temperature write",
            )

            (
                actual_temperature,
                actual_fan,
                elapsed,
            ) = wait_for_expected_state(
                client=client,
                expected_temperature=temperature,
                expected_fan=expected_fan,
            )

            passed = (
                actual_temperature == temperature
                and actual_fan == expected_fan
            )

            result = TestResult(
                test_number=test_number,
                description=description,
                temperature_written=temperature,
                temperature_read=actual_temperature,
                previous_expected_fan=(
                    previous_expected_fan
                ),
                expected_fan=expected_fan,
                actual_fan=actual_fan,
                elapsed_seconds=round(
                    elapsed,
                    3,
                ),
                passed=passed,
            )

            results.append(result)

            status = (
                "PASS"
                if passed
                else "FAIL"
            )

            print(
                f"{status} | "
                f"Test {test_number} | "
                f"{description} | "
                f"Written={temperature} | "
                f"Read={actual_temperature} | "
                f"Expected fan="
                f"{'ON' if expected_fan else 'OFF'} | "
                f"Actual fan="
                f"{'ON' if actual_fan else 'OFF'} | "
                f"Elapsed={elapsed:.3f}s"
            )

    finally:
        client.close()

    write_csv(
        results=results,
        output_file=output_file,
    )

    return results


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Validate the OpenPLC temperature "
            "controller over Modbus TCP."
        )
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
        "--output",
        type=Path,
        default=Path(
            "results/validation_results.csv"
        ),
    )

    args = parser.parse_args()

    try:
        results = run_validation(
            host=args.host,
            port=args.port,
            output_file=args.output,
        )
    except (
        ConnectionError,
        RuntimeError,
        OSError,
    ) as error:
        print(f"ERROR: {error}")
        return 1

    failure_count = sum(
        not result.passed
        for result in results
    )

    print()
    print(f"Tests completed: {len(results)}")
    print(
        f"Tests passed: "
        f"{len(results) - failure_count}"
    )
    print(f"Tests failed: {failure_count}")
    print(f"Results saved to: {args.output}")

    return 1 if failure_count else 0


if __name__ == "__main__":
    raise SystemExit(main())