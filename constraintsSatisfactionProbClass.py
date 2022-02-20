from ortools.sat.python import cp_model
import printContentClass as dataManagement

# implementation for the constraints satisfaction that we learned in the lecture
# it tries to satisfy all the constraints (hence its name), that each bartender will receive exactly the amount
# of shifts he asked to work per week (this is the number of shifts and not the specific days he requested), and in
# this way also minimize the number of shifts we received even though we did not mark the shift. Therefore, if it
# succeeds, the model will return the solution it found, but if there is no proper and legal placement that will
# satisfy all these constraints, the model will return that there is no solution.
def main(amountOfBartenders, requestsPerBartender, numWorkingDays, numShiftsPerDay, maxAmountShiftsPerBartender):
    equation = cp_model.CpModel()
    realSchedule = {}
    for currentBartender in range(amountOfBartenders):
        for currentDay in range(numWorkingDays):
            for currentShift in range(numShiftsPerDay):
                realSchedule[(currentBartender, currentDay, currentShift)] = equation.NewBoolVar(
                    'shift_n%id%is%i' % (currentBartender, currentDay, currentShift))
    for currentDay in range(numWorkingDays):
        for currentShift in range(numShiftsPerDay):
            equation.Add(sum(realSchedule[(currentBartender, currentDay, currentShift)] for currentBartender in
                             range(amountOfBartenders)) >= 3)
    for currentDay in range(numWorkingDays):
        for currentShift in range(numShiftsPerDay):
            equation.Add(sum(realSchedule[(currentBartender, currentDay, currentShift)] for currentBartender in
                             range(amountOfBartenders)) <= 5)
    for currentBartender in range(amountOfBartenders):
        for currentDay in range(numWorkingDays):
            equation.Add(sum(realSchedule[(currentBartender, currentDay, currentShift)] for currentShift in
                             range(numShiftsPerDay)) <= 1)
    for currentBartender in range(amountOfBartenders):
        for currentDay in range(numWorkingDays):
            tomorrow = currentDay + 1
            if tomorrow <= numWorkingDays - 1:
                equation.Add(realSchedule[(currentBartender, currentDay, 1)] + realSchedule[
                    (currentBartender, tomorrow, 0)] <= 1)
    for currentBartender in range(amountOfBartenders):
        equation.Add(sum(
            realSchedule[(currentBartender, currentDay, currentShift)] for currentDay in range(numWorkingDays) for
            currentShift in range(numShiftsPerDay)) == maxAmountShiftsPerBartender[currentBartender])
    for currentBartender in range(amountOfBartenders):
        for currentDay in range(numWorkingDays):
            for currentShift in range(numShiftsPerDay):
                if requestsPerBartender[currentBartender][currentDay][currentShift] == 1:
                    equation.Add(realSchedule[(currentBartender, currentDay, currentShift)] == 0)
    equationSolver = cp_model.CpSolver()
    equationSolverResult = equationSolver.Solve(equation)
    sumRequestedShifts = 0
    for currentBartender in range(amountOfBartenders):
        for currentDay in range(numWorkingDays):
            for currentShift in range(numShiftsPerDay):
                if requestsPerBartender[currentBartender][currentDay][currentShift] == 1:
                    sumRequestedShifts += 1
    conclusions = []
    if equationSolverResult != 3:
        for currentDay in range(numWorkingDays):
            conclusions.append("Day " + str(currentDay + 1))
            for currentBartender in range(amountOfBartenders):
                for currentShift in range(numShiftsPerDay):
                    if equationSolver.Value(realSchedule[(currentBartender, currentDay, currentShift)]) == 1:
                        if requestsPerBartender[currentBartender][currentDay][currentShift] == 1:
                            conclusions.append('currentBartender ' + str(currentBartender) + ' works shift ' + str(currentShift) + ' (not requested)')
                        else:
                            conclusions.append('currentBartender ' + str(currentBartender) + ' works shift ' + str(currentShift))
        dataManagement.pushData('The total time that took to find this solution is %f currentShift' % equationSolver.WallTime())
    else:
        conclusions.append("can not find any solution for this case, try to change your requests")
        dataManagement.pushData("can not find any solution for this case, try to change your requests")
    return conclusions

