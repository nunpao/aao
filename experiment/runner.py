from collections.abc import Callable, Sequence
from time import perf_counter

from models import InstanceData, InstanceReport, ReportRow, SolutionData


ConstructiveFn = Callable[[InstanceData], SolutionData]
LocalSearchFn = Callable[[InstanceData, SolutionData], SolutionData]
ConstructiveSpec = tuple[str, ConstructiveFn]
LocalSearchSpec = tuple[str, LocalSearchFn]


def _run_combination(
    instance: InstanceData,
    constructive_name: str,
    initial_solution: SolutionData,
    constructive_runtime: float,
    local_search_name: str,
    local_search_fn: LocalSearchFn,
) -> ReportRow:
    """
    Executes one local search on top of a previously generated constructive solution and records the corresponding report row.
    """
    start_time = perf_counter()

    found_solution = local_search_fn(instance, initial_solution)

    # The reported runtime should reflect the full combination cost: constructive phase plus local search phase.
    local_search_runtime = perf_counter() - start_time
    runtime = constructive_runtime + local_search_runtime
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
    """
    Evaluates all constructive/local-search combinations for one instance.

    The constructive solution is generated once per constructive heuristic and then reused across all local searches so that every comparison starts from the same base solution.
    """

    rows = []

    for constructive_name, constructive_fn in constructives:
        # Reuse the same constructive solution for every local search tied to this constructive heuristic.
        constructive_start = perf_counter()
        initial_solution = constructive_fn(instance)
        constructive_runtime = perf_counter() - constructive_start

        for local_search_name, local_search_fn in local_searches:
            row = _run_combination(
                instance,
                constructive_name,
                initial_solution,
                constructive_runtime,
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
    """
    Aggregates the report rows produced for a single instance into the report object exported later to CSV.
    """
    rows = run_combinations(instance, constructives, local_searches)
    return InstanceReport(instance=instance, rows=rows)
