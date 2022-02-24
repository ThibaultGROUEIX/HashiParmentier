import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import torch
from easydict import EasyDict
import os



def main(path="./input/"):
    global_args= EasyDict()
    street_names = []
    street_start = []
    street_end = []
    street_time = []
    street_to_index = {}
    index_to_street = {}

    car_num_street = []
    car_streets = []
    car_cost = []
    car_length = []

    intersection = {}
    intersection_dict = {}
    intersection_start_dict = {}
    intersection_usage = {}

    line = 0
    with open(path, 'r') as file_reader:
        first_args_list = file_reader.readline().split(' ')

        global_args["duration"] = int(first_args_list[0])
        global_args["num_intersection"] = int(first_args_list[1])
        global_args["num_street"] = int(first_args_list[2])
        global_args["num_car"] = int(first_args_list[3])
        global_args["bonus"] = int(first_args_list[4])
        for i in range(global_args["num_street"]):
            next_args = file_reader.readline().split(' ')
            street_start.append(int(next_args[0]))
            street_end.append(int(next_args[1]))
            street_names.append(next_args[2])
            street_time.append(int(next_args[3]))
            street_to_index[next_args[2]] = i
            index_to_street[i] = next_args[2]
            if int(next_args[1]) in intersection.keys():
                intersection[int(next_args[1])].append(i)
                intersection_dict[int(next_args[1])][i] = 0
                intersection_start_dict[int(next_args[1])][i] = 0
                intersection_usage[int(next_args[1])] = 0
            else:
                intersection[int(next_args[1])] = [i]
                intersection_dict[int(next_args[1])] = {}
                intersection_start_dict[int(next_args[1])] = {}
                intersection_dict[int(next_args[1])][i] = 0
                intersection_start_dict[int(next_args[1])][i] = 0
                intersection_usage[int(next_args[1])] = 0


        car_length = np.zeros(global_args["num_car"])

        num_intersection = len(intersection.keys())
        for i in range(global_args["num_car"]):
            next_args = file_reader.readline().split(' ')
            car_num_street.append(int(next_args[0]))
            street_path = [street_to_index[next_args[j+1].rstrip("\n")] for j in range(len(next_args)-1)]
            length = 0
            street_end_0 = street_end[street_path[0]]
            intersection_start_dict[street_end_0][street_path[0]] = intersection_start_dict[street_end_0][street_path[0]] + 1
            for street in street_path:
                street_end_ = street_end[street]
                intersection_dict[street_end_][street] = intersection_dict[street_end_][street] + 1
                intersection_usage[street_end_] = intersection_usage[street_end_] + 1
                length = length + street_time[street]

            car_length[i] = length
            car_streets.append(street_path)

        # car cost
        # car_cost = np.zeros(len(car_num_street))
        #
        # for i in range(len(car_num_street)):
        #     car_num_street_ = car_num_street[i]
        #     car_streets_ = car_streets[i]
        #     for street in car_streets_:
        #         street_end_ = street_end[street]
        #         if intersection_dict[street_end_][street] < 2 and intersection_usage[street_end_] > 25:
        #             car_cost[i] = car_cost[i] + 1
        # # remove from intersection_dict
        # number_of_car_removed = 0
        # for i in range(len(car_num_street)):
        #     if car_cost[i] > 21 or car_length[i] > 0.99*global_args["duration"]:
        #         number_of_car_removed = number_of_car_removed + 1
        #         for street in car_streets[i]:
        #             street_end_ = street_end[street]
        #             intersection_dict[street_end_][street] = intersection_dict[street_end_][street] - 1
        # print(f"number_of_car_removed {number_of_car_removed}")

        with open(path[:-4] + "_output.txt", 'w') as file_reader:
            file_reader.write(f"{num_intersection}\n")

            for i in range(num_intersection):
                file_reader.write(f"{i}\n")

                total_use = 0
                for street in intersection_dict[i]:
                    total_use = total_use + intersection_dict[i][street]


                if intersection_dict[i].keys().__len__() == 0 or total_use==0:
                    file_reader.write("1\n")
                    key = intersection[i][0]
                    street_name = index_to_street[key]
                    file_reader.write(f"{street_name} 1 \n")
                else:
                    if total_use == 0:
                        print("not possible")
                        file_reader.write(f"{street_name} 1 \n")

                    else:
                        num_schedule = 0
                        for key in intersection[i]:
                            if intersection_dict[i][key] > 0:
                                num_schedule = num_schedule + 1

                        file_reader.write(f"{num_schedule}\n")
                        local_dict = {k: v for k, v in sorted(intersection_start_dict[i].items(), key=lambda item: -item[1])}
                        for key in local_dict.keys():
                            if intersection_dict[i][key] > 0:
                                street_name = index_to_street[key]
                                value = 5
                                time = value*intersection_dict[i][key]/total_use
                                if time < 1:
                                    file_reader.write(
                                        f"{street_name} 1\n")
                                else:
                                    file_reader.write(f"{street_name} {int(value*intersection_dict[i][key]/total_use)} \n")

        print("done")


if __name__ == '__main__':
    main("./input/b.txt")
    main("./input/a.txt")
    main("./input/c.txt")
    main("./input/d.txt")
    main("./input/e.txt")
    main("./input/f.txt")
