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
    return SolutionData (initial_solution.solution.copy(), initial_solution.z)

def get_constructives() -> list[ConstructiveSpec]:
    constructives: list[ConstructiveSpec] = [
        ("weight", weight_greedy),
        ("efficiency", efficiency_greedy),
        ("random", partial(random_greedy, alpha=0.1)),
    ]

    return constructives


def get_local_searches(include_two_exchange: bool = False) -> list[LocalSearchSpec]:
    local_searches: list[LocalSearchSpec] = [
        ("", _no_local_search),
        ("one_exchange", one_exchange),
        ("limited_two_exchange_kin_100_kout_50", partial(limited_two_exchange, k_in=100, k_out=50)),
    ]

    if include_two_exchange:
        local_searches.append(("two_exchange", two_exchange))

    return local_searches
