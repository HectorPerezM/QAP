import json
import matplotlib.pyplot as plt

class Util:
    def __init__(self, fpath, dpath):
        self.fpath = fpath
        self.dpath = dpath

    def getfpath(self):
        return self.fpath
    
    def getdpath(self):
        return self.dpath
    
    def readDataFiles(self, path=""):
        """
            Read QAP files.

            Arguments:
            path -- path to file.

            Return:
            data -- matrix with file data.
        """
        if path == "":
            print("Empty path.")
            return []
        
        data_file = open(path, "r")
        data = []
        for line in data_file:
            aux = list(map(int, line.split()))
            data.append(aux)
        
        return data


    def checkInputs(self, matrix = []):
        """
            check that matrix is not empty.

            Arguments:
            matrix -- matrix with data.

            Return:
            boolean.
        """
        if matrix == []:
            print("Input is empty.")
            return False
        return True


    def selectedConfigFile(self):
        print("Select your configuration file: ")
        print(" 1. Simmulated Annealing configuration")
        print(" 2. Genetic Algorithm configuration")
        print(" 3. other configuration")

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
            path = "./config/config_SA.json"
        else:
            path = "./config/config_SA.json"
            
        return path, selection


    def readConfigFile(self, config_path=""):
        if config_path == "":
            print("Empty config path.")
            return []
        
        with open(config_path) as f:
            data = json.load(f)
        
        return data
        


    def configFileInfo(self):
        print("### How to use config file ###")
        print(" - Posible values are: ")
        print("     'initial_solution': ['random', 'heuristic']")
        print("     'neighbour_selection': ['firstBest', 'bestRandom', 'bestImprovement']")
        print("")

    
    def plot(self, title, xAxis, yAxis, values):
        fig = plt.plot(values)
        plt.setp(fig,"linestyle","none","marker","s","color","r")
        plt.title(title) 
        plt.ylabel(yAxis)
        plt.xlabel(xAxis)
        plt.show()
        return True