from bartenderMainClass import bartendersShiftsClass
import random
import os
import printContentClass as dataManagement
import matplotlib.pyplot as matplotlibVar
import matplotlib
matplotlib.use('Agg')

# implementation for the hill climbing algorithm that we learned in the lecture (start at a random start point
# but only at the first time- without random restart). start with some initial situation and try to improve it during
# the different iterations. As we said, in the above model there is no promise to find an optimal solution, but it is
# guaranteed that when we stop the algorithm, at any stage, the algorithm will return the best state so far (because it
# chooses each time an action that increases the value in If the value of the best neighbor is equal to or greater than
# the present value, then this neighbor is selected so that it will be the new current state). Recall that according to
# the basic algorithm, a random point is chosen as the starting point, and in each iteration we choose one of the
# heirs (whose value is greater than the current vertex) at random. That is, in the above algorithm it is guaranteed
# that when we stop we will be in a good place at least like the place where we started, but it is possible that if the
# algorithm can run indefinitely we will not reach a global optimum yet, as the model can get stuck at a local optimum
def randomBegining(amountOfBartenders, numWorkingDays, numShiftsPerDay):
    randomBeginingList = []
    for currentElement in range(numWorkingDays * amountOfBartenders * numShiftsPerDay):
        randomBeginingList.append(random.randint(0, 1))
    return randomBeginingList
def transferZeroOne(requestsPerBartenderVector):
    currentInputVec = requestsPerBartenderVector[0:(len(requestsPerBartenderVector))]
    for iter in range(len(requestsPerBartenderVector)):
        if currentInputVec[iter] == 0:
            currentInputVec[iter] = 1
        else:
            currentInputVec[iter] = 0
    return currentInputVec
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
def convertArrIntoVector(numWorkingDays , requestsPerBartender, numShiftsPerDay , amountOfBartenders):
    requestsPerBartenderVector = []
    for currentBartender in range(amountOfBartenders):
        for currentDay in range(numWorkingDays):
            for currentShift in range(numShiftsPerDay):
                requestsPerBartenderVector.append(requestsPerBartender[currentBartender][currentDay][currentShift])
    return requestsPerBartenderVector

def main(amountOfBartenders, requestsPerBartender, numWorkingDays, numShiftsPerDay, maxAmountShiftsPerBartender):
    # the hard constraint is 10
    bartendersShiftsClassReturn = bartendersShiftsClass(10, amountOfBartenders, requestsPerBartender, numWorkingDays, numShiftsPerDay, maxAmountShiftsPerBartender)
    requestsPerBartenderState = transferZeroOne(convertArrIntoVector(numWorkingDays , requestsPerBartender , numShiftsPerDay , amountOfBartenders))
    index = 0
    indexList = []
    index += 1
    score = []
    while True:
        infinite = float('inf')
        next = 0
        nextScore = infinite
        for currentNeighbor in neighborsOfCurrentState(requestsPerBartenderState):
            neighborScore = bartendersShiftsClassReturn.scoreRet(currentNeighbor)
            if nextScore > neighborScore:
                scoreLength = len(score)
                score.insert(scoreLength, neighborScore)
                indexListLength = len(indexList)
                # insert the index into the indexList
                indexList.insert(indexListLength , index)
                index = index + 1
                dataManagement.pushData("found better state, with :" + str(neighborScore))
                next = currentNeighbor
                nextScore = neighborScore
        if bartendersShiftsClassReturn.scoreRet(requestsPerBartenderState)<= nextScore:
            break
        requestsPerBartenderState = next
    matplotlibVar.clf()
    matplotlibVar.ylabel("value score of each state")
    matplotlibVar.xlabel("indexs")
    currentPlot, = matplotlibVar.plot(indexList, score)
    if os.path.isfile(os.getcwd() + "/static/OptimizationGui.png"):
        os.remove(os.getcwd() + "/static/OptimizationGui.png")
    matplotlibVar.savefig(os.getcwd() + "/static/OptimizationGui")
    currentPlot.remove()
    dataManagement.pushData("the Minimum local score is: " + str(bartendersShiftsClassReturn.scoreRet(requestsPerBartenderState)))
    return bartendersShiftsClassReturn.printAllData(requestsPerBartenderState)
