import random

class QAP:
    def __init__(self, type_initial_solution, fmatrix, dmatrix):
        self.fmatrix = fmatrix
        self.dmatrix = dmatrix
        
        self.type_initial_solution = type_initial_solution
        self.initial_solution = []
    

    def randomInitalSolution(self, num_facilities):
        all_facilities = list(range(1, num_facilities + 1))
        random.shuffle(all_facilities)
        return all_facilities


    def generateInitialSolution(self):
        if self.type_initial_solution == "random":
            return self.randomInitalSolution(len(self.fmatrix))
        else:
            print("Not implemented yet.")


    def exchange(self, s, i, j):
        x = list(s)
        x[i] = s[j]
        x[j] = s[i]
        return x


    def objectiveFunction(self, permutations, fmatrix, dmatrix):
        m = len(permutations)
        total = 0

        for i in range(m):
            for j in range(m):
                iD = permutations[i] - 1
                jD = permutations[j] - 1

                d = dmatrix[iD][jD]
                f = fmatrix[i][j]

                total += f*d
        
        return total