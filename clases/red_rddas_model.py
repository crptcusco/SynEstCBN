import random  # generate random numbers
from random import randint  # generate random numbers integers
from itertools import product  # generate combinations of numbers
import networkx as nx  # library to work with graphs
import matplotlib.pyplot as plt  # library to make draws
import pickle  # Library to Serialization of object
import json
import xml.etree.ElementTree as ET

from clases.rdda_model import RddaModel
from clases.signal_model import SignalModel
from clases.variable_model import VariableModel


class RedRddasModel(object):
    def __init__(self, number_of_rddas, number_of_variables_rdda, number_of_signals_rdda, number_exit_variables,
                 number_clauses_function):
        self.number_of_rddas = number_of_rddas
        self.number_of_variables_rdda = number_of_variables_rdda
        self.number_of_signals_rdda = number_of_signals_rdda
        self.number_exit_variables = number_exit_variables
        self.number_clauses_function = number_clauses_function
        self.list_of_rddas = []
        # self.generateRDDAs()

    def show(self):
        print("================================================================")
        print("NETWORK RDDA DESCRIPTION")
        print("================================================================")
        print("Number of RDDs : " + str(self.number_of_rddas))
        print("Number of variables by RDD : " + str(self.number_of_variables_rdda))
        print("Number of coupling signals by RDD : " + str(self.number_of_signals_rdda))
        print("Maximum number of exit variables by signal : " + str(self.number_of_rddas))
        print("Maximum number of clauses by function : " + str(self.number_of_rddas))
        print("================================================================")
        for o_rdda in self.list_of_rddas:
            # print(oRdd)
            o_rdda.show()

    def generate_rddas(self, type_network="ALEATORY"):
        # generate the RDDAs variables
        v_contador_variable = 1
        for v_number_of_rdda in range(1, self.number_of_rddas + 1):
            print("RDDA : ", v_number_of_rdda)
            list_of_v_intern = []
            for v_numero_variable in range(v_contador_variable, v_contador_variable + self.number_of_variables_rdda):
                list_of_v_intern.append(v_numero_variable)
                v_contador_variable = v_contador_variable + 1
            print("VARIABLES : ", list_of_v_intern)
            oRddaModel = RddaModel(v_number_of_rdda, list_of_v_intern)
            self.list_of_rddas.append(oRddaModel)

        # generate coupling signals in one auxiliary list
        aux1_list_of_rddas = []
        for oRddaModel in self.list_of_rddas:
            # how many coupling signals will they have
            number_of_signals_rdda = randint(1, self.number_of_signals_rdda)
            # we create a list to choose the neighboring networks
            l_aux_rddas = self.list_of_rddas.copy()
            l_aux_rddas.remove(oRddaModel)
            # select the neighboring network
            l_rdda_co = random.sample(l_aux_rddas, number_of_signals_rdda)
            lista_signals = []
            for v_rdda_co in l_rdda_co:
                # generate the list of coupling variables
                l_variaveis_saida = random.sample(v_rdda_co.list_of_v_intern, self.number_exit_variables)

                # FUTURE JOB!!!
                # generate the coupling function
                # acoplament_function = " & ".join( list(map(str, l_variaveis_saida)))
                # acoplament_function = "|".join( list(map(str, l_variaveis_saida)))

                # We validate if we have one or several output variables
                if (self.number_exit_variables == 1):
                    acoplament_function = l_variaveis_saida[0]
                else:
                    acoplament_function = " ∨ ".join(list(map(str, l_variaveis_saida)))
                # print(acoplament_function)
                # sys.exit()
                # define the maximum number of output variables with professor
                oSignalModel = SignalModel(oRddaModel.number_of_rdda, v_rdda_co.number_of_rdda, l_variaveis_saida,
                                           v_contador_variable, acoplament_function)
                oSignalModel.show()
                lista_signals.append(oSignalModel)
                v_contador_variable = v_contador_variable + 1
            oRddaModel.list_of_signals = lista_signals.copy()
            aux1_list_of_rddas.append(oRddaModel)
        self.list_of_rddas = aux1_list_of_rddas.copy()

        # show the RDDAs with signals and with description
        # for v_rdda in self.list_of_rddas:
        #    v_rdda.show() 

        # GENERATE THE DYNAMICS
        number_max_of_clausules = self.number_clauses_function
        number_max_of_literals = 3
        # we generate an auxiliary list to add the coupling signals
        aux2_lista_of_rddas = []
        for oRddaModel in self.list_of_rddas:
            # Create a list of all RDDAs variables
            l_aux_variables = []
            # Add the variables of the coupling signals
            for signal in oRddaModel.list_of_signals:
                l_aux_variables.append(signal.name_variable)
            # add local variables
            l_aux_variables.extend(oRddaModel.list_of_v_intern)

            # generate the function description of the variables
            description_variables = []
            # generate clauses
            for v_description_variable in oRddaModel.list_of_v_intern:
                l_clausules_node = []
                for v_clausula in range(0, randint(1, number_max_of_clausules)):
                    v_num_variable = randint(1, number_max_of_literals)
                    # randomly select from the signal variables
                    l_literais_variables = random.sample(l_aux_variables, v_num_variable)
                    l_clausules_node.append(l_literais_variables)
                # adding the description of variable in form of object
                oVariableModel = VariableModel(v_description_variable, l_clausules_node)
                description_variables.append(oVariableModel)
                # adding the description in functions of every variable
            # adding the RDDA to list of RDDAs
            oRddaModel.description_variables = description_variables.copy()
            aux2_lista_of_rddas.append(oRddaModel)
            # actualized the list of rddas
        self.list_of_rddas = aux2_lista_of_rddas.copy()

        for rdda in self.list_of_rddas:
            rdda.proccesParameters()
            print("RDDA CREATED")

    @staticmethod
    def save_file_pickle(oRedRddasModel, v_path):
        # oRedRddasModel.show()
        # save information about the Network
        with open(v_path + ".pickle", 'wb') as f:
            # Pickle the 'data' dictionary using the highest protocol available.
            pickle.dump(oRedRddasModel, f, pickle.HIGHEST_PROTOCOL)
        print("file : " + v_path + ".pickle saved")
        # pickle.dump(oRedRddasModel, v_path + ".pickle")

    @staticmethod
    def load_file_pickle(v_path):
        with open(v_path, 'rb') as f:
            # The protocol version used is detected automatically, so we do not
            # have to specify it.
            data = pickle.load(f)
            return data

    @staticmethod
    def saveInFileXML(oRedRddasModel, v_path):
        print("file : " + v_path + "pickle saved")

    @staticmethod
    def saveInFileXML(oRedRddasModel, v_path):
        print("file : " + v_path + "pickle saved")
        # number_of_rddas = ET.Element('number_of_rddas')
        # number_of_variables_rdda = ET.Element('number_of_variables_rdda')
        # number_of_signals_rdda = ET.Element('number_of_signals_rdda')
        # number_exit_variables = ET.Element('number_exit_variables')
        # number_clausules_function = ET.Element('number_clausules_function')
        # list_of_rddas = ET.Element('list_of_rddas')

        # list_of_rddas = ET.SubElement(a, 'b')
        #
        # number_of_rdda = number_of_rdda
        # list_of_v_intern = list_of_v_intern
        # list_of_signals = list_of_signals
        # description_variables = []
        #
        # list_of_v_exterm = []
        # list_of_v_total = []
        # dic_var_cnf = {}
        #
        # number_of_v_intern = 0
        # number_of_v_extern = 0
        # number_of_v_total = 0
        # set_of_attractors = []
        # dic_res_var = {}
        #
        # print("lista de rddas")
        # print(oRedRddasModel.list_of_rddas)

        # a = ET.Element('a')
        # b = ET.SubElement(a, 'b')
        # c = ET.SubElement(a, 'c')
        # d = ET.SubElement(c, 'd')
        # print(ET.dump(a))
        # print("file saved")

    def graph_topology(self, save_graph: bool = False, path_graph="", show_graph: bool = False):

        # Using the Networkx Library
        print("Show the adjacency list in a Graph")
        o_graph = nx.DiGraph()
        for oRDDA in self.list_of_rddas:
            for oSignal in oRDDA.list_of_signals:
                # oSignal.show()
                o_graph.add_edge(oSignal.rdda_entrada, oSignal.rdda_salida)

        # Drawing the graph
        nx.draw_networkx(o_graph, pos=nx.circular_layout(o_graph), with_labels=True, font_weight='normal')
        plt.axis('off')
        if save_graph:
            plt.savefig(path_graph + '_network_model.eps', format='eps')
        if show_graph:
            plt.show()
        print("------------------------------------------------------")

    @staticmethod
    def calculate_attractors_fields(oRedRddasModel, save_graph: bool = False, path_graph="", show_graph: bool = False):
        # FORMAT : [field1 , field2, [[rdda1, attractor],[rdda2, attractor], ...], field 4 , ...]
        # list_of_field_attractors = []

        # New form  to calculate the fields of attractors by the form of the network of RDDAs
        # Process the topology of the network of RDDAs

        print("BEGIN CALCULATE ALL LOCAL ATTRACTORS BY PERMUTATION")
        # CREATE A LIST OF: NETWORKS, PERMUTATION AND ATTRACTORS
        l_rdda_permutation_attractors = []

        # FIND THE ATTRACTORS FOR EACH RDDA
        for oRdda in oRedRddasModel.list_of_rddas:
            # GENERATE THE POSSIBLES COMBINATIONS ACCORDING TO THE COUPLING SIGNALS
            l_permutation = product(list('01'), repeat=len(oRdda.list_of_signals))
            for v_permutation in l_permutation:
                # ADD NETWORK, PERMUTATION AND LIST OF ATTRACTORS TO LIST OF ALL ATTRACTORS BY NETWORK
                # EST [RDDA Object, permutation,[List of attractors]]
                l_rdda_permutation_attractors.append([oRdda, ''.join(v_permutation),
                                                      RddaModel.findLocalAtractorsSATSatispy(oRdda,
                                                                                             ''.join(v_permutation))])
        print("END CALCULATE ALL LOCAL ATTRACTORS")
        print("######################################################")

        # SHOW ATTRACTORS GROUP BY RDDA AND PERMUTATION
        print("ATTRACTORS GROUP BY RDDA AND PERMUTATION")
        for element in l_rdda_permutation_attractors:
            print("RDDA:", element[0].number_of_rdda, " - Signal:", element[1])
            count_attractor_by_rdda = 1
            for attractor in element[2]:
                print("A_" + str(element[0].number_of_rdda) + "_" + str(count_attractor_by_rdda) + ":", attractor)
                count_attractor_by_rdda += 1
                # SUGGESTION : CREATE A MODEL OR LIST OF: RDDA, SIGNAL, ATTRACTOR
        print("######################################################")

        # GROUPS ATTRACTORS BY RDDA WITHOUT PERMUTATIONS
        print("BEGIN GROUP ATTRACTORS BY RDDA")
        l_rdda_attractors = []
        for oRdda in oRedRddasModel.list_of_rddas:
            l_aux_local_attractors = []
            for l_local_permutation_attractors in l_rdda_permutation_attractors:
                if oRdda.number_of_rdda == l_local_permutation_attractors[0].number_of_rdda:
                    l_aux_local_attractors.extend(l_local_permutation_attractors[2])
            # ADD THE ATTRACTORS TO THE LIST
            l_rdda_attractors.append([oRdda, l_aux_local_attractors])
        # print("######################################################")

        # SHOW THE ATTRACTORS BY NETWORK
        print("GROUP ATTRACTORS BY NETWORK")
        for l_network_attractors in l_rdda_attractors:
            # print("######################################################")
            # l_network_attractors[0].show()
            print("LIST OF ATTRACTORS OF RDDA: ", l_network_attractors[0].number_of_rdda)
            count_attractor_by_rdda = 1
            for l_attractor in l_network_attractors[1]:
                print("RDDA:", l_network_attractors[0].number_of_rdda, "- A_" + str(element[0].number_of_rdda) + "_"
                      + str(count_attractor_by_rdda) + ":", l_attractor)
                count_attractor_by_rdda += 1
            print("======================================================")
        print("END GROUP ATTRACTORS BY RDDA")
        print("######################################################")

        # CALCULATING THE LINKS BETWEEN TWO RDDAS
        l_links_two_rddas = []
        l_supported_attractor_pairs =[]
        print("GENERATING THE LINKS BETWEEN TWO RDDAS ")
        print("######################################################")

        # CREATE A GLOBAL DICTIONARY
        d_global_rdda_attractor = {}
        v_cont_dict_global = 0
        print("WALK FOR EVERY GROUP OF ATTRACTORS OF THE PERMUTATION OF RDDA")
        print("======================================================")
        for l_local_permutation_attractors in l_rdda_permutation_attractors:
            print("WALK FOR EVERY ATTRACTOR OF THE PERMUTATION OF RDDA")
            print("======================================================")
            for v_local_attractor in l_local_permutation_attractors[2]:
                # The signal corresponds a one letter of the permutation
                v_cont_letter_permutation = 0
                v_rdda_input = l_local_permutation_attractors[0].number_of_rdda
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

        print("======================================================")
        print("LIST OF UNION BETWEEN TWO RDDAs")
        print("======================================================")
        print("FORMAT : [RDDA , ATTRACTOR] INPUT, [RRDA, ATTRACTOR] OUTPUT, PERMUTATION, VARIABLE INPUT, VARIABLES "
              "OUTPUT SET")
        for v_link in l_links_two_rddas:
            print(v_link)
        print("NUMBER OF LINKS : " + str(len(l_links_two_rddas)))
        print("======================================================")

        print("DATA PREPROCESSING")
        print("======================================================")
        print("LIST OF THE LINK BETWEEN TWO RDDAs WITH DICTIONARY")
        # Replace the RDDA Attractor with the dictionary Key
        l_aux_links_two_rddas = []
        l_t_aux_links_two_rddas = []
        for v_link in l_links_two_rddas:
            # print(v_link)
            # v_aux_link = v_link
            v_aux_link = [0, 0]
            v_tuple_1 = 0
            v_tuple_2 = 0
            for key, value in d_global_rdda_attractor.items():
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

        print("ADJACENCY MATRIX")
        print("======================================================")
        # create a adjacency_matrix from adjacency vector
        adjacency_matrix = []
        # create adjacency_matrix with 0 values
        for v_rows in range(0, len(d_global_rdda_attractor)):
            l_aux_row = []
            for v_columns in range(0, len(d_global_rdda_attractor)):
                l_aux_row.append(0)
            adjacency_matrix.append(l_aux_row)
        # fill the adjacency matrix
        for v_link in l_aux_links_two_rddas:
            adjacency_matrix[v_link[0]][v_link[1]] = 1
        # print the adjacency matrix
        # for row in adjacency_matrix:
        #    print(row)
        print("MATRIX DIMENSION " + str(len(d_global_rdda_attractor)) + " x " + str(len(d_global_rdda_attractor)))
        print("------------------------------------------------------")

        print("ADJACENCY LIST")
        # generate the adjacency list with items of dictionary,
        d_adjacent_list = {}
        for v_key in d_global_rdda_attractor.keys():
            d_adjacent_list[v_key] = []
            for v_link in l_aux_links_two_rddas:
                if v_link[0] == v_key:
                    d_adjacent_list[v_key].append(v_link[1])
        # show the adjacency List
        for v_key, v_values in d_adjacent_list.items():
            print(str(v_key) + " : " + str(v_values))
        print("------------------------------------------------------")

        print("DICTIONARY OF RDDA AND ATTRACTORS")
        # process the paths in the graph of interactions,
        # show the list of rddas and attractors [rdda, attractor]
        for v_key, v_values in d_global_rdda_attractor.items():
            print(str(v_key) + " : " + str(v_values))
        print("------------------------------------------------------")

        print("GROUP THE ITEMS BY SIGNAL ACOPLAMENT")
        # find the coupling signals of the networks
        l_coupling_signals = []
        for oRdda in oRedRddasModel.list_of_rddas:
            for oSignal in oRdda.list_of_signals:
                l_coupling_signals.append([oSignal.rdda_entrada, oSignal.rdda_salida])

        # show the list of signals in list format [rdda_input, rdda_output]
        for v_signal in l_coupling_signals:
            print(v_signal)

            # generate one list of links for every signal
        d_coupling_signal = {}
        for v_signal in l_coupling_signals:
            d_coupling_signal[str(v_signal[0]) + "_" + str(v_signal[1])] = []
            for v_link in l_links_two_rddas:
                if str(v_link[0][0]) + "_" + str(v_link[1][0]) == str(v_signal[0]) + "_" + str(v_signal[1]):
                    d_coupling_signal[str(v_signal[0]) + "_" + str(v_signal[1])].append(v_link)
        # show the adjacency List
        for v_key, v_values in d_coupling_signal.items():
            print(str(v_key) + " : " + str(v_values))
        print("------------------------------------------------------")

        # print("Show the adjacency list in a Graph")
        # # Using the Networkx Library
        # oGraph = nx.DiGraph()
        # for v_key, v_values in d_adjacent_list.items():
        #     print(str(v_key) + " : " + str(v_values))
        #     for v_attractor in d_adjacent_list[v_key]:
        #         oGraph.add_edge(v_key, v_attractor)
        #
        # # Drawing the graph
        # nx.draw_networkx(oGraph, pos=nx.spring_layout(oGraph), with_labels=True, font_weight='normal')
        # plt.axis('off')
        # if save_graph:
        #     plt.savefig(path_graph + 'adjacency_graph.eps', format='eps')
        # plt.show()
        # # if (save_graph):
        # #    plt.savefig(path_graph + 'adjacency_graph.eps', format='eps')
        # print("------------------------------------------------------")

        print("BEGIN CALCULATE ATTRACTORS FIELDS")
        # PRINT THE LIST OF ATTRACTORS FIELDS

        #         print("FIND FIELDS OF ATTRACTORS BY EXHAUSTIVE METHOD")
        #         #exahustive method to fin the attractors field
        #         #List of paths
        #         l_path_attractors = []
        #         for v_signal, l_links in d_acoplament_signal.items():
        #             print("SIGNAL: " +  v_signal)
        #             #print(l_links)
        #             for v_link in l_links:
        #                 #save the rdda who is visited
        #                 l_rdda_visited = []
        #                 v_path = []
        #                 v_rdda_begin = v_signal.split("_")[0]
        #                 v_rdda_end = v_signal.split("_")[1]
        #                 print("added link")
        #                 #print(v_link)
        #                 v_path.append(v_link)
        #                 #add the already rddas visited
        #                 l_rdda_visited.append(v_rdda_begin)
        #                 l_rdda_visited.append(v_rdda_end)
        #                 for v_in_signal, l_in_links in d_acoplament_signal.items():
        #                     v_rdda_in_begin = v_in_signal.split("_")[0]
        #                     v_rdda_in_end = v_in_signal.split("_")[1]
        #                     for v_in_link in l_in_links:
        #                         if v_rdda_end != v_rdda_in_begin:
        #                             continue
        #                         else:
        #                             if v_rdda_in_end in l_rdda_visited:
        #                                 continue
        #                             else:
        #                                 v_path.append(v_in_link)
        #                                 v_rdda_begin = v_rdda_in_begin
        #                                 v_rdda_end = v_rdda_in_end
        #                                 l_rdda_visited.append(v_rdda_begin)
        #                                 l_rdda_visited.append(v_rdda_end)
        #                 #add the path to the list of paths
        #                 l_path_attractors.append(v_path)
        #                 print(v_path)
        #         print("------------------------------------------------------")

        #         #trying with the simply method
        #         l_atractor_fields = []
        #         #listar todos los atractores
        #         for v_key,v_values in d_global_rdda_attractor.items():
        #             print(str(v_key) + " : " + str(v_values))
        #             print(d_adjancency_list[v_key])
        #             for v_cont_rddas in range(self.rdda):
        #                 for v_attractor in d_adjancency_list[v_key] :
        #                     print(v_attractor)
        #                     print(d_global_rdda_attractor[v_attractor])

        #         #dictionary of pairs compativel attractors
        #         for v_signal, l_links in d_acoplament_signal.items():
        #             print("SIGNAL: " +  v_signal)
        #             print(l_links)
        #             for v_link in l_links:
        #                 print(v_link)

        # Drawing the grapph diferent layouts
        # nx.draw(oGraph, with_labels=True, font_weight='bold')
        # plt.show()
        # nx.draw_circular(oGraph, with_labels=True, font_weight='bold')
        # plt.show()
        # nx.draw_kamada_kawai(oGraph, with_labels=True, font_weight='bold')
        # plt.show()
        # nx.draw_planar(oGraph, with_labels=True, font_weight='bold')
        # plt.show()
        # nx.draw_random(oGraph, with_labels=True, font_weight='bold')
        # plt.show()
        # nx.draw_spectral(oGraph, with_labels=True, font_weight='bold')
        # plt.show()
        # nx.draw_spring(oGraph, with_labels=True, font_weight='bold')
        # plt.show()
        # nx.draw_shell(oGraph, with_labels=True, font_weight='bold')
        # plt.show()

        # find all the path betwen two vertices
        # for path in nx.all_simple_paths(oGraph, source=0, target=3):
        #    print(path)

        # return list_of_field_attractors
        print("END CALCULATE ATTRACTORS FIELDS")
        print("######################################################")
