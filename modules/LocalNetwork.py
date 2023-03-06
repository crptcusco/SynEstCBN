from modules.CouplingSignal import CouplingSignal


class LocalNetwork:
    def __init__(self, i_network=1, n_variables=2, n_var_begin=1, l_variables=[], relations=[]):
        self.i_network = i_network
        self.n_variables = n_variables
        self.n_var_begin = n_var_begin
        self.l_variables = l_variables
        self.relations = relations

    def __str__(self):
        res = 'Network: {}, Number of variables: {}'.format(self.i_network, self.n_variables)
        # add the relations
        return res

    def show(self):
        # res = 'Network {} \n'.format(self.i_network)
        # res += 'Variables:'.format(self.l_variables)
        # print(res)
        print(f'Network: {self.i_network}')
        print(f'Variables: {self.l_variables}')
