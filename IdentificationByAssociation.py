import mysql.connector
from datetime import datetime, timedelta, time
import outputData

connection = mysql.connector.connect(user='parker', password='password', host='192.168.20.30', database='user_profiling')
spotifyTime = []
# Get application times just like before
# SPOTIFY
print("Identifying traffic associated with Spotify")

try:
    qSpotify = connection.cursor()
    query = "SELECT * FROM user_profiling.Flows WHERE Source_name = 'Spotify' or Destination_name = 'Spotify'"
    qSpotify.execute(query)
    result = qSpotify.fetchall()
    for r in result:
        spotifyTime.append(datetime.strptime(r[1], '%Y-%m-%d %H:%M:%S.%f'))
except Error as e:
    print(e)


previous = " "
StartTimes = []
newTimesList = []
newTimesList.append([])
loopNum = 0
newStart = 0
secondNum = 0
for time in spotifyTime:
    if previous != " ":
        # Time may need tweeking
        newTime = previous + timedelta(minutes = 10)
        # Less than
        if(time <= newTime):
            newTimesList[secondNum].append(time)
        else:
            newTimesList.append([])
            secondNum += 1
            newTimesList[secondNum].append(time)
        previous = time
    else:
        previous = time
        newTimesList[secondNum].append(time)

num = -1
for element in newTimesList:
    length = len(element) - 1
    num += 1
    if(length >= 2):
        startTime = newTimesList[num][0] - timedelta(minutes = 10)
        endTime = newTimesList[num][length] + timedelta(minutes = 10)
        StartTimes.append((str(startTime) + "/" + str(endTime)))

# output to database
    # search for flows within the time frames
try:
    for time in StartTimes:
        splitTime = time.split('/')
        tFlows = connection.cursor()
        tQuery = "SELECT * FROM Flows WHERE Flow_Date_Time between %s and %s"
        data = (splitTime[0], splitTime[1])
        tFlows.execute(tQuery, data)
        result = tFlows.fetchall()
        for r in result:
            if r[7] == "CDN":
                addAssoc = connection.cursor()
                assocQuery = "UPDATE Flows SET Assoc_1 = %s WHERE Flow_ID = %s"
                data = ("SPOTIFY", r[0])
                print(data)
                addAssoc.execute(assocQuery, data)
                connection.commit()
                addAssoc.close()
            
except Error as e:
    print(e)    


