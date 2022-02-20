import numpy as numpyVar
import printContentClass as dataManagement

# In the bartendersShiftsClass class we set all the hard constraints and all the soft constraints. also we set all
# the rules of how many days each bartender should work a week.
class bartendersShiftsClass:
    def __init__(self, punishHardConstraints, amountOfBartenders, requestsPerBartender, numWorkingDays, numShiftsPerDay, maxAmountShiftsPerBartender):
        self.MbartendersList = []
        self.MpunishHardConstraints = punishHardConstraints
        self.weeks = 1
        for currentBartender in range(amountOfBartenders):
            self.MbartendersList.append(str(currentBartender))
        self.MshiftMin = [3, 3]
        self.MshiftMax = [5, 5]
        #print("***************************************1type1****************************")
        #print(type(maxAmountShiftsPerBartender))
        #print("***************************************1type1****************************")
        self.MmaxAmountShiftsPerBartender = maxAmountShiftsPerBartender
        self.MrequestsPerBartender = requestsPerBartender
        self.MnumShiftsPerDay = numShiftsPerDay
        self.MnumWorkingDays = numWorkingDays
        self.M2maxAmountShiftsPerBartender = self.MnumShiftsPerDay * self.MnumWorkingDays
       # print("***************************************2type2****************************")
        #print(type(maxAmountShiftsPerBartender))
        #print("***************************************2type2****************************")
    def __len__(self):
        lenMbartendersList = len(self.MbartendersList)
        return self.M2maxAmountShiftsPerBartender * lenMbartendersList
    def scoreRet(self, givenShiftsPerBartender):
        if len(givenShiftsPerBartender) != self.__len__():
            raise ValueError("size of givenShiftsPerBartender list should be equal to ", self.__len__())
        DictOfBartendersShifts = self.getDictOfBartendersShifts(givenShiftsPerBartender)
        sumOfMorningEveningSequenceShifts = self.numOfMorningEveningSequenceShifts(DictOfBartendersShifts)
        sumOfViolationsShiftsInWeek = self.numOfViolationsShiftsInWeek(DictOfBartendersShifts)[1]
        sumOfBartendersViolationsPerShift = self.numOfBartendersViolationsPerShift(DictOfBartendersShifts)[1]
        sumOfDeviationPreferencesShifts = self.numOfDeviationPreferencesShifts(DictOfBartendersShifts)
        # Return the the violation of the soft-constraint + violation of the hard-constraint
        # The calculate of the violation of the soft-constraint are: sumOfDeviationPreferencesShifts
        # The calculate of the violation of the hard-constraint are: sumOfViolationsShiftsInWeek + sumOfBartendersViolationsPerShift + sumOfMorningEveningSequenceShifts
        return sumOfDeviationPreferencesShifts + (self.MpunishHardConstraints * (sumOfViolationsShiftsInWeek + sumOfBartendersViolationsPerShift + sumOfMorningEveningSequenceShifts))
    def getDictOfBartendersShifts(self, givenShiftsPerBartender):
        amountOfBartenders = len(self.MbartendersList)
        bartenderShifts = self.__len__() // amountOfBartenders
        index = 0
        DictOfBartendersShifts = {}
        for currentBartender in self.MbartendersList:
            DictOfBartendersShifts[currentBartender] = givenShiftsPerBartender[index:index + bartenderShifts]
            index = index + bartenderShifts
        return DictOfBartendersShifts
    def numOfMorningEveningSequenceShifts(self, DictOfBartendersShifts):
        numMorningEveningSequenceShifts = 0
        for shiftsOfTheCurrentBartender in DictOfBartendersShifts.values():
            for currentShift, consecutiveShift in zip(shiftsOfTheCurrentBartender, shiftsOfTheCurrentBartender[1:]):
                if consecutiveShift == 1 and currentShift == 1:
                    numMorningEveningSequenceShifts = numMorningEveningSequenceShifts + 1
        return numMorningEveningSequenceShifts
    def numOfViolationsShiftsInWeek(self, DictOfBartendersShifts):
        numShiftsInWeekPerBartender = []
        numViolationsShiftsInWeek = 0
        for j, shiftsOfBartender in enumerate(DictOfBartendersShifts.values()):
            for i in range(0, self.weeks*self.M2maxAmountShiftsPerBartender, self.M2maxAmountShiftsPerBartender):
                currentShiftsInWeek = sum(shiftsOfBartender[i:i + self.M2maxAmountShiftsPerBartender])
                numShiftsInWeekPerBartender.append(currentShiftsInWeek)
                if currentShiftsInWeek > self.MmaxAmountShiftsPerBartender[j]:
                    numViolationsShiftsInWeek = numViolationsShiftsInWeek - self.MmaxAmountShiftsPerBartender[j] + currentShiftsInWeek
                else:
                    numViolationsShiftsInWeek = numViolationsShiftsInWeek + self.MmaxAmountShiftsPerBartender[j] - currentShiftsInWeek
        return numShiftsInWeekPerBartender, numViolationsShiftsInWeek
    def numOfBartendersViolationsPerShift(self, DictOfBartendersShifts):
        numBartendersViolationsPerShift = 0
        sumOfAllShifts = [sum(currentShiftVal) for currentShiftVal in zip(*DictOfBartendersShifts.values())]
        for indexOfCurrentshift, amountOfBartenders in enumerate(sumOfAllShifts):
            # Normalized the index of the current shift to be 0, 1 (morning or evening)
            indexOfCurrentshiftNormalized = indexOfCurrentshift % self.MnumShiftsPerDay
            if (self.MshiftMax[indexOfCurrentshiftNormalized] < amountOfBartenders):
                numBartendersViolationsPerShift = numBartendersViolationsPerShift - self.MshiftMax[indexOfCurrentshiftNormalized] + amountOfBartenders
            elif (self.MshiftMin[indexOfCurrentshiftNormalized] > amountOfBartenders):
                numBartendersViolationsPerShift = numBartendersViolationsPerShift + self.MshiftMin[indexOfCurrentshiftNormalized] - amountOfBartenders
        return sumOfAllShifts, numBartendersViolationsPerShift
    def numOfDeviationPreferencesShifts(self, DictOfBartendersShifts):
        numDeviationPreferencesShifts = 0
        for indexOfCurrentBartender, requestsPerBartender in enumerate(self.MrequestsPerBartender):
            preferencesShifts = []
            for currentBartender in range(len(requestsPerBartender)):
                for currentShift in range(len(requestsPerBartender[currentBartender])):
                    preferencesShifts.append(requestsPerBartender[currentBartender][currentShift])
            realShifts = DictOfBartendersShifts[self.MbartendersList[indexOfCurrentBartender]]
            for realShift , preferencesShift in zip(realShifts , preferencesShifts):
                if realShift == 1 and preferencesShift == 1:
                    numDeviationPreferencesShifts = numDeviationPreferencesShifts + 1

        return numDeviationPreferencesShifts

    def printAllData(self, givenShiftsPerBartender):
        DictOfBartendersShifts = self.getDictOfBartendersShifts(givenShiftsPerBartender)
        dataToPrint = []
        for currentDay in range(self.MnumWorkingDays):
            dataToPrint.append("Day " + str(currentDay + 1))
            for currentBartender in self.MbartendersList:
                for currentShift in range(self.MnumShiftsPerDay):
                    if (DictOfBartendersShifts[currentBartender])[(currentDay * self.MnumShiftsPerDay) + currentShift] == 1:
                        if self.MrequestsPerBartender[int(currentBartender)][currentDay][currentShift] == 1:
                            dataToPrint.append('dataToPrint ' + str(currentBartender) + ' works shift ' + str(currentShift) + ' (not requested)')
                        else:
                            dataToPrint.append('dataToPrint ' + str(currentBartender) + ' works shift ' + str(currentShift))
        dataManagement.pushData("consecutive shift violations = " + str(self.numOfMorningEveningSequenceShifts(DictOfBartendersShifts)))
        numShiftsInWeekPerBartender, numViolationsShiftsInWeek = self.numOfViolationsShiftsInWeek(DictOfBartendersShifts)
        dataManagement.pushData("number of Shifts for each bartender = " + str(numShiftsInWeekPerBartender))
        dataManagement.pushData("Shifts Per Week Violations = " + str(numViolationsShiftsInWeek))
        sumOfAllShifts, numBartendersViolationsPerShift = self.numOfBartendersViolationsPerShift(DictOfBartendersShifts)
        dataManagement.pushData("number of bartenders Per Shift = " + str(sumOfAllShifts))
        dataManagement.pushData("bartenders Per Shift Violations = " + str(numBartendersViolationsPerShift))
        sumOfDeviationPreferencesShifts = self.numOfDeviationPreferencesShifts(DictOfBartendersShifts)
        dataManagement.pushData("num of conflict in bartenders requests: " + str(sumOfDeviationPreferencesShifts))
        return dataToPrint
def main():
    MbartendersList = bartendersShiftsClass(10)
    randomSolution = numpyVar.random.randint(2, size=len(MbartendersList))
    MbartendersList.printAllData(randomSolution)

if __name__ == "__main__":
    main()