import argparse

from file_io.instance_loader import load_all_instances
from file_io.csv_exporter import export_instance_report
from experiment.config import get_constructives, get_local_searches
from experiment.runner import build_instance_report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--include-two-exchange",
        action="store_true",
        help="Include the two_exchange local search in the experiment set.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    instances = load_all_instances("instances")
    constructives = get_constructives()
    local_searches = get_local_searches(args.include_two_exchange)

    print(f"Successfully loaded {len(instances)} files.")
    print(f"Using {len(constructives)} constructive heuristics and {len(local_searches)} local searches.")

    for instance in instances:
        report = build_instance_report(instance, constructives, local_searches)
        export_instance_report(report, "results/")


if __name__ == "__main__":
    main()
