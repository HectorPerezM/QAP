import random
import math

class SA:
    def __init__(self, problem, cooling, iter_per_temp, temp_initial, temp_min):
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


        #TODO: quizas poner como parametro configurable
        self.beta = 10
        self.alpha = 0.1

    


    def acceptance_prob(self, delta_E, temp):
        n = random.uniform(0,1)
        value = math.exp(-(delta_E/temp))
        if value >= n:
            return True
        else:
            return False


    def update_temperature(self, iteration):
        new_temp = 0

        print(iteration)
        #Depends on choseen cooling
        if self.cooling == "linear":
            new_temp = self.temp_initial - (iteration * self.beta)
        elif self.cooling == "geometric":
            new_temp = self.alpha * self.temp[-1]
        elif self.cooling == "logaritmic":
            new_temp = (self.temp_initial)/math.log(iteration)
        else:
            #None above, default is Linear
            new_temp = self.temp_initial - (iteration * self.beta)
        
        print("old_temp: {} | new_temp: {}".format(self.temp[-1], new_temp))
        self.temp.append(new_temp)


    def generateRandomNeighbour(self, currently_solution):
        neighborhood = []
        m = len(currently_solution)

        for i in range(m-1):
            for j in range(i+1, m):
                neighbour = self.qap.exchange(currently_solution, i, j)
                neighborhood.append(neighbour)

        
        return random.choice(neighborhood)


    def run(self):
        delta_E = 0
        i = 1
        currently_solution = self.qap.initial_solution
        of_value = self.qap.objectiveFunction(currently_solution, self.qap.fmatrix, self.qap.dmatrix)

        #Always access last temperature
        while self.temp_min < self.temp[-1]:
            for j in range(self.iter_per_temp):
                new_sol = self.generateRandomNeighbour(currently_solution)
                new_of_value = self.qap.objectiveFunction(new_sol, self.qap.fmatrix, self.qap.dmatrix)

                # print("[new_sol]: {}".format(new_sol))
                # print("[currently_sol]: {}".format(currently_solution))

                print("[of_value]: {}".format(of_value))
                print("[new_of_value]: {}".format(new_of_value))
                # print(self.temp)

                delta_E = new_of_value - of_value
                if delta_E <= 0:
                    currently_solution = new_sol
                    of_value = new_of_value

                else:
                    if self.acceptance_prob(delta_E, self.temp[-1]):
                        currently_solution = new_sol
                        of_value = new_of_value

            self.update_temperature(i)
            i += 1
        

        print("-------------------")
        print("Final OF: {}".format(of_value))
        print("Final Solutiion: {}".format(currently_solution))

