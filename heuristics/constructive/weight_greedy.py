from models import InstanceData, SolutionData

def weight_greedy(instance: InstanceData):
    """
    Builds a feasible knapsack solution by prioritizing lighter items first.

    This heuristic sorts all items in ascending order of weight and then inserts them into the knapsack while capacity remains available. 
    This strategy favors low-weight items because they consume less capacity and therefore tend to allow the selection of a larger number of items.

    Args:
        instance:
            Problem instance containing the number of items, knapsack capacity, and the aligned ``values`` and ``weights`` vectors used during the solution construction.

    Returns:
        SolutionData:
            A feasible solution represented by a binary selection vector and its corresponding objective value ``z``.
    """

    # Sort item indices by increasing weight
    items = sorted(range(instance.item_count), key = lambda i: instance.weights[i])

    solution = [0] * instance.item_count
    z = 0
    current_weight = 0

    for i in items:
        # Since the items are ordered by nondecreasing weight, if this item no longer fits, every remaining item is at least as heavy and will also be infeasible for the current partial solution.
        if current_weight + instance.weights[i] > instance.capacity:
            break

        solution[i] = 1
        current_weight += instance.weights[i]
        z += instance.values[i]

    return SolutionData(solution, z)