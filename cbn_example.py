from modules.CBN import CBN
from modules.CouplingSignal import CouplingSignal
from modules.LocalNetwork import LocalNetwork

# initial parameters
n_networks = 4
n_variables = [3, 4, 3, 4]
t_relations = ((2, 1), (3, 2), (2, 3), (4, 3))
t_var_output = ((4, 5), (8, 9), (6, 7), (13, 14))
t_var_input = (15, 16, 17, 18)

# generate the  networks
print("List of Networks")
l_networks = []
n_var_begin = 1
for i_network in range(1, n_networks + 1):
    l_variables = list(range(n_var_begin, n_var_begin + n_variables[i_network - 1]))
    o_network = LocalNetwork(i_network=i_network, l_variables=l_variables)
    l_networks.append(o_network)
    n_var_begin += n_variables[i_network - 1]

# generate the relations
l_relations = []
i_relation = 0
d_dictionary = {
    1:"a",
    2:"b",
    3:"c",
    4:"d",
    5:"e",
    6:"f",
    7:"g"
}
for relation in t_relations:
    print(f'{d_dictionary.get(t_var_output[i_relation][0])} ∨ {d_dictionary.get(t_var_output[i_relation][1])}')
    o_coupling_signal = CouplingSignal(relation[1], relation[0], t_var_output[i_relation],
                                       t_var_input[i_relation],
                                       f'{d_dictionary.get(t_var_output[i_relation][0])} ∨ {d_dictionary.get(t_var_output[i_relation][1])}')
    i_relation += 1

o_cbn = CBN(n_networks=n_networks, l_networks=l_networks, l_relations=l_relations)
print(o_cbn)
