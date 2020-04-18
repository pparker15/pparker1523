from datetime import datetime, timedelta, time
spotifyTime = []
facebookTime = []
previousTime = " "
twitterTime = []
bbcTime = []

# SPOTIFY

with open("spotifyfacebooktwitterbbcsky.txt") as file:
    number = -1
    for line in file:
        if "SPOTIFY" in line:
            splitLine = line.split()
            spotifyTime.append(datetime.strptime(splitLine[2] + " " + splitLine[4], '%Y-%m-%d %H:%M:%S.%f'))
            number += 1

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

numTime = 0
with open("spotifyfacebooktwitterbbcsky.txt") as file:
    for line in file:
        if "SOCIAL MEDIA" not in line:
            if "NEWS" not in line:
                # if the time on the line is after estFirstSpotify but before spotify
                times = StartTimes[numTime]
                splitTime = times.split("/")
                lineSplit = line.split()
                splitLine = line.split()
                lineTime = splitLine[2] + " " + splitLine[4]
                if lineTime + "000" >= splitTime[0] and lineTime + "000" <= splitTime[1]:
                    fileOut = open("AfterSpotify.txt", "a")
                    fileOut.write(str(line.rstrip() + " - " + "***ASSOCIATED SPOTIFY***"))
                    fileOut.write('\n')
                    fileOut.close()
            else:
                fileOut = open("AfterSpotify.txt", "a")
                fileOut.write(str(line))
                fileOut.close()
        else:
            fileOut = open("AfterSpotify.txt", "a")
            fileOut.write(str(line))
            fileOut.close()
        if lineTime + "000" == splitTime[1]:
            comNum = len(StartTimes) - 1
            if numTime != comNum:
                numTime += 1

# FACEBOOK

# look for facebook in the line and add the time to a list.
with open("AfterSpotify.txt") as file:
    for line in file:
        if "FACEBOOK" in line:
            splitLine = line.split()
            facebookTime.append(datetime.strptime(splitLine[3] + " " + splitLine[5], '%Y-%m-%d %H:%M:%S.%f'))

previous = " "
StartTimes = []
newTimesList = []
newTimesList.append([])
loopNum = 0
newStart = 0
secondNum = 0
for time in facebookTime:
    if previous != " ":
        # Time may need tweeking
        newTime = previous + timedelta(seconds = 15)
        #print(time, newTime)
        # Less than
        if(time <= newTime):
            #loopNum +=1
            #print(loopNum)
            newTimesList[secondNum].append(time)
        else:
            #StartTimes.append(facebookTime.index(time))
            newTimesList.append([])
            secondNum += 1
            newTimesList[secondNum].append(time)
        previous = time
    else:
        previous = time
        newTimesList[secondNum].append(time)

#print(len(newTimesList[0]))
num = -1
for element in newTimesList:
    length = len(element) - 1
    num += 1
    if(length >= 4):
        startTime = newTimesList[num][0]
        endTime = newTimesList[num][length]
        StartTimes.append((str(startTime) + "/" + str(endTime)))
        
numTime = 0
with open("AfterSpotify.txt") as file:
    for line in file:
        times = StartTimes[numTime]
        splitTime = times.split("/")
        lineSplit = line.split()
        if "SOCIAL MEDIA" in line:
            lineTime = lineSplit[3] + " " + lineSplit[5]
        else:
            lineTime = lineSplit[2] + " " + lineSplit[4]
        if lineTime + "000" >= splitTime[0] and lineTime + "000" <= splitTime[1]:
            if "STREAMING" or "NEWS" or "TWITTER" not in line:
                fileOut = open("AfterFacebook.txt", "a")
                fileOut.write(str(line.rstrip() + " - " + "***ASSOCIATED FACEBOOK***"))
                fileOut.write('\n')
                fileOut.close()
        else:
            # Prints out the beginning of the file but not the end. Why?
            fileOut = open("AfterFacebook.txt", "a")
            fileOut.write(line.rstrip())
            fileOut.write('\n')
            fileOut.close()
        if lineTime + "000" == splitTime[1]:
            print(numTime, len(StartTimes))
            comNum = len(StartTimes) - 1
            print(numTime, comNum)
            if numTime != comNum:
                numTime += 1

