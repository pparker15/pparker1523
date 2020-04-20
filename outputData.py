def database(line, connection):
    #database output
    extractedLine = line.split(" - ")
    length = len(extractedLine) - 1
    if length == 12:
        try:
            cursor = connection.cursor()
            insertData = ("INSERT INTO user_profiling.processed_nfdump_data (Category, Flow_date_time, Protocol, AS_Src, AS_Dst, NS_Src, NS_Dst, Associated_1, Associated_2, Associated_3) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
            data = (extractedLine[0], extractedLine[1] + " " + extractedLine[2], extractedLine[3], extractedLine[4], extractedLine[5], extractedLine[6], extractedLine[7], extractedLine[10], extractedLine[11], extractedLine[12])
            cursor.execute(insertData, data)
            cursor.close()
            connection.commit()
        except:
            print("1 - Error inserting data into the database")
    elif length == 11:
        try:
            cursor = connection.cursor()
            insertData = ("INSERT INTO user_profiling.processed_nfdump_data (Category, Flow_date_time, Protocol, AS_Src, AS_Dst, NS_Src, NS_Dst, Associated_1, Associated_2, Associated_3) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
            data = (extractedLine[0], extractedLine[1] + " " + extractedLine[2], extractedLine[3], extractedLine[4], extractedLine[5], extractedLine[6], extractedLine[7], extractedLine[10], extractedLine[11], " ")
            cursor.execute(insertData, data)
            cursor.close()
            connection.commit()
        except:
            print("2 - Error inserting data into the database")

    elif length == 10:
        try:
            cursor = connection.cursor()
            insertData = ("INSERT INTO user_profiling.processed_nfdump_data (Category, Flow_date_time, Protocol, AS_Src, AS_Dst, NS_Src, NS_Dst, Associated_1, Associated_2, Associated_3) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
            data = (extractedLine[0], extractedLine[1] + " " + extractedLine[2], extractedLine[3], extractedLine[4], extractedLine[5], extractedLine[6], extractedLine[7], extractedLine[10], " ", " ")
            cursor.execute(insertData, data)
            cursor.close()
            connection.commit()
        except:
            print("3 - Error inserting data into the database")

    else:
        try:
            cursor = connection.cursor()
            insertData = ("INSERT INTO user_profiling.processed_nfdump_data (Category, Flow_date_time, Protocol, AS_Src, AS_Dst, NS_Src, NS_Dst, Associated_1, Associated_2, Associated_3) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
            data = (extractedLine[0], extractedLine[1] + " " + extractedLine[2], extractedLine[3], extractedLine[4], extractedLine[5], extractedLine[6], extractedLine[7], " ", " ", " ")
            cursor.execute(insertData, data)
            cursor.close()
            connection.commit()
        except:
            print("4 - Error inserting data into the database")
    
def outputFile(line, application, fileOut):
    if application != " ":
        fileOut = open(fileOut, "a")
        fileOut.write(str(line.rstrip() + " - " + application))
        fileOut.write('\n')
        fileOut.close()
    else:
        fileOut = open(fileOut, "a")
        fileOut.write(str(line))
        fileOut.close()



