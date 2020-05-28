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
                                name = connection.cursor(buffered=True)
                                #query = "SELECT application_type.Application_name, name_table.IP_address FROM application_type INNER JOIN name_table ON name_table.App_ID = application_type.App_ID WHERE name_table.IP_address = %s";
                                query = "SELECT name_ID FROM name_table WHERE IP_address = %s"
                                data = (" " + srcIP,)     
                                name.execute(query, data)
                                result = name.fetchone()
                                if result is not None:
                                    srcName = result[0]
                                name.close()
                            except Error as e:
                                 print(e)

                            try:
                                getDstName = connection.cursor(buffered=True)
                                #query2 = "SELECT application_type.Application_name, name_table.IP_address FROM application_type INNER JOIN name_table ON name_table.App_ID = application_type.App_ID WHERE name_table.IP_address = %s"
                                query2 = "SELECT name_ID FROM name_table WHERE IP_address = %s"
                                data2 = (" " + dstIP,)     
                                getDstName.execute(query2, data2)
                                result2 = getDstName.fetchone()
                                if result2 is not None:
                                    dstName = result2[0]
                                getDstName.close()
                            except Error as e:
                                print(e)

                            
                # Categorise the flow
                # check the category of the source and destination
                # the one that isn't USERS or NETWORK is to be used

                            srcCat = connection.cursor()
                            #srcQuery = "SELECT Category FROM application_type WHERE application_name = %s"
                            srcQuery = "SELECT application_type.Category FROM name_table INNER JOIN application_type on application_type.App_ID = name_table.App_ID WHERE name_table.name_id = %s"
                            data = (srcName,)
                            srcCat.execute(srcQuery, data)
                            result = srcCat.fetchone()
                            dstCat = connection.cursor()
                            #dstQuery = "SELECT Category FROM application_type WHERE application_name = %s"
                            dstQuery = "SELECT application_type.Category FROM name_table INNER JOIN application_type on application_type.App_ID = name_table.App_ID WHERE name_table.name_id = %s"
                            ddata = (dstName,)
                            dstCat.execute(dstQuery, ddata)
                            dresult = dstCat.fetchone()
                            if (dresult is None) or (result is None):
                                category = "UNKNOWN"
                            elif (dresult[0] == "USERS" or dresult[0] == "NETWORK") and (result[0] == "USERS" or result[0] == "NETWORK"):
                                category = "NETWORK"
                            elif(dresult[0] == "USERS" or dresult[0] == "NETWORK") and (result[0] != "USERS" or result[0] != "NETWORK"):
                                category = result[0]
                            elif(dresult[0] != "USERS" or dresult[0] != "NETWORK") and (result[0] == "USERS" or result[0] == "NETWORK"):
                                category = dresult[0]
                                

                # output to database - if still need to output nslookup or as name
                            
                
                            try:

                                
                                insertFlow = connection.cursor()
                                query3 = "INSERT INTO Flows (FLow_Date_Time, Source_Name_ID, Destination_Name_ID, Flow_Category) VALUES (%s, %s, %s, %s)"
                                if srcName != " " and dstName != " ":
                                    data3 = (extractedLine[0] + " " + extractedLine[1], srcName, dstName, category)
                                elif srcName != " " and dstName == " ":
                                    data3 = (extractedLine[0] + " " + extractedLine[1], srcName, "1", category)
                                elif srcName == " " and dstName != " ":
                                    data3 = (extractedLine[0] + " " + extractedLine[1], "1", dstName, category)
                                else:
                                    data3 = (extractedLine[0] + " " + extractedLine[1], "1", "1", category)
                                        
                                insertFlow.execute(query3, data3)
                                srcName = " "
                                dstName = " "
                                connection.commit()
                                insertFlow.close()
                            except Error as e:
                                print(e)

