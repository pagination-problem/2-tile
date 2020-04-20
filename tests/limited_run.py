import context
from tree import Tree
import cplex
import math
import networkx as nx
import matplotlib.pyplot as plt
import random
import time
#import tools_for_cplex

"""
    This script takes a tree in input,
    finds the optimal solution using CPLEX
    and checks two conditions: one about the number of
    duplicated symbols in the optimal solution and
    one about the optimal value.

    The program will have a limited number of runs
    to find  optimal solution with 2 or less duplicated symbols.

    I usually use this program on inputs found by cplex_launch.py where
    the condition on the number of duplicated symbols is not verified.
"""

def checks_number_of_duplicated_symbols(t, cplex_input):
    cpt = 0
    for u in t.tree.nodes():
        (val_1, val_2) = cplex_input.solution.get_values( ["x_1"+str(u), "x_2"+str(u)] )

        if val_1 == 0 and val_2 == 0:
            cpt = cpt + 1

    return cpt

def adds_a_no_good_cut_inequality(t, cplex_input, OPT):
    """
        the constraint is: \sum_{i\in S} x_i    \leq    |S| -1 + \sum_{i \in Variables \setminus S}
        but will be written in the standard format (all
        variables in the left side and the constants in the right side):
            \sum_{i\in S} x_i  - \sum_{i \in Variables \setminus S}  \leq    |S| -1 

        For a better clarity in the code, i'll use names according the first way of writting the constraint:
        the list left_side will contain all the variables = 1 in the solution, the list
    """
    variables = []
    coefficients = []

    for u in t.tree.nodes():
        (val_1, val_2) = cplex_input.solution.get_values( ["x_1"+str(u), "x_2"+str(u)] )

        if val_1 == 1:
            variables.append("x_1"+str(u))
            variables.append("x_2"+str(u))

            coefficients.append(1.0)
            coefficients.append(-1.0)

        elif val_2 == 1:
            variables.append("x_2"+str(u))
            variables.append("x_1"+str(u))

            coefficients.append(1.0)
            coefficients.append(-1.0)
        else:
            variables.append("x_1"+str(u))
            variables.append("x_2"+str(u))

            coefficients.append(-1.0)
            coefficients.append(-1.0)

    constraints = []
    constraint_senses = []
    rhs = []
    lin_expr = [ variables, coefficients]
    constraints.append(lin_expr)
    constraint_senses.append("L")
    rhs.append(OPT - 1)

    cplex_input.linear_constraints.add(lin_expr = constraints,
                                    senses = constraint_senses,
                                    rhs = rhs,)

def saves_a_potential_problematic_model(path, name, model, tree):
    """
    inputs:
        path: relative or absolute path to the folder where we want to store the model
        name: name that the three files will have
        model: the model we are working on
        tree: an networkx graph, the base of our work

    outputs: three files stored in path/ folder
        name.lp: the model written in a file that cplex can read
        name.sol: the last solution found for this model
        .pdf: a graphic representation of the graph we are working on
    """
    cplex_input.write(path+name+".lp", "lp")

    plt.figure(figsize=(5,5))
    nx.draw_networkx (tree)
    plt.savefig(path+name+".pdf")

    cplex_input.solution.write(path+name+".sol")

# ------------------------------------------------------------------------------------ #
# ------------------------ Information needed for the program ------------------------ #
number_of_authorized_tries = 900

name = "problematic_tree_4_n=23"
sequence = [19, 13, 5, 18, 13, 8, 21, 9, 13, 17, 6, 4, 15, 17, 7, 9, 2, 13, 2, 10, 4]
wrong_ub_path = "saved_trees/petit_test/wrong_UB/"
out_of_time_path = "saved_trees/petit_test/out_of_time/"
problem_solved_path = "saved_trees/petit_test/found_a_solution/"

# ------------------------------------------------------------------------------------ #

problem_count = 0
input_count = 0

try:
    t = Tree(sequence)
    
    start = time.time()    
    cplex_input = t.to_cplex_input()
    cplex_input.solve()
    
    n = len(t.tree)
    # cpt = tools_for_cplex.checks_number_of_duplicated_symbols(t, cplex_input)
    cpt = checks_number_of_duplicated_symbols(t, cplex_input)
    OPT = cplex_input.solution.get_objective_value() + n

    if OPT > math.ceil( (len(t.tree)) / 2 ) + 1:
        print(f"The supposed UB is not verified for this input: {str(t.prufer_sequence)}")
        # tools_for_cplex.saves_a_potential_problematic_model(wrong_ub_path, name, cplex_input, t.tree)
        saves_a_potential_problematic_model(wrong_ub_path, name, cplex_input, t.tree)

    elif cpt > 2 :
        count = 0
        waiting = 0
        while "The number of duplicated symbols is strictly greater than 2":
            # tools_for_cplex.adds_a_no_good_cut_inequality(t, cplex_input, OPT)
            adds_a_no_good_cut_inequality(t, cplex_input, OPT)
            cplex_input.solve()
            # cpt = tools_for_cplex.checks_number_of_duplicated_symbols(t, cplex_input)
            cpt = checks_number_of_duplicated_symbols(t, cplex_input)

            if cpt <= 2 or waiting >= number_of_authorized_tries:
                break
            waiting = waiting + 1
            count = count + 1

        end = time.time() - start

        if waiting >= number_of_authorized_tries:
            problem_count = problem_count + 1
            print(f"Could not find a solution with C <= 2 after {number_of_authorized_tries} tries")
            # tools_for_cplex.saves_a_potential_problematic_model(out_of_time_path, name, cplex_input, t.tree)
            saves_a_potential_problematic_model(out_of_time_path, name, cplex_input, t.tree)
        else:
            # tools_for_cplex.saves_a_potential_problematic_model(problem_solved_path, name, cplex_input, t.tree)
            saves_a_potential_problematic_model(problem_solved_path, name, cplex_input, t.tree)
            print(f"A solution with C =< 2 was found after {count} tries.")

        print(f"And it took {end} seconds or {math.ceil(end/60)} minutes or {math.ceil((end/60)/60)} hours to end.")
  
    else:
        print("Everything is fine after the first optimization.")
        input_count = input_count + 1
except:
   print(f"Bugged occured on input number : {str(input_count)}")
   print(f"on input sequence: {str(t.prufer_sequence)}")
   print(f"Number of nodes: {str(n)}")
   print(f"Number of already computed inputs: {str(input_count)}")
   print(f"Last waiting was: {number_of_authorized_tries}")

