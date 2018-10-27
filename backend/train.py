class Train:
    def __init__(self, origin_start, real_start, origin_arrival, real_arrival, rail):
        self.origin_start = origin_start
        self.real_start = real_start
        self.origin_arrival = origin_arrival
        self.real_arrival = real_arrival
        self.rail = rail
    

    def __repr__(self):
        return '''
        origin start = {}
        real start = {}
        origin arrival = {}
        real arrival = {}
        rail = {}
        '''.format(self.origin_start, self.real_start, self.origin_arrival, self.real_arrival, self.rail)

