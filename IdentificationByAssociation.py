from datetime import datetime, timedelta, time
facebook = "n"
twitter = "n"
bbc = "n"
spotify = "n"
spotifyTime = []
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
estLastSpotify = lastSpotify + timedelta(minutes = 10)
print(estFirstSpotify, estLastSpotify)

with open("spotifyfacebooktwitterbbcsky.txt") as file:
    for line in file:
        if "SOCIAL MEDIA" not in line:
            if "NEWS" not in line:
                # if the time on the line is after estFirstSpotify but before spotify
                splitLine = line.split()
                lineTime = splitLine[2] + " " + splitLine[4]
                lineTime = datetime.strptime(lineTime, '%Y-%m-%d %H:%M:%S.%f')
                if lineTime >= estFirstSpotify and lineTime <= estLastSpotify:
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
