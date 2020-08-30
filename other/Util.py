import json
import matplotlib.pyplot as plt
import csv
import os
import shutil

class Util:
    def __init__(self):
        self.selected_config = 0
        self.config_path = ""

    def readJSON(self):
        if self.config_path == "":
            print("Empty config path.")
            exit()
        
        with open(self.config_path) as f:
            data = json.load(f)
        
        return data

    def getConfig(self):
        print('Escoge configuracion: ')
        print(' 1. Simulated Annealing')
        print(' 2. Genetic Algorithm')

        self.selected_config = int(input('Seleccion: '))
        if self.selected_config == 1:
            self.config_path = 'config/config_SA.json'
        elif self.selected_config == 2:
            self.config_path = 'config/config_GA.json'
        else:
            print('Bad choice.')
            exit()
        
        config = self.readJSON()
        return config

    def configureResultsFolder(self, config):
        #results_path
        if not os.path.isdir(config['results_path']):
            try:
                os.makedirs(config['results_path'])
            except OSError:
                print("Creation of the directory %s failed" % config['results_path'])
        else:
            shutil.rmtree(config['results_path'])
            try:
                os.makedirs(config['results_path'])
            except OSError:
                print("Creation of the directory %s failed" % config['results_path'])


        #check images folder
        images_folder = config['results_path'] + config['images_path']
        if not os.path.isdir(images_folder):
            try:
                os.makedirs(images_folder)
            except OSError:
                print("Creation of the directory %s failed" % config['results_path'])
    

    def saveResults(self, config_number, e, config, solver):
        if config['metaheuristic'] == 'simulated_annealing':
            with open(config['results_path'] + config['csv_path'] + str(config_number) + "_" +str(e) + ".csv", 'a') as csv_file:
                writer = csv.writer(csv_file, delimiter=',')

                for i in range(len(solver.experiment_results['iteration'])):
                    writer.writerow([config_number, 
                                    e, 
                                    solver.experiment_results['iteration'][i],
                                    solver.experiment_results['of_values'][i],
                                    solver.experiment_results['best_of_values'][i],
                                    solver.experiment_results['solutions'][i],
                                    solver.experiment_results['best_solutions'][i],
                                    solver.experiment_results['temperatures'][i],
                                    solver.experiment_results['time_per_iteration'][i],
                                    solver.experiment_results['probabilities'][i]])

        if config['metaheuristic'] == 'genetic_algorithm':
            exit()

    def savePlot(self, config_number, e, config, solver):
        if config['metaheuristic'] == "simulated_annealing":
            plt.figure(1, figsize=(10,10))
            plt.subplot(4, 1, 1)
            best = plt.plot(solver.experiment_results['of_values'])
            plt.setp(best,"linestyle","none","marker",".","color","b","markersize","1")
            plt.title("Simulated Annealing QAP: " + config['dataset_name']) 
            plt.ylabel("Objective Value")
            
            plt.subplot(4, 1, 2)
            grafico = plt.plot(solver.experiment_results['best_of_values'])
            plt.setp(grafico,"linestyle","none","marker","s","color","r","markersize","1")
            plt.ylabel("Objective Value")

            plt.subplot(4, 1, 3)
            grafico = plt.plot(solver.experiment_results['temperatures'])
            plt.setp(grafico,"linestyle","none","marker","s","color","orange","markersize","1")
            plt.ylabel("Temperature")
            
            plt.subplot(4, 1, 4)
            grafico = plt.plot(solver.experiment_results['probabilities'])
            plt.setp(grafico,"linestyle","none","marker","o","color","g","markersize","1")
            plt.ylabel("Probability")

            # plt.subplot(5, 1, 5)
            # grafico = plt.plot(solver.experiment_results['time_per_iteration'])
            # plt.setp(grafico,"linestyle","none","marker",".","color","black","markersize","1")
            # plt.ylabel("Time")
            
            path_to_save = config['results_path'] + config['images_path'] + str(config_number) + "_" +str(e) + ".png"
            plt.savefig(path_to_save)
            plt.clf()
        
        if config['metaheuristic'] == "genetic_algorithm":
            plt.figure(1, figsize=(10,10))
            plt.subplot(1, 1, 1)
            best = plt.plot(solver.experiment_results['of_values'])
            plt.setp(best,"linestyle","none","marker",".","color","b","markersize","1")
            plt.title("Genetic Algorithm QAP: " + config['dataset_name']) 
            plt.ylabel("Objective Value")


            path_to_save = config['results_path'] + config['images_path'] + str(config_number) + "_" +str(e) + ".png"
            plt.savefig(path_to_save)
            plt.clf()
            
            

    def readDataFiles(self, path=""):
        if path == "":
            print("Empty path.")
            return []

        print(path)
        
        data_file = open(path, "r")
        data = []
        for line in data_file:
            aux = list(map(int, line.split()))
            data.append(aux)
        
        return data


   
    def selectedConfigFile(self):
        print("Select your configuration file: ")
        print(" 1. Simmulated Annealing configuration")
        print(" 2. Genetic Algorithm configuration")
        print(" 3. other configuration (default SA config)")

        selection = -1
        options = [*range(1,4)]
        
        while selection not in options:
            try:
                selection = int(input("Selection: "))
            except ValueError:
                selection = -1
        
        #TODO cambiar cuando corresponda
        path = ""
        if selection == 1:
            path = "./config/config_SA.json"
        elif selection == 2:
            path = "./config/config_GA.json"
        else:
            path = "./config/config_SA.json"
            
        return path, selection


    def readConfigFile(self, config_path=""):
        if config_path == "":
            print("Empty config path.")
            return []
        
        with open(config_path) as f:
            data = json.load(f)
        
        print(data)
        return data
        

    # def configFileInfo(self):
    #     print("### How to use config file ###")
    #     print(" - Posible values are: ")
    #     print("     'initial_solution': ['random', 'heuristic']")
    #     print("     'neighbour_selection': ['firstBest', 'bestRandom', 'bestImprovement']")
    #     print("")

    
    # def plot(self, config, title, xAxis, yAxis, values, e, subname):
    #     fig = plt.plot(values)
    #     plt.setp(fig,"linestyle","none","marker",".","color","b")
    #     plt.title(title) 
    #     plt.ylabel(yAxis)
    #     plt.xlabel(xAxis)

    #     path_to_save = config['results_path'] + config['images_path'] + str(e) + "_" + subname + ".png"
    #     plt.savefig(path_to_save)
    #     plt.clf()
        

    # def createEmptyCsv(self, path):
    #     fields = ['nro_experiment', 'dataset', 'cooling', 'max_iter', 'iter_per_tem', 'temp_initial', 'temp_min', 'solution', 'fo_value']
    #     with open(path, 'w') as csv_file:
    #         writer = csv.writer(csv_file)
    #         writer.writerow(fields)
    

    """
        csv:

        nro_exp, dataset, cooling, max_iter, iter_per_temp, temp_initial, temp_min, solution, fo_value, time
    """
    # def saveResults(self, solver, e, config):
    #     if config['metaheuristic'] == 'SA':
    #         with open(config['results_path'] + config['csv_path'], 'a') as csv_file:
    #             writer = csv.writer(csv_file, delimiter=',')
    #             writer.writerow([e, config['dataset_name'], solver.cooling,
    #                             solver.max_iter, solver.iter_per_temp, solver.temp_initial,
    #                             solver.temp_min, solver.solution, solver.of_list[-1], solver.total_time])
        
    #     elif config['metaheuristic'] == 'GA':
    #         print('-----')

    #     else:
    #         print('------')

    
    # def savePlot(self, solver, e, config):
    #     plt.figure(1)
    #     plt.subplot(3, 1, 1)
    #     best = plt.plot(solver.best_ofvalues)
    #     plt.setp(best,"linestyle","none","marker",".","color","b","markersize","1")
    #     plt.title("Simulated Annealing QAP: " + config['dataset_name']) 
    #     plt.ylabel("Valor objetivo")
        
    #     plt.subplot(3, 1, 2)
    #     grafico = plt.plot(solver.of_list)
    #     plt.setp(grafico,"linestyle","none","marker","s","color","r","markersize","1")
    #     plt.ylabel("Valor objetivo")
        
    #     plt.subplot(3, 1, 3)
    #     grafico = plt.plot(solver.probabilities)
    #     plt.setp(grafico,"linestyle","none","marker","o","color","g","markersize","1")
    #     plt.ylabel("Probability")
        
    #     path_to_save = config['results_path'] + config['images_path'] + str(e) + ".png"
    #     plt.savefig(path_to_save)
    #     plt.clf()
    #     #plt.xlabel("Valor Óptimo : " + str(mejorObjetivo))


        
        
        
        # self.plot(config, 'Simmulated Annealing ' + config['dataset_name'], 'Iterations', 'Objective Function', solver.of_list, e, 'of')
        # self.plot(config, 'Simmulated Annealing ' + config['dataset_name'], 'Iterations', 'Temperature', solver.temp, e, 'temp')
        # self.plot(config, 'Simmulated Annealing ' + config['dataset_name'], 'Iterations', 'Time (s)', solver.time_per_iteration, e, 'time')


    def createResultFolder(self, config):
        #results_path
        if not os.path.isdir(config['results_path']):
            try:
                os.mkdir(config['results_path'])
            except OSError:
                print("Creation of the directory %s failed" % config['results_path'])
        else:
            shutil.rmtree(config['results_path'])
            try:
                os.mkdir(config['results_path'])
            except OSError:
                print("Creation of the directory %s failed" % config['results_path'])


        #check images folder
        images_folder = config['results_path'] + config['images_path']
        if not os.path.isdir(images_folder):
            try:
                os.mkdir(images_folder)
            except OSError:
                print("Creation of the directory %s failed" % config['results_path'])

