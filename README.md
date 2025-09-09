# Traveling Salesman Problem (TSP) Solver Using Genetic Algorithm

This project provides a solution to the **Traveling Salesman Problem (TSP)** using a **Genetic Algorithm (GA)**. The implementation is written in Python and aims to find an optimized solution for the TSP through evolutionary techniques.

## Project Structure

- **Graph Creation**: Generates a weighted graph representing the cities and the distances between them.
- **Population Initialization**: Creates a population of possible TSP routes (solutions).
- **Fitness Evaluation**: Calculates the fitness (total distance) of each route in the population.

## Tools & Libraries Used

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/AronKG/TSP.git
   cd TSP
   ```

# Installation for mac users:
1. **Packages**: To install all packages at once, run the following command in the terminal:
   - `python -m pip install -U -r requirements.txt` 
1. **Run the program**: To run the program, run the following command in the terminal:
   - `python genetic_algorithm.py` 

# Installation for windows users:
1. **Python**: The primary language for the project.
2. **Icecream**: Installed for debugging. Provides clearer and more readable output for troubleshooting during development.
3. **Logging**: Used instead of standard `print()` for more structured output during program execution, especially in a production environment.
4. **Matplotlib**: For visualizing the city locations and paths.
   - Install via: `pip install icecream`
   - for windows in terminal first:
      - `python -c "import matplotlib.pyplot as plt; print('Matplotlib is installed')" `
      - `python file_name.py` 
   - or 
      1. Command Palette (Ctrl + Shift + P).
      2. Type Python: Select Interpreter 
      3. Choose Python 3.1.. the version you have 
      4. Restart run --> start debug 