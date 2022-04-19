from clases.rdda_model import RddaModel
from clases.signal_model import SignalModel
from clases.variable_model import VariableModel
class AttractorModel(object):
    def __init__(self, v_number, v_rdda, l_states):
        self.number = v_number
        self.rdda = v_rdda
        self.l_states = l_states

    def show(self):
        print("Number :", self.number , "RDDA :", self.rdda)
        print("States :")
        for l_state in self.l_states:
            print(l_state)