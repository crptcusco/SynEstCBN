# Imports
from clases.red_rddas_model import RedRddasModel
import ray
import time
import pandas as pd
import numpy as np

# Ray Configurations
# ray.shutdown()
# runtime_env = {"working_dir": "/home/reynaldo/Documents/RESEARCH/SynEstRDDA", "pip": ["requests", "pendulum==2.1.2"]}
# ray.init(address='ray://172.17.163.253:10001', runtime_env=runtime_env, log_to_driver=False)
# ray.init(address='ray://172.17.163.244:10001', runtime_env=runtime_env , log_to_driver=False, num_cpus=12)
ray.init(log_to_driver=False, num_cpus=12)

#capture the time for all the experiment
v_begin_exp = time.time()
# Experiment for global relations growth
n_experiments = 20
l_experiments = []
for cont_experiment in range(1,n_experiments+1):
    print("============================")
    print("Experiment:", cont_experiment)
    print("============================")

    # Variable Parameters
    n_of_signals_rdd_min = 2
    n_of_signals_rdd_max = 4

    # Fixed Parameters
    n_of_rdds = 5
    n_of_var_by_rdd = 5
    n_output_variables = 2
    n_clauses_function = 2
    type_network = "ALEATORY"

    # List of Result for the Experiments
    l_res_sample = []

    v_n_network = 1
    for n_of_signals_rdd in range(n_of_signals_rdd_min, n_of_signals_rdd_max + 1):
        print("Number of Network:", v_n_network)
        print("Number of RDDs:", n_of_rdds)
        print("Number of Signals by RDD:", n_of_signals_rdd)
        print("-------------------------------")

        # generate the RDDAs of the Network of RDDAs
        print("generating the Network of RDDAs ...")
        o_rdda_model = RedRddasModel(n_of_rdds, n_of_var_by_rdd, n_of_signals_rdd, n_output_variables,
                                       n_clauses_function)

        # Generate the RDDs
        print("generating the rdds ...")
        o_rdda_model.generate_local_networks(type_network=type_network)

        # Calculate the Attractors by RDDA and by Signal
        v_begin_0 = time.time()
        result = RedRddasModel.find_attractors_rddas_ray.remote(o_rdda_model)
        o_rdda_model = ray.get(result)
        v_end_0 = time.time()
        v_time_0 = v_end_0 - v_begin_0

        # Calculate the Attractors by RDDA and by Signal
        v_begin_1 = time.time()
        result = RedRddasModel.calculation_compatible_pairs_ray.remote(o_rdda_model)
        o_rdda_model = ray.get(result)
        v_end_1 = time.time()
        v_time_1 = v_end_1 - v_begin_1

        # Calculate the Attractors by RDDA and by Signal with optimized Method
        v_begin_2 = time.time()
        result = RedRddasModel.assembly_attractor_fields_pruning_ray.remote(o_rdda_model)
        o_rdda_model = ray.get(result)
        v_end_2 = time.time()
        v_time_2 = v_end_2 - v_begin_2

        # Save the results for the experiment , numeric and time indicators
        res_dict = {
                    "n_network": v_n_network,
                    "n_variables": n_of_var_by_rdd,
                    "n_coupling_signals": n_of_signals_rdd,
                    "n_rdda_attractors": len(o_rdda_model.d_global_rdda_attractor.items()),
                    "t_find_attractors_method": v_time_0,
                    "n_pair_attractors": len(o_rdda_model.list_attractors_pairs),
                    "t_comp_paris_method": v_time_1,
                    "n_attractor_fields": len(o_rdda_model.attractor_fields),
                    "t_optimized_method": v_time_2
                    }
        l_res_sample.append(res_dict)
        v_n_network = v_n_network + 1

    # Add the sample data to pandas dataframe
    df = pd.DataFrame.from_dict(l_res_sample)
    l_experiments.append(df)

print("END EXPERIMENT")
# Take the time of the experiment
v_end_exp = time.time()
v_time_exp = v_end_exp - v_begin_exp
print("Time experiment (in seconds): ", v_time_exp )

# Time of Experiment (in seg) 1898.2322750091553
# Time of Experiment (in hours, minutes and seconds) 00:31:38
# Total Time 359606.66107463837 segs  - 4,16 days
print("RESUME OF THE EXPERIMENT")
print("--------------------------------------------------------------------")
print("Name of the Experiment:", "Experiment 2 - Internal Variable Growth")
print("Variable Parameters : Number os Relations")
print("Range of signals by RDD :", n_of_signals_rdd_min , "-",n_of_signals_rdd_max)
print("Fixed parameters")
print("Number of RDDs:",n_of_rdds )
print("Number of variables:",n_of_var_by_rdd)

print("Number of output variables:", n_output_variables)
print("Number of function clauses:", n_clauses_function)
print("Network Type:", type_network)
print("--------------------------------------------------------------------")
print("Time of Experiment (in seg)", v_time_exp)
print("Time of Experiment (in hours, minutes and seconds)", time.strftime("%H:%M:%S", time.gmtime(v_time_exp)))
print("--------------------------------------------------------------------")
pf_res = pd.concat(l_experiments, keys=range(1,n_experiments+1), names=["n_sample","n_aux"], ignore_index=False)
pf_res.reset_index(drop=True, inplace=True, level=1)

# Save the experiment data in csv, using pandas Dataframe
path = "data/exp3_global_relations_growth_data20.csv"
pf_res.to_csv(path)
print("Experiment saved in:", path)
