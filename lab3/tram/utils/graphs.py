import networkx as nx
import graphviz
from graphviz import Digraph
import heapq

class Graph:
    def __init__(self, start=None, values=None, directed=False):
        self._adjlist = {}
        if values is None:
            values = {}
        self._valuelist = values
        self._isdirected = directed

        if start is not None:
            if isinstance(start, tuple):  # If start is an edge
                self.add_edge(start[0], start[1])
            elif isinstance(start, (list, set, tuple)):  # If start is multiple edges
                for edge in start:
                    self.add_edge(edge[0], edge[1])
            else:  # If start is a node
                self.add_vertex(start)

    def vertices(self):
        return list(self._adjlist.keys())

    def edges(self):
        edge_list = []
        for v1 in self.vertices():
            for v2 in self._adjlist.get(v1):
                if (v1, v2) not in edge_list:
                    edge_list.append((v1, v2))
        return edge_list

    def neighbours(self, v):
        return self._adjlist.get(v, [])

    def add_edge(self, a, b):
        self.add_vertex(a)
        self.add_vertex(b)
        self._adjlist[a].append(b)
        self._adjlist[b].append(a)


        # if not self._isdirected:
        #     self._adjlist[b].append(a)

    def add_vertex(self, a):
        if a not in self._adjlist:
            self._adjlist[a] = []

    def is_directed(self):
        return self._isdirected

    def get_vertex_value(self, v):
        return self._valuelist.get(v)

    def set_vertex_value(self, v, x):
        if v in self._valuelist.keys():
            self._valuelist[v] = x

class WeightedGraph(Graph):
    def __init__(self, start=None, values=None, directed=False):
        super().__init__(start, values, directed)
        self._weights = {}

    def set_weight(self, a, b, w):
        if (a, b) not in self._weights:
            self._weights[(a, b)] = w
        elif (b, a) not in self._weights:
            self._weights[(b, a)] = w

    def get_weight(self, a, b):
        return self._weights.get((a, b), None)

    def costs2attributes(self,G, cost_function, attr='weight'):
        for a, b in self.edges():
            self._weights[(a, b)] = cost_function(a, b)
            if not self.is_directed():
                self._weights[(b, a)] = cost_function(b, a)

def dijkstra(G, source, cost=lambda u, v: 1):
    distances = {node: float('inf') for node in G.vertices()}
    previous = {node: None for node in G.vertices()}
    pq = [(0, source)]

    distances[source] = 0

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        if current_distance > distances[current_node]:
            continue

        for neighbor in G.neighbours(current_node):
            edge_cost = cost(current_node, neighbor)

            if edge_cost is not None:
                new_distance = current_distance + edge_cost

                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current_node
                    heapq.heappush(pq, (new_distance, neighbor))
            elif True:
                edge_cost = cost(neighbor, current_node)
                new_distance = current_distance + edge_cost
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current_node
                    heapq.heappush(pq, (new_distance, neighbor))
                if edge_cost == None:
                    print(current_node, neighbor, edge_cost) #onödigt
                
                
    paths = {}
    lengths = distances.copy()
    for node in G.vertices():
        path = []
        current = node
        while current is not None:
            path.insert(0, current)
            current = previous[current]
        paths[node] = {'path': path, 'length': lengths[node]}

    
    return paths


