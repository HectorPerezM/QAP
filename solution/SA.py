import random
import math
import time
import numpy as np


class SA:
    def __init__(self, problem, config, number_exp, number_config):
        #QAP
        self.qap = problem
        self.type_initial_solution = config['type_initial_solution']
        self.neighbour_selection = config['neighbour_selection']
        
        self.cooling = config['cooling']
        self.max_iter = 1000
        self.iter_per_temp = config['iter_per_temp']

        #Set temperatures
        self.temp_initial = config['temp_initial']
        self.temp_min = config['temp_min']

        #Used in cooling functions
        # if self.cooling == 'linear':
        #     self.beta = config['beta']
        # else:
        #     self.beta = 0
        self.beta = 150

        #Alpha mus be between ]0, 1[, othewise forced to 0.5
        if self.cooling == 'geometric':
            if config['alpha'] <= 0 or config['alpha'] >= 1:
                self.alpha = 0.5
            else:
                self.alpha = config['alpha']
        else:
            self.alpha = 0


        self.mean_best_of_value = 0
        self.mean_all_of_value = 0
        self.mean_time_per_iter = 0
        self.total_time = 0

        self.results = {
            "nro_exp": number_exp,
            "nro_config": number_config,
            'dataset': config['dataset_name'],
            'iter_per_temp': config['iter_per_temp'],
            'temp_initial': config['temp_initial'],
            'temp_min': config['temp_min'],
            'alpha': config['alpha'],
            "cooling": config['cooling'],
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
                if iteration == 1:
                    t = self.temp_initial
                    return t
                else:
                    t = (self.temp_initial)/math.log(iteration)
                    return t
            else:
                return 0


    def getMean(self, values):
        m = len(values)
        total = 0
        for i in range(m):
            total += values[i]
        
        return round(total/m)


    def run(self):
        solution = self.generateInitialSolution()
        of_value = self.qap.objectiveFunction(solution)
        
        best_of_value = of_value
        best_solution = solution.copy()

        self.results['of_values'].append(of_value)
        self.results['best_of_values'].append(best_of_value)
        self.results['solutions'].append(list(solution))
        self.results['best_solutions'].append(list(best_solution))

        temp = self.temp_initial
        self.results['temperatures'].append(temp)

        i = 1
        start_total = time.time()
        while temp > self.temp_min:
            start_time_iterations = time.time()
            self.results['iteration'].append(i)

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
                
                self.results['time_per_iteration'].append(time.time() - start_time_iterations)
                
                self.results['of_values'].append(of_value)
                self.results['best_of_values'].append(best_of_value)
                
                self.results['solutions'].append(solution)
                self.results['best_solutions'].append(best_solution)

                self.results['probabilities'].append(prob_value)
                self.results['temperatures'].append(temp)

            temp = self.update_temperature(temp, i)
            i += 1
        

        self.mean_all_of_value = self.getMean(self.results['of_values'])
        self.mean_best_of_value = self.getMean(self.results['best_of_values'])
        self.mean_time_per_iter = self.getMean(self.results['time_per_iteration'])
        self.total_time = time.time() - start_total

        
        
        

