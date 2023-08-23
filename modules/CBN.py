from itertools import product  # generate combinations of numbers

from modules.LocalNetwork import LocalNetwork


class CBN(object):
    def __init__(self, n_networks, generated=False, **kwargs):
        self.n_networks = n_networks
        self.generated = generated
        if self.generated:
            self.generate_cbn()
        else:
            self.l_networks = kwargs['l_networks']
            self.l_relations = kwargs['l_relations']

        # calculate properties
        self.l_cbn_permutation_attractors = []


    def __str__(self):
        res = 'Number of Networks: {}, Generated: {}'.format(self.n_networks, self.generated)
        return res

    def show(self):
        # show the networks
        print('------------------------')
        print("Networks")
        print('------------------------')
        if self.l_networks:
            for o_network in self.l_networks:
                o_network.show()

        # show the relations
        print('------------------------')
        print("Relations")
        print('------------------------')
        if self.l_relations:
            for o_relation in self.l_relations:
                o_relation.show()

    def generate_cbn(self):
        pass

    # @staticmethod
    # def find_attractors(o_cbn):
    #     print("BEGIN CALCULATE ALL LOCAL ATTRACTORS BY PERMUTATION")
        # CREATE A LIST OF: NETWORKS, PERMUTATION AND ATTRACTORS

        # # FIND THE ATTRACTORS FOR EACH RDDA
        # for o_network in o_cbn.l_networks:
        #     # GENERATE THE POSSIBLES COMBINATIONS ACCORDING TO THE COUPLING SIGNALS
        #     l_permutation = product(list('01'), repeat=len(o_network.list_var_extrem))
        #     for v_permutation in l_permutation:
        #         print("v_permutation")
        #         print(v_permutation)
        #         print("end")
        #         # ADD NETWORK, PERMUTATION AND LIST OF ATTRACTORS TO LIST OF ALL ATTRACTORS BY NETWORK
        #         # EST [RDDA Object, permutation,[List of attractors]]
        #         o_cbn.l_cbn_permutation_attractors.append([o_network, ''.join(v_permutation),
        #                                                    LocalNetwork.find_attractors(o_network,
        #                                                                                 ''.join(v_permutation))])
        # print("END CALCULATE ALL LOCAL ATTRACTORS")
        # print("######################################################")
        # return o_cbn

    @staticmethod
    def find_attractors_rddas(o_cbn):
        print("BEGIN CALCULATE ALL LOCAL ATTRACTORS BY PERMUTATION")
        # CREATE A LIST OF: NETWORKS, PERMUTATION AND ATTRACTORS

        # FIND THE ATTRACTORS FOR EACH RDDA
        for o_network in o_cbn.l_networks:
            # GENERATE THE POSSIBLES COMBINATIONS ACCORDING TO THE COUPLING SIGNALS
            l_permutation = product(list('01'), repeat=len(o_network.list_external_var))
            for v_permutation in l_permutation:
                # ADD NETWORK, PERMUTATION AND LIST OF ATTRACTORS TO LIST OF ALL ATTRACTORS BY NETWORK
                # EST [RDDA Object, permutation,[List of attractors]]
                o_cbn.l_cbn_permutation_attractors.append([o_network, ''.join(v_permutation),
                                                            LocalNetwork.findLocalAtractorsSATSatispy(o_network,
                                                                                                      ''.join(
                                                                                                          v_permutation))])
        print("END CALCULATE ALL LOCAL ATTRACTORS")
        print("######################################################")
        return o_cbn

    def show_local_networks_attractors(self):
        print("List of Attractors")
        print("========================")
        for permutation_attractor in self.l_cbn_permutation_attractors:
            print("Network: ", permutation_attractor[0].i_network)
            print("Permutation: ", permutation_attractor[1], " - Attractors: ")
            for attractor in permutation_attractor[2]:
                print(attractor)
        print("========================")

    @staticmethod
    def calculation_compatible_pairs(o_cbn):
        # SHOW ATTRACTORS GROUP BY RDDA AND PERMUTATION
        print("ATTRACTORS GROUP BY RDDA AND PERMUTATION")
        for element in o_cbn.l_cbn_permutation_attractors:
            print("RDDA:", element[0].i_network, " - Signal:", element[1])
            count_attractor_by_rdda = 1
            for attractor in element[2]:
                print("A_" + str(element[0].i_network) + "_" + str(count_attractor_by_rdda) + ":", attractor)
                count_attractor_by_rdda += 1
                # SUGGESTION : CREATE A MODEL OR LIST OF: RDDA, SIGNAL, ATTRACTOR
        print("######################################################")

        # GROUPS ATTRACTORS BY RDDA WITHOUT PERMUTATIONS
        print("BEGIN GROUP ATTRACTORS BY RDDA")
        l_rdda_attractors = []
        for oRdda in o_cbn.l_networks:
            l_aux_local_attractors = []
            for l_local_permutation_attractors in o_cbn.l_cbn_permutation_attractors:
                if oRdda.i_network == l_local_permutation_attractors[0].i_network:
                    l_aux_local_attractors.extend(l_local_permutation_attractors[2])
            # ADD THE ATTRACTORS TO THE LIST
            l_rdda_attractors.append([oRdda, l_aux_local_attractors])
        # print("######################################################")

        # CALCULATING THE LINKS BETWEEN TWO RDDAS
        l_links_two_rddas = []
        l_supported_attractor_pairs = []
        print("GENERATING THE LINKS BETWEEN TWO RDDAS ")
        print("######################################################")

        # CREATE A GLOBAL DICTIONARY
        d_global_rdda_attractor = {}
        v_cont_dict_global = 0
        print("WALK FOR EVERY GROUP OF ATTRACTORS OF THE PERMUTATION OF RDDA")
        print("======================================================")
        for l_local_permutation_attractors in o_cbn.l_cbn_permutation_attractors:
            print("WALK FOR EVERY ATTRACTOR OF THE PERMUTATION OF RDDA")
            print("======================================================")
            for v_local_attractor in l_local_permutation_attractors[2]:
                # The signal corresponds a one letter of the permutation
                v_cont_letter_permutation = 0
                v_rdda_input = l_local_permutation_attractors[0].i_network
                # We evaluate the attractor for every signal
                print("ANALYZING ATTRACTOR :", v_local_attractor)
                print("NETWORK INPUT: " + str(v_rdda_input))
                # print("PERMUTATION:", l_local_permutation_attractors[1])
                print("EVALUATE THE ATTRACTORS FOR EVERY SIGNAL")
                # adding attractor to the global dictionary
                d_global_rdda_attractor[v_cont_dict_global] = [v_rdda_input, v_local_attractor]
                v_cont_dict_global = v_cont_dict_global + 1
                for v_sinal in l_local_permutation_attractors[0].list_of_signals:
                    print("======================================================")
                    print("NETWORK OUTPUT : " + str(v_sinal.rdda_salida))
                    # evaluate if exist stationary condition in this signal and with this value
                    print("PERMUTATION: " + l_local_permutation_attractors[1])
                    v_letter = l_local_permutation_attractors[1][v_cont_letter_permutation]
                    print("PART OF PERMUTATION: " + v_letter)
                    print("======================================================")

                    # FIND ALL THE ATTRACTORS IN THE OUTPUT NETWORK
                    l_attractors_output = []
                    l_v_intern_output = []
                    for v_rdda_attractors in l_rdda_attractors:
                        if v_rdda_attractors[0].number_of_rdda == v_sinal.rdda_salida:
                            l_attractors_output = v_rdda_attractors[1]
                            l_v_intern_output = v_rdda_attractors[0].list_of_v_intern
                    # print(l_attractors_output)
                    # print(l_v_intern_output)

                    # FIND ALL THE ENTRY'S IN THE TRUE TABLE THAT HAVE THE RESULT EQUAL TO THE VALUE OF PERMUTATION
                    v_list_combinations = []
                    for key, value in v_sinal.true_table.items():
                        if value == v_letter:
                            v_list_combinations.append(key)

                    print("COMBINATIONS EQUALS TO THE VALUE OF THE SIGNAL")
                    print(v_list_combinations)

                    print("OUTPUT VARIABLES")
                    print(v_sinal.l_variaveis_saida)

                    # EVALUATE EVERY ATTRACTOR
                    print("EVALUATE THE VALUE OF THE SIGNAL FOR EVERY ATTRACTOR IN OUTPUT NETWORK")
                    for v_attractor_output in l_attractors_output:
                        print("ATTRACTOR:")
                        print(v_attractor_output)
                        # VALIDATE THE VALUES OF EVERY STATE OF ATTRACTOR
                        v_flag_accept_attractor = True
                        for v_state_attractor in v_attractor_output:
                            dictionary_values = dict(zip(l_v_intern_output, v_state_attractor))
                            print("------------------------------------------------------")
                            print("ANALYSIS OF THE STATE ATTRACTOR")
                            print(v_state_attractor)
                            print(dictionary_values)
                            # EVALUATION OF THE VALUES OF EACH STATE

                            # GENERATE ONE TEXT WITH THE VALUES
                            v_texto_union = ""
                            for v_saida in v_sinal.l_variaveis_saida:
                                v_texto_union = v_texto_union + dictionary_values[v_saida]
                            print(v_texto_union)
                            if v_texto_union not in v_list_combinations:
                                v_flag_accept_attractor = False
                            print("------------------------------------------------------")
                            # SAVE THE FIELD ATTRACTOR
                            # THE FIELD OF ATTRACTOR GONNA HAVE THIS INFORMATION:
                            # RDDA INPUT
                            # RRDA OUTPUT
                            # PERMUTATION
                            # VARIABLE INPUT
                            # VARIABLES OUTPUT SET
                            # ATTRACTOR INPUT
                            # ATTRACTOR OUTPUT

                        if v_flag_accept_attractor:
                            l_links_two_rddas.append(
                                [[l_local_permutation_attractors[0].number_of_rdda, v_local_attractor],
                                 [v_sinal.rdda_salida, v_attractor_output],
                                 v_letter,
                                 v_sinal.name_variable,
                                 v_sinal.l_variaveis_saida])

                            # preparing the format of attractors

                            l_supported_attractor_pairs = []

                    # pass to the next letter with cont
                    v_cont_letter_permutation = v_cont_letter_permutation + 1
        o_cbn.d_global_rdda_attractor = d_global_rdda_attractor
        o_cbn.l_links_two_rddas = l_links_two_rddas

        print("DATA PREPROCESSING")
        print("======================================================")
        print("LIST OF THE LINK BETWEEN TWO RDDAs WITH DICTIONARY")
        # Replace the RDDA Attractor with the dictionary Key
        l_aux_links_two_rddas = []
        l_t_aux_links_two_rddas = []
        for v_link in o_cbn.l_links_two_rddas:
            # print(v_link)
            # v_aux_link = v_link
            v_aux_link = [0, 0]
            v_tuple_1 = 0
            v_tuple_2 = 0
            for key, value in o_cbn.d_global_rdda_attractor.items():
                if v_link[0] == value:
                    v_aux_link[0] = key
                    v_tuple_1 = key
                if v_link[1] == value:
                    v_aux_link[1] = key
                    v_tuple_2 = key
            # print(v_aux_link)
            l_aux_links_two_rddas.append(v_aux_link)
            l_t_aux_links_two_rddas.append((v_tuple_1, v_tuple_2))
        # SHOW THE LIST OF LINKS
        print("FORMAT : KEY INPUT (RDDA INPUT - ATTRACTOR), KEY OUTPUT (RRDA OUTPUT - ATTRACTOR)")
        for v_link in l_aux_links_two_rddas:
            print(v_link)
        print("NUMBER OF LINKS : " + str(len(l_aux_links_two_rddas)))
        print("------------------------------------------------------")

        # print("ADJACENCY MATRIX")
        # print("======================================================")
        # # create a adjacency_matrix from adjacency vector
        # adjacency_matrix = []
        # # create adjacency_matrix with 0 values
        # for v_rows in range(0, len(oRedRddasModel.d_global_rdda_attractor)):
        #     l_aux_row = []
        #     for v_columns in range(0, len(oRedRddasModel.d_global_rdda_attractor)):
        #         l_aux_row.append(0)
        #     adjacency_matrix.append(l_aux_row)
        # # fill the adjacency matrix
        # for v_link in l_aux_links_two_rddas:
        #     adjacency_matrix[v_link[0]][v_link[1]] = 1
        # # print the adjacency matrix
        # # for row in adjacency_matrix:
        # #    print(row)
        # print("MATRIX DIMENSION " + str(len(oRedRddasModel.d_global_rdda_attractor)) + " x " + str(len(oRedRddasModel.d_global_rdda_attractor)))
        # print("------------------------------------------------------")
        #
        # print("ADJACENCY LIST")
        # # generate the adjacency list with items of dictionary,
        # d_adjacent_list = {}
        # for v_key in oRedRddasModel.d_global_rdda_attractor.keys():
        #     d_adjacent_list[v_key] = []
        #     for v_link in l_aux_links_two_rddas:
        #         if v_link[0] == v_key:
        #             d_adjacent_list[v_key].append(v_link[1])
        # # show the adjacency List
        # for v_key, v_values in d_adjacent_list.items():
        #     print(str(v_key) + " : " + str(v_values))
        # print("------------------------------------------------------")

        print("DICTIONARY OF RDDA AND ATTRACTORS")
        # process the paths in the graph of interactions,
        # show the list of rddas and attractors [rdda, attractor]
        for v_key, v_values in o_cbn.d_global_rdda_attractor.items():
            print(str(v_key) + " : " + str(v_values))
        print("------------------------------------------------------")

        print("GROUP THE ITEMS BY SIGNAL ACOPLAMENT")
        # find the coupling signals of the networks
        l_coupling_signals = []
        for oRdda in o_cbn.list_of_rddas:
            for oSignal in oRdda.list_of_signals:
                l_coupling_signals.append([oSignal.rdda_entrada, oSignal.rdda_salida])

        # show the list of signals in list format [rdda_input, rdda_output]
        # for v_signal in l_coupling_signals:
        #     print(v_signal)

        # generate one list of links for every signal
        d_coupling_signal = {}
        for v_signal in l_coupling_signals:
            d_coupling_signal[str(v_signal[0]) + "_" + str(v_signal[1])] = []
            for v_link in o_cbn.l_links_two_rddas:
                if str(v_link[0][0]) + "_" + str(v_link[1][0]) == str(v_signal[0]) + "_" + str(v_signal[1]):
                    d_coupling_signal[str(v_signal[0]) + "_" + str(v_signal[1])].append(v_link)
        # show the adjacency List
        # for v_key, v_values in d_coupling_signal.items():
        #     print(str(v_key) + " : " + str(v_values))
        # print("------------------------------------------------------")

        # ENUMERATE METHOD TO FIND ATTRACTOR FIELDS
        print("BEGIN CALCULATE ATTRACTORS FIELDS")
        rddas_attractors = []
        # print (oRedRddasModel.list_of_rddas)
        for element in range(0, len(o_cbn.list_of_rddas)):
            list_attractor_rdda = []
            for v_key, v_values in o_cbn.d_global_rdda_attractor.items():
                # print(str(v_key) + " : " + str(v_values))
                if v_values[0] == element + 1:
                    list_attractor_rdda.append(v_key)
            rddas_attractors.append(list_attractor_rdda)
        o_cbn.rddas_attractors = rddas_attractors

        # # Attractors by RDDA
        # print("Attractors by RDDA")
        # print(rddas_attractors)
        #
        # # Signals coupling
        # print("Coupling Signals between RDDAs")
        # print(l_coupling_signals)
        #
        # # Pares Compatibles
        # print("Compatible pairs")
        # print(l_aux_links_two_rddas)

        # Generate Groups of pairs by Signal
        print("")
        list_attractors_pairs = []
        group_signals_pairs = []
        for group in l_coupling_signals:
            list_pairs = []
            for pair in l_aux_links_two_rddas:
                if pair[0] in rddas_attractors[group[0] - 1] and pair[1] in rddas_attractors[group[1] - 1]:
                    list_pairs.append(pair)
            group_signals_pairs.append([group, list_pairs])
            list_attractors_pairs = list_attractors_pairs + list_pairs
            # print(list_attractors_pairs)
            print(group, list_pairs)
        o_cbn.group_signals_pairs = group_signals_pairs
        o_cbn.list_attractors_pairs = list_attractors_pairs
        # group_signals_pairs

        # Generate a List of signal pairs
        list_signal_pairs = []
        for group in group_signals_pairs:
            list_signal_pairs.append(group[1])
        print(list_signal_pairs)
        o_cbn.list_signal_pairs = list_signal_pairs

        print("======================================================")
        print("LIST OF UNION BETWEEN TWO RDDAs")
        print("======================================================")
        print("FORMAT : [RDDA , ATTRACTOR] INPUT, [RRDA, ATTRACTOR] OUTPUT, PERMUTATION, VARIABLE INPUT, VARIABLES "
              "OUTPUT SET")
        for v_link in l_links_two_rddas:
            print(v_link)
        print("NUMBER OF LINKS : " + str(len(l_links_two_rddas)))
        print("======================================================")
        return o_cbn

    def show_attractor_pairs(self):
        print("List of Attractor Pairs")
        print("========================")

        for pair in self.list_attractors_pairs:
            print(pair)

        print("========================")
