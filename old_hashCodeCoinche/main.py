import numpy as np
from utilities.read_write import read_input, submitter
import sys
from alterne_feux import alterne_feux_sol
from update_from_car_path import update_from_car

def main(*args):
    datasetname=args[0]

    print("call main with :" + datasetname)
    input_args, streets, cars = read_input(path="input/"+datasetname+".txt")

    for car in cars:
        car.get_list_Streets(streets)

    schedule= alterne_feux_sol(input_args, streets, cars)

    if len(args)>1:
        num_iterations_change = int(args[1])
    else:
        num_iterations_change = 15
    schedule = update_from_car(input_args, streets, schedule, cars, num_iterations= num_iterations_change)

    # print("sol:", schedule)
    submitter("output/"+datasetname, schedule)
    ###schedule :  {intersectID: [(route1, Tps), ... (route1, Tps) ]}




if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SyntaxError("Insufficient arguments.")
    else:
        # If there are keyword arguments
        main(*sys.argv[1:])