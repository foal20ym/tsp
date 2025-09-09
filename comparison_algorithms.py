from itertools import permutations
from utils.decorators import timer
from helpers.calculate_path_distance import calculate_path_distance
import networkx as nx

@timer
def naive_tsp(graph):
    cities = list(range(graph.num_of_cities))
    shortest_path = None
    min_path_weight = float('inf')
    
    for permutation in permutations(cities):
        current_weight = calculate_path_distance(graph, permutation)
        if current_weight < min_path_weight:
            min_path_weight = current_weight
            shortest_path = permutation
    
    shortest_path = list(shortest_path) + [shortest_path[0]]  #start
    return shortest_path, min_path_weight

@timer
def nearest_neighbor_tsp(graph):
    num_of_cities = graph.num_of_cities
    unvisited = set(range(num_of_cities))
    current_city = 0  
    path = [current_city]
    total_weight = 0

    while len(unvisited) > 1:
        unvisited.remove(current_city)
        next_city = min(unvisited, key=lambda city: graph.matrix_graph[current_city][city])
        total_weight += graph.matrix_graph[current_city][next_city]
        path.append(next_city)
        current_city = next_city

    total_weight += graph.matrix_graph[current_city][path[0]]
    path.append(path[0])
    
    return path, total_weight

@timer
def nx_tsp_solver(number_of_nodes,graph):
    G = nx.complete_graph(number_of_nodes)
    for i in range(number_of_nodes):
        for j in range(i+1,number_of_nodes):
            G[i][j]['weight'] = graph[i][j]
    return G