import random
from data.models import InstanceData, SolutionData


def efficiency_greedy(instance: InstanceData):
    efficiency = [instance.values[i] / instance.weights[i] for i in range(instance.item_count)]
    items = sorted(range(instance.item_count), key = lambda i: efficiency[i], reverse=True)

    solution = [0] * instance.item_count
    z = 0
    current_weight = 0

    for i in items:
        if current_weight + instance.weights[i] <= instance.capacity:
            solution[i] = 1
            current_weight += instance.weights[i]
            z += instance.values[i]

    return SolutionData(solution, z)

def weight_greedy(instance: InstanceData):
    items = sorted(range(instance.item_count), key = lambda i: instance.weights[i])

    solution = [0] * instance.item_count
    z = 0
    current_weight = 0

    for i in items:
        if current_weight + instance.weights[i] > instance.capacity:
            break #se w[i] já não cabe, mais nenhum caberia, desta forma, acabamos com o ciclo aqui

        solution[i] = 1
        current_weight += instance.weights[i]
        z += instance.values[i]

    return SolutionData(solution, z)


def random_greedy(instance: InstanceData, alpha: float):
    if not 0 <= alpha <= 1:
        raise ValueError("alpha must be in [0, 1]")

    rng = random

    efficiency = [instance.values[i] / instance.weights[i] for i in range(instance.item_count)]
    candidates = sorted(range(instance.item_count), key=lambda i: efficiency[i], reverse=True)

    solution = [0] * instance.item_count
    z = 0
    current_weight = 0

    while candidates:
        feasible = [i for i in candidates if current_weight + instance.weights[i] <= instance.capacity]
        if not feasible:
            break

        emax = efficiency[feasible[0]]
        emin = efficiency[feasible[-1]]
        tau = emax - alpha * (emax - emin)
        lrc = [i for i in feasible if efficiency[i] >= tau]

        chosen = rng.choice(lrc)
        solution[chosen] = 1
        current_weight += instance.weights[chosen]
        z += instance.values[chosen]
        candidates.remove(chosen)

    return SolutionData(solution, z)
