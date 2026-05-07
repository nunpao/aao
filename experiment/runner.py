from collections.abc import Callable, Sequence
from time import perf_counter

from models import InstanceData, InstanceReport, ReportRow, SolutionData


ConstructiveFn = Callable[[InstanceData], SolutionData]
LocalSearchFn = Callable[[InstanceData, SolutionData], SolutionData]
ConstructiveSpec = tuple[str, ConstructiveFn]
LocalSearchSpec = tuple[str, LocalSearchFn]


def run_combination(
    instance: InstanceData,
    constructive_name: str,
    constructive_fn: ConstructiveFn,
    local_search_name: str,
    local_search_fn: LocalSearchFn,
) -> ReportRow:
    start_time = perf_counter()

    initial_solution = constructive_fn(instance)
    found_solution = local_search_fn(instance, initial_solution)

    runtime = perf_counter() - start_time
    deviation = (instance.optimal - found_solution.z) / instance.optimal

    return ReportRow(
        constructive_name=constructive_name,
        local_search_name=local_search_name,
        initial_solution=initial_solution.z,
        found_solution=found_solution.z,
        deviation=deviation,
        runtime=runtime,
    )


def run_combinations(
    instance: InstanceData,
    constructives: Sequence[ConstructiveSpec],
    local_searches: Sequence[LocalSearchSpec],
) -> list[ReportRow]:
    rows = []

    for constructive_name, constructive_fn in constructives:
        for local_search_name, local_search_fn in local_searches:
            row = run_combination(
                instance,
                constructive_name,
                constructive_fn,
                local_search_name,
                local_search_fn,
            )
            rows.append(row)

    return rows


def build_instance_report(
    instance: InstanceData,
    constructives: Sequence[ConstructiveSpec],
    local_searches: Sequence[LocalSearchSpec],
) -> InstanceReport:
    rows = run_combinations(instance, constructives, local_searches)
    return InstanceReport(instance=instance, rows=rows)
