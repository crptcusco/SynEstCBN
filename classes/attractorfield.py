class FieldAttractorModel(object):
    def __init__(self, list_rdda_attractor):
        self.list_rdda_attractor = list_rdda_attractor

    def show(self):
        for t_element in self.list_rdda_attractor:
            print("RDDA : ", t_element[0], " Attractor : ", t_element[1])

    def show_graphic(self):
        print("Graphic of field of attractors")
        pass