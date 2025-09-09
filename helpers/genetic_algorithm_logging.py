from utils.gen_graph import logging

class GeneticAlgorithmLogging:
    def logPopulationAndPath(self):
        logging.info("Population, Paths Between Cities, and Fitness:")
        for i, individual in enumerate(self.population):
            fitness, distances = self.fitnessFunction(individual)
            path_labels = self.cityLabels(individual)
            logging.info(f"Path {i+1}: {path_labels}")
            logging.info("City-to-City Path and Distances:")
            for (city1, city2, dist) in distances:
                logging.info(f"City {city1} -> City {city2}: {dist:.2f} units")
            logging.info(f"Fitness (Total Distance): {fitness:.2f} units\n")

    def logMutationWithDistanceAndOffspring(self, selected):
        offspring1, offspring2 = self.crossoverFunction(selected[0], selected[1])
        logging.info("Offspring from Crossover:")
        logging.info(f"Parent 1: {self.cityLabels(selected[0])}")
        logging.info(f"Parent 2: {self.cityLabels(selected[1])}")
        logging.info(f"Offspring 1: {self.cityLabels(offspring1)}")
        logging.info(f"Offspring 2: {self.cityLabels(offspring2)}")
        fitness1, distances1 = self.fitnessFunction(offspring1)
        fitness2, distances2 = self.fitnessFunction(offspring2)
        logging.info(f"Offspring 1 Fitness (Total Distance): {fitness1:.2f} units")
        logging.info(f"Offspring 2 Fitness (Total Distance): {fitness2:.2f} units")
        logging.info("Offspring 1 City-to-City Path and Distances:")
        for (city1, city2, dist) in distances1:
            logging.info(f"City {city1} -> City {city2}: {dist:.2f} units")
        logging.info("Offspring 2 City-to-City Path and Distances:")
        for (city1, city2, dist) in distances2:
            logging.info(f"City {city1} -> City {city2}: {dist:.2f} units")

        mutated_offspring1 = self.mutationFunction(offspring1)
        mutated_offspring2 = self.mutationFunction(offspring2)
        logging.info("Mutated Offspring:")
        logging.info(f"Offspring 1: {self.cityLabels(offspring1)}")
        logging.info(f"Mutated Offspring 1: {self.cityLabels(mutated_offspring1)}")
        logging.info(f"Offspring 2: {self.cityLabels(offspring2)}")
        logging.info(f"Mutated Offspring 2: {self.cityLabels(mutated_offspring2)}")
        fitness1, distances1 = self.fitnessFunction(mutated_offspring1)
        fitness2, distances2 = self.fitnessFunction(mutated_offspring2)
        logging.info(f"Mutated Offspring 1 Fitness (Total Distance): {fitness1:.2f} units")
        logging.info(f"Mutated Offspring 2 Fitness (Total Distance): {fitness2:.2f} units")
        logging.info("Mutated Offspring 1 City-to-City Path and Distances:")
        for (city1, city2, dist) in distances1:
            logging.info(f"City {city1} -> City {city2}: {dist:.2f} units")
        logging.info("Mutated Offspring 2 City-to-City Path and Distances:")
        for (city1, city2, dist) in distances2:
            logging.info(f"City {city1} -> City {city2}: {dist:.2f} units")