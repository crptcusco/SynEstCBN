from modules.CBN import CBN
from modules.CouplingSignal import CouplingSignal
from modules.LocalNetwork import LocalNetwork


def main(t_variables=None):
    # Initial Parameters
    print("BEGIN")
    t_networks = [1, 2, 3, 4]
    t_variables = ((1, 2, 3),
                   (4, 5, 6, 7),
                   (8, 9, 10),
                   (11, 12, 13, 14))
    t_relations = ((2, 1), (3, 2), (2, 3), (4, 3))
    t_var_output = ((4, 5), (8, 9), (6, 7), (13, 14))
    t_var_input = (15, 16, 17, 18)

    # 1,2,3,4,15
    # 4,5,6,7,16
    # 8,9,10, 17, 18
    # 11, 12, 13, 14
    t_description_variables = ((1, '2 ∧ 3 '),
                               (2, '4 ∨ 15 '),
                               (3, '3 ∨ 1 ∨ 15 '),
                               (4, '5 ∨ 6 ∨ 7 '),
                               (5, '6 ∧ 7 ∧ 16 '),
                               (6, '4 ∧ 5 ∧ 16 '),
                               (7, '5 ∧ 16 ∨ 7 '),
                               (8, '9 ∨ 10 ∨ 17 '),
                               (9, '8 ∨ 18 '),
                               (10, '8 ∨ 9 '),
                               (11, '12 ∨ 13 '),
                               (12, '11 ∨ 13 '),
                               (13, '14 ∨ 11 ∨ 12 '),
                               (14, '11 ∧ 12 '))

    # '∧': operator.and_,
    # '∨': operator.or_,

    # Create the CBN
    print("========================")
    print("Inputs for the CBN")
    print("========================")

    # Create the local networks
    print("List of Networks")
    l_networks = []
    for i_network in t_networks:
        # generate the Boolean Networks
        o_local_network = LocalNetwork(i_network=i_network, l_variables=t_variables[i_network - 1])
        l_networks.append(o_local_network)
        print(o_local_network)

    # Create the relations
    print("Relations: ", t_relations)
    l_relations = []
    i_relation = 0
    for relation in t_relations:
        coupling_function = " " + " ∨ ".join(list(map(str, t_var_output[i_relation]))) + " "
        print(coupling_function)
        o_coupling_signal = CouplingSignal(relation[1], relation[0], t_var_output[i_relation],
                                           t_var_input[i_relation], coupling_function)
        l_relations.append(o_coupling_signal)
        i_relation += 1

    # Create the CBN
    print("========================")
    print("Coupling Boolean Network")
    print("========================")
    o_cbn = CBN(n_networks=len(t_networks), l_networks=l_networks, l_relations=l_relations)
    o_cbn.show()

    # Fill the description from variables

    # find the attractors by local networks
    print("------------------------")
    print("List of Attractors")
    print("------------------------")
    o_cbn = CBN.find_attractors(o_cbn)
    for o_network in o_cbn.l_networks:
        for attractor in o_network.set_of_attractors:
            print(attractor)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
    print('END')
