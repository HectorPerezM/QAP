import math

class GA:

    def __init__(self, problem, total_iteration):
        #GA for QAP problem
        self.qap = problem
        
        #CONFIGURABLE PARAMETERS
        self.select_first_best = int(math.floor((0.3*self.qap.amount_population)))

        self.total_iteration = total_iteration
        self.population = []
        self.evaluation = []
        




    def selectionCriteria(self):
        #Get the x% of the best actual population
        new_population = []
        
        for i in range(self.select_first_best):
            index = self.evaluation[i]["index"]
            new_population.append(self.population[index])
        
        return new_population

    #Evalua cada individuo y guarda su indice/valor en evaluation, luego lo ordena
    def evaluatePopulation(self):
        m = len(self.population)
        for i in range(m):
            of_value = self.qap.objectiveFunction(self.population[i])
            aux = {"index": i, "of_value": of_value}
            self.evaluation.append(aux)

        
        self.evaluation = sorted(self.evaluation, key=lambda k: k['of_value']) 
        
        
    def run(self):
        #Initial population
        self.population = self.qap.initial_solution
        new_population = []
        t = 99
        
        #Termination critearia
        while t < self.total_iteration:
            self.evaluation = []

            #Evaluate population
            self.evaluatePopulation()

            #Select new population
            new_population = self.selectionCriteria()

            #Reproduction

            #Evaluation of new generation

            #Replace critiria


            t += 1


        print("Finished GA")
        
        #Return best indidual or best population