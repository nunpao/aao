import random

from models import InstanceData, SolutionData

def random_greedy(instance: InstanceData, alpha: float):
    """
    Builds a solution using a randomized greedy construction strategy.

    This heuristic begins by ranking items according to their efficiency, defined as the ratio between value and weight. At each iteration, it does not immediately choose the single best item. Instead, it creates a restricted candidate list containing the feasible items with the highest efficiencies, and then randomly selects one of them.

    The ``alpha`` parameter controls the size of this restricted candidate list. Smaller values make the method behave more like a strict greedy heuristic, while larger values allow a wider set of feasible items to be considered at each step.

    Args:
        instance:
            Problem instance containing the number of items, knapsack capacity, and the aligned ``values`` and ``weights`` vectors used during the solution construction.
        alpha:
            Parameter in the interval ``[0, 1]`` used to define the threshold for the restricted candidate list.

    Returns:
        SolutionData:
            A solution represented by a binary selection vector and its corresponding objective value ``z``.
    """

    if not 0 <= alpha <= 1:
        raise ValueError("alpha must be in [0, 1]")

    rng = random

    # Compute the efficiency of each item
    efficiency = [instance.values[i] / instance.weights[i] for i in range(instance.item_count)]

    # Sort item indices by decreasing efficiency
    candidates = sorted(range(instance.item_count), key=lambda i: efficiency[i], reverse=True)

    solution = [0] * instance.item_count
    z = 0
    current_weight = 0

    while candidates:
        # Keep only the items that still fit in the remaining capacity.
        feasible = [i for i in candidates if current_weight + instance.weights[i] <= instance.capacity]
        if not feasible:
            break

        # Define the threshold for the restricted candidate list (RCL).
        emax = efficiency[feasible[0]]
        emin = efficiency[feasible[-1]]
        tau = emax - alpha * (emax - emin)

        # The RCL contains the feasible items whose efficiency is at least tau.
        lrc = [i for i in feasible if efficiency[i] >= tau]

        # Randomly choose one item from the RCL and add it to the solution.
        chosen = rng.choice(lrc)
        solution[chosen] = 1
        current_weight += instance.weights[chosen]
        z += instance.values[chosen]
        candidates.remove(chosen)

    return SolutionData(solution, z)