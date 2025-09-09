import matplotlib.pyplot as plt

def plot_path(graph, path, title, showPlottedPath):
    """
    Plots the given path on a 2D plane and annotates the edges with their weights.

    This method generates a plot of the cities and the path taken by the TSP algorithm.
    It draws lines between each pair of cities in the path and annotates the edges with
    their respective weights (distances).

    Parameters:
    graph (Graph): The graph object containing city coordinates and distance matrix.
    path (list): The list of city indices representing the path.
    title (str): The title of the plot.
    """
    x_coords = [graph.city_coordinates[city][0] for city in path]
    y_coords = [graph.city_coordinates[city][1] for city in path]

    plt.figure(figsize=(8, 8))
    plt.plot(x_coords, y_coords, marker='o', linestyle='-', color='b', zorder=5)

    for i, city in enumerate(path):
        plt.text(graph.city_coordinates[city][0], graph.city_coordinates[city][1], str(city), fontsize=12, ha='right', zorder=10)

    for i in range(len(path) - 1):
        city1 = path[i]
        city2 = path[i + 1]
        mid_x = (graph.city_coordinates[city1][0] + graph.city_coordinates[city2][0]) / 2
        mid_y = (graph.city_coordinates[city1][1] + graph.city_coordinates[city2][1]) / 2
        dist = graph.matrix_graph[city1][city2]
        plt.text(mid_x, mid_y, f'{dist:.0f}', color='black', fontsize=8, ha='center', zorder=10)

    plt.xlim(0, 1000)
    plt.ylim(0, 1000)
    plt.title(title)
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid(True)
    if showPlottedPath:
        plt.show()
