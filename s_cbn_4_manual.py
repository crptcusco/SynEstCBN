from classes.cbnetwork import CBN
from classes.internalvariable import InternalVariable
from classes.localnetwork import LocalNetwork
from classes.directededge import DirectedEdge

print("=============================================")
print("EXAMPLE OF A CBN WITH 4 MANUAL LOCAL NETWORKS")
# Create the CBN

# Initial Parameters
n_local_nets = 4
indexs = [1, 2, 3, 4]
d_variables = {1: (1, 2, 3),
               2: (4, 5, 6, 7),
               3: (8, 9, 10),
               4: (11, 12, 13, 14)}

l_relations = [(2, 1), (3, 2), (2, 3), (4, 3)]
l_var_output = [[4, 5], [8, 9], [6, 7], [13, 14]]
l_var_input = [15, 16, 17, 18]

d_description_variables = {1: {1: [[2, 3], [1, -15]],
                               2: [[1, 15]],
                               3: [[3, -1, 15]]},
                           2: {4: [[-5, 6, 7]],
                               5: [[6, 7, -16]],
                               6: [[-4, -5, 16]],
                               7: [[-5, 16, 7]]},
                           3: {8: [[9, 10, 17]],
                               9: [[8, 18]],
                               10: [[8, 9]]},
                           4: {11: [[-12, 13]],
                               12: [[-11, 13]],
                               13: [[14, 11, 12]],
                               14: [[11, -12]]}}

# '∧': operator.and_,
# '∨': operator.or_,

# Create the local networks
print("---------------------")
print("Creating the networks")
l_local_nets = []
for index in indexs:
    # generate the Boolean Networks
    o_local_network = LocalNetwork(index, d_variables[index])
    l_local_nets.append(o_local_network)
    o_local_network.show()

# Create the relations between the networks
print("======================")
print("Creating the relations")
print("Relations: ", l_relations)

l_directed_edges = []
i_relation = 0
for t_edge in l_relations:
    coupling_function = " " + " ∨ ".join(list(map(str, l_var_output[i_relation]))) + " "
    t_edge = DirectedEdge(t_edge[1], t_edge[0], l_var_output[i_relation],
                          l_var_input[i_relation], coupling_function)
    l_directed_edges.append(t_edge)
    i_relation += 1

# Create the CBN
o_cbn = CBN(l_local_nets, generated=False)

# Generate the variables for the local networks
for o_network in o_cbn.l_local_nets:
    # Fill the description from variables
    for key_variable, value_variable in d_description_variables[o_network.index].items():
        o_variable_model = InternalVariable(key_variable, value_variable)
        o_network.l_desc_vars.append(o_variable_model)

        print("Variable description from Network:", o_network.index)
        print(o_network.l_desc_vars)

    # Fill the relations for every network
    for o_directed_edge in l_directed_edges:
        if o_directed_edge.rdda_entrada == o_network.index:
            o_network.l_var_total += [o_directed_edge.name_variable]
            o_network.l_var_exterm += [o_directed_edge.name_variable]

# Show the cbn and his networks
o_cbn.show_local_networks()

# # find the attractors by local networks
# print("------------------------")
# print("List of Attractors")
# print("------------------------")
# o_cbn = CBN.find_attractors_rddas(o_cbn)
#
# # Show the attractors of the RDDs by Signal
# print("Show the List of attractors")
# o_cbn.show_local_networks_attractors()
#
# # Calculation the Attractor Pairs
# o_cbn = CBN.calculation_compatible_pairs(o_cbn)
#
# # Show the list of attractor pairs
# o_cbn.show_attractor_pairs()
#
# # # Assembly the attractor fields
# # l_partial_paths = o_rdda.assembly_attractor_fields_pruning(o_rdda)
# #
# # # Show the list of attractor fields
# # o_rdda.show_attractor_fields_detail()
