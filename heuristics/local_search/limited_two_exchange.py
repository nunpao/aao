from itertools import combinations

from models import InstanceData, SolutionData


def limited_two_exchange(
    instance: InstanceData,
    initial_solution: SolutionData,
    k_in: int =40,
    k_out: int =20,
) -> SolutionData:
    """
    Improves a solution by exploring a restricted 2-exchange neighborhood.

    Instead of testing every possible pairwise exchange, this heuristic limits the search to a subset of promising selected and unselected items controlled by ``k_out`` and ``k_in``.

    Args:
        instance:
            Problem instance containing the number of items, knapsack capacity, and the aligned ``values`` and ``weights`` vectors.
        initial_solution:
            Starting solution that will be used as the base for this local search procedure.
        k_in:
            Maximum number of candidate unselected items considered for insertion.
        k_out:
            Maximum number of candidate selected items considered for removal.

    Returns:
        SolutionData:
            The final solution obtained after no further improving restricted 2-item exchanges can be found.
    """
    solution = initial_solution.solution.copy()
    z = initial_solution.z

    # Track the current weight explicitly so each candidate exchange can be tested in constant time.
    current_weight = sum(instance.weights[i] for i in range(instance.item_count) if solution[i] == 1)

    s1 = {i for i in range(instance.item_count) if solution[i] == 1}
    s0 = {i for i in range(instance.item_count) if solution[i] == 0}

    improved = True

    while improved:
        improved = False

        # Prioritize weak selected items for removal and strong unselected items for insertion.
        selected_candidates = sorted(
            s1,
            key=lambda i: (instance.values[i] / instance.weights[i], instance.values[i]),
        )[:k_out]
        unselected_candidates = sorted(
            s0,
            key=lambda i: (instance.values[i] / instance.weights[i], instance.values[i]),
            reverse=True,
        )[:k_in]

        for i1, i2 in combinations(selected_candidates, 2):
            removed_weight = instance.weights[i1] + instance.weights[i2]
            removed_value = instance.values[i1] + instance.values[i2]

            for j1, j2 in combinations(unselected_candidates, 2):
                added_weight = instance.weights[j1] + instance.weights[j2]
                delta_v = instance.values[j1] + instance.values[j2] - removed_value

                if delta_v <= 0:
                    continue

                new_weight = current_weight - removed_weight + added_weight
                if new_weight > instance.capacity:
                    continue

                # Commit the improving move and keep the support sets synchronized with the new solution.
                solution[i1] = solution[i2] = 0
                solution[j1] = solution[j2] = 1

                s1.difference_update((i1, i2))
                s0.update((i1, i2))

                s0.difference_update((j1, j2))
                s1.update((j1, j2))

                current_weight = new_weight
                z += delta_v
                improved = True
                break

            if improved:
                break

    return SolutionData (solution,z)
