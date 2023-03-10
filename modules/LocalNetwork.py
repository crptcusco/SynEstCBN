from satispy import Variable  # Library to resolve SAT
from satispy.solver import Minisat  # Library to resolve SAT
import ray  # Library to parallelization, distribution and scalability

from modules.CouplingSignal import CouplingSignal
from modules.VariableCNF import VariableCNF


class LocalNetwork:
    def __init__(self, i_network=1, l_variables=None):
        if l_variables is None:
            l_variables = []
        self.i_network = i_network
        self.l_variables = list(l_variables)

        # calculate properties
        self.list_of_v_total = []
        self.description_variables = []
        self.set_of_attractors = []
        self.list_var_extrem = []
        self.dic_var_cnf = {}

        print(f'Network: {self.i_network}, All variables: {self.list_of_v_total}')

    def __str__(self):
        res = 'Network: {}, Variables: {}'.format(self.i_network, self.l_variables)
        return res

    def process_description_variables(self, description):
        # Description of Variables
        i_var_description = 0
        for variable in self.l_variables:
            cnf_function = description[i_var_description]
            o_variable_cnf = VariableCNF(variable, cnf_function)
        pass

    def show(self):
        print(f'Network: {self.i_network}, Variables: {self.l_variables}')

    @staticmethod
    def generate_boolean_formulation(o_network, number_of_transitions, l_atractors_clausules, l_signal_coupling):
        # create dictionary of cnf variables!!
        for variable in o_network.list_of_v_total:
            for transition_c in range(0, number_of_transitions):
                o_network.dic_var_cnf[str(variable) + "_" + str(transition_c)] = Variable(
                    str(variable) + "_" + str(transition_c))

        # transition_aux = 0
        cont_transition = 0
        boolean_function = Variable("0_0")
        for transition in range(1, number_of_transitions):
            # transition_aux = transition
            cont_clausula_global = 0
            boolean_expresion_equivalence = Variable("0_0")
            for oVariableModel in o_network.description_variables:
                cont_clausula = 0
                boolean_expresion_clausule_global = Variable("0_0")
                for clausula in oVariableModel.cnf_function:
                    boolean_expresion_clausule = Variable("0_0")
                    cont_termino = 0
                    for termino in clausula:
                        termino_aux = abs(int(termino))
                        if (cont_termino == 0):
                            if (str(termino)[0] != "-"):
                                boolean_expresion_clausule = o_network.dic_var_cnf[
                                    str(termino_aux) + "_" + str(transition - 1)]
                            else:
                                boolean_expresion_clausule = -o_network.dic_var_cnf[
                                    str(termino_aux) + "_" + str(transition - 1)]
                        else:
                            if (str(termino)[0] != "-"):
                                boolean_expresion_clausule = o_network.dic_var_cnf[str(termino_aux) + "_" + str(
                                    transition - 1)] | boolean_expresion_clausule
                            else:
                                boolean_expresion_clausule = -o_network.dic_var_cnf[
                                    str(termino_aux) + "_" + str(transition - 1)] | boolean_expresion_clausule
                        cont_termino = cont_termino + 1
                    if (cont_clausula) == 0:
                        boolean_expresion_clausule_global = boolean_expresion_clausule
                    else:
                        boolean_expresion_clausule_global = boolean_expresion_clausule_global & boolean_expresion_clausule
                    cont_clausula = cont_clausula + 1
                if cont_clausula_global == 0:
                    boolean_expresion_equivalence = o_network.dic_var_cnf[str(oVariableModel.name_variable) + "_" + str(
                        transition)] >> boolean_expresion_clausule_global
                    boolean_expresion_equivalence = boolean_expresion_equivalence & (
                            boolean_expresion_clausule_global >> o_network.dic_var_cnf[
                        str(oVariableModel.name_variable) + "_" + str(transition)])
                else:
                    boolean_expresion_equivalence = boolean_expresion_equivalence & (o_network.dic_var_cnf[
                                                                                         str(oVariableModel.name_variable) + "_" + str(
                                                                                             transition)] >> boolean_expresion_clausule_global)
                    boolean_expresion_equivalence = boolean_expresion_equivalence & (
                            boolean_expresion_clausule_global >> o_network.dic_var_cnf[
                        str(oVariableModel.name_variable) + "_" + str(transition)])
                if (oVariableModel.cnf_function == []):
                    print("ENTRO CASO ATIPICO")
                    boolean_function = boolean_function & (
                            o_network.dic_var_cnf[str(oVariableModel.name_variable) + "_" + str(transition)] | -
                    o_network.dic_var_cnf[str(oVariableModel.name_variable) + "_" + str(transition)])
                cont_clausula_global = cont_clausula_global + 1
            if cont_transition == 0:
                boolean_function = boolean_expresion_equivalence
            else:
                boolean_function = boolean_function & boolean_expresion_equivalence
            # VALIDAR LOS GENES EN BLANCO
            cont_transition = cont_transition + 1

        # ASSING VALUES FOR PERMUTATIONS
        cont_permutacion = 0
        for elemento in o_network.list_var_extrem:
            # print oRDD.list_of_v_exterm
            for v_transition in range(0, number_of_transitions):
                # print l_signal_coupling[cont_permutacion]
                if l_signal_coupling[cont_permutacion] == "0":
                    boolean_function = boolean_function & -o_network.dic_var_cnf[str(elemento) + "_" + str(v_transition)]
                    # print (str(elemento) +"_"+ str(v_transition))
                else:
                    boolean_function = boolean_function & o_network.dic_var_cnf[str(elemento) + "_" + str(v_transition)]
                    # print (str(elemento) +"_"+ str(v_transition))
            cont_permutacion = cont_permutacion + 1

        # add atractors to boolean function
        if (len(l_atractors_clausules) > 0):
            boolean_function_of_atractors = Variable("0_0")
            cont_clausula = 0
            for clausula in l_atractors_clausules:
                boolean_expresion_clausule_of_atractors = Variable("0_0")
                cont_termino = 0
                for termino in clausula:
                    termino_aux = abs(int(termino))
                    # print str(termino_aux) + "_" + str(number_of_transitions-1)
                    if (cont_termino == 0):
                        if (termino[0] != "-"):
                            boolean_expresion_clausule_of_atractors = o_network.dic_var_cnf[
                                str(termino_aux) + "_" + str(number_of_transitions - 1)]
                        else:
                            boolean_expresion_clausule_of_atractors = -o_network.dic_var_cnf[
                                str(termino_aux) + "_" + str(number_of_transitions - 1)]
                    else:
                        if (termino[0] != "-"):
                            boolean_expresion_clausule_of_atractors = boolean_expresion_clausule_of_atractors & \
                                                                      o_network.dic_var_cnf[str(termino_aux) + "_" + str(
                                                                          number_of_transitions - 1)]
                        else:
                            boolean_expresion_clausule_of_atractors = boolean_expresion_clausule_of_atractors & - \
                                o_network.dic_var_cnf[str(termino_aux) + "_" + str(number_of_transitions - 1)]
                    cont_termino = cont_termino + 1
                if (cont_clausula) == 0:
                    boolean_function_of_atractors = -boolean_expresion_clausule_of_atractors
                else:
                    boolean_function_of_atractors = boolean_function_of_atractors & - boolean_expresion_clausule_of_atractors
                cont_clausula = cont_clausula + 1
            boolean_function = boolean_function & boolean_function_of_atractors

        # Add all the variables of the position 0 to the booblean function
        for variable in o_network.list_of_v_total:
            boolean_function = boolean_function & (
                    o_network.dic_var_cnf[str(variable) + "_0"] | - o_network.dic_var_cnf[str(variable) + "_0"])
        # print(boolean_function)
        return boolean_function

    def find_attractors(o_network, l_signal_coupling):
        def countStateRepeat(v_estate, path_solution):
            # input type [[],[],...[]]
            number_of_times = 0
            for v_element in path_solution:
                if v_element == v_estate:
                    number_of_times = number_of_times + 1
            return number_of_times

        # print "BEGIN TO FIND ATTRACTORS"
        print("NETWORK NUMBER : " + str(o_network.i_network) + " PERMUTATION SIGNAL COUPLING: " + l_signal_coupling)
        # create boolean expression initial with "n" transitions
        o_network.set_of_attractors = []
        v_num_transitions = 3
        l_atractors = []
        l_atractors_clausules = []

        # REPEAT CODE
        v_bool_function = o_network.generate_boolean_formulation(o_network, v_num_transitions, l_atractors_clausules,
                                                                 l_signal_coupling)
        print(v_bool_function)
        m_respuesta_sat = []
        o_solver = Minisat()
        o_solution = o_solver.solve(v_bool_function)

        # print(oRDD.number_of_v_total)
        if o_solution.success:
            for j in range(0, v_num_transitions):
                m_respuesta_sat.append([])
                for i in o_network.list_of_v_total:
                    # print("_________________________________________")
                    # print("Variable de Erro:", f"{i}_{j}")
                    # print(v_bool_function)
                    m_respuesta_sat[j].append(o_solution[o_network.dic_var_cnf[f'{i}_{j}']])
        else:
            print("The expression cannot be satisfied")

        # BLOCK ATRACTORS
        m_auxliar_sat = []
        if (len(m_respuesta_sat) != 0):
            # TRANFORM BOOLEAN TO MATRIZ BOOLEAN RESPONSE
            for j in range(0, v_num_transitions):
                matriz_aux_sat = []
                for i in range(0, len(o_network.list_of_v_total)):
                    if m_respuesta_sat[j][i] == True:
                        matriz_aux_sat.append("1")
                    else:
                        matriz_aux_sat.append("0")
                m_auxliar_sat.append(matriz_aux_sat)
            # m_resp_booleana = m_auxliar_sat
        m_resp_booleana = m_auxliar_sat
        # BLOCK ATRACTORS
        # REPEAT CODE

        while (len(m_resp_booleana) > 0):
            # print ("path")
            # print (m_resp_booleana)
            # print ("path")
            path_solution = []
            for path_trasition in m_resp_booleana:
                path_solution.append(path_trasition)

            # new list of state attractors
            l_news_estates_atractor = []
            # check atractors
            for v_state in path_solution:
                v_state_count = countStateRepeat(v_state, path_solution)
                if (v_state_count > 1):
                    atractor_begin = path_solution.index(v_state) + 1
                    atractor_end = path_solution[atractor_begin:].index(v_state)
                    l_news_estates_atractor = path_solution[atractor_begin - 1:(atractor_begin + atractor_end)]
                    l_atractors = l_atractors + l_news_estates_atractor
                    # add atractors like list of list
                    o_network.set_of_attractors.append(l_news_estates_atractor)
                    break

            # print oRDD.set_of_attractors
            if len(l_news_estates_atractor) == 0:
                # print ("DOBLANDO")
                v_num_transitions = v_num_transitions * 2

            # TRANFORM LIST OF ATRACTORS TO CLAUSULES
            for clausule_atractor in l_atractors:
                clausule_variable = []
                cont_variable = 0
                for estate_atractor in clausule_atractor:
                    if (estate_atractor == "0"):
                        clausule_variable.append("-" + str(o_network.list_of_v_total[cont_variable]))
                    else:
                        clausule_variable.append(str(o_network.list_of_v_total[cont_variable]))
                    cont_variable = cont_variable + 1
                l_atractors_clausules.append(clausule_variable)

            # print l_atractors_clausules
            # REPEAT CODE
            v_bool_function = o_network.generate_boolean_formulation(o_network, v_num_transitions, l_atractors_clausules,
                                                                     l_signal_coupling)
            m_respuesta_sat = []
            o_solver = Minisat()
            o_solution = o_solver.solve(v_bool_function)

            if o_solution.success:
                for j in range(0, v_num_transitions):
                    m_respuesta_sat.append([])
                    for i in o_network.list_of_v_total:
                        m_respuesta_sat[j].append(o_solution[o_network.dic_var_cnf[f'{i}_{j}']])
            else:
                # print(" ")
                print("The expression cannot be satisfied")

            # BLOCK ATRACTORS
            m_auxliar_sat = []
            if (len(m_respuesta_sat) != 0):
                # TRANFORM BOOLEAN TO MATRIZ BOOLEAN RESPONSE
                for j in range(0, v_num_transitions):
                    matriz_aux_sat = []
                    for i in range(0, o_network.number_of_v_total):
                        if m_respuesta_sat[j][i] == True:
                            matriz_aux_sat.append("1")
                        else:
                            matriz_aux_sat.append("0")
                    m_auxliar_sat.append(matriz_aux_sat)
                # m_resp_booleana = m_auxliar_sat
            m_resp_booleana = m_auxliar_sat
            # BLOCK ATRACTORS
            # REPEAT CODE

        # print oRDD.set_of_attractors
        # print(" ")
        # print ("END OF FIND ATRACTORS")
        return o_network.set_of_attractors

    def show_permutation_attractors(self):
        for permutation_attractor in self.list_permutations_attractors:
            print("Permutation: ", permutation_attractor[0], "Attractors: ")
            print(permutation_attractor[1])
