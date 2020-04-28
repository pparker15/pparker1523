import mysql.connector
from mysql.connector import Error
connection = mysql.connector.connect(user='parker', password='password', host='192.168.20.30', database='user_profiling')

with open("asnOutput.txt", 'r') as file:
    for line in file:
        if "Bulk mode; " not in line:
            if "Error: " not in line:
                if "AS" not in line:
                    try:
                        asnLine = line.split('|')
                        cursor = connection.cursor()
                        insertData = ("INSERT INTO name_table (IP_address, AS_name, AS_number, NS_name) VALUES (%s, %s, %s, 'NA')")
                        data = (asnLine[1], asnLine[2], asnLine[0])
                        cursor.execute(insertData, data)
                        cursor.close()
                        connection.commit()
                    except Error as e:
                        print(e)

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
                            insertData = ("INSERT INTO name_table (IP_address, AS_name, AS_number, NS_name) VALUES (%s, 'NA', 'NA', %s)")
                            data = (ipAddressSplit, name)
                            cursor.execute(insertData, data)
                            cursor2.close()
                        cursor.close()
                    except Error as e: 
                        print(e)
                except:
                    continue
                
                
