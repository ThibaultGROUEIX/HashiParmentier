
from street_car import Street,Car



def alterne_feux_sol(input_args, streets, cars):
    # input_args["duration"] = int(first_args_list[0])
    # input_args["num_intersect"] = int(first_args_list[1])
    # input_args["num_streets"] = int(first_args_list[2])
    # input_args["num_cars"] = int(first_args_list[3])
    # input_args["bonus"]

    ###schedule :  {intersectID: [(route1, Tps), ... (route1, Tps) ]}
    schedule_dict = {}

    streets_ending_at_inter = {inter_idx: [] for inter_idx in range(input_args["num_intersect"])}

    for street in streets:
        streets_ending_at_inter[street.end].append(street)

    for inter_idx in range(input_args["num_intersect"]):
        schedule_dict[inter_idx] = [(street, 1) for street in streets_ending_at_inter[inter_idx]]

    return schedule_dict

