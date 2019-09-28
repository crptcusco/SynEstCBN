from .variable_model import VariableModel
from .rdda_model import RddaModel
from .signal_model import SignalModel

#import os #create directories
#import sys #receive arguments by command line
#import shutil # directories management

import random #generate random numbers
from random import randint #generate random numbers integers
from itertools import product #generate combinations of numbers 
import sys #system interaction
from functools import reduce # importing functools for reduce()

class RedRddasModel(object):
    def __init__(self,number_of_rddas,number_of_variables_rdda,number_of_sinais_rdda,number_exit_signals):
        self.number_of_rddas = number_of_rddas
        self.number_of_variables_rdda = number_of_variables_rdda
        self.number_of_sinais_rdda = number_of_sinais_rdda
        self.lista_of_rddas = []
        self.number_exit_signals = number_exit_signals
        
    def generateRDDAs(self, type_network = "ALEATORY", v_generate_files=False, data_path=""):
        #generate the RDDAs variables
        v_contador_variable = 1
        for number_of_rdda in range(1,self.number_of_rddas+1):
            print (number_of_rdda)
            list_of_v_intern = []
            for v_numero_variable in range(v_contador_variable,v_contador_variable + self.number_of_variables_rdda):
                list_of_v_intern.append(v_numero_variable)
                v_contador_variable = v_contador_variable + 1
            print(list_of_v_intern)
            oRddaModel = RddaModel(number_of_rdda,list_of_v_intern)
            self.lista_of_rddas.append(oRddaModel)
        
        #generate acoplament signals
        #we generate an auxiliary list to add the coupling signals
        aux1_lista_of_rddas = []
        for oRddaModel in self.lista_of_rddas :
            #how many coupling signals will they have
            number_of_signals_rdda = randint(1,self.number_of_sinais_rdda)
            #we create a list to choose the neighboring networks   
            l_aux_rddas = self.lista_of_rddas.copy()
            l_aux_rddas.remove(oRddaModel)
            #select the neighboring network
            l_rdda_co = random.sample(l_aux_rddas,number_of_signals_rdda)
            lista_signals = []
            for v_rdda_co in l_rdda_co:
                #generate the list of coupling variables
                l_variaveis_saida = random.sample(v_rdda_co.list_of_v_intern, self.number_exit_signals)
                
                #FUTURE JOB!!!
                #generate the acoplament function
                #acoplament_function = " & ".join( list(map(str, l_variaveis_saida)))
                #acoplament_function = "|".join( list(map(str, l_variaveis_saida)))
                
                #We validate if we have one or several output variables
                if(self.number_exit_signals == 1):
                    acoplament_function = l_variaveis_saida[0]
                else:
                    acoplament_function = " ∨ ".join(list(map(str, l_variaveis_saida)))
                #print(acoplament_function)
                #sys.exit() 
                #define the maximum number of output variables with professor
                oSignalModel = SignalModel(oRddaModel.number_of_rdda,v_rdda_co.number_of_rdda, l_variaveis_saida, v_contador_variable,acoplament_function)
                oSignalModel.show()
                lista_signals.append(oSignalModel)
                v_contador_variable = v_contador_variable + 1 
            oRddaModel.list_of_signals = lista_signals.copy()
            aux1_lista_of_rddas.append(oRddaModel)  
        self.lista_of_rddas=aux1_lista_of_rddas.copy()
        
        #show the RDDAs with signals and with description
        #for v_rdda in self.lista_of_rddas:
        #    v_rdda.show() 
        
        #GENERATE THE DYNAMICS
        number_max_of_clausules = 3
        number_max_of_literals = 3
        #we generate an auxiliary list to add the coupling signals
        aux2_lista_of_rddas = []
        for oRddaModel in self.lista_of_rddas:
            #Create a list of all RDDAs variables
            l_aux_variables = []
            #Add the variables of the coupling signals
            for signal in oRddaModel.list_of_signals:
                l_aux_variables.append(signal.name_variable)
            #add local variables
            l_aux_variables.extend(oRddaModel.list_of_v_intern)
            
            #generate the function description of the variables
            description_variables = []
            #generate clauses
            for v_description_variable in oRddaModel.list_of_v_intern:
                l_clausules_node = []
                for v_clausula in range(0,randint(1,number_max_of_clausules)):
                    v_num_variable = randint(1,number_max_of_literals)
                    #randomly select from the signal variables
                    l_literais_variables = random.sample(l_aux_variables,v_num_variable)
                    l_clausules_node.append(l_literais_variables)
                #adding the description of variable in form of object
                oVariableModel = VariableModel(v_description_variable,l_clausules_node)
                description_variables.append(oVariableModel) 
            #adding the description in functions of every variable
            #adding the RDDA to list of RDDAs
            oRddaModel.description_variables = description_variables.copy()
            aux2_lista_of_rddas.append(oRddaModel) 
        #actualized the list of rddas
        self.lista_of_rddas=aux2_lista_of_rddas.copy()   
        
        for rdda in self.lista_of_rddas:
            rdda.proccesParameters()
        
        #show the RDDAs with signals and with description
        #for v_rdda in self.lista_of_rddas:
        #    v_rdda.show() 
                  
        if v_generate_files :
            print("RDDAs generated")
    
    @staticmethod
    def calculateAttractorsFields(oRedRddasModel):        
        print("BEGIN CALCULATE LOCAL ATTRACTORS")      
        #create a list of fields of attractors
        l_global_atractors=[]
        #find the attractors for each RDDA
        for oRdda in oRedRddasModel.lista_of_rddas:
            #generate the possible combinations according to the coupling signals
            for v_permutacion in product(list('01'), repeat=len(oRdda.list_of_signals)):
                #format list??
                l_global_atractors.append([oRdda.list_of_signals, oRdda.number_of_rdda ,''.join(v_permutacion),RddaModel.findLocalAtractorsSATSatispy(oRdda,''.join(v_permutacion))])
        print("END CALCULATE LOCAL ATTRACTORS")
                
        #List of attractors fields RDDA1:A1 , RDDA2 : A2 
        l_attractors_fields=[]
                
        print("BEGIN CALCULATE ATTRACTORS FIELD")
        for l_local_atractors in l_global_atractors:
            for v_signal in l_local_atractors[0]:
                print(v_signal.rdda_entrada)
                print(v_signal.rdda_salida)
                #look for the attractors of the output RDDA
                l_aux_neigborgth_atractors=[]
                for aux_local_atractors in l_global_atractors:
                    if aux_local_atractors[1] == v_signal.rdda_salida :
                        l_aux_neigborgth_atractors.extend(aux_local_atractors[3])
                print("BEGIN List of Atrators of neigborght")
                print(l_aux_neigborgth_atractors)
                print("END List of Atrators of neigborght")
                #Print the permutation
                print("Imprimir Permutacion")
                print(l_local_atractors[2])
                #list the attractors of the incoming RDDA
                print("List of Input Attractors")
                for attractor in l_local_atractors[3]:
                    print (attractor)
                print("True Table of Acoplament Signal")
                print(v_signal.true_table)
                print("List of Output Variables")
                print(v_signal.l_variaveis_saida)
                #list the attractors of the output RDDA
                print("List of Output Attractors")
                for elemento in l_aux_neigborgth_atractors:
                    print(elemento)
                #Analyze if there is a correlation between one and the other
                
                sys.exit()

        
        print("END CALCULATE ATTRACTORS FIELDS")
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
            