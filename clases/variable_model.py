# VARIABLE MODEL ONLY HAVE NUMBER, VARIABLE_NAME, INTERACTORS LIST, CNF FUNCTION
class VariableModel():
    name_variable = 0
    list_interactors = []
    cnf_function = []

    def __init__(self, name_variable, cnf_function):
        self.name_variable = int(name_variable)
        self.cnf_function = cnf_function

    def show(self):
        print("V: " + str(self.name_variable) + " CNF :" + str(self.cnf_function))
