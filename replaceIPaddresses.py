# database connection
import mysql.connector
from mysql.connector import Error
connection = mysql.connector.connect(user='parker', password='password', host='192.168.20.30', database='user_profiling')
srcName = " "
dstName = " "
# loop through nfdump file
with open("nfDumpOutput.txt", 'r') as captureFile:
    for captureLine in captureFile:
        if "Date" not in captureLine:
            if "Summary" not in captureLine:
                if "Time" not in captureLine:
                    if "Total" not in captureLine:
                        if "Sys:" not in captureLine:
                            extractedLine = captureLine.split()
                            try:
                                srcIP = extractedLine[5]
                                dstIP = extractedLine[7]
                                srcIP = str(srcIP.split(":",1)[0])
                                dstIP = str(dstIP.split(":",1)[0])
                            except:
                                continue
                # Get source and destination name from the database
                            
                            try:
                                getSrcName = connection.cursor()
                                query = "SELECT application_type.Application_name, name_table.IP_address FROM application_type INNER JOIN name_table ON name_table.App_ID = application_type.App_ID WHERE name_table.IP_address = %s";
                                data = (" " + srcIP,)     
                                getSrcName.execute(query, data)
                                result = getSrcName.fetchone()
                                if result is not None:
                                    srcName = result[0]
                                getSrcName.close()
                            except Error as e:
                                print(e)

                            try:
                                getDstName = connection.cursor()
                                query2 = "SELECT application_type.Application_name, name_table.IP_address FROM application_type INNER JOIN name_table ON name_table.App_ID = application_type.App_ID WHERE name_table.IP_address = %s";
                                data2 = (" " + dstIP,)     
                                getDstName.execute(query2, data2)
                                result2 = getDstName.fetchone()
                                if result2 is not None:
                                    dstName = result2[0]
                                getDstName.close()
                            except Error as e:
                                print(e)

                # output to database
                            try:
                                insertFlow = connection.cursor()
                                query3 = "INSERT INTO Flows (FLow_Date_Time, Source_Name, Destination_Name) VALUES (%s, %s, %s)"
                                if srcName != " " and dstName != " ":
                                    data = (extractedLine[0] + " " + extractedLine[1], srcName, dstName)
                                elif srcName != " " and dstName == " ":
                                    data = (extractedLine[0] + " " + extractedLine[1], srcName, "Unknown")
                                elif srcName == " " and dstName != " ":
                                    data = (extractedLine[0] + " " + extractedLine[1], "Unknown", dstName)
                                else:
                                    data = (extractedLine[0] + " " + extractedLine[1], "Unknown", "Unknown")
                                insertFlow.execute(query3, data)
                                print(data)
                                srcName = " "
                                dstName = " "
                                connection.commit()
                                insertFlow.close()
                            except Error as e:
                                print(e)


