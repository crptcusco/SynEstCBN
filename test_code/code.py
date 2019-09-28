def findAtractorsSATGlobal(self):
        print "RED NUMBER : " + str(self.number_of_rdda)
        #create boolean expresion initial with transition = n
        number_of_transitions = 2
        list_atractors=[]
        list_clausules_atractors = []

        #REPEAT CODE
        boolean_function = self.generateBooleanFunctionTransition(number_of_transitions,list_clausules_atractors)
        matriz_respuesta_sat =[]
        v_solver = Minisat()
        solution = v_solver.solve(boolean_function)

        if solution.success:
            for j in range(0,number_of_transitions):
                matriz_respuesta_sat.append([])
                for i in self.list_of_v_total:
                    matriz_respuesta_sat[j].append(solution[self.dic_var_cnf[str(i)+"_"+str(j)]])
        else:
            print ("The expression cannot be satisfied")

        #print "RESPUESTA SAT"
        #print matriz_respuesta_sat
        #print "RESPUESTA SAT"

        #BLOCK ATRACTORS
        matriz_auxliar_sat=[]
        if(len(matriz_respuesta_sat) != 0 ):
            #TRANFORM BOOLEAN TO MATRIZ BOOLEAN RESPONSE
            for j in range(0,number_of_transitions):
                matriz_aux_sat = []
                for i in range(0,self.number_of_v_total):
                    if matriz_respuesta_sat[j][i] == True:
                        matriz_aux_sat.append("1")
                    else:
                        matriz_aux_sat.append("0")
                matriz_auxliar_sat.append(matriz_aux_sat)
            #matriz_respuesta_booleana = matriz_auxliar_sat
        matriz_respuesta_booleana = matriz_auxliar_sat
        #BLOCK ATRACTORS
        #REPEAT CODE
        
        while (len(matriz_respuesta_booleana) > 0 ):
            path_solution = matriz_respuesta_booleana
            print ("Path Transition Begin")
            for path_trasition in path_solution:
                print path_trasition
            print ("Path Transition End")
            #new list of state attractors
            news_estates_atractor = []
            #check atractors
            for v_state in path_solution:
                v_state_count = self.countStateRepeat(v_state, path_solution)
                if (v_state_count > 1):
                    atractor_begin = path_solution.index(v_state)+1
                    atractor_end = path_solution[atractor_begin:].index(v_state)
                    news_estates_atractor = path_solution[atractor_begin-1:(atractor_begin + atractor_end)]
                    list_atractors = list_atractors + news_estates_atractor
                    #add atractors like list of list
                    self.set_of_atractors.append(news_estates_atractor)
                    break

            #print self.set_of_atractors

            if len(news_estates_atractor) == 0 :
                number_of_transitions = number_of_transitions * 2

            #TRANFORM LIST OF ATRACTORS TO CLAUSULES
            for clausule_atractor in list_atractors:
                clausule_variable = []
                cont_variable = 0
                for estate_atractor in clausule_atractor:
                    print cont_variable
                    if (estate_atractor == "0"):
                        clausule_variable.append("-" + str(self.list_of_v_intern[cont_variable]))
                    else:
                        clausule_variable.append(str(self.list_of_v_intern[cont_variable]))
                    cont_variable = cont_variable + 1
                list_clausules_atractors.append(clausule_variable)

            print list_clausules_atractors
            
            #REPEAT CODE
            boolean_function = self.generateBooleanFunctionTransition(number_of_transitions,list_clausules_atractors)
            matriz_respuesta_sat =[]
            v_solver = Minisat()
            solution = v_solver.solve(boolean_function)
    
            if solution.success:
                for j in range(0,number_of_transitions):
                    matriz_respuesta_sat.append([])
                    for i in self.list_of_v_total:
                        matriz_respuesta_sat[j].append(solution[self.dic_var_cnf[str(i)+"_"+str(j)]])
            else:
                print ("The expression cannot be satisfied")
    
            #print "RESPUESTA SAT"
            #print matriz_respuesta_sat
            #print "RESPUESTA SAT"
    
            #BLOCK ATRACTORS
            matriz_auxliar_sat=[]
            if(len(matriz_respuesta_sat) != 0 ):
                #TRANFORM BOOLEAN TO MATRIZ BOOLEAN RESPONSE
                for j in range(0,number_of_transitions):
                    matriz_aux_sat = []
                    for i in range(0,self.number_of_v_total):
                        if matriz_respuesta_sat[j][i] == True:
                            matriz_aux_sat.append("1")
                        else:
                            matriz_aux_sat.append("0")
                    matriz_auxliar_sat.append(matriz_aux_sat)
                #matriz_respuesta_booleana = matriz_auxliar_sat
            matriz_respuesta_booleana = matriz_auxliar_sat
            #BLOCK ATRACTORS
            #REPEAT CODE
        print self.set_of_atractors
        print ("TODO ESTA OK")
        return list_atractors
