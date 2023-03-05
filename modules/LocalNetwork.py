from modules.CouplingSignal import CouplingSignal


class LocalNetwork:
    def __init__(self, i_network=1, n_variables=2, n_var_begin=1, relations=[]):
        self.i_network = i_network
        self.n_variables = n_variables
        self.n_var_begin = n_var_begin
        self.relations = relations

    def __str__(self):
        res = 'Network: {}, Number of variables: {}'.format(self.i_network, self.n_variables)
        # add the relations
        return res

