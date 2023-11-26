# Imports
from clases.red_rddas_model import RedRddasModel
import ray

# Parameters
n_of_rddas = 5
n_of_variables_rdda = 10
n_of_signals_rdda = 2
n_exit_variables = 2
n_clauses_function = 2
type_network = "ALEATORY"
# this name has to be unique
unique_path = "30_05_2022"
path = "files/" + unique_path + "_" + str(n_of_rddas) + "_" + str(n_of_variables_rdda) + "_" + str(n_of_signals_rdda) \
       + "_" + str(n_exit_variables) + "_" + str(n_clauses_function)


print("PROGRAM TO FIND")
# generate the RDDAs of the Network of RDDAs
print("generating the Network of RDDAs ...")
oRedRddasModel = RedRddasModel(n_of_rddas, n_of_variables_rdda, n_of_signals_rdda, n_exit_variables,
                               n_clauses_function)

# generate the RDDAs
print("generating the rddas ...")
oRedRddasModel.generate_local_networks(type_network=type_network)


# Calculate the Attractors by RDDA and by Signal
oRedRddasModel  = RedRddasModel.find_attractors_rddas(oRedRddasModel)


# Save the Network of RDDAs in a Pickle file
RedRddasModel.save_file_pickle(oRedRddasModel, path)
path += ".pickle"

print("=======================================================")
print("The Network of RDDAs is saved in: ", path)

# Load the Network of RDDAs in a Pickle file
# oRedRddasModel2 = RedRddasModel.load_file_pickle(path)

# Show the Network of RDDAs
# oRedRddasModel2.show()

print("END SCRIPT")