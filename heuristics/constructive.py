import random


def efficiency_greedy(n, W, v, w):
    efficiency = [v[i] / w[i] for i in range(n)]
    items = sorted(range(n), key = lambda i: efficiency[i], reverse=True)

    solution = [0] * n
    z = 0
    current_weight = 0

    for i in items:
        if current_weight + w[i] <= W:
            solution[i] = 1
            current_weight += w[i]
            z += v[i]

    return solution, z

def weight_greedy(n, W, v, w):
    items = sorted(range(n), key = lambda i: w[i])

    solution = [0] * n
    z = 0
    current_weight = 0

    for i in items:
        if current_weight + w[i] > W:
            break #se w[i] já não cabe, mais nenhum caberia, desta forma, acabamos com o ciclo aqui

        solution[i] = 1
        current_weight += w[i]
        z += v[i]

    return solution, z


def random_greedy(n, W, v, w, alpha):
    if not 0 <= alpha <= 1:
        raise ValueError("alpha must be in [0, 1]")

    rng = random

    efficiency = [v[i] / w[i] for i in range(n)]
    candidates = sorted(range(n), key=lambda i: efficiency[i], reverse=True)

    solution = [0] * n
    z = 0
    current_weight = 0

    while candidates:
        feasible = [i for i in candidates if current_weight + w[i] <= W]
        if not feasible:
            break

        emax = efficiency[feasible[0]]
        emin = efficiency[feasible[-1]]
        tau = emax - alpha * (emax - emin)
        lrc = [i for i in feasible if efficiency[i] >= tau]

        chosen = rng.choice(lrc)
        solution[chosen] = 1
        current_weight += w[chosen]
        z += v[chosen]
        candidates.remove(chosen)

    return solution, z
