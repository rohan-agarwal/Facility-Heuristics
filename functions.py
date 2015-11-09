from constants import *
import numpy as np
import csv


def csv_to_array(filename):
    array = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) > 0:
                array.append([float(x) for x in row])
    array = [x[0] for x in array]
    array = np.array(array)
    return array


def csv_to_matrix(filename):
    mat = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) > 0:
                mat.append([float(x) for x in row])
    mat = np.matrix(mat)
    return mat


def get_data():
    t_cost = csv_to_matrix(transportation_file)
    fixed_cost = csv_to_matrix(fixed_file)
    demand = csv_to_array(demand_file)
    return t_cost, fixed_cost, demand


# For this specific problem, there are small and large facilities
def cost_split(fixed_cost):
    small_cost = fixed_cost[:, 0]
    large_cost = fixed_cost[:, 1]
    return small_cost, large_cost


def initialize_binary(small_cost):
    has_small = np.zeros(len(small_cost))
    has_large = np.zeros(len(large_cost))
    return has_small, has_large


def initialize_demand(t_cost):
    satisfied_demand = np.zeros(t_cost.shape)
    # Open small facilities
    available_demand = np.array([small_cap] * 5)
    return satisfied_demand, available_demand


def get_mins(t_cost):
    indices = np.argmin(t_cost, axis=0)
    indices = indices[0].tolist()[0]
    return indices


def choose_locs(indices, available_demand, satisfied_demand):
    for i in range(len(indices)):
        f = indices[i]
        available_demand[f] = available_demand[f] - demand[i]
        if available_demand[f] < 0:
            has_small[f] = 0
            has_large[f] = 1
            available_demand[f] = available_demand[
                f] - small_cap + large_cap
        else:
            has_small[f] = 1
        satisfied_demand[f, i] = satisfied_demand[f, i] + demand[i]
    return has_small, has_large, satisfied_demand, available_demand


def get_cost(has_small, has_large, t_cost, satisfied_demand):
    fixed_cost = has_small * small_cost + has_large * large_cost
    transport_costs = sum(np.multiply(satisfied_demand, t_cost))
    transport_costs = transport_costs[0].tolist()[0]
    total = sum(transport_costs) + fixed_cost
    return total


def combine_locs(available_demand, has_large, has_small, demand, satisfied_demand):
    large_indices = [x for x in range(0, len(has_large)) if has_large[x] == 1]
    small_indices = [x for x in range(0, len(has_large)) if has_small[x] == 1]
    for i in large_indices:
        for j in small_indices:
            if available_demand[i] > small_cap - available_demand[j]:
                available_demand[i] = available_demand[
                    i] - (small_cap - available_demand[j])
                has_small[j] = 0
                demand_loc = np.argmax(satisfied_demand[j])
                d = np.max(satisfied_demand[j])
                satisfied_demand[j] = 0
                satisfied_demand[i, demand_loc] = d
                available_demand[j] = small_cap
    return available_demand, has_large, has_small, satisfied_demand