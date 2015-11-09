from functions import *


def main():
t_cost, fixed_cost, demand = get_data()
small_cost, large_cost = cost_split(fixed_cost)
has_small, has_large = initialize_binary(small_cost)
satisfied_demand, available_demand = initialize_demand(t_cost)
indices = get_mins(t_cost)
has_small, has_large, satisfied_demand, available_demand = choose_locs(
    indices, available_demand, satisfied_demand)
available_demand, has_large, has_small, satisfied_demand = combine_locs(
    available_demand, has_large, has_small, demand, satisfied_demand)
    total = get_cost(has_small, has_large, t_cost, satisfied_demand)
    return has_small, has_large, total
