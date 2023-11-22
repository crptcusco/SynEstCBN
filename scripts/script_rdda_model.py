from clases.red_rddas_model import RedRddasModel
import ray
ray.init(num_cpus=4)
# import random  # generate random numbers
# from random import randint  # generate random numbers integers
# from itertools import product  # generate combinations of numbers

# path = "files/17_05_2022_2_5_1_2_2.pickle"
# path = "files/17_05_2022_3_5_2_2_2.pickle"
# path = "files/17_05_2022_4_5_2_2_2.pickle"
# path = "files/17_05_2022_5_5_2_2_2.pickle"
# path = "files/17_05_2022_6_5_2_2_2.pickle"
# path = "files/17_05_2022_7_5_2_2_2.pickle"
# path = "files/17_05_2022_8_5_2_2_2.pickle"
# path = "files/17_05_2022_9_5_2_2_2.pickle"
path = "files/17_05_2022_10_5_2_2_2.pickle"
path_base = path[:-7]

print("Reading the file: ", path)
oRedRddasModel = RedRddasModel.load_file_pickle(path)

#Show the RDDA Information
oRedRddasModel.show()

# # generate the diagram of the Network RDDA, show and save graph in .eps format
# # Show the topology of the RDDA in a graph using the igraph library and save the graph in eps format
# print("Topology Graph of the RDDA using igraph Library")
# oRedRddasModel.graph_topology_igraph(show_graph=True,save_graph=True,path_graph="")

# Calculate the Attractors by RDDA and by Signal
result = RedRddasModel.calculation_compatible_pairs.remote(oRedRddasModel)
oRedRddasModel = ray.get(result)

import time
inicio = time.time()
# Calculate the Attractors by RDDA and by Signal with iterative Method
oRedRddasModel = RedRddasModel.assembly_attractor_fields_optimized(oRedRddasModel)
fim = time.time()
print(" Number of Fields Attractors :", len(oRedRddasModel.attractor_fields))
print("Duration 1:", fim - inicio)

# Show the topology graph using the Networkx library
# oRedRddasModel.graph_topology_networkx(show_graph = True ,save_graph=False,path_graph="")

# # Show the Graph of the attractor pairs
# oRedRddasModel.graph_attractor_pairs(export_graph=True, path=path_base)

# # Show the Graphs of the attractor fields
# oRedRddasModel.graph_attractor_fields()

# # Show the detail for each attractor field
# oRedRddasModel.show_detail_attractor_fields()

# Explicit stop Ray
ray.shutdown()