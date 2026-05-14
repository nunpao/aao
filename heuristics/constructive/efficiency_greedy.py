from models import InstanceData, SolutionData

def efficiency_greedy(instance: InstanceData):
    """
    Builds a feasible knapsack solution using a greedy efficiency criterion.

    This heuristic ranks all items by their efficiency, defined as the ratio between value and weight, and then iteratively selects the most efficient items while there is still enough remaining capacity in the knapsack.

    Args:
        instance:
            Problem instance containing the number of items, knapsack capacity, and the aligned ``values`` and ``weights`` vectors used to evaluate each candidate item.

    Returns:
        SolutionData:
            A feasible solution represented by a binary selection vector and its corresponding objective value ``z``.
    """
    
    # Compute the efficiency of each item
    efficiency = [instance.values[i] / instance.weights[i] for i in range(instance.item_count)]

    # Sort item indices by decreasing efficiency
    items = sorted(range(instance.item_count), key = lambda i: efficiency[i], reverse=True)

    solution = [0] * instance.item_count
    z = 0
    current_weight = 0

    for i in items:
        # Insert the current item only if the knapsack remains within the allowed capacity after the insertion.
        if current_weight + instance.weights[i] <= instance.capacity:
            solution[i] = 1
            current_weight += instance.weights[i]
            z += instance.values[i]

    return SolutionData(solution, z)