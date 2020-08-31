import math
import random
import time

class GA:

    def __init__(self, problem, config):
        #GA for QAP problem
        self.qap = problem
        
        #Config parameters
        self.type_initial_solution = config['type_initial_solution']
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
        
        if config['selection_criteria'] == 'random':
            self.size_random_selection = config['random_selection']
        else:
            self.size_random_selection = 0
        
        if config['selection_criteria'] == 'best_percentage':
            self.size_random_selection = config['best_pct']
        else:
            self.size_random_selection = 0

        self.mutation_chance = config['mutation_chance']

        self.mean_all_of_value = 0
        self.mean_best_of_value = 0
        self.mean_time_per_iter = 0
        self.total_time = 0

        self.results = {
            'population_of_best': [],
            'mean_generation': [],
            'time_per_gen': []
        }
    


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
        
        return population


    def generateInitialPopulation(self):
        if self.type_initial_solution == "random":
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


    def bestPercentageSelection(self):
        exit()


    def selectionCriteria(self):
        if self.selection_criteria == "random":
            return self.randomSelection()
        
        elif self.selection_criteria == 'tournament':
            return self.tournamentSelection()
        
        elif self.selection_criteria == 'best_percentage':
            return self.bestPercentageSelection()
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
        chance = random.random()
        if chance < self.mutation_chance:
           #Swap mutation
           i = random.randint(0, (self.qap.solution_size - 1))
           j = random.randint(0, (self.qap.solution_size - 1))

           x = child['solution'][i]
           y = child['solution'][j]

           child['solution'][i] = y
           child['solution'][j] = x

        return child


    def one_point_crossover(self, parent1, parent2):
        child1 = {
            'fitness': 0,
            'solution': [0] * self.qap.solution_size
        }

        child2 = {
            'fitness': 0,
            'solution': [0] * self.qap.solution_size
        }
        
        
        i = random.randint(1, (math.floor(self.qap.solution_size/2) - 1))
        j = random.randint(math.floor(self.qap.solution_size/2), (self.qap.solution_size - 1))
        
        
        #Child1
        selected_values = parent1['solution'][i:j]
        child1['solution'][i:j] = selected_values
        parent2_values = []
        for m in range(len(parent2['solution'])):
            if not parent2['solution'][m] in selected_values:
                parent2_values.append(parent2['solution'][m])
        
        
        k = 0
        for m in range(len(child1['solution'])):
            if child1['solution'][m] == 0:
                child1['solution'][m] = parent2_values[k]
                k += 1 
            
        
        #Child2
        selected_values = parent2['solution'][i:j]
        child2['solution'][i:j] = selected_values
        
        
        parent1_values = []
        for n in range(len(parent1['solution'])):
            if not parent1['solution'][n] in selected_values:
                parent1_values.append(parent1['solution'][n])
        
    
        k = 0
        for m in range(len(child2['solution'])):
            if child2['solution'][m] == 0:
                child2['solution'][m] = parent1_values[k]
                k += 1 

        return child1, child2


    def reproducePopulation(self, selected_population):
        new_population = []
        reproduction_times = 100

        for i in range(reproduction_times):
            index_parent1 = random.randint(0, (len(selected_population) - 1))
            index_parent2 = random.randint(0, (len(selected_population) - 2))

            #Check that parent1 is not the same as parent2
            if index_parent1 == index_parent2:
                index_parent2 += 1
            
            parent1 = selected_population[index_parent1]
            parent2 = selected_population[index_parent2]
            # print("--------")
            # print(f"{parent1}")
            # print(f"{parent2}")
            # print("-******-")
            child1, child2 = self.one_point_crossover(parent1, parent2)

            #Mutate childs
            child1 = self.mutateChild(child1)
            child2 = self.mutateChild(child2)

            new_population.append(child1)
            new_population.append(child2)
        
        return new_population

    """
    def reproducePopulation(self, selected_population):
        #1 Point CrossOver

        new_population = selected_population.copy()


        #Take a parent, select a portion of his solution, and create a new child
        m = len(selected_population) 

        #Los indices de la solucion se dejaron fijos entre el 30% y el 60% de la solucion 
        first_index = math.floor(self.qap.solution_size * 0.3)
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
    """


    def findBestInPopulation(self, population):
        best_index = 0
        best_value = 999999999
        m = len(population)

        for p in range(m):
            if population[p]['fitness'] <= best_value:
                best_index = p
                best_value = population[p]['fitness']

        self.results['population_of_best'].append(population[best_index]['fitness']) 


    def replacePopulation(self, new_population):
        all_population = new_population.copy()
        all_population.extend(self.population)

        #Sort best_population
        all_population = sorted(all_population, key=lambda k: k['fitness'])
        best = []
        for i in range(self.size_population):
            best.append(all_population[i])
        
        return best
    

    def calculateMeanPopulation(self):
        total = 0
        m = len(self.population)
        for i in range(m):
            total += self.population[i]['fitness']

        self.results['mean_generation'].append((total/m))


    def getMean(self, values):
        m = len(values)
        total = 0
        for i in range(m):
            total += values[i]
        
        return round(total/m)


    def run(self):
        #Initial population
        self.generateInitialPopulation()

        # print("----- Initial population. ---------")
        # self.printPopulation(10)
        # print("------------------------------------")

        new_population = []
        t = 0

        start_total = time.time()

        #Termination critearia
        while t < self.total_generations:
            start_time_iterations = time.time()

            #Evaluate population
            self.evaluatePopulation(self.population)
            #Select new population
            selected_population = self.selectionCriteria()


            #Reproduction
            new_population = self.reproducePopulation(selected_population)
            self.evaluatePopulation(new_population)
            final_population = self.replacePopulation(new_population)

            #Find best in generation
            self.findBestInPopulation(final_population)
            self.population = final_population.copy()
            self.evaluatePopulation(self.population)
            self.calculateMeanPopulation()

            self.results['time_per_gen'].append(time.time() - start_time_iterations)
        
            t += 1
        

        self.mean_all_of_value = self.getMean(self.results['mean_generation'])
        self.mean_best_of_value = self.getMean(self.results['population_of_best'])
        self.mean_time_per_iter = self.getMean(self.results['time_per_gen'])
        self.total_time = time.time() - start_total

