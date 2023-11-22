# -*- coding: utf-8 -*-
import os
import sys
import random
from random import randint
import shutil
#from os import listdir
#import time
#from random import sample

print ("PROGRAM TO CREATE RDDA")

v_n_rddas = int(sys.argv[1])
v_n_variables_rdda = int(sys.argv[2])
v_num_constans_in_rddas = int(sys.argv[3])
v_num_total_nodes_in_rdda = v_n_variables_rdda + v_num_constans_in_rddas

#create the directory
#defined the v_path when the files are saved
v_path_dir = "files/"
v_path_base = "rddas_" +"r"+str(v_n_rddas) + "_v"+ str(v_n_variables_rdda) + "_c"+ str(v_num_constans_in_rddas)
v_path_dir = v_path_dir + v_path_base
print (v_path_dir)
#create directory with name of red

try:
    shutil.rmtree(v_path_dir)
except OSError:  
    print ("Delete of the directory %s failed" % v_path_dir)
else:  
    print ("Successfully deleted the directory %s " % v_path_dir)
   
try: 
    os.mkdir(v_path_dir)
except OSError:  
    print ("Creation of the directory %s failed" % v_path_dir)
else:  
    print ("Successfully created the directory %s " % v_path_dir)

#CREATE THE INPUT FILE
v_var_begin = 1
l_global_variables = list(range(1,(v_n_variables_rdda*v_n_rddas)+1))
#print (l_global_variables)

for v_num_rdd in range(1, v_n_rddas + 1):
    #generate the variables
    l_variables = range(v_var_begin, v_var_begin + v_n_variables_rdda)
    #generate the constants delete the local variables
    #l_posbible_constants = l_global_variables[:]
    l_posbible_constants = l_global_variables.copy()
    for v_local_variable in l_variables:
        l_posbible_constants.remove(v_local_variable)    
    l_constants = random.sample(l_posbible_constants, v_num_constans_in_rddas)
    l_union_variable_constants = list(l_variables[:]) + list(l_constants[:])
    #generate the list of variables for the cnf function
    v_number_max_clausules_cnf = 4
    v_number_max_variable_clausule_cnf = 4
    v_number_min_variable_clausule_cnf = 2
    
    l_description_nodes=[]
    for v_description_variable in l_variables:
        l_clausules_node = []
        for v_clausula in range(0,randint(1,v_number_max_clausules_cnf)):
            l_variables_clausule = []
            v_num_variable = randint(v_number_min_variable_clausule_cnf,v_number_max_variable_clausule_cnf)
            l_aux_variables = random.sample(l_union_variable_constants,v_num_variable)
            l_clausules_node.append( [x * random.sample([-1,1],1)[0] for x in l_aux_variables])
        l_description_nodes.append(l_clausules_node)    
        
    #GENERATE THE FILE OUTPUT
    v_texto = "c \n"
    v_texto = v_texto + "c - " + v_path_base + "_" + str(v_num_rdd) + "\n"
    v_texto = v_texto + "c \n"
    v_texto = v_texto + "c r "+ str(v_num_rdd) + "\n"
    v_texto = v_texto + "c v " + str(v_n_variables_rdda) + " " + str(v_num_constans_in_rddas) + " " + str(v_num_total_nodes_in_rdda) + "\n"
    v_texto = v_texto + "c i "+ " ".join(map(str,l_variables))  + "\n"
    v_texto = v_texto + "c e "+ " ".join(map(str,l_constants))  + "\n"
    #PRINT THE DESCRIPTION OF THE NODES
    v_aux_node = 0 
    for v_node in l_variables:
        v_texto = v_texto = v_texto + "p cnf "+ str(v_node) + " " + str(len(l_description_nodes[v_aux_node])) + "\n"
        for v_aux_line in l_description_nodes[v_aux_node]:
            v_texto = v_texto = v_texto + " ".join(map(str,v_aux_line)) + " 0\n"
        v_aux_node = v_aux_node + 1 
    #print (v_texto)
    
    #SAVE OUTPUT IN FILE
    #CREATE NAME FILE
    archivo = open(v_path_dir +"/" + v_path_base +"_" + str(v_num_rdd) +".rdd", "w")
    archivo.write(v_texto)
    archivo.close()
    #print ("RDD SAVE")
    v_var_begin = l_variables[-1] + 1
    #print v_var_begin 
print("RDDs CREATED")