class CBN(object):
    def __init__(self, n_networks, generated=False, **kwargs):
        self.n_networks = n_networks
        self.generated = generated
        if self.generated:
            self.generate_cbn()
        else:
            self.l_networks = kwargs['l_networks']
            self.l_relations = kwargs['l_relations']

    def __str__(self):
        res = 'Number of Networks: {}, Generated: {}'.format(self.n_networks, self.generated)
        # show the networks
        if self.l_networks:
            for o_network in self.l_networks:
                o_network.show()

        # show the relations
        if self.l_relations:
            for o_relation in self.l_relations:
                o_relation.show()

        return res

    def generate_cbn(self):
        pass

