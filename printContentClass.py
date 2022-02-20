import threading

# set all the basic functions such get,set, delete
l = threading.Lock()
dataList = []
def getData():
    global dataList
    lengthOfData = len(dataList)
    return dataList[0:lengthOfData]
def pushData(data):
    global dataList
    dataList.append(data)
def deleteDataFromList():
    global dataList
    dataList.clear()
