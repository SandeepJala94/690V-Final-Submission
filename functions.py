import xlrd
import numpy as np
import datetime




def openSensorFile():
    file_location = "Sensor_Data.xlsx"
    sensorFile = xlrd.open_workbook(file_location)
    sensorInfo = sensorFile.sheet_by_index(0)        
    
    v = []
    
    for r in range(1, sensorInfo.nrows):
        sensorTuple = ( sensorInfo.cell_value(r, 0), sensorInfo.cell_value(r, 1), sensorInfo.cell_value(r, 2), sensorInfo.cell_value(r, 3) )                       
        v.append(sensorTuple)
    
    return v, file_location



def openMeteorFile():
    file_location = "Meteorological_Data.xlsx"
    file = xlrd.open_workbook(file_location)
    meteorFile = file.sheet_by_index(0)        
    
    v = []
    
    for r in range(1, meteorFile.nrows):
        sensorTuple = ( meteorFile.cell_value(r, 0), meteorFile.cell_value(r, 1), meteorFile.cell_value(r, 2) )                       
        v.append(sensorTuple)
    
    return v






def findClosestTimeIndex(timeFrames, timeOfInterest):
    print("type(timeFrames) = ", type(timeFrames[0]))
    print("type(timeOfInterest) = ", type(timeOfInterest))
    for i in range(0, len(timeFrames)):
        #print("type(int(timeFrames[i])) = ", type(int(timeFrames[i])))
        #print("type(int(timeOfInterest)) = ", type(int(timeOfInterest)))
        if int(timeFrames[i]) > int(timeOfInterest):
            if i >= 1:
                return i-1
            else:
                return 0
    
    return len(timeFrames)-1



def addMeteorDataToDict(timeDict, m):
    print("len(m) = ", len(m))
    uniqueMTime = []
    allMTime = []
    for row in m:
        allMTime.append(row[0])
        if row[0] not in uniqueMTime:
            uniqueMTime.append(row[0])
    print("len(uniqueM) = ", len(uniqueMTime))
    print("len(allMTime) = ", len(allMTime))
    
    
    missingTimeFrames = []
    for keyTriple in timeDict.keys():
        if keyTriple[0] not in uniqueMTime:
            missingTimeFrames.append(keyTriple[0])
            
    print("len(missingTimeFrames) = ", len(missingTimeFrames))
    
    #for keyTriple in timeDict.keys():
        #print(type(keyTriple), " ) ", type(timeDict[keyTriple]))
    
    #for time in uniqueMTime:
    #    for keyTriple in timeDict.keys():
    #        if time == keyTriple[0]:
    #            index = allMTime.index(time)
    #            direction = m[index][1]
    #            speed = m[index][2]
    #            timeDict[keyTriple].append(direction)
    #            timeDict[keyTriple].append(speed)
    #            #print(keyTriple, " ) ", timeDict[keyTriple])
    #        else:
    #            index = findClosestTimeIndex(uniqueMTime, keyTriple[0])
    #            direction = m[index][1]
    #            speed = m[index][2]
    #            timeDict[keyTriple].append(direction)
    #            timeDict[keyTriple].append(speed)
    
    lastKnownIndex = -1
    index = -1
    for keyTriple in timeDict.keys():
        
        if keyTriple[0] in uniqueMTime:
            index = allMTime.index(keyTriple[0])
            lastKnownIndex = allMTime.index(keyTriple[0])
        else:
            index = lastKnownIndex
            
        direction = m[index][1]
        speed = m[index][2]
        timeDict[keyTriple].append(direction)
        timeDict[keyTriple].append(speed)
                
    print("Last for loop------------------------------------------------------------")
    #for keyTriple in timeDict.keys():
    #    print(keyTriple, " ) ", timeDict[keyTriple])
    
    return timeDict
                
    
    
    
    
    
    
def addMeteorDataToDictTwo(timeDict, m):
    print("len(m) = ", len(m))
    uniqueMTime = []
    allMTime = []
    for row in m:
        allMTime.append(row[0])
        if row[0] not in uniqueMTime:
            uniqueMTime.append(row[0])
    print("len(uniqueM) = ", len(uniqueMTime))
    print("len(allMTime) = ", len(allMTime))
    
    
    lastKnownIndex = -1
    index = -1
    for time in timeDict.keys():
        
        if time in uniqueMTime:
            index = allMTime.index(time)
            lastKnownIndex = allMTime.index(time)
        else:
            index = lastKnownIndex
            
        direction = m[index][1]
        speed = m[index][2]
        timeDict[time].append(["Wind Direction", direction, "Wind Speed", speed])
        #timeDict[keyTriple].append(speed)
    
    return timeDict

            
    
    
    


def combineData(s, m, sensor_file_location):
    print("went into combineData")
    
    book = xlrd.open_workbook(sensor_file_location)
    bookDateMode = book.datemode
    timeDict = {}
    numToDateHashMap = {}
    
    for i in range(0, len(s)):
       
        timePeriod = datetime.datetime(*xlrd.xldate_as_tuple(s[i][2], bookDateMode))
        numToDateHashMap[s[i][2]] = timePeriod

        
        if s[i][2] not in timeDict.keys():
            timeDict[s[i][2]] = [[ s[i][1], s[i][0], s[i][3] ]]
        else:
            timeDict[s[i][2]].append([ s[i][1], s[i][0], s[i][3] ])
        
    for keyTriple in timeDict.keys():
        print(keyTriple, " ) ", timeDict[keyTriple])
        print()
        
        
    print("len(timeDict) = ",  len(timeDict))
        
    #newTimeDict = addMeteorDataToDict(timeDict, m)
    #return newTimeDict
    
    newTimeDict = addMeteorDataToDictTwo(timeDict, m)
    return newTimeDict, numToDateHashMap
    
    #return timeDict
    
    
    
    
    
    
    
    
    
    
    