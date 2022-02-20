from ortools.sat.python import cp_model
import printContentClass as dataManagement

# implementation for the constraints satisfaction that we learned in the lecture but here it set the schedule in
# a way that set minimum shifts to bartenders who wasn't ask that shift.
def main(amountOfBartenders, requestsPerBartender, numWorkingDays, numShiftsPerDay, maxAmountShiftsPerBartender):
    equation = cp_model.CpModel()
    shifts = {}
    for currentBartender in range(amountOfBartenders):
        for currentDay in range(numWorkingDays):
            for currentShift in range(numShiftsPerDay):
                shifts[(currentBartender, currentDay, currentShift)] = equation.NewBoolVar('shift_n%id%is%i' % (currentBartender, currentDay, currentShift))
    for currentDay in range(numWorkingDays):
        for currentShift in range(numShiftsPerDay):
            equation.Add(sum(shifts[(currentBartender, currentDay, currentShift)] for currentBartender in range(amountOfBartenders)) >= 3)
    for currentDay in range(numWorkingDays):
        for currentShift in range(numShiftsPerDay):
            equation.Add(sum(shifts[(currentBartender, currentDay, currentShift)] for currentBartender in range(amountOfBartenders)) <= 5)
    for currentBartender in range(amountOfBartenders):
        for currentDay in range(numWorkingDays):
            equation.Add(sum(shifts[(currentBartender, currentDay, currentShift)] for currentShift in range(numShiftsPerDay)) <= 1)
    for currentBartender in range(amountOfBartenders):
        for currentDay in range(numWorkingDays):
            if (currentDay + 1) <= numWorkingDays - 1:
                equation.Add(shifts[(currentBartender, currentDay, 1)] + shifts[(currentBartender, (currentDay + 1), 0)] <= 1)
    for currentBartender in range(amountOfBartenders):
            equation.Add(sum(shifts[(currentBartender, currentDay, currentShift)] for currentDay in range(numWorkingDays) for currentShift in range(numShiftsPerDay)) == maxAmountShiftsPerBartender[currentBartender])
    equation.Minimize(
        sum(requestsPerBartender[currentBartender][currentDay][currentShift] * shifts[(currentBartender, currentDay, currentShift)] for currentBartender in range(amountOfBartenders)
            for currentDay in range(numWorkingDays) for currentShift in range(numShiftsPerDay)))
    equationSolver = cp_model.CpSolver()
    equationSolverResult = equationSolver.Solve(equation)
    numShiftsWereSet = 0
    isWorking = 1
    for currentBartender in range(amountOfBartenders):
        for currentDay in range(numWorkingDays):
            for currentShift in range(numShiftsPerDay):
                if requestsPerBartender[currentBartender][currentDay][currentShift] == isWorking:
                    numShiftsWereSet = numShiftsWereSet + 1
    funcOutput = []
    if equationSolverResult != 3:
        for currentDay in range(numWorkingDays):
            currentDayToPresent = currentDay + 1
            funcOutput.append("Day " + str(currentDayToPresent))
            isWorking = 1
            for currentBartender in range(amountOfBartenders):
                for currentShift in range(numShiftsPerDay):
                    if equationSolver.Value(shifts[(currentBartender, currentDay, currentShift)]) == isWorking:
                        if requestsPerBartender[currentBartender][currentDay][currentShift] == isWorking:
                            funcOutput.append('Bartender ' + str(currentBartender) + ' works shift ' + str(currentShift) + ' (not requested)')
                        else:
                            funcOutput.append('Bartender ' + str(currentBartender) + ' works shift ' + str(currentShift))
        dataManagement.pushData(
             str(numShiftsWereSet) + ' shifts were set, but ' + str(equationSolver.ObjectiveValue()) + ' shifts were set even though they was not requested.')
        dataManagement.pushData('The total time that took to find this solution is %f s' % equationSolver.WallTime())
    else:
        funcOutput.append("there is no solution!")
        dataManagement.pushData("can not find any solution for this case, try to change your requests")
    return funcOutput

