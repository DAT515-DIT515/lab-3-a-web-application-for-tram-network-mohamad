# visualization of shortest path in Lab 3, modified to work with Django
from .trams import readTramNetwork #.
from .graphs import dijkstra #.
from .color_tram_svg import color_svg_network #.
import os
from django.conf import settings


def show_shortest(dep, dest):
    # TODO: uncomment this when it works with your own code
    network = readTramNetwork()

    # def time_cost_function(current_stop, next_stop):
    #     return network.transition_time(current_stop, next_stop)

    # def distance_cost_function(current_stop, next_stop):
    #     return network.geo_distance(current_stop, next_stop)

 
    quickest_path = dijkstra(network, dep, cost=lambda u,v: network.transition_time(u,v))[dest]['path']


    shortest_path = dijkstra(network, dep, cost=lambda u,v: network.geo_distance(u,v))[dest]['path']

    quickest_path_time = sum(
        network.transition_time(quickest_path[i], quickest_path[i + 1]) 
        if network.transition_time(quickest_path[i], quickest_path[i + 1]) is not None
        else 0
        for i in range(len(quickest_path) - 1))

    shortest_path_distance = sum(
        network.geo_distance(shortest_path[i], shortest_path[i + 1]) 
        if network.geo_distance(shortest_path[i], shortest_path[i + 1]) is not None
        else 0
        for i in range(len(shortest_path) - 1))

    timepath = 'Quickest: ' + ' - '.join(quickest_path) + " " + str(round(quickest_path_time, 1)) + " minutes "
    geopath = 'Shortest: ' + ' - '.join(shortest_path) + " " + str(round(shortest_path_distance, 1)) + " km "

    def colors(v):
        if v in shortest_path and quickest_path:
            return "cyan"
        elif v in shortest_path:
            return 'green'
        elif v in quickest_path:
            return 'orange'
        else:
            return 'white'

    # this part should be left as it is:
    # change the SVG image with your shortest path colors
    color_svg_network(colormap=colors)
    # return the path texts to be shown in the web page
    return timepath, geopath