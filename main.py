from other.Util import Util
from solution.SA import SA
from problem.QAP import QAP

def main():
    #Create Util object & pass data files
    util = Util("./data/FChr12a.txt", "./data/DChr12a.txt")
    # util.configFileInfo()

    #Load configuration file
    config_path, selection = util.selectedConfigFile()
    config = util.readConfigFile(config_path)
    

    fmatrix = util.readDataFiles(util.getfpath())
    dmatrix = util.readDataFiles(util.getdpath())

    assert(util.checkInputs(fmatrix))
    assert(util.checkInputs(dmatrix))

    #Configurate problem
    qap = QAP(config["initial_solution"], fmatrix, dmatrix)
    qap.initial_solution = qap.generateInitialSolution()


    #Solve with SA
    if selection == 1:
        solver = SA(qap, config["max_iter"], config["cooling"], config["iter_per_temp"], config["temp_initial"], config["temp_min"])
    
    #Solve with GA
    elif selection == 2:
        print("Not implemented yet.")

    #Solve with default SA
    else:
        print("Not implemented yet.")

    solver.run()


    #Plot
    util.plot("Simmulated Annealing", "Iterations", "OF", solver.of_list)
    util.plot("Simmulated Annealing", "Iterations", "Temp", solver.temp)




if __name__ == "__main__":
    main()