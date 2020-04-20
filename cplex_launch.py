from tree import Tree
import cplex
import math
import networkx as nx
import matplotlib.pyplot as plt
import random
import time
import tools_for_cplex
import sys

"""
    This script generates random trees
    (with a number of nodes between a lower and an upper born),
    finds the optimal solution using CPLEX
    and checks two conditions: one about the number of
    duplicated symbols in the optimal solution and
    one about the optimal value.

    If a tree doesn't verify one of the condition,
    it is stored in specific folders that need to be specified.
"""

MIN_NODE_NUMBER = 5
MAX_NODE_NUMBER = 26

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
        the list left_side will contain all the variables = 1 in the solution, the coefficients_for_left_side will
        all be equal to 1, etc.
    """
    left_side = []
    right_side = []
    coefficients_for_left_side = []
    coefficients_for_right_side = []

    for u in t.tree.nodes():
        (val_1, val_2) = cplex_input.solution.get_values( ["x_1"+str(u), "x_2"+str(u)] )

        if val_1 == 1:
            left_side.append("x_1"+str(u))
            right_side.append("x_2"+str(u))
        elif val_2 == 1:
            left_side.append("x_2"+str(u))
            right_side.append("x_1"+str(u))
        else:
            right_side.append("x_1"+str(u))
            right_side.append("x_2"+str(u))

        coefficients_for_left_side.append(1.0)
        coefficients_for_right_side.append(-1.0)

    constraints = []
    constraint_senses = []
    rhs = []
    lin_expr = [ left_side + right_side, coefficients_for_left_side + coefficients_for_right_side]
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

number_of_authorized_tries = 900
problem_count = 0
too_many_duplicated_symbol_count = 0
wrong_UB_count = 0
waiting = 0

wrong_ub_path = "saved_trees/petit_test/wrong_UB/"
out_of_time_path = "saved_trees/petit_test/out_of_time/"

start = time.time()
try:
    for input_count in range(1,10000):
        n = random.randint(MIN_NODE_NUMBER, MAX_NODE_NUMBER)
        t = Tree(n)
        
        cplex_input = t.to_cplex_input()
        cplex_input.solve()

        # cpt = tools_for_cplex.checks_number_of_duplicated_symbols(t, cplex_input)
        cpt = checks_number_of_duplicated_symbols(t, cplex_input)
        OPT = cplex_input.solution.get_objective_value() + n

        name = "problematic_tree_" + str(problem_count) + "_n=" + str(n)

        if OPT > math.ceil( (len(t.tree)) / 2 ) + 1:
            print(f"The supposed UB is not verified for this input: {str(t.prufer_sequence)}")
            # tools_for_cplex.saves_a_potential_problematic_model(wrong_ub_path, name, cplex_input, t.tree)
            saves_a_potential_problematic_model(wrong_ub_path, name, cplex_input, t.tree)

            wrong_UB_count = wrong_UB_count + 1
            problem_count = problem_count + 1

        elif cpt > 2 :
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

            if waiting >= number_of_authorized_tries:
                problem_count = problem_count + 1
                # tools_for_cplex.saves_a_potential_problematic_model(out_of_time_path, name, cplex_input, t.tree)
                saves_a_potential_problematic_model(out_of_time_path, name, cplex_input, t.tree)

    print(str(input_count) + " were computed.")
    print(f"For {str(too_many_duplicated_symbol_count)} inputs, we could not find optimal solutions with less than 2 duplicated symbols after {number_of_authorized_tries} tries")
    print(f"For {str(wrong_UB_count)} inputs, the UB is not verified.")
    end = time.time() - start
    print(f"And it took {end} seconds or {math.ceil(end/60)} minutes or {math.ceil((end/60)/60)} hours to end.")


except:
    print("Unexpected error:", sys.exc_info()[0])
    print(f"Bugged occured on input number : {str(input_count)}")
    print(f"on input sequence: {str(t.prufer_sequence)}")
    print(f"Number of nodes: {str(n)}")
    print(f"Number of already computed inputs: {str(input_count)}")
    print(f"For {str(too_many_duplicated_symbol_count)} inputs, we could not find optimal solutions with less than 2 duplicated symbols after {number_of_authorized_tries} tries")
    print(f"For {str(wrong_UB_count)} inputs, the UB is not verified.")
    print(f"Last waiting was: {str(waiting)}")
    end = time.time() - start
    print(f"The program was running for {str(end)} seconds or {str(math.ceil(end/60))} minutes or {str(math.ceil((end/60)/60))} hours to end.")





