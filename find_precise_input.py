from tree import Tree
import cplex
import math
import networkx as nx
import matplotlib.pyplot as plt
import random
import time

MIN_NODE_NUMBER = 5
MAX_NODE_NUMBER = 25

def checks_number_of_duplicated_symbols(t, cplex_input):
    cpt = 0
    for u in t.tree.nodes():
        (val_1, val_2) = cplex_input.solution.get_values( ["x_1"+str(u), "x_2"+str(u)] )

        if val_1 == 0 and val_2 == 0:
            cpt = cpt + 1

    return cpt

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

def checks_if_all_the_duplicated_vertices_are_linked(t, cplex_input):
    list_of_duplicated_symbols = []
    for u in t.tree.nodes():
        (val_1, val_2) = cplex_input.solution.get_values( ["x_1"+str(u), "x_2"+str(u)] )

        if val_1 == 0 and val_2 == 0:
            list_of_duplicated_symbols.append(u)

    v1 = list_of_duplicated_symbols[0]
    v2 = list_of_duplicated_symbols[1]
    v3 = list_of_duplicated_symbols[2]

    if t.tree.has_edge(v1,v2) and t.tree.has_edge(v1,v3) and t.tree.has_edge(v2,v3):
        return True
    else:
        return False

def finds_another_solution(t, cplex_input, OPT):
    adds_a_no_good_cut_inequality(t, cplex_input, OPT)
    cplex_input.solve()
    # cpt = tools_for_cplex.checks_number_of_duplicated_symbols(t, cplex_input)
    cpt = checks_number_of_duplicated_symbols(t, cplex_input)

path = "saved_trees/C_equals_3/"
wrong_ub_path = "saved_trees/wrong_UB"
name = "my_input"
try_count = 0
end_of_time = False
# max_time = 7200 #2 hours
max_time = 1800 #30 min
start =  time.time()


while "I didn't find a solution with C = 3 and in which the three vertices are linked" and not end_of_time:
    n = random.randint(MIN_NODE_NUMBER, MAX_NODE_NUMBER)
    t = Tree(n)

    cplex_input = t.to_cplex_input()
    cplex_input.solve()

    # cpt = tools_for_cplex.checks_number_of_duplicated_symbols(t, cplex_input)
    cpt = checks_number_of_duplicated_symbols(t, cplex_input)
    OPT = cplex_input.solution.get_objective_value() + n

    if OPT <= math.ceil( (len(t.tree)) / 2 ) + 1 :
        if cpt == 3 :
            if checks_if_all_the_duplicated_vertices_are_linked(t, cplex_input):
                saves_a_potential_problematic_model(path, name, cplex_input, t.tree)
                break
            else:
                for i in range(0,3):
                    adds_a_no_good_cut_inequality(t, cplex_input, OPT)
                    cplex_input.solve()
                    # cpt = tools_for_cplex.checks_number_of_duplicated_symbols(t, cplex_input)
                    cpt = checks_number_of_duplicated_symbols(t, cplex_input)

                    if cpt == 3:
                        if checks_if_all_the_duplicated_vertices_are_linked(t, cplex_input):
                            saves_a_potential_problematic_model(path, name, cplex_input, t.tree)
                            break

        else:

    else:
        saves_a_potential_problematic_model(wrong_ub_path, name, cplex_input, t.tree)

    try_count = try_count + 1
    if time.time() - start > max_time:
        end_of_time = True

if end_of_time:
    print(f"The programs use the {max_time} seconds or {math.ceil(max_time/60)} minutes or {math.ceil((max_time/60)/60)} hours that it was allowed to use.")

print(f"The program computed {try_count} inputs before it ended.")
