from functools import partial

from heuristics.constructive import efficiency_greedy, random_greedy, weight_greedy
from heuristics.local_search import no_local_search, one_exchange, two_exchange
from experiment.runner import ConstructiveSpec, LocalSearchSpec


def get_constructives() -> list[ConstructiveSpec]:
    constructives: list[ConstructiveSpec] = [
        ("weight", weight_greedy),
        ("efficiency", efficiency_greedy),
        ("random", partial(random_greedy, alpha=0.1)),
    ]

    return constructives


def get_local_searches(include_two_exchange: bool = False) -> list[LocalSearchSpec]:
    local_searches: list[LocalSearchSpec] = [
        ("", no_local_search),
        ("one_exchange", one_exchange),
    ]

    if include_two_exchange:
        local_searches.append(("two_exchange", two_exchange))

    return local_searches
