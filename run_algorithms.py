import sys
import numpy as np
import os.path as osp
import os

# from <Branch and Bound File Name> import <Function Name>
# from <Approximation File Name> import <Function Name>
from simulated_annealing import LS1
# from <Local Search 2 File Name> import <Function Name>

'''
NOTE: To run this file in the command line, type python "run_algorithms.py" followed by the executable line given in 
      the rubric (ie. exec -inst <filename> -alg [BnB|Approx|LS1|LS2] -time <cutoff in seconds> -seed <random seed>)
'''

def read_input(file_name:str):
    '''
    read_input: Takes a valid input file for the knapsack problem and returns the total number of given items,
                the weight capacity of the knapsack, the values of each item and the weight of each item.
    inputs:     file_name - string - The name of the file we want to read. Returns an error if file does not exist.
    outputs:    num_items - integer - Represents the total number of items available to put in the knapsack.
                capacity - integer - Represents the maximum amount of weight that the knapsack can hold.
                values - numpy array - Contains integers representing the value of each available item, where the
                    ith element of the array represents the value of the ith item.
                weight - numpy array - Contains integers representing the weight of each available item, where the
                    ith element of the array represents the value of the ith item.
    '''
    file_path = "DATA/DATASET/"+file_name
    if not osp.isfile(file_path):
        print("read_input: ERROR - Given File Does Not Exist")
        return -1, None, None, None
    
    f = open(file_path, "r")
    overview = f.readline().split()
    num_items = int(overview[0])
    capacity = int(overview[1])

    values = np.full(num_items, -1)
    weights = np.full(num_items, -1)
    t = 0
    for line in f:
        x = line.split()
        if x[0] != "EOF":
            v = int(x[0]); w = int(x[1]); 
            values[t] = v
            weights[t] = w
        else:
            break
        t += 1
    return num_items, capacity, values, weights

def run_algorithm(file_inputs, algorithm, time_cutoff, randseed):
    '''
    run_algorithm: Selects which algorithm to run, and makes sure the algorithm detailed is valid
    inputs: file_inputs - string - a 4-tuple containing information about the specific knapsack problem we solve.
                                    Contains the number of items, the capacity of the knapsack, and the values and weights
                                    of all items (in that order).
            algorithm - string - the name of the algorithm we use to find a solution.
            time_cutoff - string - the amount of time our algorithm runs before being cut off.
            rand_seed - string - a random seed value that is used for any random functions.

    '''
    if algorithm == "BnB":
        # Branch and Bound Algorithm Function Name Goes Here
        raise NotImplementedError
    elif algorithm == "Approx":
        # Approximation Algorithm Function Name Goes Here
        raise NotImplementedError
    elif algorithm == "LS1":
        return LS1(file_inputs, time_cutoff, randseed)
    elif algorithm == "LS2":
        # Second Local Search Algorithm Function Name Goes Here
        raise NotImplementedError
    else:
        print("ERROR: Argument given for Algorithm is invalid.")
        return -1, None

def output(quality:int, index_list, file_name:str, algorithm, time_cutoff, rand_seed):
    '''
    output: Takes in the results from an algorithm run, and formats/outputs a solution file for the results.
    inputs: quality - integer - The total value of the best solution found.
            index_list - numpy array - The indexes of the objects included in our solution.
            file_name - string - the name of the file we have evaluated the solution for.
            algorithm - string - the name of the algorithm we have used to find a solution
            time_cutoff - string - the amount of time our algorithm runs before being cut off.
            rand_seed - string - a random seed value that was used for random functions.
    '''
    if algorithm == "BNB":
        new_file_name = "DATA/DATASET/"+file_name+"_"+algorithm+"_"+time_cutoff+".sol"
    else:
        new_file_name = "DATA/DATASET/"+file_name+"_"+algorithm+"_"+time_cutoff+"_"+rand_seed+".sol"

    f = open(new_file_name, "w")
    f.write(str(quality))
    f.close()

    f = open(new_file_name, "a")
    f.write("\n")
    for ind in range(len(index_list)):
        iter = index_list[ind]
        f.write(str(iter))
        if ind != len(index_list)-1:
            f.write(", ")
    f.write("\n")
    f.close()
    return

def trace_out(trace, file_name:str, algorithm, time_cutoff, rand_seed):
    if algorithm == "BNB":
        new_file_name = "DATA/DATASET/"+file_name+"_"+algorithm+"_"+time_cutoff+".trace"
    else:
        new_file_name = "DATA/DATASET/"+file_name+"_"+algorithm+"_"+time_cutoff+"_"+rand_seed+".trace"
    f = open(new_file_name, "w")
    for improve in trace:
        time, solution = improve
        f.write(str(time)+", "+str(solution)+"\n")
    f.close()
    return

def main():
    '''
    main:   The combination of all previous functions into one unit.
            Possibly changed to function as an executable file at a later date (???)
    '''
    args = sys.argv
    # Check Formatting of Input
    if len(args) != 10:
        print("ERROR : Number of arguments is incorrect")
        return
    if (args[1] != "exec" or args[2] != "-inst" or args[4] != "-alg" 
        or args[6] != "-time" or args[8] != "-seed"):
        print("ERROR: Formatting of input incorrect.\nInput should be in the following format: "
              +"exec -inst <filename> -alg [BnB|Approx|LS1|LS2] -time <cutoff in seconds> -seed <random seed>")
        return
    
    filename = args[3]
    algorithm = args[5]
    time_cutoff = args[7]
    rand_seed = args[9]

    # Checks if time cutoff and random seed are valid
    if not time_cutoff.isdigit() or int(time_cutoff) <= 0:
        print("ERROR: Provided time cutoff is not a valid, positive integer.")
        return
    if not rand_seed.isdigit():
        print("ERROR: Provided random seed is not a valid integer.")
        return

    # Checks filename and reads given input file
    file_inputs = read_input(filename)
    if file_inputs[0] == -1:
        return
    
    # Runs the desired algorithm
    quality, index_list, trace = run_algorithm(file_inputs, algorithm, int(time_cutoff), int(rand_seed))
    if quality == -1:
        return
    
    output(quality, index_list, filename, algorithm, time_cutoff, rand_seed)
    trace_out(trace, filename, algorithm, time_cutoff, rand_seed)
    return

# print(sys.argv)
main()