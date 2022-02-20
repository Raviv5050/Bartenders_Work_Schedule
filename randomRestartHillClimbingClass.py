import os
from bartenderMainClass import bartendersShiftsClass
import printContentClass as dataManagement
import random
import matplotlib.pyplot as matplotlibVar
import matplotlib
matplotlib.use('Agg')

# implementation for the hill climbing algorithm that we learned in the lecture (start at a random start point)
# with the random restart version- so it start from a new start point each time, amd saves the max score it found
# while it keep searching for a better score result.
def randomBegining(amountOfBartenders, numWorkingDays, numShiftsPerDay):
    # create a list of a random beginning state
    randomBeginingList = []
    for currentElement in range(numWorkingDays * numShiftsPerDay * amountOfBartenders):
        randomBeginingList.append(random.randint(0, 1))
    return randomBeginingList
# Return the neighbors of current state
def neighborsOfCurrentState(shiftsInput):
    currentStateNeighbors = []
    for currentShift in range(len(shiftsInput)):
        shifts = shiftsInput[0:(len(shiftsInput))]
        if shifts[currentShift] == 0:
            shifts[currentShift] = 1
        else:
            shifts[currentShift] = 0
        currentStateNeighbors.append(shifts)
    return currentStateNeighbors
# transfer all the zero's to one and one's to zero
def transferZeroOne(input):
    currentInput = input[0:(len(input))]
    for iter in range(len(input)):
        if currentInput[iter] == 0:
            currentInput[iter] = 1
        else:
            currentInput[iter] = 0
    return currentInput
# The func gets arr and return vector
def convertArrIntoVector(numWorkingDays , requestsPerBartender, numShiftsPerDay , amountOfBartenders):
    requestsPerBartenderVector = []
    for currentBartender in range(amountOfBartenders):
        for currentDay in range(numWorkingDays):
            for currentShift in range(numShiftsPerDay):
                requestsPerBartenderVector.append(requestsPerBartender[currentBartender][currentDay][currentShift])
    return requestsPerBartenderVector

def main(amountOfBartenders, requestsPerBartender, numWorkingDays, numShiftsPerDay, maxAmountShiftsPerBartender, amountOfStarts):
    bartendersShiftsClassReturn = bartendersShiftsClass(10, amountOfBartenders, requestsPerBartender, numWorkingDays, numShiftsPerDay, maxAmountShiftsPerBartender)
    requestsPerBartenderState = transferZeroOne(convertArrIntoVector(numWorkingDays , requestsPerBartender, numShiftsPerDay , amountOfBartenders))
    index = 0
    indexList = []
    index += 1
    score = []
    maxScoresRequests = []
    counter = 0
    while counter < amountOfStarts:
        infinite = float('inf')
        next = 0
        nextScore = infinite
        for currentNeighbor in neighborsOfCurrentState(requestsPerBartenderState):
            neighborScore = bartendersShiftsClassReturn.scoreRet(currentNeighbor)
            if nextScore > neighborScore:
                lenScore = len(score)
                lenIndexList = len(indexList)
                score.insert(lenScore , neighborScore)
                # insert the index into the indexList
                indexList.insert(lenIndexList , index)
                index = index + 1
                dataManagement.pushData("found better state, with :" + str(neighborScore))
                nextScore = neighborScore
                next = currentNeighbor
        if bartendersShiftsClassReturn.scoreRet(requestsPerBartenderState) <= nextScore:
            requestsPerBartenderState = randomBegining(amountOfBartenders, numWorkingDays, numShiftsPerDay)
            counter = counter + 1
            maxScoresRequests.append(requestsPerBartenderState)
        else:
            requestsPerBartenderState = next
    minScoreState = maxScoresRequests[0]
    for maxScoreState in maxScoresRequests:
        if bartendersShiftsClassReturn.scoreRet(maxScoreState) < bartendersShiftsClassReturn.scoreRet(minScoreState):
            minScoreState = maxScoreState
    requestsPerBartenderState = minScoreState
    matplotlibVar.clf()
    matplotlibVar.ylabel("value score of each state")
    matplotlibVar.xlabel("indexs")
    ln, = matplotlibVar.plot(indexList, score)
    if os.path.isfile(os.getcwd() + "/static/OptimizationGui.png"):
        os.remove(os.getcwd() + "/static/OptimizationGui.png")
    matplotlibVar.savefig(os.getcwd() + "/static/OptimizationGui")
    ln.remove()
    dataManagement.pushData("the Minimum local score is: " + str(bartendersShiftsClassReturn.scoreRet(requestsPerBartenderState)))
    return bartendersShiftsClassReturn.printAllData(requestsPerBartenderState)
