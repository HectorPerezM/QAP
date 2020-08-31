import json
import matplotlib.pyplot as plt
import csv
import os
import shutil
import glob

class Util:
    def __init__(self):
        self.selected_config = 0
        self.config_path = ""
        self.results_path = "./results/"
        self.experiment = []


    def readJSON(self, path):
        with open(path) as f:
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
        
        config = self.readJSON(self.config_path)
        return config


    def configureResultsFolder(self):
        #results_path
        if not os.path.isdir(self.results_path):
            os.makedirs(self.results_path)
            os.makedirs(self.results_path + "sa/")
            os.makedirs(self.results_path + "ga/")
            
        else:
            shutil.rmtree(self.results_path)
            os.makedirs(self.results_path)
            os.makedirs(self.results_path + "sa/")
            os.makedirs(self.results_path + "ga/")

        #check images folder
        sa_images_folder = self.results_path + 'sa/images/'
        if not os.path.isdir(sa_images_folder):
            os.makedirs(sa_images_folder)
        
        ga_images_folder = self.results_path + 'ga/images/'
        if not os.path.isdir(ga_images_folder):
            os.makedirs(ga_images_folder)
            

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
            plt.subplot(5, 1, 1)
            best = plt.plot(solver.experiment_results['of_values'])
            plt.setp(best,"linestyle","none","marker",".","color","b","markersize","1")
            plt.title("Simulated Annealing QAP: " + config['dataset_name']) 
            plt.ylabel("Objective Value")
            
            plt.subplot(5, 1, 2)
            grafico = plt.plot(solver.experiment_results['best_of_values'])
            plt.setp(grafico,"linestyle","none","marker","s","color","r","markersize","1")
            plt.ylabel("Objective Value")

            plt.subplot(5, 1, 3)
            grafico = plt.plot(solver.experiment_results['temperatures'])
            plt.setp(grafico,"linestyle","none","marker","s","color","orange","markersize","1")
            plt.ylabel("Temperature")
            
            plt.subplot(5, 1, 4)
            grafico = plt.plot(solver.experiment_results['probabilities'])
            plt.setp(grafico,"linestyle","none","marker","o","color","g","markersize","1")
            plt.ylabel("Probability")

            # plt.subplot(5, 1, 5)
            # grafico = plt.plot(solver.experiment_results['MSE'])
            # plt.setp(grafico,"linestyle","none","marker",".","color","black","markersize","1")
            # plt.ylabel("Error")
            
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


    # def readJSON(self, path=""):
    #     if path == "":
    #         print("Empty config path.")
    #         return []
        
    #     with open(path) as f:
    #         data = json.load(f)
        
    #     return data
    

    def wirteResults(self, dataset, nro_config):
        if self.selected_config == 1:
            path = f"./results/sa/{dataset}_{nro_config}.json"

            with open(path, 'w') as fp:
                json.dump(self.experiment, fp)
        
        if self.selected_config == 2:
            path = f"./results/ga/{dataset}_{nro_config}.json"

            with open(path, 'w') as fp:
                json.dump(self.experiment, fp)

    
    def saveBoxplot(self,dataset, nro_config, label_type):
        #best of val
        best_high = []
        best_medium = []
        best_low = []

        #all of val
        all_high = []
        all_medium = []
        all_low = []

        #total time
        total_time_high = []
        total_time_medium = []
        total_time_low = []

        i = nro_config
        max_config = i+3
        while i < max_config:
            if self.selected_config == 1:
                path = f"./results/sa/{dataset}_{i}.json"
            if self.selected_config == 2:
                path = f"./results/ga/{dataset}_{i}.json"

            data = self.readJSON(path)
            for j in range(len(data)):
                if i == nro_config:
                    best_high.append(data[j]['best_of_value'])
                    all_high.append(data[j]['all_of_value'])
                    total_time_high.append(data[j]['total_time'])
                elif i == nro_config + 1:
                    best_medium.append(data[j]['best_of_value'])
                    all_medium.append(data[j]['all_of_value'])
                    total_time_medium.append(data[j]['total_time'])
                else:
                    best_low.append(data[j]['best_of_value'])
                    all_low.append(data[j]['all_of_value'])
                    total_time_low.append(data[j]['total_time'])
            
            i += 1
        
        if label_type == 1 and self.selected_config == 1:
            name_img = "initial_temp"
            title_best = f'Initial Temperature (Best OF Values), {dataset}.'
            title_all = f'Initial Temperature (All OF Values), {dataset}.'
            title_time = f'Initial Temperature (Total Time), {dataset}.'
            labels = ['High (1.000.000)', 'Medium (500.000)', 'Low (1.000)']
        
        if label_type == 1 and self.selected_config == 2:
            name_img = "population_size"
            title_best = f'Population Size (Best OF Values), {dataset}.'
            title_all = f'Population Size (All OF Values), {dataset}.'
            title_time = f'Population Size (Total Time), {dataset}.'
            labels = ['High (350)', 'Medium (200)', 'Low (50)']
        
        if label_type == 2 and self.selected_config == 1:
            name_img = "alpha"
            title_best = f'Alpha (Best OF Values), {dataset}.'
            title_all = f'Alpha (All OF Values), {dataset}.'
            title_time = f'Alpha (Total Time), {dataset}.'
            labels = ['High (0.99)', 'Medium (0.70)', 'Low (0.55)']
        
        if label_type == 2 and self.selected_config == 2:
            name_img = "mutation"
            title_best = f'Mutation Chance (Best OF Values), {dataset}.'
            title_all = f'Mutation Chance (All OF Values), {dataset}.'
            title_time = f'Mutation Chance (Total Time), {dataset}.'
            labels = ['High (0.3)', 'Medium (0.1)', 'Low (0.01)']
            
        
        data = [best_high, best_medium, best_low]
        plt.boxplot(data, labels=labels)
        plt.title(title_best)
        plt.ylabel('Objective Value')
        if self.selected_config == 1:
            path_to_save = f"./results/sa/images/{name_img}_best_{dataset}.png"
        if self.selected_config == 2:
            path_to_save = f"./results/ga/images/{name_img}_best_{dataset}.png"
        
        plt.savefig(path_to_save)
        plt.clf()

        data = [all_high, all_medium, all_low]
        plt.boxplot(data, labels=labels)
        plt.title(title_all)
        plt.ylabel('Objective Value')
        
        if self.selected_config == 1:
            path_to_save = f"./results/sa/images/{name_img}_all_{dataset}.png"
        if self.selected_config == 2:
            path_to_save = f"./results/ga/images/{name_img}_all_{dataset}.png"

        plt.savefig(path_to_save)
        plt.clf()

        data = [total_time_high, total_time_medium, total_time_low]
        plt.boxplot(data, labels=labels)
        plt.title(title_time)
        plt.ylabel('Time')
        if self.selected_config == 1:
            path_to_save = f"./results/sa/images/{name_img}_time_{dataset}.png"
        if self.selected_config == 2:
            path_to_save = f"./results/ga/images/{name_img}_time_{dataset}.png"

        plt.savefig(path_to_save)
        plt.clf()
        


            


                
            




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

