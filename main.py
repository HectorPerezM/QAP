from other.Util import Util
from solution.SA import SA
from solution.GA import GA
from problem.QAP import QAP

def main():
    #Create Util object
    util = Util()

    config = util.getConfig()
    m = len(config)
    for i in range(m):
        #Configure folder
        util.configureResultsFolder(config[i])

        #Init QAP
        qap = QAP()
        qap.readData(config[i])

        #Start experiments
        for e in range(config[i]['size_experiment']):
            #Solve with SA
            if util.selected_config == 1:            
                solver = SA(qap, config[i])
                solver.run()
                util.saveResults(i, e, config[i], solver)
                util.savePlot(i, e, config[i], solver)

            #Solve with GA
            elif selection == 2:
                solver = GA(qap, config[i])

            #Solve with default SA
            else:
                print("Not implemented yet.")


            
            # solver.run()

            # #Save results
            # if selection == 1:
            #     util.saveResults(solver, e, config[i])
            #     util.savePlot(solver, e, config[i])
            
            # elif selection == 2:
            #     util.saveResults(solver, e, 'GA')
            
            # else:
            #     print('Not implemented yet.')
            

            print(f"finished: exp -> {e} config -> {i}")


if __name__ == "__main__":
    main()