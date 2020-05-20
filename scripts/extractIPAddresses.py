import mysql.connector
from mysql.connector import Error
connection = mysql.connector.connect(user='parker', password='password', host='192.168.20.30', database='application_identification')

with open("nfDumpOutput.txt", 'r') as captureFile:
    for captureLine in captureFile:
        if "Date" not in captureLine:
            if "Summary" not in captureLine:
                if "Time" not in captureLine:
                    if "Total" not in captureLine:
                        if "Sys:" not in captureLine:
                            try:
                                extractedLine = captureLine.split()
                                srcIP = extractedLine[5]
                                dstIP = extractedLine[7]
                                srcIP = srcIP.split(":", 1)[0]
                                dstIP = dstIP.split(":", 1)[0]
                                
                                #check the database to see if there is a match
                                checkMatch1 = connection.cursor()
                                query = "SELECT IP_address FROM name_table WHERE IP_address = %s"
                                # addr was added because it wouldn't work without it.
                                addr = (" " + srcIP,)
                                checkMatch1.execute(query, addr)
                                result = checkMatch1.fetchone()
                                if result is None:
                                    # output to file
                                    fileOut = open("ipAddressesPython.txt", 'a')
                                    fileOut.write(str(srcIP))
                                    fileOut.write('\n')
                                    fileOut.close()
                                checkMatch1.close()
                                checkMatch2 = connection.cursor()
                                query = "SELECT IP_address FROM name_table WHERE IP_address = %s"
                                addr2 = (" " + dstIP,)
                                checkMatch2.execute(query, addr2)
                                result = checkMatch2.fetchone()
                                if result is None:
                                    # output to file                                
                                    fileOut = open("ipAddressesPython.txt", 'a')
                                    fileOut.write(str(dstIP))
                                    fileOut.write('\n')
                                    fileOut.close()
                                checkMatch2.close()
                            except Error as e: 
                                print(e)
