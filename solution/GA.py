import math
import random

class GA:

    def __init__(self, problem, config):
        #GA for QAP problem
        self.qap = problem
        
        #Config parameters
        
        #Population
        self.total_generations = config['total_generations']
        self.size_population = config['size_population']
        self.population = []

        #Selection criteria
        self.selection_criteria = config['selection_criteria']
        if config['selection_criteria'] == 'tournament':
            self.tournament_size = config['tournament_size']
            self.tournament_times = config['tournament_times']
        else:
            self.tournament_size = 0
            self.tournament_times = 0


        self.mutation_chance = config['mutation_chance']
        self.best_generation = []
    


    def printPopulation(self, number):
        for i in range(number):
            print(f"    {self.population[i]}")

    def randomInitialPopulation(self):
        population = []
        for _ in range(self.size_population):
            individual = {
                'fitness': 0,
                'solution': self.qap.randomInitalSolution(len(self.qap.fmatrix))
            }

            population.append(individual)
        
        print(f"randomInitialPopulation: {len(population)}")
        return population

    def generateInitialPopulation(self):
        if self.qap.type_initial_solution == "randomGA":
            self.population = self.randomInitialPopulation()

    def rouletteSelection(self):
        m = len(self.population)
        total_fitness = 0

        for i in range(m):
            total_fitness += self.population[i]['fitness']
        
        for i in range(m):
            self.population[i]['selection_prob'] = self.population[i]['fitness'] / total_fitness
        
        return []
    
    def bestOfTournament(self, tournament):
        best_index = 0
        best_value = 0
        m = len(tournament)

        for i in range(m):
            if tournament[i]['fitness'] <= best_value:
                best_index = i
                best_value = tournament[i]['fitness']
        
        return tournament[best_index]

    def tournamentSelection(self):
        new_population = []

        #tournament repeats mu times
        for _ in range(self.tournament_times):
            #Selected for the tournament:
            tournament = []
            for _ in range(self.tournament_size):
                index = random.randint(0, (self.size_population - 1))
                tournament.append(self.population[index])
            
            #Get the best of the tournament
            best = self.bestOfTournament(tournament)
            new_population.append(best)
            
        return new_population

    def selectionCriteria(self):
        if self.selection_criteria == "roulette":
            return self.rouletteSelection()
        
        elif self.selection_criteria == 'tournament':
            return self.tournamentSelection()
        
        else:
            return []


    #Evalua cada individuo y guarda su indice/valor en evaluation, luego lo ordena
    def evaluatePopulation(self, population):
        m = len(population)

        for i in range(m):
            of_value = self.qap.objectiveFunction(population[i]['solution'])
            population[i]['fitness'] = of_value

        
        #self.evaluation = sorted(self.evaluation, key=lambda k: k['of_value'])


    def mutateChild(self, child):
        chance = random.uniform(0, 1)
        if chance <= self.mutation_chance:
           #Swap mutation
           i = random.randint(0, (self.qap.solution_size - 1))
           j = random.randint(0, (self.qap.solution_size - 1))

           x = child['solution'][i]
           y = child['solution'][j]

           child['solution'][i] = y
           child['solution'][j] = x
        
        return child


    def reproducePopulation(self, selected_population):
        new_population = selected_population.copy()


        #Take a parent, select a portion of his solution, and create a new child
        m = len(selected_population) 

        #Los indices de la solucion se dejaron fijos entre el 20% y el 60% de la solucion 
        first_index = math.floor(self.qap.solution_size * 0.2)
        second_index = math.floor(self.qap.solution_size * 0.6)

        for i in range(m):
            extracted_numbers = selected_population[i]['solution'][first_index : second_index + 1]
            child = [0] * self.qap.solution_size

            child[first_index : second_index + 1] = extracted_numbers

            #Obtener numeros restantes
            all_facilities = list(range(1, self.qap.solution_size + 1))
            not_in_child = []
            for j in range(len(all_facilities)):
                if not all_facilities[j] in child:
                    not_in_child.append(all_facilities[j])
            
            #Insertar numeros
            k = 0
            second_index += 1
            while second_index < len(child):
                child[second_index] = not_in_child[k]
                k += 1
                second_index += 1
            

            z = 0
            while z < first_index:
                child[z] = not_in_child[k]
                k += 1
                z += 1
            
            new_child = {
                'fitness': 0,
                'solution': child
            }

            new_child = self.mutateChild(new_child)

            new_population.append(new_child)
        
        if len(new_population) < self.size_population:
            print("La poblacion se redujo, error!")
            exit()
        
        return new_population


    def findBestInPopulation(self, population):
        best_index = 0
        best_value = 9999999
        m = len(population)

        for p in range(m):
            if population[p]['fitness'] <= best_value:
                best_index = p
                best_value = population[p]['fitness']

        self.best_generation.append(population[best_index]['fitness']) 

        
    def run(self):
        #Initial population
        self.generateInitialPopulation()

        print("----- Initial population. ---------")
        self.printPopulation(10)
        print("------------------------------------")

        new_population = []
        t = 0
        
        #Termination critearia
        while t < self.total_generations:
            #Evaluate population
            self.evaluatePopulation(self.population)

            print(f"---- Gen: {t} --")
            self.printPopulation(10)
            # print(len(self.population))
            print("-----------------")

            #Select new population
            new_population = self.selectionCriteria()

            #Reproduction
            new_population = self.reproducePopulation(new_population)

            self.evaluatePopulation(new_population)

            #Find best in generation
            self.findBestInPopulation(new_population)

            self.population = new_population.copy()

            t += 1


        print("Finished GA")
        print(self.best_generation)
        
        #Return best indidual or best population