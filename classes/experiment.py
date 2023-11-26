# imports
import pickle  # library to serialization object


class ExperimentModel(object):
    def __init__(self,d_meta, l_data):
        self.d_meta = d_meta
        self.l_data = l_data

    def show(self):
        # print every information in d_meta
        for key, value in self.d_meta.items():
            print(key, ":", value)
        #
        # for l_dict in self.l_data:
        #     for d_data in l_dict:
        #         for key, value in d_data.items():
        #             print(key, ":", value)
        #
        # for l_rddas in self.l_l_rdda:
        #     for o_rdda in l_rddas:
        #         o_rdda.show()

    @staticmethod
    def save_file_pickle(o_experiment, v_path):
        # save information about the RDDA
        with open(v_path + ".pickle", 'wb') as f:
            # Pickle the 'data' dictionary using the highest protocol available.
            pickle.dump(o_experiment, f, pickle.HIGHEST_PROTOCOL)
        print("file : " + v_path + ".pickle saved")
        # pickle.dump(oRedRddasModel, v_path + ".pickle")

    @staticmethod
    def load_file_pickle(v_path):
        with open(v_path, 'rb') as f:
            # The protocol version used is detected automatically, so we do not have to specify it.
            data = pickle.load(f)
            return data
