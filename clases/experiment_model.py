# imports
import pickle  # library to serialization object


class ExperimentModel(object):
    def __init__(self, d_data, o_rdda):
        self.d_data = d_data
        self.o_rdda = o_rdda

    def show(self):
        # print every information in d_data
        for key, value in self.d_data.items():
            print(key, ":", value)
        self.o_rdda.show()

    @staticmethod
    def save_file_pickle(o_experiment, v_path):
        # o_experiment_model.show()
        # save information about the RDDA
        with open(v_path + ".pickle", 'wb') as f:
            # Pickle the 'data' dictionary using the highest protocol available.
            pickle.dump(o_experiment, f, pickle.HIGHEST_PROTOCOL)
        print("file : " + v_path + ".pickle saved")
        # pickle.dump(oRedRddasModel, v_path + ".pickle")

    @staticmethod
    def load_file_pickle(v_path):
        with open(v_path, 'rb') as f:
            # The protocol version used is detected automatically, so we do not
            # have to specify it.
            data = pickle.load(f)
            return data
