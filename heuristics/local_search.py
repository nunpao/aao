from itertools import combinations

from models import InstanceData, SolutionData


def no_local_search(instance: InstanceData, initial_solution: SolutionData):
    return SolutionData(initial_solution.solution.copy(), initial_solution.z)


def one_exchange(instance: InstanceData, initial_solution: SolutionData):

    solution = initial_solution.solution.copy()
    z = initial_solution.z

    current_weight = sum(instance.weights[i] for i in range(instance.item_count) if solution[i] == 1)

    s1 = {i for i in range(instance.item_count) if solution[i] == 1}
    s0 = {i for i in range(instance.item_count) if solution[i] == 0}

    improved = True

    while improved:
        improved = False

        for i in list(s1):
            for j in list(s0):
                new_weight = current_weight - instance.weights[i] + instance.weights[j]
                delta_v = instance.values[j] - instance.values[i]

                if new_weight <= instance.capacity and delta_v > 0:
                    solution[i] = 0
                    solution[j] = 1

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

def two_exchange(instance: InstanceData, initial_solution: SolutionData):
    solution = initial_solution.solution.copy()
    z = initial_solution.z

    current_weight = sum(instance.weights[i] for i in range(instance.item_count) if solution[i] == 1)

    s1 = {i for i in range(instance.item_count) if solution[i] == 1}
    s0 = {i for i in range(instance.item_count) if solution[i] == 0}

    improved = True

    while improved:
        improved = False
        for i1, i2 in combinations(list(s1), 2):
            for j1, j2 in combinations(list(s0), 2):
                new_weight = (current_weight - instance.weights[i1] - instance.weights[i2]
                              + instance.weights[j1] + instance.weights[j2])
                delta_v = instance.values[j1] + instance.values[j2] - instance.values[i1] - instance.values[i2]

                if new_weight <= instance.capacity and delta_v > 0:
                    solution[i1] = solution[i2] = 0
                    solution[j1] = solution[j2] = 1

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
