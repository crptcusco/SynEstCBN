#IMPORTS
import time
import sys
from os import listdir
from clases.rdda_model import RddaModel
from itertools import product

#PROGRAM
print ("PROGRAM TO FIND STABILTY AND SYNCRONISM IN RDDAs")
print ("Dealing with coupling signals in RDDs with SAT")
v_t0 = time.time()
v_path = sys.argv[1]
v_solver = sys.argv[2]

print("Ruta : " + v_path)
print("Solver : " + v_solver)

#list the number of files in the rddas
l_directory = listdir(v_path)
print ("List of the files of RDDAs")
for v_file_path in l_directory:
    print (v_file_path)

l_rddas = []
for v_rdda_path in l_directory:
    # noinspection PyArgumentList
    l_rddas.append(RddaModel(v_path + v_rdda_path))
#show the rddas created
#for elemento in l_rddas:
#    elemento.showRdda()
print ("RDDAs CREATED")
print ("#############################")
print ("FINDING LOCAL ATRACTORS ...")
print ("#############################")

#oRdda = l_rddas[0]
#oRdda.findAtractorsSAT()
#print (oRdda.set_of_attractors)

#find atractors for every permutation in each RDDA
#good place to parallel
l_local_atractors = []
v_cont_rdda=1
for o_rdda in l_rddas:
    for v_permutacion in product(list('01'), repeat=o_rdda.n_of_v_extern):
        l_local_atractors.append((v_cont_rdda ,v_permutacion ,RddaModel.findAtractorsSATStatic(o_rdda,''.join(v_permutacion))))
    v_cont_rdda = v_cont_rdda + 1    

#trying make parallel function
#def aux_findAtractorsSAT(oRdda):
#    return oRdda.findAtractorsSAT()
#p = mp.Pool(mp.cpu_count())
#l_local_atractors = p.map(aux_findAtractorsSAT, l_rddas)

print ("LIST OF LOCAL ATTRACTORS")
for t_group_atractors in l_local_atractors:
    print (t_group_atractors)

#SHOW TIME TO EXECUTION SCRIPT
v_time_execution = time.time() - v_t0
print ("TIME OF EXECUTION: "+ str(v_time_execution))

