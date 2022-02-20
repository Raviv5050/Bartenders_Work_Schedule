from ortools.sat.python import cp_model
import printContentClass as dataManagement

# implementation for the constraints satisfaction that we learned in the lecture
def main(amountOfBartenders, requestsPerBartender, numWorkingDays, numShiftsPerDay, maxAmountShiftsPerBartender):
    equation = cp_model.CpModel()
    realSchedule = {}
    for currentBartender in range(amountOfBartenders):
        for currentDay in range(numWorkingDays):
            for currentShift in range(numShiftsPerDay):
                realSchedule[(currentBartender, currentDay, currentShift)] = equation.NewBoolVar('shift_n%id%is%i' % (currentBartender, currentDay, currentShift))

    # run over the days
    for currentDay in range(numWorkingDays):
        # run over the shifts
        for currentShift in range(numShiftsPerDay):
            # At most 5 bartenders in shift.
            equation.Add(sum(realSchedule[(currentBartender, currentDay, currentShift)] for currentBartender in range(amountOfBartenders)) <= 5)


    # run over days
    for currentDay in range(numWorkingDays):
        # run over the shifts
        for currentShift in range(numShiftsPerDay):
            # At least 3 bartenders in a shift.
            equation.Add(sum(realSchedule[(currentBartender, currentDay, currentShift)] for currentBartender in range(amountOfBartenders)) >= 3)


   #run over the bartenders
    for currentBartender in range(amountOfBartenders):
        # run over the days
        for currentDay in range(numWorkingDays):
            # At most one shift for bartender in day
            equation.Add(sum(realSchedule[(currentBartender, currentDay, currentShift)] for currentShift in range(numShiftsPerDay)) <= 1)

   # run over the bartenders
    for currentBartender in range(amountOfBartenders):
        #run over the days
        for currentDay in range(numWorkingDays):
            tomorrow = currentDay + 1
            # check if bartender works in two shits (one after one)
            if tomorrow <= numWorkingDays - 1:
                equation.Add(realSchedule[(currentBartender, currentDay, 1)] + realSchedule[(currentBartender, tomorrow, 0)] <= 1)

    for currentBartender in range(amountOfBartenders):
        # check if the number of days that the bartender works is the same like the number of shits he ask
            equation.Add(sum(realSchedule[(currentBartender, currentDay, currentShift)] for currentDay in range(numWorkingDays) for currentShift in range(numShiftsPerDay)) == maxAmountShiftsPerBartender[currentBartender])


    equation.Minimize(
        sum(requestsPerBartender[currentBartender][currentDay][currentShift] * realSchedule[(currentBartender, currentDay, currentShift)] for currentBartender in range(amountOfBartenders)
            for currentDay in range(numWorkingDays) for currentShift in range(numShiftsPerDay)))
    equationSolver = cp_model.CpSolver()
    equationSolverResult = equationSolver.Solve(equation)

    sumRequestedShifts = 0
    for currentBartender in range(amountOfBartenders):
        for currentDay in range(numWorkingDays):
            for currentShift in range(numShiftsPerDay):
                if requestsPerBartender[currentBartender][currentDay][currentShift] == 1:
                    sumRequestedShifts += 1

    returnList = []
    conclusions = []
    if equationSolverResult != 3:
        for currentDay in range(numWorkingDays):
            conclusions.append("Day " + str(currentDay + 1))
            for currentBartender in range(amountOfBartenders):
                for currentShift in range(numShiftsPerDay):
                    returnList.append(equationSolver.Value(realSchedule[(currentBartender, currentDay, currentShift)]))
                    if equationSolver.Value(realSchedule[(currentBartender, currentDay, currentShift)]) == 1:
                        if requestsPerBartender[currentBartender][currentDay][currentShift] == 1:
                            conclusions.append('bartender ' + str(currentBartender) + ' works shift ' + str(currentShift) + ' (not requested)')
                        else:
                            conclusions.append('bartender ' + str(currentBartender) + ' works shift ' + str(currentShift))

        dataManagement.pushData(str(sumRequestedShifts) + ' shifts were set, but ' + str(equationSolver.ObjectiveValue()) + ' shifts were set even though they was not requested.')

        dataManagement.pushData('The total time that took to find this solution is %f currentShift' % equationSolver.WallTime())
        dataManagement.pushData("")
    else:
        dataManagement.pushData("can not find any solution for this case, try to change your requests")
        conclusions.append("can not find any solution for this case, try to change your requests")
    return conclusions

