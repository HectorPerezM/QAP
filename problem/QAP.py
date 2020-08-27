import random

class QAP:
    def __init__(self, type_initial_solution, fmatrix, dmatrix):
        self.fmatrix = fmatrix
        self.dmatrix = dmatrix
        self.solution_size = len(fmatrix) 

        self.type_initial_solution = type_initial_solution
        self.initial_solution = []
    


    #Initial Solution
    def randomInitalSolution(self, num_facilities):
        all_facilities = list(range(1, num_facilities + 1))
        random.shuffle(all_facilities)
        return all_facilities



    def generateInitialSolution(self):
        #Initial solution for SA
        if self.type_initial_solution == "random":
            self.initial_solution = self.randomInitalSolution(len(self.fmatrix))
            return True

        #Initial solution (Generation) for GA
        elif self.type_initial_solution == "randomGA":
            self.initial_solution = self.randomInitialPopulation(len(self.fmatrix))
            return True
            
        else:
            return False


    #Neighbourhood generators
    def generateRandomNeighbour(self, currently_solution):
        neighborhood = []
        m = len(currently_solution)

        for i in range(m-1):
            for j in range(i+1, m):
                neighbour = self.exchange(currently_solution, i, j)
                neighborhood.append(neighbour)

        
        return random.choice(neighborhood)


    # QAP Operators
    def exchange(self, s, i, j):
        x = list(s)
        x[i] = s[j]
        x[j] = s[i]
        return x


    # Objective Function
    def objectiveFunction(self, permutations):
        m = len(permutations)
        total = 0

        for i in range(m):
            for j in range(m):
                iD = permutations[i] - 1
                jD = permutations[j] - 1

                d = self.dmatrix[iD][jD]
                f = self.fmatrix[i][j]

                total += f*d
        
        return total