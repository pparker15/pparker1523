import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta, time

connection = mysql.connector.connect(user='parker', password='password', host='192.168.20.30', database='user_profiling')
Time = []

try:
    cursor1 = connection.cursor()
    query = "SELECT * FROM user_profiling.application_type WHERE time_between_flows is not null and no_required_flows is not null"
    cursor1.execute(query)
    results = cursor1.fetchall()
    for app in results:
        print("Associating flows for " + app[1])
        # reset variables for each application
        numTime = 0
        num = -1
        previous = " "
        StartTimes = []
        newTimesList = []
        newTimesList.append([])
        loopNum = 0
        newStart = 0
        secondNum = 0
        rowSplit = app[4].split(" ")
        Time = []
        
        qApp = connection.cursor()
        query1 = "SELECT * FROM user_profiling.Flows WHERE Source_name = %s or Destination_name = %s"
        data = (app[1], app[1])
        qApp.execute(query1, data)
        result = qApp.fetchall()
        for r in result:
            Time.append(datetime.strptime(r[1], '%Y-%m-%d %H:%M:%S.%f'))
        qApp.close()
        
        for t in Time:
            if previous != " ":
                # keyword cannot be an expression error
                if rowSplit[1] == "minutes":
                    newTime = previous + timedelta(minutes = int(rowSplit[0]))
                    if(t <= newTime):
                        newTimesList[secondNum].append(t)
                    else:
                        newTimesList.append([])
                        secondNum += 1
                        newTimesList[secondNum].append(t)
                    previous = t
                else:
                    newTime = previous + timedelta(seconds = int(rowSplit[0]))                    
                    if(t <= newTime):
                        newTimesList[secondNum].append(t)
                    else:
                        newTimesList.append([])
                        secondNum += 1
                        newTimesList[secondNum].append(t)
                    previous = t
            else:
                previous = t
                newTimesList[secondNum].append(t)

        num = -1
        for element in newTimesList:
            length = len(element) - 1
            num += 1
            if(length >= app[5]):
                startTime = newTimesList[num][0]
                endTime = newTimesList[num][length]
                StartTimes.append((str(startTime) + "/" + str(endTime)))

        #output to the database      
        
        getFlows = connection.cursor()
        flowQuery = "SELECT * FROM Flows WHERE Flow_Category = 'CDN'"
        getFlows.execute(flowQuery)
        result = getFlows.fetchall()
        for res in result:
            times = StartTimes[numTime]
            splitTime = times.split("/")
            if res[1] + "000" >= splitTime[0] and res[1] + "000" <= splitTime[1]:
                addAssoc = connection.cursor()
                assocQuery = "INSERT INTO Associated (Flow_ID, Associated_With) Values (%s, %s) "
                data1 = (res[0], app[1])
                addAssoc.execute(assocQuery, data1)
                connection.commit()
                addAssoc.close()
            elif res[1] + "000" == splitTime[1] or res[1] + "000" >= splitTime[1]:
                comNum = len(StartTimes) - 1
                if numTime != comNum:
                    numTime += 1
       
    cursor1.close()                     
except Error as e:
    print(e)
