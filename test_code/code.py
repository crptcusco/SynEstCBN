def findAtractorsSATGlobal(self):
        print "RED NUMBER : " + str(self.n_of_rdda)
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
                for i in self.l_of_v_total:
                    matriz_respuesta_sat[j].append(solution[self.d_var_cnf[str(i) + "_" + str(j)]])
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
                for i in range(0, self.n_of_v_total):
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
                    self.set_of_attractors.append(news_estates_atractor)
                    break

            #print self.set_of_attractors

            if len(news_estates_atractor) == 0 :
                number_of_transitions = number_of_transitions * 2

            #TRANFORM LIST OF ATRACTORS TO CLAUSULES
            for clausule_atractor in list_atractors:
                clausule_variable = []
                cont_variable = 0
                for estate_atractor in clausule_atractor:
                    print cont_variable
                    if (estate_atractor == "0"):
                        clausule_variable.append("-" + str(self.l_var_intern[cont_variable]))
                    else:
                        clausule_variable.append(str(self.l_var_intern[cont_variable]))
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
                    for i in self.l_of_v_total:
                        matriz_respuesta_sat[j].append(solution[self.d_var_cnf[str(i) + "_" + str(j)]])
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
                    for i in range(0, self.n_of_v_total):
                        if matriz_respuesta_sat[j][i] == True:
                            matriz_aux_sat.append("1")
                        else:
                            matriz_aux_sat.append("0")
                    matriz_auxliar_sat.append(matriz_aux_sat)
                #matriz_respuesta_booleana = matriz_auxliar_sat
            matriz_respuesta_booleana = matriz_auxliar_sat
            #BLOCK ATRACTORS
            #REPEAT CODE
        print self.set_of_attractors
        print ("TODO ESTA OK")
        return list_atractors
    

        #USSING NETWOKRX LIBRARY PYTHON
#         o_G = nx.DiGraph()
#         o_G.add_nodes_from(range(0,len(d_global_rdda_attractor)))
#         o_G.add_edges_from(l_t_aux_links_two_rddas)
#         
#         l_path_all = []
#         for v_aux_attractor in range(0,len(d_global_rdda_attractor)):
#             print("LIST OF PATHS OF THE ATRACTOR : " + str(v_aux_attractor))
#             l_path_all.append(nx.multi_source_dijkstra_path(o_G,[v_aux_attractor]))   
        
        #print(nx.is_tree(o_G))
        #print(nx.is_forest(o_G))
        #print(o_G.number_of_nodes())
        
        #for path in l_path:
        #        print(path)
        
        #creating and show the list of adjacency
        #l_adjacency = nx.generate_adjlist(o_G)
        #for v_element in l_adjacency:
        #    print(v_element)

        #d_paths = list(nx.find_cycle(o_G, orientation='original'))
        #for key_path,value_path in d_paths.items():
        #    print(key_path)
        #    print(value_path)
        #for path in d_paths:
        #    print(path)
        #print(d_paths)
        
#         reverse dictironary
#         d_inv_global_rdda_attractor = {v: k for k, v in d_global_rdda_attractor.items()}
#         
#         l_links_two_rddas_aux = []     
#         fill the adjacency graph
#         for v_link in l_links_two_rddas:
#             v_link[0] = d_inv_global_rdda_attractor[v_link[0]]
#             v_link[1] = d_inv_global_rdda_attractor[v_link[1]]
#             l_links_two_rddas_aux.append(v_link)
#         
#         show the list of links with others values
#         print("LIST OF UNION BETWEM TWO RDDAs WITH DICTIONARY")
#         print("FORMAT : RDDA INPUT - ATTRACTOR , RRDA OUTPUT - ATTRACTOR, PERMUTATION, VARIABLE INPUT, VARIABLES OUTPUT SET")
#         for v_link in l_links_two_rddas:
#             print(v_link)
#         print("NUMBER OF LINKS : " + str(len(l_links_two_rddas)))
        
        #JOIN THE ATRACTORS WITH THE SYNCRONIZED STATES.
        
        ##CREATE ONE DATA STRUCTURE IN PANDAS
        #panda_df = pd.DataFrame(np.array(l_links_two_rddas), columns=['RI', 'RO', 'PE', 'VI','VO', 'AI', 'AO' ])
        #print(panda_df)       
        #panda_df2 = panda_df.groupby(['RI', 'RO','PE']).AO
        #panda_df2 = panda_df2.to_frame()
        #print(panda_df2.first())
        #panda_df_group =  panda_df.groupby(['AI'])
