import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta, time
#connection = mysql.connector.connect(user='parker', password='password', host='192.168.20.30', database='application_identification')
connection = mysql.connector.connect(user='parker', password='password', host='192.168.20.30', database='user_profiling')

# Loop through the users to ensure association is kept separate for each user.
users = connection.cursor()
usersQuery = "SELECT DISTINCT application_type.App_ID, application_type.Application_name, application_type.Category FROM application_type INNER JOIN Identify_apps on application_type.App_ID = Identify_apps.App_ID WHERE application_type.Category = 'USERS'"
users.execute(usersQuery)
userResults = users.fetchall()
for user in userResults:
    try:
        # Retrieve the applications that can be identified by association
        cursor1 = connection.cursor()
        query = "SELECT * FROM application_type WHERE time_between_flows is not null and no_required_flows is not null"
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

            # Retrieve the times of all the flows for the user and application
            qApp = connection.cursor()
            #query1 = "SELECT * FROM Flows WHERE Source_Name = %s AND Destination_Name = %s or Destination_Name = %s AND Source_Name = %s"
            query1 = "SELECT Flows.Flow_ID, Flows.Flow_Date_Time, Flows.Source_Name_ID, Flows.Destination_Name_ID, Flows.Flow_Category, n1.App_ID, n2.App_ID FROM Flows INNER JOIN name_table as n1 on n1.name_id = Flows.Source_Name_ID INNER JOIN name_table as n2 on n2.name_id = Flows.Destination_Name_ID WHERE (n1.App_ID = %s and n2.App_ID = %s) or (n2.App_ID = %s and n1.App_ID = %s) ORDER BY Flows.Flow_Date_Time ASC"
            data = (user[0], app[0], user[0], app[0])
            qApp.execute(query1, data)
            result = qApp.fetchall()
            for r in result:
                Time.append(datetime.strptime(r[1], '%Y-%m-%d %H:%M:%S.%f'))
            qApp.close()
            
            # Check the flow is within the time limit
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
            # if the number of flows is greater or equal to the number of required flows, its a new instance of an application so get the first and last flow times.
            for element in newTimesList:
                length = len(element) - 1
                num += 1
                if(length >= app[5]):
                    startTime = newTimesList[num][0]
                    endTime = newTimesList[num][length]
                    StartTimes.append((str(startTime) + "/" + str(endTime)))

            #output to the database      
            # Get all the flows for that user between the start and end times that have the category of CDN or unknown
            getFlows = connection.cursor()
            #flowQuery = "SELECT * FROM Flows WHERE (Source_name = %s or Destination_name = %s) AND (Flow_Category = 'CDN' or Flow_Category = 'UNKNOWN')"
            flowQuery = "SELECT Flows.Flow_ID, Flows.Flow_Date_Time, Flows.Source_Name_ID, Flows.Destination_Name_ID, Flows.Flow_Category, n1.App_ID, n2.App_ID FROM Flows INNER JOIN name_table as n1 on n1.name_id = Flows.Source_Name_ID INNER JOIN name_table as n2 on n2.name_id = Flows.Destination_Name_ID WHERE (n1.App_ID = %s or n2.App_ID = %s) AND (Flows.Flow_Category = 'CDN' or Flows.Flow_Category = 'UNKNOWN') ORDER BY Flows.Flow_Date_Time ASC"
            data = (user[0], user[0])
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

                        # get the name_ID from source and destination
                        # find out the category of the name_ID
                        # if CDN or Unknown then add 1 to assocation stat within name_table



                        # select the category using name_id from the flows table - for the source - repeat for destination
                        #Where am i going to get the name_id from?
                        #source
                        cursor4 = connection.cursor()
                        query4 = "SELECT application_type.Category FROM name_table INNER JOIN application_type on application_type.App_ID = name_table.App_ID WHERE name_table.name_ID = %s"
                        data4 = (res[2],)
                        cursor4.execute(query4, data4)
                        result4 = cursor4.fetchone()
                        sourceCat = result4[0]
                        cursor4.close()

                        # destination
                        cursor5 = connection.cursor()
                        query5 = "SELECT application_type.Category FROM name_table INNER JOIN application_type on application_type.App_ID = name_table.App_ID WHERE name_table.name_ID = %s"
                        data5 = (res[3],)
                        cursor5.execute(query5, data5)
                        result5 = cursor5.fetchone()
                        destCat = result5[0]
                        cursor5.close()
                            
                       
                        

                        if sourceCat == "USERS":
                            # add +1 to the destID name thing where assoc app = spotify as an example
                            # need to get the app name
                            if (app[1] == "Twitter"):
                                updateTwitter = connection.cursor()
                                query6 = "UPDATE name_table SET Assoc_Twitter = Assoc_Twitter + 1 WHERE name_id = %s"
                                data6 = (res[3],)
                                updateTwitter.execute(query6, data6)
                                connection.commit()
                            elif (app[1] == "Facebook"):
                                updateTwitter = connection.cursor()
                                query6 = "UPDATE name_table SET Assoc_Facebook = Assoc_Facebook + 1 WHERE name_id = %s"
                                data6 = (res[3],)
                                updateTwitter.execute(query6, data6)
                                connection.commit()
                            elif (app[1] == "BBC"):
                                updateTwitter = connection.cursor()
                                query6 = "UPDATE name_table SET Assoc_BBC = Assoc_BBC + 1 WHERE name_id = %s"
                                data6 = (res[3],)
                                updateTwitter.execute(query6, data6)
                                connection.commit()
                            elif (app[1] == "Spotify"):
                                updateTwitter = connection.cursor()
                                query6 = "UPDATE name_table SET Assoc_Spotify = Assoc_Spotify + 1 WHERE name_id = %s"
                                data6 = (res[3],)
                                updateTwitter.execute(query6, data6)
                                connection.commit()
                        elif destCat == "USERS":
                            if (app[1] == "Twitter"):
                                updateTwitter = connection.cursor()
                                query6 = "UPDATE name_table SET Assoc_Twitter = Assoc_Twitter + 1 WHERE name_id = %s"
                                data6 = (res[2],)
                                updateTwitter.execute(query6, data6)
                                connection.commit()
                            elif (app[1] == "Facebook"):
                                updateTwitter = connection.cursor()
                                query6 = "UPDATE name_table SET Assoc_Facebook = Assoc_Facebook + 1 WHERE name_id = %s"
                                data6 = (res[2],)
                                updateTwitter.execute(query6, data6)
                                connection.commit()
                            elif (app[1] == "BBC"):
                                updateTwitter = connection.cursor()
                                query6 = "UPDATE name_table SET Assoc_BBC = Assoc_BBC + 1 WHERE name_id = %s"
                                data6 = (res[2],)
                                updateTwitter.execute(query6, data6)
                                connection.commit()
                            elif (app[1] == "Spotify"):
                                updateTwitter = connection.cursor()
                                query6 = "UPDATE name_table SET Assoc_Spotify = Assoc_Spotify + 1 WHERE name_id = %s"
                                data6 = (res[2],)
                                updateTwitter.execute(query6, data6)
                                connection.commit()
                  
                        updateTwitter.close()
                    # ensure each application instance is associated.
                    elif res[1] + "000" == splitTime[1] or res[1] + "000" >= splitTime[1]:
                        comNum = len(StartTimes) - 1
                        if numTime != comNum:
                            numTime += 1

             
        cursor1.close()                     
    except Error as e:
        print(e)
