import argparse
from time import perf_counter

from file_io.instance_loader import load_all_instances, load_named_instance
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
    parser.add_argument(
        "--instance",
        help="Run the experiment for a single instance file name or stem.",
    )
    return parser.parse_args()


def format_duration(seconds: float) -> str:
    total_seconds = int(seconds)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, secs = divmod(remainder, 60)

    if hours > 0:
        return f"{hours}h{minutes}m{secs}s"

    if minutes > 0:
        return f"{minutes}m{secs}s" if secs > 0 else f"{minutes}m"

    return f"{secs}s"


def main():
    total_start = perf_counter()
    args = parse_args()

    if args.instance:
        instances = [load_named_instance("instances", args.instance)]
    else:
        instances = load_all_instances("instances")

    constructives = get_constructives()
    local_searches = get_local_searches(args.include_two_exchange)

    print(f"Successfully loaded {len(instances)} files.")
    print(f"Using {len(constructives)} constructive heuristics and {len(local_searches)} local searches.")

    for instance in instances:
        instance_start = perf_counter()
        report = build_instance_report(instance, constructives, local_searches)
        export_instance_report(report, "results/")
        instance_duration = perf_counter() - instance_start
        print(f"Finished processing instance {instance.name} in {format_duration(instance_duration)}.")

    total_duration = perf_counter() - total_start
    print(f"Finished processing {len(instances)} instance(s) in {format_duration(total_duration)}.")


if __name__ == "__main__":
    main()
