oRedRddas = RedRddasModel(4,5,3,2,2, created=True)
oRedRddas.generate_rddas()
# oRedRddas.create_rddas()


print(oRedRddas.create_rddas())
print(oRedRddas.number_of_rddas)
print(oRedRddas.number_of_variables_rdda)
print(oRedRddas.number_of_signals_rdda)

# self.created = created
# self.number_of_rddas = number_of_rddas  # number of rdds
# self.number_of_variables_rdda = number_of_variables_rdda  # number of variables for each rdd
# self.number_of_signals_rdda = number_of_signals_rdda  # number of signals who have each rdd
# self.number_exit_variables = number_exit_variables  # number of exit variables in the set of exit
# self.number_clauses_function = number_clauses_function  # number of clauses for each transition function
# self.list_of_rddas = []  # List of th object of each RDD
# self.l_rdda_permutation_attractors = []  # List who join RDD - Permutation - Attractors
# self.rddas_attractors = []  # List of attractors in form of key, Without RDD
# self.list_attractors_pairs = []  # List of attractors pairs in only one list without RDD
# self.group_signals_pairs = []  # List of attractors pairs group by relations between RDDs
# self.list_signal_pairs = []  # List of signal pairs group by relations,but without labels
# self.d_global_rdda_attractor = {}  # Dictionary for each attractor with his RDD
# self.attractor_fields = []  # The List of attractor fields in format of pair attractors
# self.generateRDDAs()


