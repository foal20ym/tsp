def calculate_path_distance(graph, path):
    total_distance = 0
    for i in range(len(path) - 1):
        total_distance += graph.matrix_graph[path[i]][path[i+1]]
    total_distance += graph.matrix_graph[path[-1]][path[0]]  
    return total_distance