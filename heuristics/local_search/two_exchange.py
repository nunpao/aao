from models import InstanceData, SolutionData
from itertools import combinations

def two_exchange(instance: InstanceData, initial_solution: SolutionData):
    """
    Improves a solution by exchanging two selected items with two unselected items.

    This local search heuristic explores the 2-exchange neighborhood of the current solution. Instead of testing single-item swaps, it considers moves where two items currently inside the knapsack are removed and replaced by two items that are currently outside it.

    This wider neighborhood allows the heuristic to evaluate changes that may not be reachable through a single exchange. For each candidate move, the method checks whether the new total weight is feasible and whether the new combination increases the objective value.

    Args:
        instance:
            Problem instance containing the number of items, knapsack capacity, and the aligned ``values`` and ``weights`` vectors.
        initial_solution:
            Starting solution that will be used as the base for this local search procedure.

    Returns:
        SolutionData:
            The final solution obtained after no further improving 2-item exchanges can be found.
    """

    solution = initial_solution.solution.copy()
    z = initial_solution.z

    # Compute the total weight of the initial solution so that each candidate exchange can be evaluated relative to the current state.
    current_weight = sum(instance.weights[i] for i in range(instance.item_count) if solution[i] == 1)

    # s1 contains the selected items, while s0 contains the items that are not currently part of the solution.
    s1 = {i for i in range(instance.item_count) if solution[i] == 1}
    s0 = {i for i in range(instance.item_count) if solution[i] == 0}

    improved = True

    while improved:
        improved = False
        for i1, i2 in combinations(list(s1), 2):
            for j1, j2 in combinations(list(s0), 2):
                # Evaluate the effect of removing items i1 and i2 and adding items j1 and j2.
                new_weight = (current_weight - instance.weights[i1] - instance.weights[i2]
                              + instance.weights[j1] + instance.weights[j2])
                delta_v = instance.values[j1] + instance.values[j2] - instance.values[i1] - instance.values[i2]

                # Accept the exchange only if the new solution is feasible and improves the total objective value.
                if new_weight <= instance.capacity and delta_v > 0:
                    solution[i1] = solution[i2] = 0
                    solution[j1] = solution[j2] = 1

                    # Update the selected and unselected sets to reflect the accepted exchange.
                    s1.difference_update((i1, i2))
                    s0.update((i1, i2))

                    s0.difference_update((j1, j2))
                    s1.update((j1,j2))

                    current_weight = new_weight
                    z += delta_v
                    improved = True
                    break
            if improved:
                break
    return SolutionData (solution, z)
