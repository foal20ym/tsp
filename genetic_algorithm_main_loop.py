from genetic_algorithm import GeneticAlgorithm
from helpers.calculate_path_distance import calculate_path_distance
from utils.decorators import timer

@timer
def geneticAlgorithmMainLoop(ga: GeneticAlgorithm, num_generations, population_size, graph, opt=None, optimal_solution=None):
    
    for generation in range(num_generations):
        new_offspring = []
        
        # Selection and Crossover
        for _ in range(population_size // 2):
            selected = ga.selectionFunction()
            offspring = ga.crossoverFunction(selected[0], selected[1])
            new_offspring.extend(offspring)
        
        # Mutation
        if not opt:
            mutated_offspring = [ga.mutationFunction(individual) for individual in new_offspring]
        else:
            mutated_offspring = [ga.guidedMutationFunction(individual, generation, num_generations) for individual in new_offspring]

        # Form New Population
        new_population = ga.population + mutated_offspring  # Combine old and new population
        fitness_scores = [ga.fitnessFunction(individual)[0] for individual in new_population]
        
        # Select the Best Individuals
        sorted_population = [individual for _, individual in sorted(zip(fitness_scores, new_population))]
        ga.population = sorted_population[:population_size]
        
        # Evaluate new population
        fitness_scores = [ga.fitnessFunction(individual)[0] for individual in ga.population]

        # Stopping criterion
        if optimal_solution:
            if sorted(fitness_scores)[0] <= optimal_solution:
                print(f"Optimal solution found in generation {generation}")
                break

    GA_final_path = ga.population[0]
    
    if GA_final_path[0] != GA_final_path[-1]:
        GA_final_path.append(GA_final_path[0])

    GA_final_cost = calculate_path_distance(graph, GA_final_path)
    return GA_final_path, GA_final_cost