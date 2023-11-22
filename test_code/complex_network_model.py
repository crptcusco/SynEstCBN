from random import randint

class ComplexNetworkModel(object):
    number_of_rddas = 0
    number_variables_in_rddas = 0
    number_relations_in_rddas = 0
    number_clausules_in_node = 0
    total_number_of_variables = 0
    #strict_variables = True
    #strict_relations = True
    
    def __init__(self,number_of_rdds,number_variables_in_rddas,number_relations_in_rddas, number_clausules_in_node,rddas_path):
        self.number_of_rddas = number_of_rdds
        self.number_variables_in_rddas = number_variables_in_rddas
        self.number_relations_in_rddas = number_relations_in_rddas
        self.number_clausules_in_node = number_clausules_in_node
        self.total_number_of_variables = number_variables_in_rddas + number_relations_in_rddas
        
        #creating the rddas
        for i in range(1,self.number_of_rddas): 
            create_rdda(i)
        
        print ("ALL THE RDDAS WAS CREATED")
    
    def create_rdda(self,rdda_number):
        
        texto = "v. " + self.total_number_of_variables + "\n\n"        
        for node in range(1,self.number_variables_in_rddas):
            n_predictores = randint(1, self.total_number_of_variables)
            #Generando los predictores
            for predictor in ()
            
            l_predictores = 
            texto = texto + ".n " + str(node) + " " + str(n_predictores)
            #sorteo de predictores
            
            for 
            
            
        print ("rdda " + str(rdda_number) + " creada")
        