# LINEAL CBN ALEATORY SCRIPT EXAMPLE

# import libraries
from classes.cbnetwork import CBN
from classes.directededge import DirectedEdge
from classes.internalvariable import InternalVariable
from classes.localnetwork import LocalNetwork

# pass the parameters
n_local_networks = 10
n_var_network = 5
n_output_variables = 2
n_clauses_function = 2
v_topology = 4

CBN.show_allowed_topologies()

# create a Coupled Boolean Network with the parameters
o_cbn = CBN.generate_cbn(n_local_networks=n_local_networks,
                         n_var_network=n_var_network,
                         v_topology=v_topology,
                         n_output_variables=n_output_variables,
                         n_clauses_function=n_clauses_function)

# Adding a network to make restricted the signals
# generate a network
print("---------------------------------")
print("GENERATE A NEW NETWORK")
l_internal_variables = [101, 102, 103, 104]
o_local_network = LocalNetwork(100, l_internal_variables)
o_local_network.l_var_total = l_internal_variables
o_local_network.num_var_total = len(o_local_network.l_var_total)

# generate the internal dynamic
d_variable_cnf_function = {101: [[-102, 103]],
                           102: [[101, 103]],
                           103: [[104, -101, 102]],
                           104: [[101, -102]]}

for i_local_variable in o_local_network.l_var_intern:
    o_variable_model = InternalVariable(i_local_variable, d_variable_cnf_function[i_local_variable])
    o_local_network.des_funct_variables.append(o_variable_model)
o_cbn.l_local_networks.append(o_local_network)
print("New network created")

# generate the directed edge
"---------------------------------"
print("generate the directed edge")
i_variable_signal = 105
t_edge = (1, 100)
l_output_variables = [103, 104]
coupling_function = " " + " ∨ ".join(map(str, l_output_variables)) + " "
o_directed_edge = DirectedEdge(i_variable_signal, t_edge[0], t_edge[1], l_output_variables, coupling_function)
o_cbn.l_directed_edges.append(o_directed_edge)


# update the function of one variable in the first network
o_local_network = o_cbn.find_network_by_index(1)
o_local_network.l_var_exterm.append(105)
o_local_network.l_var_total.append(105)
o_local_network.l_input_signals.append(o_directed_edge)
o_local_network.num_var_total += 1

# # update one internal variable
# o_internal_variable = o_local_network.get_internal_variable(1)
# o_internal_variable.show()
# o_internal_variable.cnf_function.append([105])
# o_local_network.update_internal_variable(o_internal_variable)

# # update all the internal variables with clause
# for o_internal_variable in o_local_network.des_funct_variables:
#     o_internal_variable.cnf_function.append([105])
#     o_local_network.update_internal_variable(o_internal_variable)

# update all the internal variables with literal
for o_internal_variable in o_local_network.des_funct_variables:
    o_internal_variable.cnf_function[0].append(-105)
    o_local_network.update_internal_variable(o_internal_variable)

o_cbn.update_network_by_index(1, o_local_network)

# show the kind of the edges
o_cbn.show_directed_edges()

for o_directed_edge in o_cbn.l_directed_edges:
    print(o_directed_edge.output_local_network, "->", o_directed_edge.input_local_network)

# Find attractors
o_cbn.find_attractors_with_heap()
# # show attractors
o_cbn.show_attractors()


# o_cbn.show_directed_edges()

# show the resume of the cbn
o_cbn.show_cbn()

# show the kind of every coupled signal
o_cbn.show_coupled_signals_kind()

o_cbn.find_compatible_pairs()
o_cbn.show_attractor_pairs()
