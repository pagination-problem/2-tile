This folder contains all the trees which triggered the program by either having a
number of dulicated symbols (the set named C) strictly greater than 2 or having an
optimal solution strictly greater than ceil ( (n+1)/2 ) in an optimal solution.

For each tree, we have two files:
- the first one is a model in a .lp file that Cplex can read and solve
- the second one is the tree drawn by the program.

The name of both files contains the Prufer sequence describing the tree with the following matching:
- 0 <-> a
- 1 <-> b
- etc..

Numbers are used in the Prufer sequence and thus in the name of the files
and letters are used in the model and the drawing for better readability.

