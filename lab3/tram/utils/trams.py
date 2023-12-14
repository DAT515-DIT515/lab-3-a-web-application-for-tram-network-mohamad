import json

# imports added in Lab3 version
import math
import os
from .graphs import WeightedGraph #.
from django.conf import settings
from math import cos, sqrt, pi
from .tramdata import distance_between_stops

# path changed from Lab2 version
# TODO: copy your json file from Lab 1 here
TRAM_FILE = os.path.join(settings.BASE_DIR, 'static/tramnetwork.json')



# TODO: use your lab 2 class definition, but add one method

# import sys
# sys.path.append('../lab-1-information-extraction-mohamad')
# from .tramdata as td
import json
# import networkx as nx
from math import cos, sqrt, pi


# from tramdata import dialogue, time_between_stops
# LINE_FILE = 'D:\Fortsättnings kurs i python\lab-2-graphs-and-transport-networks-mohamad\data\tramlines.txt'
# STOP_FILE = 'D:\Fortsättnings kurs i python\lab-2-graphs-and-transport-networks-mohamad\data\tramstops.json'
#TRAM_FILE = '../lab-2-graphs-and-transport-networks-mohamad/data/tramnetwork.json'

class TramStop:
    def __init__(self, name, lines, lat, lon):
        self._name = name
        self._lines = lines
        self._position = (lat, lon)

    def add_line(self, line):
        self._lines.append(line)

    def get_lines(self):
        return self._lines

    def get_name(self):
        return self._name

    def get_position(self):
        return self._position

    def set_position(self, lat, lon):
        self._position = (lat, lon)


class TramLine:
    def __init__(self, num, stops):
        self._number = num
        self._stops = stops

    def get_number(self):
        return self._number

    def get_stops(self):
        return self._stops


class TramNetwork(WeightedGraph):
    def __init__(self, lines, stops, times):
        super().__init__(directed=True)
        # self._linedict = lines
        self._stopdict = stops
        # self._timedict = times
        for stop, destinations in times.items():
            for destination, time_trans in destinations.items():
                self.add_edge(stop, destination)
                self.set_weight(stop, destination, int(time_trans) if time_trans is not None else 0)



    def all_lines(self):
        return list(self.edges())

    def all_stops(self):
        return self.vertices()


    def extreme_positions(self):
        all_stops = self.vertices()
        if not all_stops:
            return None

        def get_lat_lon(stop):
            value = self.get_vertex_value(stop)
            return value[0] if (value and value[0] is not None) else (0, 0)

        min_lat_stop = min(all_stops, key=lambda stop: get_lat_lon(stop)[0])
        max_lat_stop = max(all_stops, key=lambda stop: get_lat_lon(stop)[0])
        min_lon_stop = min(all_stops, key=lambda stop: get_lat_lon(stop)[1])
        max_lon_stop = max(all_stops, key=lambda stop: get_lat_lon(stop)[1])

        return {
            'min_lat': min_lat_stop,
            'max_lat': max_lat_stop,
            'min_lon': min_lon_stop,
            'max_lon': max_lon_stop
        }

    def geo_distance(self, stop1, stop2):
        # value1 = self.get_vertex_value(stop1)
        # value2 = self.get_vertex_value(stop2)
        # if value1 is None or value2 is None:
        #     # Handle the case where the stop coordinates are not available
        #     return float('inf')  # or any other appropriate value
        # lat1, lon1 = value1
        # lat2, lon2 = value2

        # radius = 6371.0
        # lat_diff = (lat2 - lat1) * pi / 180
        # lon_diff = (lon2 - lon1) * pi / 180
        # middle_lat = (lat1 + lat2) / 2

        # distance = radius * sqrt(lat_diff**2 + (cos(middle_lat) * lon_diff)**2)

        # return distance
        return distance_between_stops(self._stopdict,stop1,stop2)


    def line_stops(self, line):
        return self.neighbours(line)

    def stop_lines(self, stop):
        return self.neighbours(stop)

    def stop_position(self, stop):
        return self.get_vertex_value(stop)

    def transition_time(self, a, b):
        return self.get_weight(a, b)


def readTramNetwork():
    #tram_data = td.build_tram_network(td.STOP_FILE, td.LINE_FILE)
    #return TramNetwork(tram_data['lines'], tram_data['stops'], tram_data['times'])

    with open(TRAM_FILE,"r", encoding='utf-8') as tramdat:
        trams=json.load(tramdat)
    
    stops = trams["stops"]
    times = trams["times"]
    lines = trams["lines"]
    return TramNetwork(lines, stops, times)




# Bonus task 1: take changes into account and show used tram lines

# def specialize_stops_to_lines(network):
#     # TODO: write this function as specified
#     return network


# def specialized_transition_time(spec_network, a, b, changetime=10):
#     # TODO: write this function as specified
#     return changetime


# def specialized_geo_distance(spec_network, a, b, changedistance=0.02):
#     # TODO: write this function as specified
#     return changedistance


