import csv
import math
from pathlib import Path

from models import InstanceReport, ReportRow

def export_instance_report(report: InstanceReport, output_dir: str | Path) -> Path:
    """
    Writes the results of one instance to a CSV file.

    Args:
        report:
            Instance-level report containing all evaluated heuristic combinations.
        output_dir:
            Destination directory where the CSV file will be created.

    Returns:
        Path:
            Path to the generated CSV file.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    csv_path = output_path / f"{Path(report.instance.name).stem}_results.csv"

    with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=[
                "Heuristics",
                "Instance",
                "Optimum",
                "Initial Solution",
                "Found Solution",
                "Deviation",
                "Time",
            ],
        )
        writer.writeheader()

        # Export one row per heuristic combination, preserving both solution quality and runtime metrics.
        for row in report.rows:
            writer.writerow(
                {
                    "Heuristics": _build_algorithm_name(row),
                    "Instance": report.instance.name,
                    "Initial Solution": row.initial_solution,
                    "Found Solution": row.found_solution,
                    "Optimum": report.instance.optimal,
                    "Deviation": f"{row.deviation}",
                    "Time": f"{_truncate_decimal(row.runtime)}s",
                }
            )

    return csv_path


def _build_algorithm_name(row: ReportRow) -> str:
    """
    Builds the display name used in the CSV to identify each heuristic combination.
    """
    if not row.local_search_name:
        return row.constructive_name

    return f"{row.constructive_name} + {row.local_search_name}"


def _truncate_decimal(value: float, decimal_places: int = 4) -> str:
    """
    Truncates a floating-point value to a fixed number of decimal places without rounding it up.
    """
    factor = 10 ** decimal_places
    truncated = math.trunc(value * factor) / factor
    return f"{truncated:.{decimal_places}f}"
