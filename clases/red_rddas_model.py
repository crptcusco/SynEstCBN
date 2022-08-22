import random  # generate random numbers
import networkx as nx  # library to work with graphs
import igraph as ig
import matplotlib.pyplot as plt  # library to make draws
import matplotlib.colors as mco # library who have the list of colors
import pickle  # library to serialization object
import ray # Library to parallelization, distribution and scalability

# import json # library to serialization object
# import xml.etree.ElementTree as ET # library to serialization object
# from igraph.drawing import cairo
# from igraph import *  # library to make network graphs

from random import randint  # generate random numbers integers
from itertools import product  # generate combinations of numbers

from clases.rdda_model import RddaModel
from clases.signal_model import SignalModel
from clases.variable_model import VariableModel


class RedRddasModel(object):
    def __init__(self, number_of_rddas, number_of_variables_rdda, number_of_signals_rdda, number_exit_variables,
                 number_clauses_function):
        self.number_of_rddas = number_of_rddas # number of rdds
        self.number_of_variables_rdda = number_of_variables_rdda # number of variables for each rdd
        self.number_of_signals_rdda = number_of_signals_rdda # number of signals who have each rdd
        self.number_exit_variables = number_exit_variables # number of exit variables in the set of exit
        self.number_clauses_function = number_clauses_function # number of clauses for each transition function
        self.list_of_rddas = [] # List of th object of each RDD
        self.l_rdda_permutation_attractors = [] # List who join RDD - Permutation - Attractors
        self.rddas_attractors = [] # List of attractors in form of key, Without RDD
        self.list_attractors_pairs = [] # List of attractors pairs in only one list without RDD
        self.group_signals_pairs = [] # List of attractors pairs group by relations between RDDs
        self.list_signal_pairs = [] # List of signal pairs group by relations,but without labels
        self.d_global_rdda_attractor = {} # Dictionary for each attractor with his RDD
        self.attractor_fields = [] # The List of attractor fields in format of pair attractors
        # self.generateRDDAs()

        # Dictionary of RDD as key and Color as value
        self.d_rdd_color = {}
        # List of color for the graphics
        self.rdd_color_dict = {}
        list_colors = list(mco.CSS4_COLORS.keys())
        random.shuffle(list_colors)
        for i, color in enumerate(list_colors):
            self.rdd_color_dict[i] = color

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
        # Print the list of RDDs
        # for o_rdda in self.list_of_rddas:
        #     o_rdda.show()

    def generate_rddas(self, type_network="ALEATORY"):
        # generate the RDDAs variables
        v_cont_variable = 1
        for v_number_of_rdda in range(1, self.number_of_rddas + 1):
            list_of_v_intern = []
            for v_number_variable in range(v_cont_variable, v_cont_variable + self.number_of_variables_rdda):
                list_of_v_intern.append(v_number_variable)
                v_cont_variable = v_cont_variable + 1
            # print("VARIABLES : ", list_of_v_intern)
            oRddaModel = RddaModel(v_number_of_rdda, list_of_v_intern)
            self.list_of_rddas.append(oRddaModel)

        # generate coupling signals in one auxiliary list
        aux1_list_of_rddas = []
        for oRddaModel in self.list_of_rddas:
            # how many coupling signals will they have RANDOM
            # number_of_signals_rdda = randint(1, self.number_of_signals_rdda)
            # Fixed number of coupling signals, fixed in 2
            number_of_signals_rdda = self.number_of_signals_rdda
            # we create a list to choose the neighboring networks
            l_aux_rddas = self.list_of_rddas.copy()
            l_aux_rddas.remove(oRddaModel)
            # select the neighboring network
            l_rdda_co = random.sample(l_aux_rddas, number_of_signals_rdda)
            lista_signals = []
            for v_rdda_co in l_rdda_co:
                # generate the list of coupling variables
                l_output_variables = random.sample(v_rdda_co.list_of_v_intern, self.number_exit_variables)

                # FUTURE JOB!!!
                # generate the coupling function
                # coupling_function = " & ".join( list(map(str, l_output_variables)))
                # coupling_function = "|".join( list(map(str, l_output_variables)))

                # We validate if we have one or several output variables
                if self.number_exit_variables == 1:
                    coupling_function = l_output_variables[0]
                else:
                    coupling_function = " " +" ∨ ".join(list(map(str, l_output_variables))) + " "
                o_signal_model = SignalModel(oRddaModel.number_of_rdda, v_rdda_co.number_of_rdda, l_output_variables,
                                             v_cont_variable, coupling_function)
                lista_signals.append(o_signal_model)
                v_cont_variable = v_cont_variable + 1
            oRddaModel.list_of_signals = lista_signals.copy()
            aux1_list_of_rddas.append(oRddaModel)
        self.list_of_rddas = aux1_list_of_rddas.copy()

        # show the RDDAs with signals and with description
        # for v_rdda in self.list_of_rddas:
        #    v_rdda.show() 

        # GENERATE THE DYNAMICS OF EACH RDD
        number_max_of_clauses = self.number_clauses_function
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
                l_clauses_node = []
                for v_clause in range(0, randint(1, number_max_of_clauses)):
                    v_num_variable = randint(1, number_max_of_literals)
                    # randomly select from the signal variables
                    l_literals_variables = random.sample(l_aux_variables, v_num_variable)
                    l_clauses_node.append(l_literals_variables)
                # adding the description of variable in form of object
                o_variable_model = VariableModel(v_description_variable, l_clauses_node)
                description_variables.append(o_variable_model)
                # adding the description in functions of every variable
            # adding the RDDA to list of RDDAs
            oRddaModel.description_variables = description_variables.copy()
            aux2_lista_of_rddas.append(oRddaModel)
            # actualized the list of rddas
        self.list_of_rddas = aux2_lista_of_rddas.copy()

        for rdda in self.list_of_rddas:
            rdda.process_parameters()
            # print("RDDA CREATED")

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

    # Graph the topology of the RDDA using Networkx library
    def graph_topology_networkx(self, save_graph: bool = False, show_graph: bool = False, path_graph=""):
        # Using the Networkx Library
        o_graph = nx.DiGraph()
        for oRDDA in self.list_of_rddas:
            for oSignal in oRDDA.list_of_signals:
                # oSignal.show()
                o_graph.add_edge(oSignal.rdda_entrada, oSignal.rdda_salida)

        # Drawing the graph
        options = {
            # Some configurations
            # 'node_color': ['blue', 'red', 'green'],
            # "node_color": "black",
            # 'width': 5,

            # BASIC CONFIGURATION
            'node_size': 500,
            'pos': nx.kamada_kawai_layout(o_graph),
            'with_labels': True,
            'font_weight': 'bold',
            'connectionstyle': 'arc3,rad=0.4',

            # HIGH CONTRAST
            # "font_size": 36,
            # "node_size": 3000,
            # "node_color": "white",
            # "edgecolors": "black",
            # "linewidths": 5,
            # "width": 5,
        }
        # nx.draw_networkx(o_graph, pos=nx.kamada_kawai_layout(o_graph), with_labels=True, font_weight='bold',
        # connectionstyle="arc3,rad=0.4")
        nx.draw_networkx(o_graph, **options)

        plt.axis('off')
        if save_graph:
            plt.savefig(path_graph + '_network_model.eps', format='eps')
        if show_graph:
            plt.show()

    # Graph the topology of the RDDA using igraph library
    def graph_topology_igraph(self, save_graph: bool = False, show_graph: bool = False, path_graph=""):
        # Using the Igraph Library
        # import igraph as ig
        # import matplotlib.pyplot as plt
        # path_graph = "oso2.eps"

        print("Show the Topology Graph of the RDDA")
        # Show the Topology of the RDDA
        o_graph = ig.Graph(directed=True)
        o_graph.as_directed()

        # fill the vertices
        o_graph.add_vertices(list(range(0, self.number_of_rddas)))

        # fill the edges
        list_edges = []
        for o_rdd in self.list_of_rddas:
            for oSignal in o_rdd.list_of_signals:
                list_edges.append((oSignal.rdda_entrada - 1, oSignal.rdda_salida - 1))
                # oSignal.show()

        o_graph.add_edges(list_edges)
        o_graph.degree(mode="in")

        # Add the labels
        o_graph.vs["rdd"] = range(1, self.number_of_rddas + 1)

        # # Add color for the vertices by rdd
        # list_rdda_by_attractor = []
        # for v_key, v_value in self.d_global_rdda_attractor.items():
        #     list_rdda_by_attractor.append(v_value[0])
        # o_graph.vs["rdd"] = list_rdda_by_attractor

        # fill the dictionary rdd - color
        o_graph.vs["color"] = [self.rdd_color_dict[rdd] for rdd in o_graph.vs["rdd"]]
        # o_graph.vs["color"] = [color_dict[gender] for gender in g.vs["gender"]]

        # Show the Graph
        layout = o_graph.layout("kk")
        visual_style = {}
        visual_style["vertex_color"] = o_graph.vs["color"]
        # visual_style["vertex_color"] = ["blue", "red", "green"]
        # visual_style["vertex_color"] = "black"
        # visual_style["margin"] =[70, 70, 70, 70]
        # visual_style["bbox"]=(0, 0, 1500, 1500)
        visual_style["vertex_size"] = 20
        # visual_style["vertex_color"] = "#1f78b4"
        visual_style["vertex_label"] = o_graph.vs["rdd"]
        visual_style["vertex_label_color"] = "white"
        visual_style["layout"] = layout

        # plot with MatplotLib
        fig, ax = plt.subplots(dpi=100)
        ig.plot(o_graph, target=ax, **visual_style)
        ax.set_xlim(*(-1.5, 1.5))
        ax.set_ylim(*(-1.5, 1.5))
        ax.axis('off')
        # options to generate graph with matplotlib
        if path_graph != "":
            plt.savefig(path_graph)

    # Generate the Graph of attractor pairs of the RDDA
    def graph_attractor_pairs(self,export_graph: bool = False, path=""):
        o_graph = ig.Graph(directed=True)
        o_graph.as_directed()

        # fill the vertices
        o_graph.add_vertices(list(range(0, len(self.d_global_rdda_attractor))))

        # fill the edges
        list_edges = []
        for pair_list in self.list_signal_pairs:
            list_edges.extend(pair_list)
        o_graph.add_edges(list_edges)
        o_graph.degree(mode="in")

        # for key,value in oRedRddasModel.d_global_rdda_attractor.items():
        #     print(key,":", value)
        # print(o_graph)
        # print(oRedRddasModel.d_global_rdda_attractor)

        # # Add the labels
        o_graph.vs["attractor"] = range(0, len(self.d_global_rdda_attractor))

        # Add color for the vertices by rdd
        list_rdda_by_attractor = []
        for v_key, v_value in self.d_global_rdda_attractor.items():
            list_rdda_by_attractor.append(v_value[0])
        o_graph.vs["rdd"] = list_rdda_by_attractor
        # fill the dictionary rdd - color
        o_graph.vs["color"] = [self.rdd_color_dict[rdd] for rdd in o_graph.vs["rdd"]]
        # o_graph.vs["color"] = [color_dict[gender] for gender in g.vs["gender"]]

        # Show the Graph
        layout = o_graph.layout("kk")
        visual_style = {}
        visual_style["vertex_color"] = o_graph.vs["color"]
        # visual_style["vertex_color"] = "black"
        # visual_style["margin"] =[70, 70, 70, 70]
        # visual_style["bbox"]=(0, 0, 1500, 1500)
        visual_style["vertex_size"] = 20
        # visual_style["vertex_color"] = "#1f78b4"
        visual_style["vertex_label"] = o_graph.vs["attractor"]
        visual_style["vertex_label_color"] = "white"
        visual_style["layout"] = layout

        # plot with MatplotLib
        fig, ax = plt.subplots(dpi=200)
        ig.plot(o_graph, target=ax, **visual_style)
        # ax.set_xlim(*(-1.5, 1.5))
        # ax.set_ylim(*(-1.5, 1.5))
        ax.axis('off')
        # options to generate graph with matplotlib
        # if path_graph != "":
        #     plt.savefig(path_graph)

        list_formats = [ "adjacency",  "edgelist", "graphviz", "gml", "graphml", "graphmlz", "pickle"]
        # "lgl", "dl", "dimacs", "pajet", "leda", "ncol" format not work
        if export_graph:
            for v_format in list_formats:
                o_graph.save(path + "_file." + v_format ,format=v_format)

    def graph_attractor_fields(self):
        for attractor_field in self.attractor_fields:
            # Create Graph for every attractor_field
            o_graph = ig.Graph(directed="True")
            o_graph.as_directed()
            # fill the vertices

            unique_attractors = []
            for element in attractor_field:
                if element[0] not in unique_attractors:
                    unique_attractors.append(element[0])
                if element[1] not in unique_attractors:
                    unique_attractors.append(element[1])

            # fill the vertices
            o_graph.add_vertices(list(range(0, len(unique_attractors))))
            # fill the edges
            list_edges = []
            dict_vertices = {}
            # generate the dictionary of vertices
            cont_vertices = 0
            for element in unique_attractors:
                dict_vertices[element] = cont_vertices
                cont_vertices += 1

            for attractor_pair in attractor_field:
                # print(attractor_pair)
                list_edges.append((dict_vertices[attractor_pair[0]], dict_vertices[attractor_pair[1]]))

            o_graph.add_edges(list_edges)
            # Select the in-degree
            o_graph.degree(mode="in")

            # Add RDD by attractor
            # find the rdda by attractor
            list_rdda_by_attractor = []
            for attractor in unique_attractors:
                list_rdda_by_attractor.append(self.d_global_rdda_attractor[attractor][0])
            o_graph.vs["rdd"] = list_rdda_by_attractor

            # Add the labels
            o_graph.vs["attractor"] = unique_attractors
            # fill the dictionary rdd - color
            o_graph.vs["color"] = [self.rdd_color_dict[rdd] for rdd in o_graph.vs["rdd"]]
            # o_graph.vs["color"] = [color_dict[gender] for gender in g.vs["gender"]]

            # Show the Graph
            layout = o_graph.layout("kk")
            visual_style = {}
            visual_style["vertex_color"] = o_graph.vs["color"]
            visual_style["vertex_size"] = 20
            visual_style["vertex_label"] = o_graph.vs["attractor"]
            visual_style["vertex_label_color"] = "white"
            visual_style["title"] = str(attractor_field)
            visual_style["layout"] = layout

            # plot with MatplotLib
            fig, ax = plt.subplots(dpi=100)
            ig.plot(o_graph, target=ax, **visual_style)
            ax.set_xlim(*(-1.5, 1.5))
            ax.set_ylim(*(-1.5, 1.5))
            ax.axis('off')
            # save graph with matplotlib
            # if path_graph != "":
            #     plt.savefig(path_graph)

    def show_detail_attractor_fields(self):
        v_count_fields = 1
        for attractor_field in self.attractor_fields:
            print("Attractor Field", v_count_fields)
            unique_attractors = []
            for element in attractor_field:
                if element[0] not in unique_attractors:
                    unique_attractors.append(element[0])
                if element[1] not in unique_attractors:
                    unique_attractors.append(element[1])
            v_count_fields = v_count_fields + 1
            for attractor_index in unique_attractors:
                print("Index:", attractor_index, "- RDD:", self.d_global_rdda_attractor[attractor_index][0],
                      "- Attractor:", self.d_global_rdda_attractor[attractor_index][1])

    def find_attractors_rddas(oRedRddasModel):
        print("BEGIN CALCULATE ALL LOCAL ATTRACTORS BY PERMUTATION")
        # CREATE A LIST OF: NETWORKS, PERMUTATION AND ATTRACTORS

        # FIND THE ATTRACTORS FOR EACH RDDA
        for oRdda in oRedRddasModel.list_of_rddas:
            # GENERATE THE POSSIBLES COMBINATIONS ACCORDING TO THE COUPLING SIGNALS
            l_permutation = product(list('01'), repeat=len(oRdda.list_of_signals))
            for v_permutation in l_permutation:
                # ADD NETWORK, PERMUTATION AND LIST OF ATTRACTORS TO LIST OF ALL ATTRACTORS BY NETWORK
                # EST [RDDA Object, permutation,[List of attractors]]
                oRedRddasModel.l_rdda_permutation_attractors.append([oRdda, ''.join(v_permutation),RddaModel.findLocalAtractorsSATSatispy(oRdda,''.join(v_permutation))])
        print("END CALCULATE ALL LOCAL ATTRACTORS")
        print("######################################################")
        return oRedRddasModel

    @staticmethod
    @ray.remote
    def find_attractors_rddas_ray(oRedRddasModel):
        print("BEGIN CALCULATE ALL LOCAL ATTRACTORS BY PERMUTATION")
        # CREATE A LIST OF: NETWORKS, PERMUTATION AND ATTRACTORS

        # FIND THE ATTRACTORS FOR EACH RDDA
        for oRdda in oRedRddasModel.list_of_rddas:
            # GENERATE THE POSSIBLES COMBINATIONS ACCORDING TO THE COUPLING SIGNALS
            l_permutation = product(list('01'), repeat=len(oRdda.list_of_signals))
            for v_permutation in l_permutation:
                # ADD NETWORK, PERMUTATION AND LIST OF ATTRACTORS TO LIST OF ALL ATTRACTORS BY NETWORK
                # EST [RDDA Object, permutation,[List of attractors]]
                result = RddaModel.findLocalAtractorsSATSatispy_ray.remote(oRdda,''.join(v_permutation))
                oRedRddasModel.l_rdda_permutation_attractors.append([oRdda, ''.join(v_permutation), ray.get(result)])
        print("END CALCULATE ALL LOCAL ATTRACTORS")
        print("######################################################")
        return oRedRddasModel

    @staticmethod
    @ray.remote
    def calculation_compatible_pairs(oRedRddasModel):
        # SHOW ATTRACTORS GROUP BY RDDA AND PERMUTATION
        print("ATTRACTORS GROUP BY RDDA AND PERMUTATION")
        for element in oRedRddasModel.l_rdda_permutation_attractors:
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
            for l_local_permutation_attractors in oRedRddasModel.l_rdda_permutation_attractors:
                if oRdda.number_of_rdda == l_local_permutation_attractors[0].number_of_rdda:
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
        for l_local_permutation_attractors in oRedRddasModel.l_rdda_permutation_attractors:
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
        oRedRddasModel.d_global_rdda_attractor = d_global_rdda_attractor
        oRedRddasModel.l_links_two_rddas = l_links_two_rddas

        print("DATA PREPROCESSING")
        print("======================================================")
        print("LIST OF THE LINK BETWEEN TWO RDDAs WITH DICTIONARY")
        # Replace the RDDA Attractor with the dictionary Key
        l_aux_links_two_rddas = []
        l_t_aux_links_two_rddas = []
        for v_link in oRedRddasModel.l_links_two_rddas:
            # print(v_link)
            # v_aux_link = v_link
            v_aux_link = [0, 0]
            v_tuple_1 = 0
            v_tuple_2 = 0
            for key, value in oRedRddasModel.d_global_rdda_attractor.items():
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
        for v_key, v_values in oRedRddasModel.d_global_rdda_attractor.items():
            print(str(v_key) + " : " + str(v_values))
        print("------------------------------------------------------")

        print("GROUP THE ITEMS BY SIGNAL ACOPLAMENT")
        # find the coupling signals of the networks
        l_coupling_signals = []
        for oRdda in oRedRddasModel.list_of_rddas:
            for oSignal in oRdda.list_of_signals:
                l_coupling_signals.append([oSignal.rdda_entrada, oSignal.rdda_salida])

        # show the list of signals in list format [rdda_input, rdda_output]
        # for v_signal in l_coupling_signals:
        #     print(v_signal)

        # generate one list of links for every signal
        d_coupling_signal = {}
        for v_signal in l_coupling_signals:
            d_coupling_signal[str(v_signal[0]) + "_" + str(v_signal[1])] = []
            for v_link in oRedRddasModel.l_links_two_rddas :
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
        for element in range(0, len(oRedRddasModel.list_of_rddas)):
            list_attractor_rdda = []
            for v_key, v_values in oRedRddasModel.d_global_rdda_attractor.items():
                # print(str(v_key) + " : " + str(v_values))
                if v_values[0] == element + 1:
                    list_attractor_rdda.append(v_key)
            rddas_attractors.append(list_attractor_rdda)
        oRedRddasModel.rddas_attractors = rddas_attractors

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
        oRedRddasModel.group_signals_pairs = group_signals_pairs
        oRedRddasModel.list_attractors_pairs = list_attractors_pairs
        # group_signals_pairs

        # Generate a List of signal pairs
        list_signal_pairs = []
        for group in group_signals_pairs:
            list_signal_pairs.append(group[1])
        print(list_signal_pairs)
        oRedRddasModel.list_signal_pairs = list_signal_pairs

        print("======================================================")
        print("LIST OF UNION BETWEEN TWO RDDAs")
        print("======================================================")
        print("FORMAT : [RDDA , ATTRACTOR] INPUT, [RRDA, ATTRACTOR] OUTPUT, PERMUTATION, VARIABLE INPUT, VARIABLES "
              "OUTPUT SET")
        for v_link in l_links_two_rddas:
            print(v_link)
        print("NUMBER OF LINKS : " + str(len(l_links_two_rddas)))
        print("======================================================")
        return oRedRddasModel

    @staticmethod
    @ray.remote
    def assembly_attractor_fields_iterative(oRedRddasModel):
        # return the rdda of each attractor of the pair
        def netMapping(pair):
            elements = list()
            for i in range(2):
                for net, rddas_attractor in enumerate(oRedRddasModel.rddas_attractors):
                    check_net = pair[i] in rddas_attractor
                    if check_net:
                        break
                elements.append(net + 1)
            return elements

        # validate if one candidate_field have the same attractor by rdda
        def is_valid(candidate_field):
            res = True
            rdda_dict = {}
            for pair in candidate_field:
                elements = netMapping(pair)
                if not (elements[0] in rdda_dict):
                    rdda_dict[elements[0]] = pair[0]
                else:
                    if not rdda_dict[elements[0]] == pair[0]:
                        return False
                if not (elements[1] in rdda_dict):
                    rdda_dict[elements[1]] = pair[1]
                else:
                    if not rdda_dict[elements[1]] == pair[1]:
                        return False
            return res

        # Calculate the number of combinations
        cont_combinations = 1
        for o_signal in oRedRddasModel.list_signal_pairs:
            cont_combinations = cont_combinations * len(o_signal)
        print("Number of combinations :", cont_combinations)

        # # Show Signals coupling to compare with the valid attractor fields
        # print("Coupling Signals between RDDAs")
        # print(l_coupling_signals)

        # Calculate Valid Fields
        print("Valid Attractors Fields")
        oRedRddasModel.attractor_fields = []
        # Cartesian product
        for field in product(*oRedRddasModel.list_signal_pairs):
            # print(element)
            if is_valid(field):
                oRedRddasModel.attractor_fields.append(field)
                print(field)
        print("Number of valid Attractor Fields: " + str(len(oRedRddasModel.attractor_fields)))

        print("END CALCULATE ATTRACTORS FIELDS")
        print("######################################################")
        return oRedRddasModel

    @staticmethod
    @ray.remote
    def assembly_attractor_fields_optimized(oRedRddasModel):
        # FORMAT : [field1 , field2, [[rdda1, attractor],[rdda2, attractor], ...], field 4 , ...]
        # list_of_field_attractors = []

        # New form  to calculate the fields of attractors by the form of the network of RDDAs
        # Process the topology of the network of RDDAs

        # Order the initial List of pairs attractors
        def f_order_groups(header):
            def f_inspect_group(l_base, v_group):
                for aux_par in l_base:
                    if aux_par[0] == v_group[0] or aux_par[0] == v_group[1]:
                        return True
                    elif aux_par[1] == v_group[1] or aux_par[1] == v_group[0]:
                        return True
                return False

            # Order the groups of compatible pairs
            l_base = [header[0]]
            aux_l_rest_groups = header[1:]
            for v_group in aux_l_rest_groups:
                if f_inspect_group(l_base, v_group):
                    l_base.append(v_group)
                else:
                    aux_l_rest_groups.remove(v_group)
                    aux_l_rest_groups.append(v_group)
            header = [header[0]] + aux_l_rest_groups
            return header

        Array = oRedRddasModel.group_signals_pairs
        Header = [elm[0] for elm in Array]
        Dict = {f'{elm[0]}': elm[1] for elm in Array}
        List = [[key, Dict[f'{key}']] for key in f_order_groups(Header)]
        oRedRddasModel.group_signals_pairs = List
        # Fill the list_signal_pairs with the order List
        oRedRddasModel.list_signal_pairs = []
        for l_element in List:
            oRedRddasModel.list_signal_pairs.append(l_element[1])
        oRedRddasModel.list_signal_pairs

        # Function Cartessian Product Modified
        # return the rdda of each attractor of the pair
        def f_netMapping(pair):
            elements = list()
            for i in range(2):
                for net, rddas_attractor in enumerate(oRedRddasModel.rddas_attractors):
                    check_net = pair[i] in rddas_attractor
                    if check_net:
                        break
                elements.append(net + 1)
            return elements

        # validate if one candidate_field have the same attractor by rdda
        def f_is_valid(candidate_field):
            res = True
            rdd_dict = {}
            for pair in candidate_field:
                elements = f_netMapping(pair)
                if not (elements[0] in rdd_dict):
                    rdd_dict[elements[0]] = pair[0]
                else:
                    if not rdd_dict[elements[0]] == pair[0]:
                        return False
                if not (elements[1] in rdd_dict):
                    rdd_dict[elements[1]] = pair[1]
                else:
                    if not rdd_dict[elements[1]] == pair[1]:
                        return False
            return res

        # Evaluate if the elements of pair was be in the base
        def f_evaluate_pair(l_base, v_pair):
            # generate one dictionary to evaluate if already rdd was see
            for aux_par in l_base:
                if aux_par[0] == v_pair[0] or aux_par[0] == v_pair[1]:
                    return True
                elif aux_par[1] == v_pair[1] or aux_par[1] == v_pair[0]:
                    return True
            return False

        def f_cartesian_product(l_base, list_a):
            l_res = []
            for v_element_base in l_base:
                l_line = []
                for v_element_a in list_a:
                    if type(v_element_base[0]) is list:
                        if f_evaluate_pair(v_element_base, v_element_a):
                            l_line = v_element_base + [v_element_a]
                            if f_is_valid(l_line):
                                l_res.append(l_line)
                    else:
                        if f_evaluate_pair([v_element_base], v_element_a):
                            l_line = [v_element_base] + [v_element_a]
                            if f_is_valid(l_line):
                                l_res.append(l_line)
            return l_res

        # l_total = [list(range(1,6)),list(range(6,11)),list(range(11,16)),list(range(16,21)),list(range(21,26))]
        l_total = oRedRddasModel.list_signal_pairs
        l_cartesian_product = l_total[0]
        v_cont = 1
        while v_cont < len(l_total):
            l_cartesian_product = f_cartesian_product(l_cartesian_product, l_total[v_cont])
            # print("Cartesian")
            # print(l_cartesian_product)
            v_cont = v_cont + 1

        print("OUTPUT", len(l_cartesian_product))
        # Print the elements of cartesian product
        # for v_element in l_cartesian_product:
        #     print(v_element)

        oRedRddasModel.attractor_fields = l_cartesian_product
        # print(oRedRddasModel.attractor_fields)
        return oRedRddasModel

    def assembly_attractor_fields_tree(self):
        # Order the initial List of pairs attractors
        def f_order_groups(header):
            def f_inspect_group(l_base, v_group):
                for aux_par in l_base:
                    if aux_par[0] == v_group[0] or aux_par[0] == v_group[1]:
                        return True
                    elif aux_par[1] == v_group[1] or aux_par[1] == v_group[0]:
                        return True
                return False

            # Order the groups of compatible pairs
            l_base = [header[0]]
            aux_l_rest_groups = header[1:]
            for v_group in aux_l_rest_groups:
                if f_inspect_group(l_base, v_group):
                    l_base.append(v_group)
                else:
                    aux_l_rest_groups.remove(v_group)
                    aux_l_rest_groups.append(v_group)
            header = [header[0]] + aux_l_rest_groups
            return header

        Array = self.group_signals_pairs
        Header = [elm[0] for elm in Array]
        Dict = {f'{elm[0]}': elm[1] for elm in Array}
        List = [[key, Dict[f'{key}']] for key in f_order_groups(Header)]
        self.group_signals_pairs = List
        # Fill the list_signal_pairs with the order List
        self.list_signal_pairs = []
        for l_element in List:
            self.list_signal_pairs.append(l_element[1])
        self.list_signal_pairs

        # Function Cartessian Product Modified
        # return the rdda of each attractor of the pair
        def f_netMapping(pair):
            elements = list()
            for i in range(2):
                for net, rddas_attractor in enumerate(self.rddas_attractors):
                    check_net = pair[i] in rddas_attractor
                    if check_net:
                        break
                elements.append(net + 1)
            return elements

        # validate if one candidate_field have the same attractor by rdda
        def f_is_valid(candidate_field):
            res = True
            rdd_dict = {}
            for pair in candidate_field:
                elements = f_netMapping(pair)
                if not (elements[0] in rdd_dict):
                    rdd_dict[elements[0]] = pair[0]
                else:
                    if not rdd_dict[elements[0]] == pair[0]:
                        return False
                if not (elements[1] in rdd_dict):
                    rdd_dict[elements[1]] = pair[1]
                else:
                    if not rdd_dict[elements[1]] == pair[1]:
                        return False
            return res

        # Evaluate if the elements of pair was be in the base
        def f_evaluate_pair(l_base, v_pair):
            # generate one dictionary to evaluate if already rdd was see
            for aux_par in l_base:
                if aux_par[0] == v_pair[0] or aux_par[0] == v_pair[1]:
                    return True
                elif aux_par[1] == v_pair[1] or aux_par[1] == v_pair[0]:
                    return True
            return False

        def f_cartesian_product(l_base, list_a):
            l_res = []
            for v_element_base in l_base:
                l_line = []
                for v_element_a in list_a:
                    if type(v_element_base[0]) is list:
                        if f_evaluate_pair(v_element_base, v_element_a):
                            l_line = v_element_base + [v_element_a]
                            if f_is_valid(l_line):
                                l_res.append(l_line)
                    else:
                        if f_evaluate_pair([v_element_base], v_element_a):
                            l_line = [v_element_base] + [v_element_a]
                            if f_is_valid(l_line):
                                l_res.append(l_line)
            return l_res

        # l_total = [list(range(1,6)),list(range(6,11)),list(range(11,16)),list(range(16,21)),list(range(21,26))]
        l_total = self.list_signal_pairs
        l_cartesian_product = l_total[0]
        v_cont = 1
        while v_cont < len(l_total):
            l_cartesian_product = f_cartesian_product(l_cartesian_product, l_total[v_cont])
            # print("Cartesian")
            # print(l_cartesian_product)
            v_cont = v_cont + 1

        print("OUTPUT", len(l_cartesian_product))
        # Print the elements of cartesian product
        # for v_element in l_cartesian_product:
        #     print(v_element)

        self.attractor_fields = l_cartesian_product
        # print(oRedRddasModel.attractor_fields)

        # show in a graph the trees
