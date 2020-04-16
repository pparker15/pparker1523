from datetime import datetime, timedelta, time
facebook = "n"
twitter = "n"
bbc = "n"
spotify = "n"
spotifyTime = []
facebookTime = []
previousTime = " "
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

with open("AfterSpotify.txt") as file:
    number = -1
    for line in file:
        if "FACEBOOK" in line:
            facebook = "y"
            splitLine = line.split()
            newTime = datetime.strptime(splitLine[3] + " " + splitLine[5], '%Y-%m-%d %H:%M:%S.%f')
            # if 15 seconds later than previous stop counting facebook.
            # what happens if used  twice within the same document. This is what the main script is needed for. this is just a test. Proper development comes later.
            # just assume once for now.
            if previousTime != " ":
                testTime = previousTime + timedelta(seconds = 15)
                if newTime <= testTime:
                    facebookTime.append(newTime)
                    #print(splitLine[3] + " " + splitLine[5])

            previousTime = datetime.strptime(splitLine[3] + " " + splitLine[5], '%Y-%m-%d %H:%M:%S.%f')
            number +=1
previous = " "
num = 0
for time in facebookTime:
    if previous != " ":
        previous = previous + timedelta(seconds = 15)
        if time <= previous:
            print(time)
            num += 1
        else:
            facebookTime.remove(time)
    previous = time

with open("AfterSpotify.txt") as file:
    for line in file:
        if "STREAMING" not in line:
            if "NEWS" not in line:
                if "TWITTER" not in line:
                    splitLine = line.split()
                    if "SOCIAL MEDIA" in line:
                        lineTime = splitLine[3] + " " + splitLine[5]
                        lineTime = datetime.strptime(lineTime, '%Y-%m-%d %H:%M:%S.%f')
                    else:
                        lineTime = splitLine[2] + " " + splitLine[4]
                        lineTime = datetime.strptime(lineTime, '%Y-%m-%d %H:%M:%S.%f')
                   
                    if lineTime >= facebookTime[0] and lineTime <= facebookTime[num]:
                        fileOut = open("AfterFacebook.txt", "a")
                        fileOut.write(str(line.rstrip() + " - " + "***ASSOCIATED FACEBOOK***"))
                        fileOut.write('\n')
                        fileOut.close()
                    else:
                        fileOut = open("AfterFacebook.txt", "a")
                        fileOut.write(str(line))
                        fileOut.close()
                else:
                    fileOut = open("AfterFacebook.txt", "a")
                    fileOut.write(str(line))
                    fileOut.close()
            else:
                fileOut = open("AfterFacebook.txt", "a")
                fileOut.write(str(line))
                fileOut.close()
        else:
            fileOut = open("AfterFacebook.txt", "a")
            fileOut.write(str(line))
            fileOut.close()
