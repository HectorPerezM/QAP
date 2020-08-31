import random

class QAP:
    def __init__(self):
        self.fmatrix = []
        self.dmatrix = []
        self.solution_size = 0
        
    def readData(self, config):
        if config['dataset_name'] == "":
            print('dataset_name is empty.')
            exit()
        
        #read test data
        elif config['dataset_name'] == "chr12a":
            raw_f_data = open(config['data_path'] + "/FChr12a.txt", "r")
            for line in raw_f_data:
                aux = list(map(int, line.split()))
                self.fmatrix.append(aux)
                
            raw_d_data = open(config['data_path'] + "/DChr12a.txt", "r")
            for line in raw_d_data:
                aux = list(map(int, line.split()))
                self.dmatrix.append(aux)

            self.solution_size = len(self.fmatrix)
        
        elif config['dataset_name'] == "chr18a":
            raw_f_data = open(config['data_path'] + "/FChr18a.txt", "r")
            for line in raw_f_data:
                aux = list(map(int, line.split()))
                self.fmatrix.append(aux)
                
            raw_d_data = open(config['data_path'] + "/DChr18a.txt", "r")
            for line in raw_d_data:
                aux = list(map(int, line.split()))
                self.dmatrix.append(aux)

            self.solution_size = len(self.fmatrix)
        
        elif config['dataset_name'] == "chr25a":
            raw_f_data = open(config['data_path'] + "/FChr25a.txt", "r")
            for line in raw_f_data:
                aux = list(map(int, line.split()))
                self.fmatrix.append(aux)
                
            raw_d_data = open(config['data_path'] + "/DChr25a.txt", "r")
            for line in raw_d_data:
                aux = list(map(int, line.split()))
                self.dmatrix.append(aux)

            self.solution_size = len(self.fmatrix)
        
        elif config['dataset_name'] == "esc64a":
            raw_f_data = open(config['data_path'] + "/FEsc64a.txt", "r")
            for line in raw_f_data:
                aux = list(map(int, line.split()))
                self.fmatrix.append(aux)
                
            raw_d_data = open(config['data_path'] + "/DEsc64a.txt", "r")
            for line in raw_d_data:
                aux = list(map(int, line.split()))
                self.dmatrix.append(aux)

            self.solution_size = len(self.fmatrix)

        else:
            print('No existe el archivo de datos.')
            exit()


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


    def generateNeighbour(self, currently_solution):
        i = random.randint(2, len(currently_solution) - 1)
        j = random.randint(0, len(currently_solution) - i)
        currently_solution[j: (j + i)] = reversed(currently_solution[j: (j + i)])
        return(currently_solution)

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