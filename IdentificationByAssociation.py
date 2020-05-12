import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta, time

connection = mysql.connector.connect(user='parker', password='password', host='192.168.20.30', database='user_profiling')
# need to add differentiation between users
users = connection.cursor()
usersQuery = "SELECT DISTINCT application_type.App_ID, application_type.Application_name, application_type.Category FROM application_type INNER JOIN Identify_apps on application_type.App_ID = Identify_apps.App_ID WHERE application_type.Category = 'USERS'"
users.execute(usersQuery)
userResults = users.fetchall()
for user in userResults:
    try:
        cursor1 = connection.cursor()
        query = "SELECT * FROM user_profiling.application_type WHERE time_between_flows is not null and no_required_flows is not null"
        cursor1.execute(query)
        results = cursor1.fetchall()
        for app in results:
            print("Associating flows for " + app[1] + " and " + user[1])
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
            #query1 = "SELECT * FROM user_profiling.Flows WHERE Source_name = %s or Destination_name = %s"
            query1 = "SELECT * FROM user_profiling.Flows WHERE Source_Name = %s AND Destination_Name = %s or Destination_Name = %s AND Source_Name = %s";
            data = (user[1], app[1], user[1], app[1])
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
            flowQuery = "SELECT * FROM Flows WHERE (Source_name = %s or Destination_name = %s) AND (Flow_Category = 'CDN' or Flow_Category = 'UNKNOWN')"
            data = (user[1], user[1])
            getFlows.execute(flowQuery, data)
            result = getFlows.fetchall()
            for res in result:
                if len(StartTimes) != 0:
                    times = StartTimes[numTime]
                    splitTime = times.split("/")
                    if res[1] + "000" >= splitTime[0] and res[1] + "000" <= splitTime[1]:
                        try:
                            addAssoc = connection.cursor()
                            assocQuery = "INSERT INTO Associated (Flow_ID, Associated_App_ID) Values (%s, %s)"
                            data1 = (res[0], app[0])
                            addAssoc.execute(assocQuery, data1)
                            connection.commit()
                            addAssoc.close()
                        except Error as e:
                            print(e)


                        # insert into stats table
                        # get current number from the stats table
                        getStats = connection.cursor()
                        statQuery = "SELECT * FROM stats_table"
                        getStats.execute(statQuery)
                        statResults = getStats.fetchall()
                        ID = ' '
                        if "User" in res[2]:
                            getAppID2 = connection.cursor()
                            newQuery = "SELECT App_ID FROM application_type WHERE Application_name = %s"
                            dataAppID = (res[3],)
                            getAppID2.execute(newQuery, dataAppID)
                            resultAppID = getAppID2.fetchone()
                            ID = resultAppID[0]
                            getAppID2.close()
                        elif "User" in res[3]:
                            getAppID2 = connection.cursor()
                            newQuery = "SELECT App_ID FROM application_type WHERE Application_name = %s"
                            dataAppID = (res[2],)
                            getAppID2.execute(newQuery, dataAppID)
                            resultAppID = getAppID2.fetchone()
                            ID = resultAppID[0]
                            getAppID2.close()
                        # update the current number in the stats table
                        updateStats = connection.cursor()
                        if app[2] == "SOCIAL MEDIA":
                            statQuery = "UPDATE stats_table SET Assoc_Social_Media = Assoc_Social_Media + 1 WHERE App_ID = %s"
                            dataStats = (ID,)
                            updateStats.execute(statQuery, dataStats)
                            connection.commit()
                        elif app[2] == "NEWS":
                            statQuery = "UPDATE stats_table SET Assoc_News = Assoc_News + 1 WHERE App_ID = %s"
                            dataStats = (ID,)
                            updateStats.execute(statQuery, dataStats)
                            connection.commit()
                        elif app[2] == "STREAMING":
                            statQuery = "UPDATE stats_table SET Assoc_Streaming = Assoc_Streaming + 1 WHERE App_ID = %s"
                            dataStats = (ID,)
                            updateStats.execute(statQuery, dataStats)
                            connection.commit()
                        elif app[2] == "EDUCATION":
                            statQuery = "UPDATE stats_table SET Assoc_Education = Assoc_Education + 1 WHERE App_ID = %s"
                            dataStats = (ID,)
                            updateStats.execute(statQuery, dataStats)
                            connection.commit()
                        elif app[2] == "SHOPPING":
                            statQuery = "UPDATE stats_table SET Assoc_Shopping = Assoc_Shopping + 1 WHERE App_ID = %s"
                            dataStats = (ID,)
                            updateStats.execute(statQuery, dataStats)
                            connection.commit()
                    
                        updateStats.close() 
                    elif res[1] + "000" == splitTime[1] or res[1] + "000" >= splitTime[1]:
                        comNum = len(StartTimes) - 1
                        if numTime != comNum:
                            numTime += 1

             
        cursor1.close()                     
    except Error as e:
        print(e)
