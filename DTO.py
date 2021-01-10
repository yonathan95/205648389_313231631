class Vaccine:
    def __init__(self, line):
        self.id = line[0]
        self.date = line[1]
        self.supplier = line[2]
        self.quantity = line[3]


class Supplier:
    def __init__(self, line):
        self.id = line[0]
        self.name = line[1]
        self.logistic = line[2]


class Clinic:
    def __init__(self, line):
        self.id = line[0]
        self.location = line[1]
        self.demand = line[2]
        self.logistic = line[3]


class Logistic:
    def __init__(self, line):
        self.id = line[0]
        self.name = line[1]
        self.count_sent = line[2]
        self.count_received = line[3]

