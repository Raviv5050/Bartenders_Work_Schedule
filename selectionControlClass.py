from flask import Flask, render_template, request, send_file
import MinimumShiftsClass
import hillClimbingClass
import MaxShiftsClass
import geneticClass
import basicCommunicationClass as functionVar
import randomRestartHillClimbingClass
import simulatedAnnealingClass
import printContentClass as dataManagement
import constraintsSatisfactionProbClass
import json

# In this class we check out the option that was chosen (from all the algorithms we implemented) and call to
# the specific class and functions accordingly.
app = Flask(__name__)
numWorkingDays = 5
numShiftsPerDay = 2
@app.route("/")
def main():
    return render_template("webPage.html")
@app.route('/get_data', methods=['GET'])
def get_data():
    data = dataManagement.getData()
    dataManagement.deleteDataFromList()  # delete the data from the list
    return render_template('webResultsPage.html', shifts=data)
@app.route('/user_data', methods=['POST'])
def user_input():
    data = request.get_json()
    requestsPerBartender = functionVar.getBartendersShifts(data[0])
    maxAmountShiftsPerBartender = list(map(int, data[1]))

    result = []
    amountOfBartenders = len(requestsPerBartender)
    if data[2][0] == "MaxShifts":
        result = MaxShiftsClass.main(amountOfBartenders, requestsPerBartender, numWorkingDays, numShiftsPerDay, maxAmountShiftsPerBartender)
    elif data[2][0] == "csp":
        result = constraintsSatisfactionProbClass.main(amountOfBartenders, requestsPerBartender, numWorkingDays, numShiftsPerDay, maxAmountShiftsPerBartender)
    elif data[2][0] == "hill_climbing":
        result = hillClimbingClass.main(amountOfBartenders, requestsPerBartender, numWorkingDays, numShiftsPerDay, maxAmountShiftsPerBartender)
    elif data[2][0] == "genetic":
        result = geneticClass.main(amountOfBartenders, requestsPerBartender, numWorkingDays, numShiftsPerDay, maxAmountShiftsPerBartender, int(data[2][1]))
    elif data[2][0] == "random_restart":
        result = randomRestartHillClimbingClass.main(amountOfBartenders, requestsPerBartender, numWorkingDays, numShiftsPerDay, maxAmountShiftsPerBartender,
                                                     int(data[2][1]))
    elif data[2][0] == "shift_min":
        result = MinimumShiftsClass.main(amountOfBartenders, requestsPerBartender, numWorkingDays, numShiftsPerDay, maxAmountShiftsPerBartender)
    else:
        result = simulatedAnnealingClass.main(amountOfBartenders, requestsPerBartender, numWorkingDays, numShiftsPerDay, maxAmountShiftsPerBartender,
                                              int(data[2][1]))
    return json.dumps(result)
if __name__ == "__main__":
    app.run(debug=True, host="localhost", port='80')
