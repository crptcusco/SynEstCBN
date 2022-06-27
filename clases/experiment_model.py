class ExperimentModel(object):
    def __init__(self,title_exp, n_of_samples, l_df_samples):
        self.title_exp = title_exp
        self.n_sample = n_of_samples
        self.l_df_samples = l_df_samples

    def show(self):
        print("Experiment:", self.title_exp)
