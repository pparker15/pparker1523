import pymongo
import CategoriesDatabase

# Database connections - added here to prevent continuous connections.
mongoCon = pymongo.MongoClient('mongodb://admin:password@192.168.20.31')
myDatabase = mongoCon["user_profiling"]
myCollection = myDatabase["moduleTest"]

srcIPchange = "false"
dstIPchange = "false"

# Take the nfdump file and loop through each line extracting the source IP address and destination IP address.
with open("nfDumpOutput.txt", 'r') as captureFile:
    for captureLine in captureFile:
        printed = "false"
        if "Date" not in captureLine:
            extractedLine = captureLine.split()
            try:
                srcIP = extractedLine[5]
                dstIP = extractedLine[7]
                srcIP = str(srcIP.split(":",1)[0])
                dstIP = str(dstIP.split(":",1)[0])
            except:
                continue
            
            # Extract the name from the whois output.
            with open("asnOutput.txt", 'r') as file:
                for line in file:
                    if "Bulk mode; " not in line:
                        if "Error: " not in line:
                            asnLine = line.split()
                            try:
                                if srcIP == asnLine[2]:
                                    srcIPchange = "true"
                                    newSrc = line.split("|")[-1]
                                elif dstIP == asnLine[2]:
                                    dstIPchange = "true"
                                    newDst = line.split("|")[-1]
                            except:
                                continue

                            if srcIPchange == "true" and dstIPchange == "true":
                                srcIPchange = "false"
                                dstIPchange = "false"

                                # Extract the name from the nslookup file
                                with open("nsOutput.txt", 'r') as file:
                                    for line in file:
                                        if printed != "true":
                                            if "Authoritative" not in line:
                                                if "** server " not in line:
                                                    ipAddressReverse = str(line.split(".in-addr",1)[0])
                                                    name = str(line.split("name = ", 1)[-1])
                                                    try:
                                                        ipAddressSplit = ipAddressReverse.split(".",4)[3] + "." + ipAddressReverse.split(".",4)[2] + "." + ipAddressReverse.split(".",4)[1] + "." + ipAddressReverse.split(".",4)[0]
                                                        if srcIP == ipAddressSplit:
                                                            newSrcNS = name
                                                            srcIPchange = "true"
                                                        elif dstIP == ipAddressSplit:
                                                            newDstNS = name
                                                            dstIPchange = "true"

                                                        if srcIPchange == "true" and dstIPchange == "true":
                                                            changed = newSrc.rstrip() + " - " + newDst.rstrip() + " - " + newSrcNS.rstrip() + " - " + newDstNS.rstrip()
                                                            # Added to prevent constant printing.
                                                            srcIPchange = "false"
                                                            dstIPchange = "false"
                                                            printed = "true"

                                                            # Identify the categories and add a new document to the database.
                                                            CategoriesDatabase.categoriesAndAddToDatabase(extractedLine, newSrc, newDst, newSrcNS, newDstNS, changed, myCollection)
                                                        
                                                    except:
                                                        continue
                                                    
                                                # If the address is not found, replace the ip address with unknown.
                                                else:
                                                    ipAddressUnknownRev = str(line.split(".in-addr",1)[0])
                                                    ipAddressUnknownRev = str(ipAddressUnknownRev.split("** server can't find ",1)[-1])
                                                    try:
                                                        ipAddressSplitUnk = ipAddressUnknownRev.split(".",4)[3] + "." + ipAddressUnknownRev.split(".",4)[2] + "." + ipAddressUnknownRev.split(".",4)[1] + "." + ipAddressUnknownRev.split(".",4)[0]
                                                        if srcIP == ipAddressSplitUnk:
                                                            newSrcNS = "Unknown"
                                                            srcIPchange = "true"
                                                        elif dstIP == ipAddressSplitUnk:
                                                            newDstNS = "Unknown"
                                                            dstIPchange = "true"

                                                        if srcIPchange == "true" and dstIPchange == "true":
                                                            changed = newSrc.rstrip() + " - " + newDst.rstrip() + " - " + newSrcNS.rstrip() + " - " + newDstNS.rstrip()

                                                            # Identify the categories and add a new document to the database.
                                                            CategoriesDatabase.categoriesAndAddToDatabase(extractedLine, newSrc, newDst, newSrcNS, newDstNS, changed, myCollection)
                                                    except:
                                                        continue
                                # As not all lines were printed, this ensures that each line is printed once the IP addresses are replaced.
                                try:
                                    if printed == "false":
                                        if srcIPchange == "true" and dstIPchange == "false":
                                            newDstNS = "Unknown"
                                        if dstIPchange == "true" and srcIPchange == "false":
                                            newSrcNS = "Unknown"

                                        changed = newSrc.rstrip() + " - " + newDst.rstrip() + " - " + newSrcNS.rstrip() + " - " + newDstNS.rstrip()

                                        # Identify the categories and add a new document to the database.
                                        CategoriesDatabase.categoriesAndAddToDatabase(extractedLine, newSrc, newDst, newSrcNS, newDstNS, changed, myCollection)
                                except:
                                    continue
