import os
from deap import base
from deap import creator
from deap import tools
from deap import algorithms
import random
import matplotlib.pyplot as matplotlibVar
import numpy as numpyVar
import seaborn as seabornVar
import printContentClass as dataManagement
import matplotlib
import bartenderMainClass
matplotlib.use('Agg')

defaultGEN = 200
cons = 0
aRand = 0
random.seed(42)
cons = cons + 1
aRand = aRand + 1
varTB = base.Toolbox()

# implementation for the genetic algorithm that we learned in the lecture with implementation of the elitism attribute
def elitFunc(varP , varTB, varCP , varM, newGenetic, stats=None,
                        halloffame=None, verbose=__debug__):
    varLB = tools.Logbook()
    varLB.header = ['gen', 'nevals'] + (stats.fields if stats else [])
    inv = [invalidVar for invalidVar in varP if not invalidVar.fitness.valid]
    fitN = varTB.map(varTB.evaluate, inv)
    for invalidVar, currentFitnesse in zip(inv, fitN):
        invalidVar.fitness.values = currentFitnesse

    if halloffame is None:
        raise ValueError("halloffame parameter must not be empty!")

    halloffame.update(varP)
    allFameLen = len(halloffame.items) if halloffame.items else 0

    record = stats.compile(varP) if stats else {}
    varLB.record(gen=0, nevals=len(inv), **record)
    if verbose:
        print(varLB.stream)
        dataManagement.pushData(varLB.stream)

    bigSize = 1000000000
    fOP = open("out.txt", "w")
    for gen in range(1, newGenetic + 1):
        offspring = varTB.select(varP, len(varP) - allFameLen)
        offspring = algorithms.varAnd(offspring, varTB, varCP, varM)
        inv = [invalidVar for invalidVar in offspring if not invalidVar.fitness.valid]
        fitN = varTB.map(varTB.evaluate, inv)
        for invalidVar, currentFitnesse in zip(inv, fitN):
            invalidVar.fitness.values = currentFitnesse
        offspring.extend(halloffame.items)
        halloffame.update(offspring)
        varP[:] = offspring
        record = stats.compile(varP) if stats else {}
        if bigSize > record['min']:
            bigSize = record['min']
            fOP.write(str(gen) + "  " + str(bigSize))
            fOP.write("\n")
        varLB.record(gen=gen, nevals=len(inv), **record)
        if verbose:
            print(varLB.stream)
            dataManagement.pushData(varLB.stream)
        if bigSize == 0:
            break
    fOP.close()
    return varLB , varP



creator.create("FitnessMin", base.Fitness, weights=(-1.0,))

creator.create("Individual", list, fitness=creator.FitnessMin)


def main(amountOfBartenders, requestsPerBartender, numWorkingDays, numShiftsPerDay, maxAmountShiftsPerBartender, gen):
    defaultGEN = gen
    nsp = bartenderMainClass.bartendersShiftsClass(10, amountOfBartenders, requestsPerBartender, numWorkingDays, numShiftsPerDay,
                                                   maxAmountShiftsPerBartender)
    varTB.register("zeroOrOne", random.randint, 0, 1)
    varTB.register("individualCreator", tools.initRepeat, creator.Individual, varTB.zeroOrOne, len(nsp))
    varTB.register("populationCreator", tools.initRepeat, list, varTB.individualCreator)


    def scoreRetFunc(individual):
        return nsp.scoreRet(individual),

    varTB.register("evaluate", scoreRetFunc)

    varTB.register("select", tools.selTournament, tournsize=2)
    varTB.register("mate", tools.cxTwoPoint)
    varTB.register("mutate", tools.mutFlipBit, indpb=1.0 / len(nsp))
    varP = varTB.populationCreator(n=300)
    stats = tools.Statistics(lambda invalidVar: invalidVar.fitness.values)
    stats.register("min", numpyVar.min)
    stats.register("avg", numpyVar.mean)
    hof = tools.HallOfFame(30)
    varLB , varP = elitFunc(varP , varTB, varCP=0.9 , varM=0.1, newGenetic=defaultGEN, stats=stats, halloffame=hof, verbose=True)
    best = hof.items[0]
    result = nsp.printAllData(best)
    minFitnessValues, meanFitnessValues = varLB.select("min", "avg")
    seabornVar.set_style("whitegrid")
    matplotlibVar.clf()
    matplotlibVar.xlabel('Generat')
    matplotlibVar.ylabel('Minimum and Avg')
    matplotlibVar.title('fitness')
    ln1, = matplotlibVar.plot(minFitnessValues, color='red')
    ln2, = matplotlibVar.plot(meanFitnessValues, color='green')
    if os.path.isfile(os.getcwd() + "/static/OptimizationGui.png"):
        os.remove(os.getcwd() + "/static/OptimizationGui.png")
    matplotlibVar.savefig(os.getcwd() + "/static/OptimizationGui")
    matplotlibVar.title('')
    ln1.remove()
    ln2.remove()
    return result


if __name__ == "__main__":
    main()
