from datetime import *
import time
from sqlalchemy import Column, Integer, String
from database import Base


class Train(Base):

    __tablename__ = 'trains'

    id = Column(Integer, primary_key=True)
    origin_start = Column(String(100))
    real_start = Column(String(100))
    origin_arrival = Column(String(100))
    real_arrival = Column(String(100))
    route = Column(String(100))
    date = Column(Integer)


    def __init__(self, origin_start, real_start, origin_arrival, real_arrival, route):
        self.origin_start=origin_start
        self.real_start=real_start
        self.origin_arrival=origin_arrival
        self.real_arrival=real_arrival
        self.route=route
        self.date = time.time()


        if real_arrival is not '':
            date_format_string = '%H:%M'
            origin_arrival_date = datetime.strptime(origin_arrival, date_format_string)
            real_arrival_date = datetime.strptime(real_arrival, date_format_string)
            self.delay = int((real_arrival_date - origin_arrival_date).seconds / 60)
        else:
            self.delay = 0


    def __repr__(self):
        return '''
        origin start = {}
        real start = {}
        origin arrival = {}
        real arrival = {}
        route = {}
        '''.format(self.origin_start, self.real_start, self.origin_arrival, self.real_arrival, self.route)


    def serialize(self):
        return {
            'origin_start' : self.origin_start,
            'real_start' : self.real_start,
            'origin_arrival' : self.origin_arrival,
            'real_arrival' : self.real_arrival,
            'route' : self.route,
            "delay" : self.delay
        }
