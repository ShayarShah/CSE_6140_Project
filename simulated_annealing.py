import numpy as np
from timeit import default_timer as timer

def v(candidate, values):
    quality = np.sum(np.isin(np.arange(len(values)), list(candidate)) * values) 
    return quality

def w(candidate, weights):
    total_weight = np.sum(np.isin(np.arange(len(weights)), list(candidate)) * weights)
    return total_weight

def generate_candidate(values, weights, capacity, randseed, time_cutoff):
    np.random.seed(randseed)
    if capacity < np.sum(weights):
        p = capacity/np.sum(weights)
    else:
        return set()
    candidate = set()
    time = 0
    
    vw_ratio = values*np.reciprocal(weights)
    coeff = np.square(vw_ratio/np.max(vw_ratio))
    while time < time_cutoff/5:
        test_candidate = set()
        for item in range(len(weights)):
            if np.random.random() < coeff[item]:
                test_candidate.add(item)
        weight = w(test_candidate, weights)
        if capacity > weight:
            candidate = test_candidate
            break
        time += 1
    return candidate

def choose_neighbor(solution, file_inputs):
    num_items, capacity, _, weights = file_inputs
    total_weight = w(solution, weights)
    
    # Items that can be removed from knapsack
    can_remove = solution

    # Items that can be added to knapsack
    can_add = set(range(num_items)).difference(solution)
    add_remove = (can_add.copy(), can_remove.copy())
    items_removed = []
    for item in can_add:
        if capacity < total_weight + weights[item]:
            items_removed.append(item)
    for item in items_removed:
        can_add.remove(item)

    # Items that can be swapped to and from knapsack
    can_swap = []
    for addition in add_remove[0]:
        for removal in add_remove[1]:
            if capacity >= total_weight + weights[addition] - weights[removal]:
                can_swap.append([addition, removal])

    # Actions constituting entire neighborhood
    neighborhood = can_swap + [[-1, x] for x in can_remove] + [[x, -1] for x in can_add]
    if not neighborhood:
        action = [-1, -1]
    else:
        action = neighborhood[np.random.choice(np.arange(len(neighborhood)))]

    # Constructs neighbor selected based on random action chosen
    neighbor = solution.copy()
    add, remove = action
    if add != -1:
        neighbor.add(add)
    if remove != -1:
        neighbor.remove(remove)
    return neighbor

def LS1(file_inputs, time_cutoff, randseed):
    # CONSTANTS CONTROLING INITIAL TEMPERATURE AND ANNEALING SCHEDULE
    T = 1
    A = 0.99

    np.random.seed(randseed)
    T_cur = T
    cut = 0
    best_solution = set()
    trace = []
    num_items, capacity, values, weights = file_inputs
    time_passed = 0

    solution = set()
    # generate_candidate(weights, capacity, randseed, time_cutoff)
    start_time = timer()
    while time_passed < time_cutoff:
        # Select a random neighbor of our current solution
        neighbor = choose_neighbor(solution, file_inputs)
        # Determine if neighbor has higher value
        n_solution = v(neighbor, values)
        neighbor_compare = n_solution - v(solution, values)
        if neighbor_compare > 0:
            solution = neighbor
            vb_solution = v(best_solution, values)
            if n_solution > vb_solution:
                cut = 0
                best_solution = solution
                trace.append((round(timer()-start_time, 2), vb_solution))
        else:
            r = np.random.random()
            metro = np.exp(neighbor_compare/T_cur)
            if r < metro:
                solution = neighbor
        if cut % num_items//2 == 0:
            T_cur *= A
        cut += 1
        end_time = timer()
        time_passed = end_time - start_time
        # print(time_passed)
        if cut >= 10000:
            break
    return v(best_solution, values), [x+1 for x in list(best_solution)], trace