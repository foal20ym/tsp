from utils.gen_graph import Graph
from helpers.genetic_algorithm_logging import GeneticAlgorithmLogging
import random

class GeneticAlgorithm:
    def __init__(self, pop_size, num_of_cities, matrix_graph, crossover_rate, mutation_rate):
        self.pop_size = pop_size
        self.num_of_cities = num_of_cities
        self.matrix_graph = matrix_graph
        self.population = self.initPopulation()
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate

    def initPopulation(self):
        """ Initialize the population with random permutations of cities
        args:
            pop_size: The number of individuals in the population
            num_of_cities: The number of cities in the TSP
        returns:
            list: A list of random permutations of cities
        """
        population = []
        for _ in range(self.pop_size):
            individual = list(range(self.num_of_cities))
            random.shuffle(individual)
            population.append(individual)
        return population

    def fitnessFunction(self, path):
        """ Compute the total distance of a path in the TSP
        args:
            path: A permutation of cities
            matrix_graph: A 2D matrix representing the distances between cities
        returns:
            tuple: A tuple containing the total distance and the distances between cities
        """
        total_distance = 0
        distances = []
        
        for i in range(len(path) - 1):
            city1 = path[i]
            city2 = path[i + 1]
            
            if not (0 <= city1 < self.num_of_cities and 0 <= city2 < self.num_of_cities):
                raise IndexError(f"Invalid city index: city1={city1}, city2={city2}")
            
            dist = self.matrix_graph[city1][city2]
            distances.append((city1, city2, dist))
            total_distance += dist
        
        city1 = path[-1]
        city2 = path[0]
        
        if not (0 <= city1 < self.num_of_cities and 0 <= city2 < self.num_of_cities):
            raise IndexError(f"Invalid city index: city1={city1}, city2={city2}")
        
        dist = self.matrix_graph[city1][city2]
        distances.append((city1, city2, dist))
        total_distance += dist
        
        return total_distance, distances

    def cityLabels(self, path):
        """Convert city indices to their alphabetical labels (1, 2, 3, ...).
        
        args:
            path: A permutation of cities of type list[list[int]].
        returns:
            list: A list of city labels
        """
        return [f"{str(city + 1)}" for city in path]

    def selectionFunction(self):
        """Select two different individuals from the population using tournament selection

        args:
            population: A list of individuals (permutations of cities)
            matrix_graph: A 2D matrix representing the distances between cities
        returns:
            tuple: A tuple containing the two selected individuals
        """
        tournament_size = min(3, len(self.population))
        selected = []
        for _ in range(2):
            tournament = random.sample(self.population, tournament_size)
            fitness_scores = [self.fitnessFunction(individual)[0] for individual in tournament]
            best_individual = tournament[fitness_scores.index(min(fitness_scores))]
            
            max_retries, retries = 5, 0
            while best_individual in selected and retries < max_retries:
                tournament = random.sample(self.population, tournament_size)
                fitness_scores = [self.fitnessFunction(individual)[0] for individual in tournament]
                best_individual = tournament[fitness_scores.index(min(fitness_scores))]
                retries += 1

            selected.append(best_individual)

        return tuple(selected)

    def crossoverFunction(self, parent1, parent2):
        """Performs crossover (recombination) between two parents to produce two offspring.
        This might give worse solution, but the diversity it makes can be benefical in the long run. 

        args:
            parent1: A permutation of cities (first parent)
            parent2: A permutation of cities (second parent)
        returns:
            tuple: A tuple containing two offspring (permutations of cities)
        """
        if random.random() > self.crossover_rate:
            return parent1, parent2
        
        offspring1 = [-1] * len(parent1)
        offspring2 = [-1] * len(parent2)
        start, end = sorted(random.sample(range(len(parent1)), 2))
        offspring1[start:end] = parent1[start:end]
        offspring2[start:end] = parent2[start:end]

        for i in range(len(parent1)):
            if offspring1[i] == -1:
                for gene in parent2:
                    if gene not in offspring1:
                        offspring1[i] = gene
                        break

            if offspring2[i] == -1:
                for gene in parent1:
                    if gene not in offspring2:
                        offspring2[i] = gene
                        break

        return offspring1, offspring2
    
    def mutationFunction(self, individual):
        """Perform mutation on an individual by swapping two random cities
        args:
            individual: A permutation of cities
        returns:
            list: A mutated individual (permutation of cities)
        """
        if random.random() > self.mutation_rate:
            return individual
        
        mutated = individual.copy()
        city1, city2 = random.sample(range(len(individual)), 2)
        mutated[city1], mutated[city2] = mutated[city2], mutated[city1]

        return mutated
    
    def guidedMutationFunction(self, individual, generation, num_generations):
        """Perform mutation on an individual using the 2-opt algorithm

        args:
            individual: A permutation of cities
        returns:
            list: A mutated individual (permutation of cities)
        """
        mutation_rate = 0
        
        # Calculate how much of the function that should be mutated depending on the generation
        if generation <= 0.25 * num_generations:
            mutation_rate = 0.04
        elif generation <= 0.5 * num_generations:
            mutation_rate = 0.03
        elif generation <= 0.75 * num_generations:
            mutation_rate = 0.02
        elif generation > 0.75 * num_generations:
            mutation_rate = 0.01
            
        if random.random() > mutation_rate:
            return individual
        
        def swap(path, i, k):
            new_path = path[:i] + path[i:k+1][::-1] + path[k+1:]
            return new_path
        
        best_path = individual.copy()
        best_distance, _ = self.fitnessFunction(best_path)
        improved = True
        while improved:
            improved = False
            for i in range(1, len(best_path) - 1):
                for k in range(i + 1, len(best_path)):
                    new_path = swap(best_path, i, k)
                    new_distance, _ = self.fitnessFunction(new_path)
                    if new_distance < best_distance:
                        best_path = new_path
                        best_distance = new_distance
                        improved = True
                        
        return best_path

    def run(self):
        GeneticAlgorithmLogging.logPopulationAndPath()
        selected = self.selectionFunction()
        GeneticAlgorithmLogging.logMutationWithDistanceAndOffspring(selected)

if __name__ == "__main__":
    print("This is ran when 'python genetic_algorithm.py' is ran in the terminal.")
    graph = Graph(num_of_cities=10)
    ga = GeneticAlgorithm(pop_size=5, num_of_cities=len(graph.matrix_graph), matrix_graph=graph.matrix_graph)
    ga.run()