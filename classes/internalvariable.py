class InternalVariable:
    def __init__(self, index, cnf_function=None):
        if not isinstance(cnf_function, list) and cnf_function is not None:
            raise TypeError("cnf_function must be a list or None")
        self.index = index
        self.cnf_function = cnf_function if cnf_function is not None else []

    def show(self):
        print("Index: " + str(self.index) + " Function in CNF :" + str(self.cnf_function))

