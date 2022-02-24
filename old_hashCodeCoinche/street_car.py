


class Street:
    begin = 0
    end = 0
    name = None
    L = None

    def __init__(self, begin, end, name, L):
        self.begin = begin
        self.end = end
        self.name = name
        self.L = L



class Car:
    num_streets = 0
    list_streets = []

    def __init__(self, num, list):
        self.num_streets = num
        self.list_streets = list

    def get_list_Streets(self, streets_objects):
        self.Streets=[]
        for street_str in self.list_streets:
            # print("street: ", street_str)
            street_obj = [st for st in streets_objects if st.name==street_str][0]
            self.Streets.append(street_obj)

