In order to incorporate your file into the given "run_algorithms.py" file, do the following:
(1) Replace the desired comment under the "import" statements importanting your own file name, and the function from it you wish to run.
(2a) Replace the appropriate "raise NotImplementedError" in the run_algorithm function with a return for your own function.
(2b) Currently, four variables are given that describe the problem - number of items, knapsack capcity, and two arrays corresponding to the values and weights of every item. These are given as a tuple in the "file_inputs" variable, so you can set "num_items, capacity, values, weights = file_inputs" and manipulate them however you like in your own function.
(3) Return the value of your solution, a list of 1-based indices, and the trace of your solution (which should be a list of 2-tuples consisting of the time and the value of the solution at that time)
(4) In the terminal run the command "python 'run_algorithms.py' exec -inst <filename> -alg [BnB|Approx|LS1|LS2] -time <cutoff in seconds> -seed <random seed>" to output your result, similarly to how it's describe in the rubric.
