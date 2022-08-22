# Script for generate  master_defense
# Imports
from clases.red_rddas_model import RedRddasModel
import ray
import time

# Ray Configurations
ray.init(num_cpus=12, log_to_driver=False)

# Experiment 1
print("Experiment 1")
print("============")

# Variable Parameters
n_rddas_min = 3
n_rddas_max = 10

# Fixed Parameters
n_of_variables_rdda = 5
n_of_signals_rdda = 2
n_exit_variables = 2
n_clauses_function = 2
type_network = "ALEATORY"
# this name has to be unique
unique_path = "21_01_2022"

# List of Result for the Experiments
l_res_experiment = []

v_n_network = 1
for n_of_rdds in range(n_rddas_min, n_rddas_max + 1):
    print("Number of Network:", v_n_network)
    print("-------------------------------")

    path = "files/" + unique_path + "_" + str(n_of_rdds) + "_" + str(n_of_variables_rdda) + "_" + str(n_of_signals_rdda) \
           + "_" + str(n_exit_variables) + "_" + str(n_clauses_function)

    # generate the RDDAs of the Network of RDDAs
    print("generating the Network of RDDAs ...")
    oRedRddasModel = RedRddasModel(n_of_rdds, n_of_variables_rdda, n_of_signals_rdda, n_exit_variables,
                                   n_clauses_function)

    # Generate the RDDs
    print("generating the rdds ...")
    oRedRddasModel.generate_rddas(type_network=type_network)

    # # Save the Network of RDDAs in a Pickle file
    # RedRddasModel.save_file_pickle(oRedRddasModel, path)
    # path += ".pickle"
    #
    # print("=======================================================")
    # print("The Network of RDDAs is saved in: ", path)

    # Show the Network of RDDAs
    # oRedRddasModel.show()

    # Calculate the Attractors by RDDA and by Signal
    result = RedRddasModel.find_attractors_rddas_ray.remote(oRedRddasModel)
    oRedRddasModel = ray.get(result)

    # Calculate the Attractors by RDDA and by Signal
    v_begin_0 = time.time()
    result = RedRddasModel.calculation_compatible_pairs.remote(oRedRddasModel)
    oRedRddasModel = ray.get(result)
    v_end_0 = time.time()
    v_time_0 = v_end_0 - v_begin_0

    # Calculate the Attractors by RDDA and by Signal with iterative Method
    v_begin_1 = time.time()
    # result = RedRddasModel.assembly_attractor_fields_iterative.remote(oRedRddasModel)
    # oRedRddasModel = ray.get(result)
    v_end_1 = time.time()
    v_time_1 = v_end_1 - v_begin_1

    v_begin_2 = time.time()
    # Calculate the Attractors by RDDA and by Signal with optimized Method
    result = RedRddasModel.assembly_attractor_fields_optimized.remote(oRedRddasModel)
    oRedRddasModel = ray.get(result)
    v_end_2 = time.time()
    v_time_2 = v_end_2 - v_begin_2

    res_dict = {"n_network": v_n_network,
                "n_rdds": n_of_rdds,
                "n_rdda_attractors": len(oRedRddasModel.d_global_rdda_attractor.items()),
                "n_attractor_fields": len(oRedRddasModel.attractor_fields),
                "t_comp_paris_method": v_time_0,
                # "t_iterative_method": v_time_1,
                "t_optimized_method": v_time_2,
                }
    l_res_experiment.append(res_dict)
    v_n_network = v_n_network + 1

for v_reg_dict in l_res_experiment:
    # Show the metrics
    print("===========================================")
    print("Result of Network:", v_reg_dict["n_network"])
    print("===========================================")
    print("Number of RDDs:", v_reg_dict["n_rdds"])
    print("Number of Attractors :", v_reg_dict["n_rdda_attractors"])
    print("Number of Attractor Fields:", v_reg_dict["n_attractor_fields"])
    print("Duration Compatible Pairs Method :", v_reg_dict["t_comp_paris_method"])
    # print("Duration Iterative Method :", v_reg_dict["t_iterative_method"])
    print("Duration Optimized Method:", v_reg_dict["t_optimized_method"])

print("END EXPERIMENT")
