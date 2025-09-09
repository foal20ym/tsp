from helpers.calculate_path_distance import calculate_path_distance
from genetic_algorithm_main_loop import geneticAlgorithmMainLoop
from genetic_algorithm import GeneticAlgorithm
from utils.path_plotter import plot_path
from utils.gen_graph import Graph
import comparison_algorithms
import networkx as nx
import tsplib95
import logging

def main():
    # Set to True if you want to test problems in the tsp_problem_list
    testing = False
    
    if testing: 
        tsp_lib = True
        if tsp_lib:
            tsp_problem_list = ['Files//ulysses16.tsp']
                                #'Files//ulysses22.tsp'
                                #'Files//st70.tsp',
                                #'Files//rd100.tsp',]
                                #'Files//gr202.tsp',]
                                #'Files//pcb442.tsp']
            optimal_solutions = [6859,     # Ulysses16
                                7013,      # Ulysses22
                                675,       # st70
                                7910,      # rd100
                                40160,     # gr202
                                50778]     # pcb442
        else:
            num_of_cities = [10, 50, 100, 500, 1000]
        population_size = 10
        num_generations = 200
        crossover_rate = 0.7
        mutation_rate = 0.05
        test_runs = 5

        for tsp_problem in tsp_problem_list:
            j = 0
            if tsp_lib:
                problem = tsplib95.load(tsp_problem)
                num_of_cities = problem.dimension
                optimal_solution = optimal_solutions[tsp_problem_list.index(tsp_problem)]
            else:
                num_of_cities = num_of_cities
            population_size = num_of_cities*30
            while j < test_runs:
                # Initialize the Graph
                graph = Graph(num_of_cities=num_of_cities, tsp_problem=problem, testing=True)
                matrix_graph = graph.matrix_graph

                # Naive brute-force TSP
                if(num_of_cities <= 15):
                    naive_solution_path, naive_cost = comparison_algorithms.naive_tsp(graph)
                    print(f"Naive TSP: Shortest path: {naive_solution_path} with cost: {naive_cost}")
                    logging.info(f"Naive TSP:\n  Shortest path: {naive_solution_path}\n  Distance: {naive_cost}")
                else: 
                    print(f"Naive TSP: Did not go through the calculations because num_of_cities is too high.")

                # Nearest Neighbor TSP 
                nn_solution_path, nn_cost = comparison_algorithms.nearest_neighbor_tsp(graph)
                print(f"Nearest Neighboor TSP: Shortest path: {nn_solution_path} with cost: {nn_cost}")
                logging.info(f"Nearest Neighbor TSP:\n  Shortest path: {nn_solution_path}\n  Distance: {nn_cost}")

                #NX Solver
                nx_graph = comparison_algorithms.nx_tsp_solver(num_of_cities, matrix_graph)
                tsp_nx_solution = nx.approximation.traveling_salesman_problem(nx_graph, cycle=True)
                tsp_nx_path_cost = calculate_path_distance(graph,tsp_nx_solution)
                print(f"TSP NX Shortest Path:{tsp_nx_solution} with cost: {tsp_nx_path_cost}")
                logging.info(f"TSP NX:\n  Shortest path: {tsp_nx_solution}\n  Distance: {tsp_nx_path_cost}")
                
                # Genetic Algorithms
                # This setup will allow us to instantiate different 'ga'/genetic algorithms like the one above with different parameters, and send each one into the main loop.
                # Not optimized
                ga = GeneticAlgorithm(pop_size=population_size, num_of_cities=num_of_cities, matrix_graph=matrix_graph, crossover_rate=crossover_rate, mutation_rate=mutation_rate) 
                ga_final_path, ga_final_cost = geneticAlgorithmMainLoop(ga, num_generations, population_size, graph, opt=False, optimal_solution=optimal_solution)
                print(f"Genetic Algorithm: Shortest path: {ga_final_path} with cost: {ga_final_cost}")
                logging.info(f"Best solution (Test: {num_of_cities} cities):\n  Shortest path: {ga.population[0]}\n  Distance: {ga_final_cost:.2f}")
                # Optimized
                ga_opt = GeneticAlgorithm(pop_size=population_size, num_of_cities=num_of_cities, matrix_graph=matrix_graph, crossover_rate=crossover_rate, mutation_rate=mutation_rate)
                ga_opt_final_path, ga_opt_final_cost = geneticAlgorithmMainLoop(ga_opt, num_generations, population_size, graph, opt=True, optimal_solution=optimal_solution)
                print(f"Genetic Algorithm Optimized: Shortest path: {ga_opt_final_path} with cost: {ga_opt_final_cost}")
                logging.info(f"Best solution (Test: {num_of_cities} cities) Optimized:\n  Shortest path: {ga_opt.population[0]}\n  Distance: {ga_opt_final_cost:.2f}\n")

                j += 1

    else: 
        # Here are the configuration variables, all in one place so that we can mdoify them easily
        num_of_cities = 10
        population_size = 20
        num_generations = 100
        crossover_rate = 0.7
        mutation_rate = 0.05
        # Set to false if you dont want to see the plotted path of the different algorithms
        showPlottedPath = True 
        
        # Initialize the Graph
        graph = Graph(num_of_cities=num_of_cities, tsp_problem=None, testing=False)
        matrix_graph = graph.matrix_graph

        #TSP Problem
        nx_graph = comparison_algorithms.nx_tsp_solver(num_of_cities, matrix_graph)
        tsp_nx_solution = nx.approximation.traveling_salesman_problem(nx_graph, cycle=True)
        tsp_nx_path_cost = calculate_path_distance(graph,tsp_nx_solution)
        print(f"TSP NX Shortest Path:{tsp_nx_solution} with cost: {tsp_nx_path_cost}")

        # Naive brute-force TSP
        if(num_of_cities <= 10):
            naive_solution_path, naive_cost = comparison_algorithms.naive_tsp(graph)
            print(f"Naive TSP: Shortest path: {naive_solution_path} with cost: {naive_cost}")
            plot_path(graph, naive_solution_path, "Naive brute-force TSP Path", showPlottedPath)
        else: 
            print(f"Naive TSP: Did not go through the calculations because num_of_cities is too high.")

        # Nearest Neighbor TSP 
        nn_solution_path, nn_cost = comparison_algorithms.nearest_neighbor_tsp(graph)
        print(f"Nearest Neighboor TSP: Shortest path: {nn_solution_path} with cost: {nn_cost}")
        plot_path(graph, nn_solution_path, "Nearest Neighbor TSP Path", showPlottedPath)
        
        # Genetic Algorithm TSP
        ga = GeneticAlgorithm(pop_size=population_size, num_of_cities=num_of_cities, matrix_graph=matrix_graph, crossover_rate=crossover_rate, mutation_rate=mutation_rate) 

        # Genetic Algorithm Main Loop 
        # This setup will allow us to instantiate different 'ga'/genetic algorithms like the one above with different parameters, and send each one into the main loop. 
        GA_final_path, GA_final_cost = geneticAlgorithmMainLoop(ga, num_generations, population_size, graph,graph)
        print(f"Genetic Algorithm: Shortest path: {GA_final_path} with cost: {GA_final_cost}")
        plot_path(graph, GA_final_path, "Genetic Algorithm path", showPlottedPath)

        # Logging the final solutions chromosome, the connection of the cities, and calculate distance using the distance function from gen_graph
        logging.info("Final solution:")
        logging.info(f"Shortest path: {ga.population[0]}")
        logging.info(ga.fitnessFunction(ga.population[0]))
        logging.info(f"Distance: {GA_final_cost}")

if __name__ == "__main__":
    main()