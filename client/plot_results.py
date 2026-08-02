"""Plot OpenPLC temperature-controller validation results."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt


INPUT_FILE = Path(
    "results/validation_results.csv"
)
OUTPUT_FILE = Path(
    "results/validation_plot.png"
)

FAN_ON_THRESHOLD = 30
FAN_OFF_THRESHOLD = 27


def parse_bool(value: str) -> int:
    """Convert a CSV Boolean string to zero or one."""
    normalized = value.strip().lower()

    if normalized == "true":
        return 1

    if normalized == "false":
        return 0

    raise ValueError(
        f"Unexpected Boolean value: {value}"
    )


def main() -> None:
    test_numbers: list[int] = []
    temperatures: list[int] = []
    fan_states: list[int] = []

    with INPUT_FILE.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            test_numbers.append(
                int(row["test_number"])
            )
            temperatures.append(
                int(row["temperature_read"])
            )
            fan_states.append(
                parse_bool(row["actual_fan"])
            )

    figure, temperature_axis = plt.subplots(
        figsize=(10, 5.5)
    )

    temperature_axis.plot(
        test_numbers,
        temperatures,
        marker="o",
        label="Temperature",
    )

    temperature_axis.axhline(
        FAN_ON_THRESHOLD,
        linestyle="--",
        label=(
            f"Fan ON threshold "
            f"({FAN_ON_THRESHOLD}°C)"
        ),
    )

    temperature_axis.axhline(
        FAN_OFF_THRESHOLD,
        linestyle=":",
        label=(
            f"Fan OFF threshold "
            f"({FAN_OFF_THRESHOLD}°C)"
        ),
    )

    temperature_axis.set_xlabel(
        "Validation test number"
    )
    temperature_axis.set_ylabel(
        "Temperature (°C)"
    )
    temperature_axis.set_xticks(
        test_numbers
    )
    temperature_axis.grid(True)
    temperature_axis.legend(
        loc="upper left"
    )

    fan_axis = temperature_axis.twinx()

    fan_axis.step(
        test_numbers,
        fan_states,
        where="mid",
        label="Fan state",
    )

    fan_axis.set_ylabel(
        "Fan state"
    )
    fan_axis.set_yticks(
        [0, 1]
    )
    fan_axis.set_yticklabels(
        ["OFF", "ON"]
    )
    fan_axis.legend(
        loc="upper right"
    )

    temperature_axis.set_title(
        "OpenPLC Temperature-Control Validation"
    )

    figure.tight_layout()

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    figure.savefig(
        OUTPUT_FILE,
        dpi=200,
    )

    print(f"Plot saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()