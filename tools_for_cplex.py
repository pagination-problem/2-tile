from tree import Tree
import cplex
import networkx as nx
import matplotlib.pyplot as plt

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
    model.write(path+name+".lp", "lp")

    plt.figure(figsize=(5,5))
    nx.draw_networkx (tree)
    plt.savefig(path+name+".pdf")

    model.solution.write(path+name+".sol")
