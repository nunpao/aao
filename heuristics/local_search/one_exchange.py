from models import InstanceData, SolutionData

def one_exchange(instance: InstanceData, initial_solution: SolutionData):
    """
    Improves a solution by iteratively exchanging one selected item with one unselected item.

    This local search heuristic explores the 1-exchange neighborhood of the current solution. In each step, it tries to remove one item that is currently inside the knapsack and replace it with one item that is currently outside the knapsack.

    A swap is accepted only if the new solution remains within the knapsack capacity and increases the total objective value. Whenever an improving exchange is found, the solution is updated and the search continues from the new solution.

    Args:
        instance:
            Problem instance containing the number of items, knapsack capacity, and the aligned ``values`` and ``weights`` vectors.
        initial_solution:
            Starting solution that will be used as the base for this local search procedure.

    Returns:
        SolutionData:
            The final solution obtained after no further improving 1-item exchanges can be found.
    """

    solution = initial_solution.solution.copy()
    z = initial_solution.z

    # Compute the total weight of the initial solution so that feasibility can be checked efficiently during each candidate exchange.
    current_weight = sum(instance.weights[i] for i in range(instance.item_count) if solution[i] == 1)

    # s1 contains the indices of selected items, and s0 contains the indices of unselected items.
    s1 = {i for i in range(instance.item_count) if solution[i] == 1}
    s0 = {i for i in range(instance.item_count) if solution[i] == 0}

    improved = True

    while improved:
        improved = False

        for i in list(s1):
            for j in list(s0):
                # Evaluate the effect of removing item i and inserting item j.
                new_weight = current_weight - instance.weights[i] + instance.weights[j]
                delta_v = instance.values[j] - instance.values[i]

                # Accept the exchange only if it preserves feasibility and
                # improves the objective value.
                if new_weight <= instance.capacity and delta_v > 0:
                    solution[i] = 0
                    solution[j] = 1

                    # Update the selected and unselected sets so they remain consistent with the new solution.
                    s1.remove(i)
                    s1.add(j)
                    s0.remove(j)
                    s0.add(i)

                    current_weight = new_weight
                    z += delta_v
                    improved = True
                    break

            if improved:
                break

    return SolutionData (solution, z)