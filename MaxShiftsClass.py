from ortools.linear_solver import pywraplp
import printContentClass as dataManagement

# Implementation for algorithm that return a schedule for all the bartenders in a way that maximize all the
# shifts that it can to set
# It tries to create a situation where the job percentage of each bartender will be optimal (as high as possible),
# while maintaining all the difficult constraints - of the company and trying to provide, as much as possible, the
# soft satisfactions - of the bartenders' preferences.
def main(amountOfBartenders, requestsPerBartender, numWorkingDays, numShiftsPerDay, maxAmountShiftsPerBartender):
    equationSolver = pywraplp.Solver.CreateSolver('SCIP')
    allBartenderShifts = []
    for currentBartender in range(amountOfBartenders):
        currentBartenderShifts = []
        for currentDay in range(numWorkingDays):
            dailyBartenderShifts = []
            for currentShift in range(numShiftsPerDay):
                dailyBartenderShifts.append(equationSolver.IntVar(0, 1, ''))
            currentBartenderShifts.append(dailyBartenderShifts)
        allBartenderShifts.append(currentBartenderShifts)
    for currentBartender in range(amountOfBartenders):
        for currentDay in range(numWorkingDays):
            equationSolver.Add(equationSolver.Sum([allBartenderShifts[currentBartender][currentDay][currentShift] for currentShift in range(numShiftsPerDay)]) <= 1)
    for currentDay in range(numWorkingDays):
        for currentShift in range(numShiftsPerDay):
            equationSolver.Add(
                equationSolver.Sum([allBartenderShifts[currentBartender][currentDay][currentShift] for currentBartender in range(amountOfBartenders)]) >= 3)
    for currentDay in range(numWorkingDays):
        for currentShift in range(numShiftsPerDay):
            equationSolver.Add(
                equationSolver.Sum([allBartenderShifts[currentBartender][currentDay][currentShift] for currentBartender in range(amountOfBartenders)]) <= 5)
    for currentBartender in range(amountOfBartenders):
        equationSolver.Add(equationSolver.Sum(allBartenderShifts[currentBartender][currentDay][currentShift] for currentDay in range(numWorkingDays) for currentShift in range(numShiftsPerDay)) <= maxAmountShiftsPerBartender[currentBartender])
        for currentDay in range(numWorkingDays):
            for currentShift in range(numShiftsPerDay):
                if requestsPerBartender[currentBartender][currentDay][currentShift] == 1:
                    equationSolver.Add(allBartenderShifts[currentBartender][currentDay][currentShift] == 0)
    for currentBartender in range(amountOfBartenders):
        for currentDay in range(numWorkingDays):
            tomorrow = currentDay + 1
            if tomorrow <= numWorkingDays - 1:
                equationSolver.Add(allBartenderShifts[currentBartender][currentDay][1] + allBartenderShifts[currentBartender][tomorrow][0] <= 1)
    objective = []
    for currentBartender in range(amountOfBartenders):
        sumShiftsOfCurrentBartender = 0
        for currentDay in range(numWorkingDays):
            for currentShift in range(numShiftsPerDay):
                sumShiftsOfCurrentBartender = sumShiftsOfCurrentBartender + allBartenderShifts[currentBartender][currentDay][currentShift]
        objective.append(sumShiftsOfCurrentBartender)
    equationSolver.Maximize(equationSolver.Sum(objective))
    equationSolverResult = equationSolver.Solve()
    conclusions = []
    if equationSolverResult == pywraplp.Solver.FEASIBLE or equationSolverResult == pywraplp.Solver.OPTIMAL:
        for currentDay in range(numWorkingDays):
            conclusions.append("Day " + str(currentDay + 1))
            for currentBartender in range(amountOfBartenders):
                for currentShift in range(numShiftsPerDay):
                    if allBartenderShifts[currentBartender][currentDay][currentShift].solution_value() > 0.5:
                        if requestsPerBartender[currentBartender][currentDay][currentShift] == 1:
                            conclusions.append('Bartender ' + str(currentBartender) + ' works shift ' + str(currentShift) + ' (not requested)')
                        else:
                            conclusions.append('Bartender ' + str(currentBartender) + ' works shift ' + str(currentShift))
        dataManagement.pushData("max all the shifts.")
        dataManagement.pushData(str(equationSolver.Objective().Value()) + " shifts were set, out of " + str(sum(maxAmountShiftsPerBartender)))
    else:
        conclusions.append("there is no solution!")
        dataManagement.pushData("can not find any solution for this case, try to change your requests")
    return conclusions
