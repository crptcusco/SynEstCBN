from itertools import product  # generate combinations of numbers

from modules.LocalNetwork import LocalNetwork


class CBN(object):
    def __init__(self, n_networks, generated=False, **kwargs):
        self.n_networks = n_networks
        self.generated = generated
        if self.generated:
            self.generate_cbn()
        else:
            self.l_networks = kwargs['l_networks']
            self.l_relations = kwargs['l_relations']

        # calculate properties
        self.l_cbn_permutation_attractors = []

    def __str__(self):
        res = 'Number of Networks: {}, Generated: {}'.format(self.n_networks, self.generated)
        return res

    def show(self):
        # show the networks
        print('------------------------')
        print("Networks")
        print('------------------------')
        if self.l_networks:
            for o_network in self.l_networks:
                o_network.show()

        # show the relations
        print('------------------------')
        print("Relations")
        print('------------------------')
        if self.l_relations:
            for o_relation in self.l_relations:
                o_relation.show()

    def generate_cbn(self):
        pass

    @staticmethod
    def find_attractors(o_cbn):
        print("BEGIN CALCULATE ALL LOCAL ATTRACTORS BY PERMUTATION")
        # CREATE A LIST OF: NETWORKS, PERMUTATION AND ATTRACTORS

        # FIND THE ATTRACTORS FOR EACH RDDA
        for o_network in o_cbn.l_networks:
            # GENERATE THE POSSIBLES COMBINATIONS ACCORDING TO THE COUPLING SIGNALS
            l_permutation = product(list('01'), repeat=len(o_network.list_var_extrem))
            for v_permutation in l_permutation:
                print("v_permutation")
                print(v_permutation)
                print("end")
                # ADD NETWORK, PERMUTATION AND LIST OF ATTRACTORS TO LIST OF ALL ATTRACTORS BY NETWORK
                # EST [RDDA Object, permutation,[List of attractors]]
                o_cbn.l_cbn_permutation_attractors.append([o_network, ''.join(v_permutation), LocalNetwork.find_attractors(o_network, ''.join(v_permutation))])
        print("END CALCULATE ALL LOCAL ATTRACTORS")
        print("######################################################")
        return o_cbn

