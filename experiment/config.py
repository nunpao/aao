from functools import partial

from heuristics.constructive.efficiency_greedy import efficiency_greedy
from heuristics.constructive.random_greedy import random_greedy
from heuristics.constructive.weight_greedy import weight_greedy
from heuristics.local_search.limited_two_exchange import limited_two_exchange
from heuristics.local_search.one_exchange import one_exchange
from heuristics.local_search.two_exchange import two_exchange
from experiment.runner import ConstructiveSpec, LocalSearchSpec
from models import InstanceData, SolutionData


def _no_local_search(_instance: InstanceData, initial_solution: SolutionData) -> SolutionData:
    """
    Returns the constructive solution unchanged so it can be benchmarked alongside the local searches.
    """
    return SolutionData (initial_solution.solution.copy(), initial_solution.z)

def get_constructives() -> list[ConstructiveSpec]:
    """
    Builds the list of constructive heuristics included in the experiment.

    Returns:
        list[ConstructiveSpec]:
            Pairs ``(name, function)`` describing each constructive method to evaluate.
    """
    constructives: list[ConstructiveSpec] = [
        ("weight", weight_greedy),
        ("efficiency", efficiency_greedy),
        ("random_a_0.1", partial(random_greedy, alpha=0.1)),
        ("random_a_0.3", partial(random_greedy, alpha=0.3)),
    ]

    return constructives


def get_local_searches(include_two_exchange: bool = False) -> list[LocalSearchSpec]:
    """
    Builds the local search configurations included in the experiment.

    Args:
        include_two_exchange:
            Whether to append the full 2-exchange neighborhood search to the default list.

    Returns:
        list[LocalSearchSpec]:
            Pairs ``(name, function)`` describing each local search variant to evaluate.
    """
    local_searches: list[LocalSearchSpec] = [
        ("", _no_local_search),
        ("one_exchange", one_exchange),
        # These variants restrict the 2-exchange neighborhood to the most promising candidates.
        ("limited_two_exchange_kin_100_kout_50", partial(limited_two_exchange, k_in=100, k_out=50)),
        ("limited_two_exchange_kin_125_kout_75", partial(limited_two_exchange, k_in=125, k_out=75)),
    ]

    if include_two_exchange:
        local_searches.append(("two_exchange", two_exchange))

    return local_searches
