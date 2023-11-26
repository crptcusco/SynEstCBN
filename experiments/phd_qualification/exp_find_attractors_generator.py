# Imports
from clases.red_rddas_model import RedRddasModel
import ray
import time
import pandas as pd
import numpy as np
import pickle  # library to serialization object

from clases.experiment_model import ExperimentModel

# Ray Configurations
# ray.shutdown()
# runtime_env = {"working_dir": "/home/reynaldo/Documents/RESEARCH/SynEstRDDA", "pip": ["requests", "pendulum==2.1.2"]}
# ray.init(address='ray://172.17.163.253:10001', runtime_env=runtime_env, log_to_driver=False)
# ray.init(address='ray://172.17.163.244:10001', runtime_env=runtime_env , log_to_driver=False, num_cpus=12)
ray.init(log_to_driver=False, num_cpus=12)

# capture the time for all the experiment
v_begin_exp = time.time()
# Experiment for internal variable growth
n_samples = 5
l_data = pd.DataFrame()

for cont_experiment in range(1, n_samples + 1):
    print("============================")
    print("Experiment:", cont_experiment)
    print("============================")
    l_experiment = pd.DataFrame()
    # l_rddas = []

    # Variable Parameters
    n_rddas_min = 3
    n_rddas_max = 10

    # Fixed Parameters
    n_of_variables_rdda = 5
    n_of_signals_rdda = 2
    n_exit_variables = 2
    n_clauses_function = 2
    type_network = "ALEATORY"

    # List of Result for the Experiments
    l_res_sample = []

    v_n_network = 1
    for n_of_rdds in range(n_rddas_min, n_rddas_max + 1):
        print("Number of Network:", v_n_network)
        print("-------------------------------")

        # generate the RDDAs of the Network of RDDAs
        print("generating the Network of RDDAs ...")
        oRedRddasModel = RedRddasModel(n_of_rdds, n_of_variables_rdda, n_of_signals_rdda, n_exit_variables,
                                       n_clauses_function)

        # Generate the RDDs
        print("generating the rdds ...")
        oRedRddasModel.generate_local_networks(type_network=type_network)

        # Calculate the Attractors by RDDA and by Signal
        v_begin_0 = time.time()
        result = RedRddasModel.find_attractors_rddas_ray.remote(oRedRddasModel)
        oRedRddasModel = ray.get(result)
        v_end_0 = time.time()
        v_time_0 = v_end_0 - v_begin_0

        # Save the results for the experiment , numeric and time indicators
        res_dict = pd.DataFrame([{
            "n_sample": cont_experiment,
            "n_network": v_n_network,
            "n_rdds": n_of_rdds,
            # "n_rdda_attractors": len(oRedRddasModel.d_global_rdda_attractor.items()),
            "t_find_attractors_method": v_time_0,
            # "n_pair_attractors": len(oRedRddasModel.list_attractors_pairs),
            # "t_comp_paris_method": v_time_1,
            # "n_attractor_fields": len(oRedRddasModel.attractor_fields),
            # "t_optimized_method": v_time_2
            "o_network": oRedRddasModel
        }])

        v_n_network = v_n_network + 1

        # Add the data to experiment object
        # l_experiment.append(res_dict)
        l_experiment = pd.concat([l_experiment, res_dict])
        # l_rddas.append(oRedRddasModel)
    # Add the data to the dictionary of experiments
    # cont_experiment
    l_data = l_data.append(l_experiment, ignore_index=True)
    # l_l_rddas.append(l_rddas)
print("END EXPERIMENT")

# Take the time of all the experiment
v_end_exp = time.time()
v_time_exp = v_end_exp - v_begin_exp
print("Time experiment (in seconds): ", v_time_exp)

# Resume of the Experiment
print("RESUME OF THE EXPERIMENT")
print("--------------------------------------------------------------------")
print("Name of the Experiment:", "Experiment 2 - Internal Variable Growth")
print("Variable Parameters : Number os RDDs")
print("Range of Number of RDDs:", n_rddas_min, "-", n_rddas_max)
print("Fixed parameters")
print("Number of variables:", n_of_variables_rdda)
print("Number of signals by RDD :", n_of_signals_rdda)
print("Number of output variables:", n_exit_variables)
print("Number of function clauses:", n_clauses_function)
print("Network Type:", type_network)
print("--------------------------------------------------------------------")
print("Time of Experiment (in seg)", v_time_exp)
print("Time of Experiment (in hours, minutes and seconds)", time.strftime("%H:%M:%S", time.gmtime(v_time_exp)))
print("--------------------------------------------------------------------")

# Metadata from the experiment
d_meta = {'n_samples': n_samples,
          'n_rddas_min': n_rddas_min,
          'n_rddas_max': n_rddas_max,
          'n_of_variables_rdda': n_of_variables_rdda,
          'n_of_signals_rdda': n_of_signals_rdda,
          'n_exit_variables': n_exit_variables,
          'n_clauses_function': n_clauses_function,
          'type_network': type_network,
          'total_time': v_time_exp}

# Save the experiment data in pickle
path = "data/exp_find_attractors_data"
o_experiment = ExperimentModel(d_meta, l_data)
ExperimentModel.save_file_pickle(o_experiment, path)
path += ".pickle"
print("File saved:", path)
