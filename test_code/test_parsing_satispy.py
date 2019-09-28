from libraries.satispy.satispy.solver.minisat import Minisat
from libraries.satispy.satispy import cnf

exp, symbols = cnf.CnfFromString.create("v1 & v2 | v3")

solver = Minisat()

solution = solver.solve(exp)

if solution.success:
    print ("Found a solution:")
    for symbol_name in symbols.keys():
        print ("%s is %s" % (symbol_name, solution[symbols[symbol_name]]))
else:
    print ("The express    ion cannot be satisfied")