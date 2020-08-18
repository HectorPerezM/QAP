from other.Util import Util
from solution.SA import SA
from solution.GA import GA
from problem.QAP import QAP

def main():
    #Create Util object
    util = Util()
    #util.configFileInfo()

    #Load configuration file
    config_path, selection = util.selectedConfigFile()
    config = util.readConfigFile(config_path)
    

    fmatrix = util.readDataFiles(config["facilities_data_path"])
    dmatrix = util.readDataFiles(config["distance_data_path"])

    assert util.checkInputs(fmatrix), "Facilitie matrix is empty."
    assert util.checkInputs(dmatrix), "Distance matrix is empty."

    #Configurate problem
    qap = QAP(config["type_initial_solution"], fmatrix, dmatrix)
    
    #Solve with SA
    if selection == 1:
        is_created = qap.generateInitialSolution()
        assert is_created, "Couldn't create a initial solution for SA."

        #Create the solver object, configured to run SA
        solver = SA(qap, config["max_iter"], config["cooling"], 
                    config["iter_per_temp"], config["temp_initial"], 
                    config["temp_min"], config["beta"], config["alpha"])
    
    #Solve with GA
    elif selection == 2:
        #Config QAP for GA
        qap.setAmountPopulation(config["amount_population"])
        qap.initial_solution = qap.generateInitialSolution()

        solver = GA(qap, config["total_iteration"])

    #Solve with default SA
    else:
        print("Not implemented yet.")

    #Start selected metaheuristic
    solver.run()

    #Plot
    util.plot("Simmulated Annealing", "Iterations", "OF", solver.of_list)
    util.plot("Simmulated Annealing", "Iterations", "Temp", solver.temp)
    util.plot("Simmulated Annealing", "Iterations", "Time (s)", solver.time_per_iteration)

    #Save results




if __name__ == "__main__":
    main()