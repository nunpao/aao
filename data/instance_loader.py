from pathlib import Path
from data.models import *

def load_optimal_values(optimal_file_path):
    optimal_file = Path(optimal_file_path)

    if not optimal_file.exists():
        raise FileNotFoundError(f"Optimal values file not found: {optimal_file}")

    optimal_values = {}

    for line_number, line in enumerate(optimal_file.read_text().splitlines(), start=1):
        stripped_line = line.strip()
        if not stripped_line:
            continue

        parts = stripped_line.split()
        if len(parts) != 2:
            raise ValueError(
                f"Invalid line {line_number} in {optimal_file.name}: expected "
                f"'instance_name optimal_value'."
            )

        instance_name, optimal_value_text = parts

        try:
            optimal_value = int(optimal_value_text)
        except ValueError as error:
            raise ValueError(
                f"Invalid optimal value on line {line_number} in "
                f"{optimal_file.name}: expected an integer."
            ) from error

        optimal_values[instance_name] = optimal_value

    return optimal_values


def load_instance(instance_path, optimal_values):
    instance_file = Path(instance_path)
    lines = instance_file.read_text().splitlines()

    if len(lines) < 3:
        raise ValueError("instance file is too short!")

    n = int(lines[0].strip())
    item_lines = lines[1:n + 1]
    if len(item_lines) != n:
        raise ValueError("the number of items doesnt coincide with the ??, instance may be incomplete")

    v = []
    w = []

    for expected_index, line in enumerate(item_lines):
        parts = line.split()
        if len(parts) != 3:
            raise ValueError(f"Invalid item line: {line!r}")

        item_index, item_value, item_weight = map(int, parts)
        if item_index != expected_index:
            raise ValueError(f"unexpected item index {item_index}; expected {expected_index}")

        v.append(item_value)
        w.append(item_weight)

    W = int(lines[n+1].strip())

    instance_key = instance_file.stem
    if instance_key not in optimal_values:
        raise ValueError(f"No optimal value found for instance {instance_key}.")

    return InstanceData(instance_file.name, n, W, v, w, optimal_values[instance_key])


def load_all_instances(instances_folder):
    folder_path = Path(instances_folder)

    if not folder_path.exists():
        raise FileNotFoundError(f"Instances folder not found: {folder_path}")

    if not folder_path.is_dir():
        raise NotADirectoryError(f"Expected a folder, got: {folder_path}")

    optimal_values = load_optimal_values(folder_path / "optimal.txt")

    instance_files = sorted(
        path for path in folder_path.iterdir()
        if path.is_file() and path.suffix == ".txt" and path.name != "optimal.txt"
    )

    print(f"Reading {len(instance_files)} files from {folder_path}...")

    loaded_instances = []

    for instance_file in instance_files:
        try:
            instance_data = load_instance(instance_file, optimal_values)
        except Exception as error:
            print(f"Error reading file {instance_file.name}: {error}")
            continue

        loaded_instances.append(instance_data)

    return loaded_instances
