import random
import math
import time
import numpy as np


class SA:
    def __init__(self, problem, config):
        #QAP
        self.qap = problem
        self.type_initial_solution = config['type_initial_solution']
        self.neighbour_selection = config['neighbour_selection']
        
        self.cooling = config['cooling']
        self.max_iter = config['max_iter']
        self.iter_per_temp = config['iter_per_temp']

        #Set temperatures
        self.temp_initial = config['temp_initial']
        self.temp_min = config['temp_min']

        #Used in cooling functions
        if self.cooling == 'linear':
            self.beta = config['beta']
        else:
            self.beta = 0
        
        #Alpha mus be between ]0, 1[, othewise forced to 0.5
        if self.cooling == 'geometric':
            if config['alpha'] <= 0 or config['alpha'] >= 1:
                self.alpha = 0.5
            else:
                self.alpha = config['alpha']
        else:
            self.alpha = 0


        self.experiment_results = {
            "iteration": [],
            "best_of_values": [],
            "of_values": [],
            "best_solutions": [],
            "solutions": [],
            "selected_facilities": [],
            "temperatures": [],
            "probabilities": [],
            "time_per_iteration": []
        }

        """
        self.of_list = []
        self.total_iterations = 0

        #To control time
        self.time_per_iteration = []
        self.total_time = 0
        self.solution = []
        self.probabilities = []
        self.best_ofvalues = []
        """


    def generateRandomSolution(self, num_facilities):
        all_facilities = list(range(1, num_facilities + 1))
        random.shuffle(all_facilities)
        return all_facilities


    def generateInitialSolution(self):
        if self.type_initial_solution == "random":
            return self.generateRandomSolution(self.qap.solution_size)
        else:
            print("check 'initial_solution' in config.")
            exit()


    def acceptance_prob(self, delta_E, temp):
        n = np.random.random()
        value = math.e ** -(delta_E/temp)
        if n < value:
            return True, value
        
        return False, value


    def update_temperature(self, temp, iteration):
        #Depends on choseen cooling
        if self.cooling == "linear":
            t = self.temp_initial - (iteration * self.beta)
            return t
        
        if self.cooling == "geometric":
            t = self.alpha * temp
            return t
        
        if self.cooling == "logaritmic":
            #case log(1) = 0
            if iteration < self.max_iter:
                if iteration == 0:
                    t = self.temp_initial
                    return t
                else:
                    t = (self.temp_initial)/math.log(iteration)
                    return t
            else:
                return 0



    def run(self):
        solution = self.generateInitialSolution()
        of_value = self.qap.objectiveFunction(solution)
        
        best_of_value = of_value
        best_solution = solution.copy()

        self.experiment_results['of_values'].append(of_value)
        self.experiment_results['best_of_values'].append(best_of_value)
        self.experiment_results['solutions'].append(list(solution))
        self.experiment_results['best_solutions'].append(list(best_solution))

        temp = self.temp_initial
        self.experiment_results['temperatures'].append(temp)

        i = 1
        while temp > self.temp_min:
            start_time_iterations = time.time()
            self.experiment_results['iteration'].append(i)

            for j in range(self.iter_per_temp):
                new_solution = self.qap.generateNeighbour(solution)
                new_of_value = self.qap.objectiveFunction(new_solution)

                delta_E = new_of_value - of_value
                if delta_E <= 0:
                    solution = new_solution.copy()
                    of_value = new_of_value
                    prob_value = None
                    
                else:
                    is_accepted, prob_value = self.acceptance_prob(delta_E, temp)
                    if is_accepted:
                        solution = new_solution.copy()
                        of_value = new_of_value
                
                if of_value < best_of_value:
                    best_of_value = of_value
                    best_solution = solution.copy()
                
                self.experiment_results['time_per_iteration'].append(time.time() - start_time_iterations)
                
                self.experiment_results['of_values'].append(of_value)
                self.experiment_results['best_of_values'].append(best_of_value)
                
                self.experiment_results['solutions'].append(solution)
                self.experiment_results['best_solutions'].append(best_solution)

                self.experiment_results['probabilities'].append(prob_value)
                self.experiment_results['temperatures'].append(temp)

            temp = self.update_temperature(temp, i)
            i += 1

        
        
        

