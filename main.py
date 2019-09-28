from clases.red_rddas_model import RedRddasModel

import sys
#import os
#import random
#from random import randint
#import shutil

print ("PROGRAM TO CREATE RDDAs")
#Reciving the parameters
number_of_rddas = int(sys.argv[1])
number_of_variables_rdda = int(sys.argv[2])
number_of_sinais_rdda = int(sys.argv[3])
number_exit_signals = int(sys.argv[4])

type_network = "ALEATORY"
v_generate_files = False
data_path = ""

#generate the RDDAs of the RedRDDAs
oRedRddasModel = RedRddasModel(number_of_rddas, number_of_variables_rdda, number_of_sinais_rdda, number_exit_signals)
#generate the RDDAs
oRedRddasModel.generateRDDAs(type_network)
#calculate the Attractors Field
RedRddasModel.calculateAttractorsFields(oRedRddasModel)
print("END PROGRAM")