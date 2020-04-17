from datetime import datetime, timedelta, time
facebook = "n"
twitter = "n"
bbc = "n"
spotify = "n"
spotifyTime = []
facebookTime = []
previousTime = " "

# SPOTIFY

# Check to see if there is a streaming service running in the file.
# Do I need to only get the last request time not response time?
with open("spotifyfacebooktwitterbbcsky.txt") as file:
    number = -1
    for line in file:
        if "SPOTIFY" in line:
            spotify = "y"
            splitLine = line.split()
            spotifyTime.append(splitLine[2] + " " +splitLine[4])
            number += 1


# Convert to  time format to add and take away time
firstSpotify = datetime.strptime(spotifyTime[0], '%Y-%m-%d %H:%M:%S.%f')
estFirstSpotify = firstSpotify - timedelta(minutes = 10)
lastSpotify = datetime.strptime(spotifyTime[number], '%Y-%m-%d %H:%M:%S.%f')
estLastSpotify = lastSpotify + timedelta(minutes = 3)
#print(estFirstSpotify, estLastSpotify)


with open("spotifyfacebooktwitterbbcsky.txt") as file:
    for line in file:
        if "SOCIAL MEDIA" not in line:
            if "NEWS" not in line:
                # if the time on the line is after estFirstSpotify but before spotify
                splitLine = line.split()
                lineTime = splitLine[2] + " " + splitLine[4]
                lineTime = datetime.strptime(lineTime, '%Y-%m-%d %H:%M:%S.%f')
                #print out associated spotify if within the time frame otherwise just print the line
                if lineTime >= estFirstSpotify and lineTime <= estLastSpotify:
                    fileOut = open("AfterSpotify.txt", "a")
                    fileOut.write(str(line.rstrip() + " - " + "***ASSOCIATED SPOTIFY***"))
                    fileOut.write('\n')
                    fileOut.close()
                else:
                    fileOut = open("AfterSpotify.txt", "a")
                    fileOut.write(str(line))
                    fileOut.close()
            # Not spotify so print out the line
            else:
                fileOut = open("AfterSpotify.txt", "a")
                fileOut.write(str(line))
                fileOut.close()
        #not spotify so print out the line
        else:
            fileOut = open("AfterSpotify.txt", "a")
            fileOut.write(str(line))
            fileOut.close()


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
    if(length >= 6):
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
                print("NUMTIME USED")