# TWITTER
# look for twitter in the line and add the time to a list.
with open("AfterFacebook.txt") as file:
    for line in file:
        if "TWITTER" in line:
            splitLine = line.split()
            twitterTime.append(datetime.strptime(splitLine[3] + " " + splitLine[5], '%Y-%m-%d %H:%M:%S.%f'))

previous = " "
StartTimes = []
newTimesList = []
newTimesList.append([])
loopNum = 0
newStart = 0
secondNum = 0
for time in twitterTime:
    if previous != " ":
        # Time may need tweeking
        newTime = previous + timedelta(seconds = 30)
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
    if(length >= 6):
        startTime = newTimesList[num][0]
        endTime = newTimesList[num][length]
        StartTimes.append((str(startTime) + "/" + str(endTime)))
        
numTime = 0
with open("AfterFacebook.txt") as file:
    for line in file:
        times = StartTimes[numTime]
        splitTime = times.split("/")
        lineSplit = line.split()
        if "SOCIAL MEDIA" in line:
            lineTime = lineSplit[3] + " " + lineSplit[5]
        else:
            lineTime = lineSplit[2] + " " + lineSplit[4]
        if lineTime + "000" >= splitTime[0] and lineTime + "000" <= splitTime[1]:
            if "STREAMING" or "NEWS" or "FACEBOOK" not in line:
                fileOut = open("AfterTwitter.txt", "a")
                fileOut.write(str(line.rstrip() + " - " + "***ASSOCIATED TWITTER***"))
                fileOut.write('\n')
                fileOut.close()
        else:
            # Prints out the beginning of the file but not the end. Why?
            fileOut = open("AfterTwitter.txt", "a")
            fileOut.write(line.rstrip())
            fileOut.write('\n')
            fileOut.close()
        if lineTime + "000" == splitTime[1]:
            print(numTime, len(StartTimes))
            comNum = len(StartTimes) - 1
            print(numTime, comNum)
            if numTime != comNum:
                numTime += 1

# BBC
# look for BBC in the line and add the time to a list.
with open("AfterTwitter.txt") as file:
    for line in file:
        if "BBC" in line:
            splitLine = line.split()
            bbcTime.append(datetime.strptime(splitLine[2] + " " + splitLine[4], '%Y-%m-%d %H:%M:%S.%f'))

previous = " "
StartTimes = []
newTimesList = []
newTimesList.append([])
loopNum = 0
newStart = 0
secondNum = 0
for time in bbcTime:
    if previous != " ":
        # Time may need tweeking
        newTime = previous + timedelta(seconds = 20)
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
    if(length >= 6):
        startTime = newTimesList[num][0]
        endTime = newTimesList[num][length]
        StartTimes.append((str(startTime) + "/" + str(endTime)))
        
numTime = 0
with open("AfterTwitter.txt") as file:
    for line in file:
        times = StartTimes[numTime]
        splitTime = times.split("/")
        lineSplit = line.split()
        if "SOCIAL MEDIA" in line:
            lineTime = lineSplit[3] + " " + lineSplit[5]
        else:
            lineTime = lineSplit[2] + " " + lineSplit[4]
        if lineTime + "000" >= splitTime[0] and lineTime + "000" <= splitTime[1]:
            if "STREAMING" or "SOCIAL MEDIA" not in line:
                fileOut = open("AfterBBC.txt", "a")
                fileOut.write(str(line.rstrip() + " - " + "***ASSOCIATED BBC***"))
                fileOut.write('\n')
                fileOut.close()
        else:
            # Prints out the beginning of the file but not the end. Why?
            fileOut = open("AfterBBC.txt", "a")
            fileOut.write(line.rstrip())
            fileOut.write('\n')
            fileOut.close()
        if lineTime + "000" == splitTime[1]:
            print(numTime, len(StartTimes))
            comNum = len(StartTimes) - 1
            print(numTime, comNum)
            if numTime != comNum:
                numTime += 1