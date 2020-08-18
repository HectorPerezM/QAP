import random
import math
import time

class SA:
    def __init__(self, problem, max_iter, cooling, iter_per_temp, temp_initial, temp_min, beta, alpha):
        #Set max_iter if temp condition doesnt end
        self.max_iter = max_iter

        #Set initial solution
        #self.initial_solution = initial_solution
        self.qap = problem

        #Type of cooling: "Linear", "Geometric" or "Logaritmic"
        self.cooling = cooling
        
        #Iterations per temperature
        self.iter_per_temp = iter_per_temp

        #Set temperatures
        self.temp_initial = temp_initial
        self.temp_min = temp_min
        self.temp = [temp_initial]

        #Used in cooling functions
        self.beta = beta
        #Alpha mus be between ]0, 1[, othewise forced to 0.5
        if alpha <= 0 or alpha >= 1:
            self.alpha = 0.5
        else:
            self.alpha = alpha

        self.of_list = []
        self.total_iterations = 0

        #To control time
        self.time_per_iteration = []
        self.total_time = 0


    def acceptance_prob(self, delta_E, temp):
        n = random.uniform(0,1)
        value = math.exp(-(delta_E/temp))
        if value >= n:
            return True
        else:
            return False


    def update_temperature(self, iteration):
        new_temp = 0

        #Depends on choseen cooling
        if self.cooling == "linear":
            new_temp = self.temp_initial - (iteration * self.beta)
        elif self.cooling == "geometric":
            new_temp = self.alpha * self.temp[-1]
        elif self.cooling == "logaritmic":
            #case log(1) = 0
            if iteration == 1:
                new_temp = self.temp_initial
            else:
                new_temp = (self.temp_initial)/math.log(iteration)
        else:
            #None above, default is Linear
            new_temp = self.temp_initial - (iteration * self.beta)

        self.temp.append(new_temp)


    


    def run(self):
        delta_E = 0
        i = 1
        currently_solution = self.qap.initial_solution
        of_value = self.qap.objectiveFunction(currently_solution)

        self.of_list.append(of_value)

        #Always access last temperature
        start_time_total = time.time()

        while self.temp_min < self.temp[-1] and i < self.max_iter:
            
            start_time_iterations = time.time()
            for j in range(self.iter_per_temp):
                new_sol = self.qap.generateRandomNeighbour(currently_solution)
                new_of_value = self.qap.objectiveFunction(new_sol)

                delta_E = new_of_value - of_value
                if delta_E <= 0:
                    currently_solution = new_sol
                    of_value = new_of_value

                else:
                    if self.acceptance_prob(delta_E, self.temp[-1]):
                        currently_solution = new_sol
                        of_value = new_of_value
            
            self.time_per_iteration.append(time.time() - start_time_iterations)

            self.of_list.append(of_value)
            self.update_temperature(i)
            i += 1
        
        self.total_time = time.time() - start_time_total
        print("-------------------")
        print("Total Time: {}".format(self.total_time))
        print("Final OF: {}".format(of_value))
        print("Final Solutiion: {}".format(currently_solution))

        self.total_iterations = i

        

