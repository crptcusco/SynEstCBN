from clases.red_rddas_model import RedRddasModel
# import random  # generate random numbers
# from random import randint  # generate random numbers integers
# from itertools import product  # generate combinations of numbers

# path = "files/example_research/rdda_3_5_2_2_2.pickle"
path = "files/15_07_2020_5_5_2_2_2.pickle"
# path = "files/18_07_2020_5_5_2_2_2.pickle"
path_base = path[:-7]

print("Reading the file: ", path)
oRedRddasModel = RedRddasModel.load_file_pickle(path)
oRedRddasModel.show()

# generate the diagram of the Network RDDA, show and save graph in .eps format
oRedRddasModel.graph_topology(path_graph=path_base, save_graph=True, show_graph=True)

# calculate the Attractors Field
# find attractor by rdda, calculate the compatibility between attractors and labeled graph montage
l_attractors_fields = RedRddasModel.calculate_attractors_fields(oRedRddasModel)

# # find the attractors for every RDDA and Permutation of signal coupling
# for o_rdda in oRedRddasModel.list_of_rddas:
#     # GENERATE THE POSSIBLES COMBINATIONS ACCORDING TO THE COUPLING SIGNALS
#     l_permutation = product(list('01'), repeat=len(o_rdda.list_of_signals))
#     for v_permutation in l_permutation:
#         print("RED NUMBER : " + str(o_rdda.number_of_rdda) + " PERMUTATION SIGNAL COUPLING: ", v_permutation)
#         o_rdda.find_local_attractor_by_permutation(''.join(v_permutation))
#         o_rdda.show_permutation_attractors()

# show the attractor group by permutation

# generate the graph of compatible attractors

print("END SCRIPT")