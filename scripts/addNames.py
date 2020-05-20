import mysql.connector
from mysql.connector import Error
connection = mysql.connector.connect(user='parker', password='password', host='192.168.20.30', database='application_identification')

# Add users to the name_table
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
                        asnLine = line.split('|')
                        cursor = connection.cursor()
                        insertData = ("INSERT INTO name_table (IP_address, AS_name, NS_name) VALUES (%s, %s, 'NA')")
                        data = (asnLine[1], asnLine[2])
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
                        cursor = connection.cursor()
                        updateData = ("UPDATE name_table SET NS_name = %s WHERE IP_address = %s")
                        data = (name.rstrip(), ipAddressSplit)
                        cursor.execute(updateData, data)
                        connection.commit()
                        if cursor.rowcount == 0:
                            cursor2 = connection.cursor()
                            insertData = ("INSERT INTO name_table (IP_address, AS_name, NS_name) VALUES (%s, 'NA', %s)")
                            data = (ipAddressSplit, name)
                            cursor2.execute(insertData, data)
                            cursor2.close()
                        cursor.close()
                    except Error as e: 
                        print(e)
                except:
                    continue

# Set the application ID for each IP address
try:
    getNames = connection.cursor()
    nameQuery = ("SELECT * FROM name_table")
    getNames.execute(nameQuery)
    nameResult = getNames.fetchall()
    for n in nameResult:
        aID = " "
        AppID = connection.cursor()
        query4 = ("SELECT * FROM Identify_apps")
        AppID.execute(query4)
        result4 = AppID.fetchall()
        printed = " "
        for r in result4:
            if r[1] in n[1] and printed != "true":
                aID = r[0]
                printed = "true"
            elif r[1] in n[2] and printed != "true":
                aID = r[0]
                printed = "true"
            elif printed != "true":
                aID = 1
        try:
            updateNames = connection.cursor()
            updateNameQuery = ("UPDATE name_table SET App_ID = %s WHERE IP_address = %s")
            dataAppID = (aID, n[0])
            updateNames.execute(updateNameQuery, dataAppID)
            connection.commit()
            updateNames.close()
            AppID.close()
        except Error as e:
            print(e)
    getNames.close()
except Error as e:
    print(e)
