from other.Util import Util
from solution.SA import SA
from solution.GA import GA
from problem.QAP import QAP
import matplotlib.pyplot as plt
import numpy as np

def main():
    #Create Util object
    util = Util()

    config = util.getConfig()
    #Configure folder
    util.configureResultsFolder()
    m = len(config)
    for i in range(m):
        #Init QAP
        qap = QAP()
        qap.readData(config[i])

        #Start experiments
        for e in range(config[i]['size_experiment']):
            #Solve with SA
            if util.selected_config == 1:            
                solver = SA(qap, config[i], e, i)
                solver.run()
                data = {
                    'best_of_value': solver.mean_best_of_value,
                    'all_of_value': solver.mean_all_of_value,
                    'time_per_iter': solver.mean_time_per_iter,
                    'total_time': solver.total_time
                }
                util.experiment.append(data)
                util.savePlot(i, e, config[i], solver)
                

            #Solve with GA
            elif util.selected_config == 2:
                solver = GA(qap, config[i])
                solver.run()
                data = {
                    'best_of_value': solver.mean_best_of_value,
                    'all_of_value': solver.mean_all_of_value,
                    'time_per_iter': solver.mean_time_per_iter,
                    'total_time': solver.total_time
                }
                util.experiment.append(data)
                util.savePlot(i, e, config[i], solver)

            else:
                print("Not implemented yet.")
                exit()

            print(f"finished: exp -> {e} config -> {i}")

        util.wirteResults(config[i]['dataset_name'], i)
    
    util.saveBoxplot('esc32a', 0, 1)
    # util.saveBoxplot('chr12a', 3, 2)
    # util.saveBoxplot('esc64a', 6, 1)
    # util.saveBoxplot('esc64a', 9, 2)
    # util.saveBoxplot('chr25a', 12, 1)
    # util.saveBoxplot('chr25a', 15, 2)


    # util.saveBoxplot()

if __name__ == "__main__":
    main()