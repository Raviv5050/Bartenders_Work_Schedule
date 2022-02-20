
# set all the shifts of the current bartender.
def getBartendersShifts(requestsPerBartender):
    allBartendersShifts = []
    amountOfBartenders = len(requestsPerBartender)
    amountOfDays = len(requestsPerBartender[0])
    for currentBartender in range(amountOfBartenders):
        currentBartenderShifts = []
        shiftsPerDay = []
        for currentDay in range(amountOfDays):
            if requestsPerBartender[currentBartender][currentDay] != ' ':
                shiftsPerDay.append(int(requestsPerBartender[currentBartender][currentDay]))
            else:
                currentBartenderShifts.append(shiftsPerDay)
                shiftsPerDay = []
        currentBartenderShifts.append(shiftsPerDay)
        allBartendersShifts.append(currentBartenderShifts)
    return allBartendersShifts
