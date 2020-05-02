import mysql.connector
from mysql.connector import Error
connection = mysql.connector.connect(user='parker', password='password', host='192.168.20.30', database='user_profiling')

# select from identifying table where = users
getUsers = connection.cursor()
userQuery = "SELECT application_type.App_ID, application_type.Application_name, Identify_apps.identify_by FROM application_type INNER JOIN Identify_apps on application_type.App_ID = Identify_apps.App_ID WHERE application_type.Category = 'USERS'"
getUsers.execute(userQuery)
userResults = getUsers.fetchall()

for user in userResults:
    with open("sortOutput.txt", 'r') as ipFile:
        for IPaddr in ipFile:
            if IPaddr.rstrip() == user[2]:
                insertUser = connection.cursor()
                insertQuery = "INSERT INTO name_table (IP_address, AS_name, NS_name, App_ID) VALUES (%s, %s, %s, %s)"
                data = (" " + IPaddr.rstrip(), user[1], user[1], user[0])
                print(data)
                insertUser.execute(insertQuery, data)
                connection.commit()
                insertUser.close()
getUsers.close()

# use AS mapping
with open("asnOutput.txt", 'r') as file:
    for line in file:
        if "Bulk mode; " not in line:
            if "Error: " not in line:
                if "AS" not in line:
                    try:
                        aID = " "
                        asnLine = line.split('|')
                        try:
                            AppID = connection.cursor()
                            query4 = "SELECT * FROM Identify_apps"
                            AppID.execute(query4)
                            result4 = AppID.fetchall()
                            printed = " "
                            for r in result4:
                                if r[1] in asnLine[2] and printed != "true":
                                    aID = r[0]
                                    printed = "true"
                                elif printed != "true":
                                    aID = r[0]
                                
                        except Error as e:
                            print(e)
                        cursor = connection.cursor()
                        insertData = ("INSERT INTO name_table (IP_address, AS_name, NS_name, App_ID) VALUES (%s, %s, 'NA', %s)")
                        data = (asnLine[1], asnLine[2], aID)
                        cursor.execute(insertData, data)
                        cursor.close()
                        connection.commit()
                    except Error as e:
                        print(e)


# use NSlookup
with open("nsOutput.txt", 'r') as file:
    for line in file:
        if "Authoritative" not in line:
            if "** server " not in line:
                try:
                    ipAddressReverse = str(line.split(".in-addr",1)[0])
                    ipAddressSplit = " " + ipAddressReverse.split(".",4)[3] + "." + ipAddressReverse.split(".",4)[2] + "." + ipAddressReverse.split(".",4)[1] + "." + ipAddressReverse.split(".",4)[0]
                    name = str(line.split("name = ", 1)[-1])
                    try:
                        try:
                            AppID = connection.cursor()
                            query6 = "SELECT * FROM Identify_apps"
                            AppID.execute(query6)
                            result6 = AppID.fetchall()
                            printed = " "
                            for r in result6:
                                if r[1] in name and printed != "true":
                                    aID = r[0]
                                    printed = "true"
                                elif printed != "true":
                                    aID = r[0]
                        except Error as e:
                            print(e)
                        cursor = connection.cursor()
                        updateData = ("UPDATE name_table SET NS_name = %s, App_ID = %s WHERE IP_address = %s")
                        data = (name.rstrip(), aID, ipAddressSplit)
                        cursor.execute(updateData, data)
                        connection.commit()
                        if cursor.rowcount == 0:
                            try:
                                AppID = connection.cursor()
                                query5 = "SELECT * FROM Identify_apps"
                                AppID.execute(query5)
                                result5 = AppID.fetchall()
                                printed = " "
                                for r in result5:
                                    if r[1] in name and printed != "true":
                                        aID = r[0]
                                        printed = "true"
                                    elif printed != "true":
                                        aID = r[0]
                                
                            except Error as e:
                                print(e)
                            cursor2 = connection.cursor()
                            insertData = ("INSERT INTO name_table (IP_address, AS_name, NS_name, App_ID) VALUES (%s, 'NA', %s, %s)")
                            data = (ipAddressSplit, name, aID)
                            cursor2.execute(insertData, data)
                            cursor2.close()
                        cursor.close()
                    except Error as e: 
                        print(e)
                except:
                    continue
