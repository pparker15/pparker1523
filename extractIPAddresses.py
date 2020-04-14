with open("0704output.txt", 'r') as captureFile:
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
                                fileOut = open("ipAddressesPython0704.txt", 'a')
                                fileOut.write(str(srcIP))
                                fileOut.write('\n')
                                fileOut.write(str(dstIP))
                                fileOut.write('\n')
                                fileOut.close()
                            except:
                                continue
print("completed")
