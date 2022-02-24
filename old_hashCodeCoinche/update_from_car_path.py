

import numpy as np
from street_car import Street,Car


def is_light_green(inter, street, t, schedule):
    ##return, bool, time to wait
    time_list_greens= schedule[inter]

    len_cycle = sum(time for (st,time) in time_list_greens)
    st_names = [ st for  (st,time) in time_list_greens]

    if not street in st_names:
        return False, None
    else:
        street_index = st_names.index(street)

    times = [ time for (st,time) in time_list_greens]

    cum_times = np.cumsum(times)
    ##green for street starts
    if street_index ==0:
        is_green =  0 <= t % len_cycle < cum_times[street_index]
        if is_green:
            time_to_wait = 0
        else:
            time_to_wait = len_cycle- (t%len_cycle)
    else:
        is_green= cum_times[street_index-1]  <= t % len_cycle < cum_times[street_index]
        if is_green:
            time_to_wait = 0
        else:
            time_to_wait =  (cum_times[street_index-1]  - (t % len_cycle))%len_cycle
    return is_green, time_to_wait


def compute_score_car(car, schedule, t_length, bonus):

    time_simu=0

    iter_street = iter(car.Streets)

    street= next(iter_street)
    num_street_visited = 1
    while time_simu < t_length and num_street_visited < car.num_streets:

        ###start at the end of first street

        inter = street.end
        is_green, time_to_wait = is_light_green(inter, street, time_simu, schedule)

        if time_to_wait is None:
            return 0 ## car will never pass

        if not is_green:
            time_simu += time_to_wait
        ##go instantly to next street

        street = next(iter_street)
        num_street_visited +=1
        time_simu += street.L

    return t_length-time_simu


def change_value_schedule_on_traj(schedule, car_list, duration, bonus):
    ##given a list of intersections, modify the schedule on this intersec
    ##pick random inter:

    car_to_focus = car_list[0]

    previous_score = sum (compute_score_car(car, schedule, duration, bonus) for car in car_list)

    traj_list = car_to_focus.Streets

    street_select = traj_list[np.random.randint(len(traj_list))]
    ##change value of green and order in list on interset fo this street
    inter_select = street_select.end
    schedule_list_inter = schedule[inter_select]

    copy_without_the_street = [ (s,t) for (s,t) in schedule_list_inter if s!=street_select]

    random_time = np.random.randint(1,15)

    random_index_in_list = 0 if (len(copy_without_the_street)==0) else np.random.randint(0,len(copy_without_the_street))
    print("new index in list : ", random_index_in_list)

    copy_without_the_street.insert(random_index_in_list, (street_select, random_time))

    # print("copy with new street inserted: ", copy_without_the_street)
    schedule[inter_select] = copy_without_the_street

    new_score = sum(compute_score_car(car, schedule, duration, bonus) for car in car_list)

    if new_score > previous_score : ##keep change!!
        print("keep new schedule, new score for car ", car_to_focus, " | ", new_score)
    else:
        schedule[inter_select] = schedule_list_inter
    return schedule





def update_from_car(input_args, streets, schedule, cars, num_iterations = 15):


    ##take a car randomly

    for it_change in range(num_iterations):

        num_cars= 3
        list_idx_to_draw = list(range(len(cars)))
        car_list_idx = []

        for it in range(num_cars):
            idx_idx = 0 if len(list_idx_to_draw)== 0  else np.random.randint(0,len(list_idx_to_draw))
            car_list_idx.append(list_idx_to_draw.pop(idx_idx))
        # car_list_idx= [np.random.randint(0, len(cars)), np.random.randint(0, len(cars))]

        print("\niter ", it_change, " indx car:", car_list_idx)

        car_list = [cars[car_idx] for car_idx in car_list_idx]

        schedule = change_value_schedule_on_traj(schedule, car_list, input_args["duration"], input_args["bonus"])

        # # score = compute_score_car(car, schedule, input_args["duration"])
        #
        # print("car idx", car_idx, ", score= ", score)

    return schedule