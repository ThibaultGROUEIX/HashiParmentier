import os
import np

def read_input(path="../input/"):
    input_args = dict()
    with open(path, 'r') as file_reader:
        first_args_list = file_reader.readline().split(' ')

        input_args["duration"] = int(first_args_list[0])
        input_args["num_intersect"] = int(first_args_list[1])
        input_args["num_streets"] = int(first_args_list[2])
        input_args["num_cars"] = int(first_args_list[3])
        input_args["bonus"] = int(first_args_list[4])

        num_lines = 0
        streets = []
        while num_lines < input_args["num_streets"]:
            line_street = file_reader.readline().split(' ')
            begin = int(line_street[0])
            end = int(line_street[1])
            name = (line_street[2])
            L = int(line_street[3])
            streets.append(Street(begin, end, name, L))
            num_lines += 1

        num_cars = 0
        cars = []
        while num_cars < input_args["num_cars"]:

            line_car = file_reader.readline().rstrip('\n').split(' ')
            # print("line car: ", line_car)
            num_s = int(line_car[0])
            list_s = line_car[1:]
            cars.append(Car(num_s, list_s))
            num_cars += 1

    return input_args, streets, cars


def write_output(file_path, sol_dict):
    with open(file_path, 'w') as file_writer:
        file_writer.write()
        file_writer.write(sol_dict["key"])

    return 1


def submitter(fname, intersect_dict):
    f = open(f"{fname}.txt", "w")
    f.write(f'{len(intersect_dict)}\n')
    for intersection, timers in intersect_dict.items():
        f.write(f'{intersection}\n')
        f.write(f'{len(timers)}\n')
        for timer in timers:
            f.write(f'{timer[0].name} {timer[1]}\n')
    f.close()
