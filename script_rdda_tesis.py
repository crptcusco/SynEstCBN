from clases.red_rddas_model import RedRddasModel

# Load the Network of RDDAs in a Pickle file
o_network_rddas_model = RedRddasModel.load_file_pickle("files/example_research/rdda_3_5_2_2_2.pickle")
o_network_rddas_model.show()

# show the diagram of the Network RDDA
o_network_rddas_model.graph_topology(True, "files/example_research/")

# calculate the Attractors Field
RedRddasModel.calculate_attractors_fields(o_network_rddas_model, save_graph=True, path_graph="files/example_research/")

print("END PROGRAM")
