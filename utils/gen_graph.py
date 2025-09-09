import matplotlib.pyplot as plt
from datetime import datetime
from tabulate import tabulate
import tsplib95
import logging
import random
import math
import json

#FILE PATHS
graph_size_10   = "Files//graph_10.json"
graph_size_50   = "Files//graph_50.json"
graph_size_100  = "Files//graph_100.json"
graph_size_500  = "Files//graph_500.json"
graph_size_1000 = "Files//graph_1000.json"

class Graph:
    def __init__(self, num_of_cities=None, tsp_problem=None, testing=None):
        self.num_of_cities = num_of_cities

        if tsp_problem:
            self.city_coordinates, self.matrix_graph = self.loadTSPProblem(tsp_problem)
        elif not testing:
            self.city_coordinates = self.generateCityCoordinates(num_of_cities)
            self.matrix_graph = self.generateGraph()
        else: 
            self.city_coordinates = self.generateGraphBySize(num_of_cities)
            self.matrix_graph = self.generateGraph()
        
        self.setupLogging()
        self.logDistanceMatrix()
        self.plotCities()
    
    def loadTSPProblem(self, tsp_problem):
        """Load a TSPLIB95 problem and convert it to city coordinates and distance matrix."""
        nodes = list(tsp_problem.get_nodes())
        size = len(nodes)
        city_coordinates = [tsp_problem.node_coords[node] for node in nodes]
        matrix_graph = [[0] * size for _ in range(size)]

        for i in range(size):
            for j in range(size):
                if i != j:
                    matrix_graph[i][j] = tsp_problem.get_weight(nodes[i], nodes[j])

        return city_coordinates, matrix_graph
    
    def generateCityCoordinates(self, num_of_cities: int):
        """Generate random city coordinates."""
        return [(random.randint(0, 1000), random.randint(0, 1000)) for _ in range(num_of_cities)]

    def generateGraph(self):
        """
        Generates a graph with a specified number of cities, including their coordinates and distance matrix.

        Returns:
            list: A 2D list (matrix) representing the distances between each pair of cities.
        """
        matrix_graph = [[0] * self.num_of_cities for _ in range(self.num_of_cities)]

        def distance(city1, city2):
            return math.sqrt((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2)

        for i in range(self.num_of_cities):
            for j in range(i + 1, self.num_of_cities):
                dist = distance(self.city_coordinates[i], self.city_coordinates[j])
                matrix_graph[i][j] = dist
                matrix_graph[j][i] = dist

        return matrix_graph

    def create_tsplib_problem(self):
        problem = tsplib95.models.StandardProblem()
        problem.dimension = self.num_of_cities
        problem.node_coords = {i + 1: coord for i, coord in enumerate(self.city_coordinates)}
        return problem
    
    def generateGraphBySize(self,input_size):
        graph_sizes = {
            10      : graph_size_10,
            50      : graph_size_50,
            100     : graph_size_100,
            500     : graph_size_500,
            1000    : graph_size_1000
        }
        file_path = graph_sizes.get(input_size,graph_size_10)
        with open(file_path,"r") as json_file:
            graph = json.load(json_file)
        return graph
    
    def setupLogging(self):
        """ Set up logging to a file named logs/{now}.log
            filename: The filename to log to
            
            format: The format to log with

            filemode: The file mode to open the file with (default is 'w')

            level: The root logger level (default is logging.WARNING)  
        """
        logging.basicConfig(
            filename="logs/" + datetime.now().strftime("%Y-%m-%d %H.%M.%S") + ".log",
            format="%(asctime)s - %(message)s",
            filemode="w",
            level=logging.DEBUG
        )
        logging.getLogger('matplotlib.font_manager').setLevel(logging.WARNING)
        logging.getLogger('matplotlib.pyplot').setLevel(logging.WARNING)
        logging.getLogger('PIL').setLevel(logging.WARNING)

    def logDistanceMatrix(self):
        headers = [''] + [str(i + 1) for i in range(len(self.matrix_graph))]
        rows = [[f"{str(i + 1)}"] + [f"{self.matrix_graph[i][j]:6.0f}" for j in range(len(self.matrix_graph))] for i in range(len(self.matrix_graph))]
        logging.info("Distance Matrix (matrix_graph):")
        logging.info(tabulate(rows, headers=headers, tablefmt='grid'))

    def plotCities(self):
        """
        Plots the cities and the weighted edges between them in a 2D graph.

        This method generates a scatter plot of cities with random coordinates and 
        draws lines between each pair of cities to represent the distances (weights) 
        between them. The plot is saved as an image file.
        """
        x_coords = [coord[0] for coord in self.city_coordinates]
        y_coords = [coord[1] for coord in self.city_coordinates]

        plt.figure(figsize=(8, 8))
        plt.scatter(x_coords, y_coords, color='red', zorder=5)

        for i, (x, y) in enumerate(self.city_coordinates):
            city_label = str(i)
            plt.text(x, y, city_label, fontsize=16, zorder=10)

        for i in range(self.num_of_cities):
            for j in range(i + 1, self.num_of_cities):
                city1 = self.city_coordinates[i]
                city2 = self.city_coordinates[j]
                dist = self.matrix_graph[i][j]
                plt.plot([city1[0], city2[0]], [city1[1], city2[1]], 'gray', linestyle='-', zorder=1)
                mid_x = (city1[0] + city2[0]) / 2
                mid_y = (city1[1] + city2[1]) / 2
                plt.text(mid_x, mid_y, f'{dist:.0f}', color='black', fontsize=8, zorder=10)

        plt.xlim(0, 1000)
        plt.ylim(0, 1000)
        plt.title("Random City Locations with Weighted Edges")
        plt.xlabel("X Coordinate")
        plt.ylabel("Y Coordinate")
        plt.grid(True)
        plt.savefig('city_weighted_graph.png')
        plt.show()
