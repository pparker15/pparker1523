def categoriesAndAddToDatabase(extractedLine, newSrc, newDst, newSrcNS, newDstNS, changed, myCollection):
    # Categories and application names.
    applications = [["FACEBOOK", "TWITTER", "SKYPE", "REDDIT"], ["BBC", "SKY", "YAHOO"], ["NETFLIX", "SPOTIFY"], ["8-BALL POOL"], ["AKAMAI", "GOOGLE", "FASTLY", "BT", "AMAZON", "MICROSOFT"]]
    categories = ["SOCIAL MEDIA", "NEWS", "STREAMING", "ONLINE GAMES", "CDN"]
    addedCat = "false"

    # Identify the category for each row.
    for section in applications:
        appIndex = applications.index(section)
        for app in section:
            if addedCat == "false":
                if(app in changed.upper()):
                    print(categories[appIndex] + " - " + extractedLine[0] + " - " + extractedLine[1] + " - " + extractedLine[4] + " - " + changed + " - " + extractedLine[11] + " - " + extractedLine[12])
                    addedCat = "true"
                    category = categories[appIndex]

                if(section.index(app) == 5 and appIndex == 4 and addedCat == "false"):
                    print("Unknown" + " - " + extractedLine[0] + " - " + extractedLine[1] + " - " + extractedLine[4] + " - " + changed + " - " + extractedLine[11] + " - " + extractedLine[12])
                    category = "Unknown"

    # Database output - need connection where module is imported.
    try:                                          
        myData = {"flow_category": category, "flow_date" : extractedLine[0], "flow_time" : extractedLine[1], "protocol" : extractedLine[4], "source_name_AS" : newSrc, "destination_name_AS" : newDst, "source_name_nslookup" : newSrcNS, "destination_name_nslookup" : newDstNS,"in_bytes" : extractedLine[11], "out_bytes" : extractedLine[12]}
        insertIntoDB = myCollection.insert_one(myData)
    except:
        print("Error inserting data into the database")  
