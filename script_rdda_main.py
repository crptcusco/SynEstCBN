from clases.red_rddas_model import RedRddasModel
import sys

print("PROGRAM TO FIND STABILITY AND SYNCHRONISM IN RDDAs")
# Receiving the parameters
# n_of_rddas = int(sys.argv[1])
# n_of_variables_rdda = int(sys.argv[2])
# n_of_signals_rdda = int(sys.argv[3])
# n_exit_variables = int(sys.argv[4])
# n_clauses_function = int(sys.argv[5])

n_of_rddas = 3
n_of_variables_rdda = 5
n_of_signals_rdda = 2
n_exit_variables = 2
n_clauses_function = 2

# type_network = "ALEATORY"
# generate the RDDAs of the Network of RDDAs
print("GENERATING THE NETWORK OF RDDAs ...")
oRedRddasModel = RedRddasModel(n_of_rddas, n_of_variables_rdda, n_of_signals_rdda, n_exit_variables,
                               n_clauses_function)
# generate the RDDAs
# print("generating the rddas ...")
oRedRddasModel.generate_rddas()

# calculate the Attractors Field
l_of_attractors_field = RedRddasModel.calculate_attractors_fields(oRedRddasModel)
print("END PROGRAM")
