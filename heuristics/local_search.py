from itertools import combinations


def one_exchange(n, W, v, w, initial_solution, initial_z):

    solution = initial_solution.copy()
    z = initial_z

    current_weight = sum(w[i] for i in range(n) if solution[i] == 1)

    s1 = {i for i in range(n) if solution[i] == 1}
    s0 = {i for i in range(n) if solution[i] == 0}

    improved = True

    while improved:
        improved = False

        for i in list(s1):
            for j in list(s0):
                new_weight = current_weight - w[i] + w[j]
                delta_v = v[j] - v[i]

                if new_weight <= W and delta_v > 0:
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

    return solution, z

def two_exchange(n, W, v, w, initial_solution, initial_z):
    solution = initial_solution.copy()
    z = initial_z

    current_weight = sum(w[i] for i in range(n) if solution[i] == 1)

    s1 = {i for i in range(n) if solution[i] == 1}
    s0 = {i for i in range(n) if solution[i] == 0}

    improved = True

    while improved:
        improved = False
        for i1, i2 in combinations(list(s1), 2):
            for j1, j2 in combinations(list(s0), 2):
                new_weight = current_weight - w[i1] - w[i2] + w[j1] + w[j2]
                delta_v = v[j1] + v[j2] - v[i1] - v[i2]

                if new_weight <= W and delta_v > 0:
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
    return solution, z

