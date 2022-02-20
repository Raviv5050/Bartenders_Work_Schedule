import os
from bartenderMainClass import bartendersShiftsClass
import numpy as numpyVar
import scipy.constants as scipyVar
import printContentClass as dataManagement
import random
import matplotlib.pyplot as matplotlibVar
import matplotlib
matplotlib.use('Agg')

# implementation for the simulated annealing algorithm that we learned in the lecture (start at a random start point)
# it Selects each time an action that will increase the value as much as possible from the current state, i.e. if the
# best neighbor value is equal to or greater than the current value, then this neighbor is selected to be the new
# current state), but different from the previous model we saw, in the above model even if the neighbor Is of lesser
# value we agree to move to it with a probability of Which is affected by the temperature (T - which represents the
# elapsed time) and the degree of difference between the value of the new neighbor and the value of the current
# neighbor. In this way, the model will allow the execution of such a "bad choice" especially at the beginning of
# its path, and when the difference is small. Of curse, all this time it saves the max score it found while it keep
# searching for a better score result.
def randomBegining(amountOfBartenders, numWorkingDays, numShiftsPerDay):
    randomBeginingList = []
    for i in range(numWorkingDays * numShiftsPerDay * amountOfBartenders):
        randomNum = random.randint(0, 1)
        randomBeginingList.append(randomNum)
    return randomBeginingList
def neighborsOfCurrentState(shiftsInput):
    zero = 0
    # Copy the shift input
    shifts = shiftsInput[zero : (len(shiftsInput))]
    # Choose a random shift
    randomShiftIndex = random.randint(0, len(shiftsInput) - 1)
    if shifts[randomShiftIndex] == 0:
        shifts[randomShiftIndex] = 1
    else:
        shifts[randomShiftIndex] = 0
    return shifts
# The func gives the temperature
def getTemperature(currentIteration):
    powNumber = 0.9
    powResulte = pow(powNumber, currentIteration)
    return (100 * powResulte)
def calculateProbability(deltaE , temperatureVar):
    #powE = deltaE / temperatureVar

    #return numpyVar.exp(powE * scipyVar.Boltzmann)
    return numpyVar.exp(deltaE / temperatureVar * scipyVar.Boltzmann)
def transferZeroOne(input):
    zero = 0
    currentInput = input[zero:(len(input))]
    for currentInputIndex in range(len(input)):
        if currentInput[currentInputIndex] == 0:
            currentInput[currentInputIndex] = 1
        else:
            currentInput[currentInputIndex] = 0
    return currentInput
def convertArrIntoVector(numWorkingDays , requestsPerBartender, numShiftsPerDay , amountOfBartenders):
    requestsPerBartenderVector = []
    for currentBartender in range(amountOfBartenders):
        for currentDay in range(numWorkingDays):
            for currentShift in range(numShiftsPerDay):
                requestsPerBartenderVector.append(requestsPerBartender[currentBartender][currentDay][currentShift])
    return requestsPerBartenderVector


def main(amountOfBartenders, requestsPerBartender, numWorkingDays, numShiftsPerDay, maxAmountShiftsPerBartender, amountOfIteration):
    score = []
    indexList = []
    bartendersShiftsClassReturn = bartendersShiftsClass(10, amountOfBartenders, requestsPerBartender, numWorkingDays, numShiftsPerDay, maxAmountShiftsPerBartender)
    requestsPerBartenderState = transferZeroOne(convertArrIntoVector(numWorkingDays , requestsPerBartender, numShiftsPerDay , amountOfBartenders))
    currentScore = bartendersShiftsClassReturn.scoreRet(requestsPerBartenderState)
    for index in range(amountOfIteration):
        currentNeighbor = neighborsOfCurrentState(requestsPerBartenderState)
        currentNeighborScore = bartendersShiftsClassReturn.scoreRet(currentNeighbor)
        if currentScore > currentNeighborScore:
            currentScore = currentNeighborScore
            requestsPerBartenderState = currentNeighbor
        else:
            # index for the getTemperature func
            indexTemperature = index + 1
            # gives the temperature
            temperatureVar = getTemperature(indexTemperature)
            if temperatureVar == 0:
                break
            dataManagement.pushData(indexTemperature)
            index = index + 1
            # send to calculateProbability the temperatureVar and the deltaE(currentScore - currentNeighborScore)
            calculateProbabilityRet = calculateProbability((currentScore - currentNeighborScore) , temperatureVar)
            if numpyVar.random.uniform(0, 1) <= calculateProbabilityRet:
                requestsPerBartenderState = currentNeighbor
                currentScore = currentNeighborScore
        lenScore = len(score)
        lenIndexList = len(indexList)
        indexList.insert(lenIndexList, index + 1)
        score.insert(lenScore, currentScore)
    dataManagement.pushData("minimum value = " + str(bartendersShiftsClassReturn.scoreRet(requestsPerBartenderState)))
    matplotlibVar.clf()
    matplotlibVar.ylabel("value score of each state")
    matplotlibVar.xlabel("indexs")
    ln, = matplotlibVar.plot(indexList, score)
    if os.path.isfile(os.getcwd() + "/static/OptimizationGui.png"):
        os.remove(os.getcwd() + "/static/OptimizationGui.png")
    matplotlibVar.savefig(os.getcwd() + "/static/OptimizationGui")
    ln.remove()
    return bartendersShiftsClassReturn.printAllData(requestsPerBartenderState)
