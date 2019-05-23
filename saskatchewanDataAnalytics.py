from datetime import datetime

class Parser:
    def __init__(self):
        self.numberOfDays = 0 # Count number of days passed
        
        self.startDate = datetime.today()
        self.endDate = datetime.today()
        
        self.fileTypeDict = {} # Contains file extension - file type information
        self.initializeFileType()
        
    def initializeFileType(self):  # Define file types for each file
        self.fileTypeDict["html"] = "HTML"
        self.fileTypeDict["htm"] = "HTML"
        self.fileTypeDict["shtml"] = "HTML"
        self.fileTypeDict["map"] = "HTML"

        self.fileTypeDict["gif"] = "Images"
        self.fileTypeDict["jpeg"] = "Images"
        self.fileTypeDict["jpg"] = "Images"
        self.fileTypeDict["xbm"] = "Images"
        self.fileTypeDict["bmp"] = "Images"
        self.fileTypeDict["rgb"] = "Images"
        self.fileTypeDict["xpm"] = "Images"

        self.fileTypeDict["au"] = "Sound"
        self.fileTypeDict["snd"] = "Sound"
        self.fileTypeDict["wav"] = "Sound"
        self.fileTypeDict["mid"] = "Sound"
        self.fileTypeDict["midi"] = "Sound"
        self.fileTypeDict["lha"] = "Sound"
        self.fileTypeDict["aif"] = "Sound"
        self.fileTypeDict["aiff"] = "Sound"

        self.fileTypeDict["mov"] = "Video"
        self.fileTypeDict["movie"] = "Video"
        self.fileTypeDict["avi"] = "Video"
        self.fileTypeDict["qt"] = "Video"
        self.fileTypeDict["mpeg"] = "Video"
        self.fileTypeDict["mpg"] = "Video"

        self.fileTypeDict["ps"] = "Formatted"
        self.fileTypeDict["eps"] = "Formatted"
        self.fileTypeDict["doc"] = "Formatted"
        self.fileTypeDict["dvi"] = "Formatted"
        self.fileTypeDict["txt"] = "Formatted"

        self.fileTypeDict["cgi"] = "Dynamic"
        self.fileTypeDict["pl"] = "Dynamic"
        self.fileTypeDict["cgi-bin"] = "Dynamic"

    def parse(self, logFile):  # Read each line from the log and process output
        index = 0
        counter = 0
        transferredBytes = 0
        succCount = 0
        notModiCount = 0
        foundCount = 0
        unsuccCount = 0
        localClientCount = 0
        remoteClientCount = 0
        localClientBytes = 0
        remoteClientBytes = 0
        totalSuccBytes = 0
        videoCount = 0
        soundCount = 0
        dynamicCount = 0
        formattedCount = 0
        htmlCount = 0
        imagesCount = 0
        othersCount = 0
        videoBytes = 0
        soundBytes = 0
        dynamicBytes = 0
        formattedBytes = 0
        htmlBytes = 0
        imagesBytes = 0
        othersBytes = 0
        uniqueObjCount = 0
        uniqueObjDict = {}
        uniqueObjByteTotal = 0
        uniqueObjByteDict = {}
        accessedOnceCount = 0
        accessedOnceBytes = 0
        for line in logFile:
            elements = line.split()
            
            # Skip to the next line if this line has an empty string
            if line is '':continue

            # Skip to the next line if this line contains not equal to 9 - 11 elements
            if not (9 <= len(elements) <= 11):continue

            # If there is more than 1 element in user information, correct the index of other elements
            timeStrIndex = 0
            for idx, val in enumerate(elements):
                timeStrIndex = idx - 1
                if '-0600]' == val:break

            sourceAddress = elements[0]
            timeStr = elements[timeStrIndex].replace('[', '')
            requestMethod = elements[timeStrIndex+2].replace('"','')
            requestFileName = elements[timeStrIndex + 3].replace('"', '')
            responseCode = elements[len(elements) - 2]
            replySizeInBytes = elements[len(elements) - 1]

            ################## From Here, implement your parser ##################
            # Inside the for loop, do simple variable assignments & modifications
            # Please do not add for loop/s
            # Only the successful requests should be used from question 5 onward

            # Prints assigned elements. Please comment print statement.
            #print('{0} , {1} , {2} , {3} , {4} , {5} '.format(sourceAddress,timeStr,requestMethod,requestFileName,responseCode, replySizeInBytes),end="")
            
            # Assigns & prints format type. Please comment print statement.
            fileType = self.getFileType(requestFileName)
            #print(' , {0}'.format(fileType))

            # Q1: Write a condition to identify a start date and an end date.


            if responseCode == "200":
                succCount += 1
                #Q10
                if requestFileName not in uniqueObjDict:
                    uniqueObjDict[requestFileName] = 1
                    uniqueObjCount += 1
                    uniqueObjByteDict[requestFileName] = replySizeInBytes
                    uniqueObjByteTotal += int(replySizeInBytes)
                elif requestFileName in uniqueObjDict:
                    uniqueObjDict[requestFileName] = uniqueObjDict[requestFileName] + 1
                    
            if responseCode == "304":
                notModiCount += 1
            if responseCode == "302":
                foundCount += 1
            if responseCode[0] == "4" or responseCode[0] == "5":
                unsuccCount += 1

            if ("usask.ca" in sourceAddress or sourceAddress[0:7] == "128.233") and responseCode == "200":
                localClientCount += 1
                if responseCode == "200" and replySizeInBytes[0] != "-":
                    localClientBytes += int(replySizeInBytes)
            elif responseCode == "200":
                remoteClientCount += 1
                if responseCode == "200" and replySizeInBytes[0] != "-":
                    remoteClientBytes += int(replySizeInBytes)
               
            if replySizeInBytes[0] != "-":
                transferredBytes += int(replySizeInBytes)

            #Q7        
            if responseCode == "200":
                if ".html" in requestFileName.lower() or ".htm" in requestFileName.lower() or ".shtml" in requestFileName.lower() or ".map" in requestFileName.lower():
                    htmlCount += 1
                    htmlBytes += int(replySizeInBytes)
                elif  ".gif" in requestFileName.lower() or ".jpg" in requestFileName.lower() or ".jpeg" in requestFileName.lower() or ".xbm" in requestFileName.lower() \
                   or ".bmp" in requestFileName.lower() or ".rgb" in requestFileName.lower() or ".xpm" in requestFileName.lower():
                    imagesCount += 1
                    imagesBytes += int(replySizeInBytes)
                elif ".au" in requestFileName.lower() or ".snd" in requestFileName.lower() or ".wav" in requestFileName.lower() or ".mid" in requestFileName.lower() \
                   or ".mid" in requestFileName.lower() or ".midi" in requestFileName.lower() or ".lha" in requestFileName.lower() or ".aif" in requestFileName.lower() \
                   or ".aiff" in requestFileName.lower():
                    soundCount += 1
                    soundBytes += int(replySizeInBytes)
                elif ".mov" in requestFileName.lower() or ".movie" in requestFileName.lower() or ".avi" in requestFileName.lower() or ".qt" in requestFileName.lower() \
                   or ".mpeg" in requestFileName.lower() or ".mpg" in requestFileName.lower():
                    videoCount += 1
                    videoBytes += int(replySizeInBytes)
                elif ".ps" in requestFileName.lower() or ".eps" in requestFileName.lower() or ".doc" in requestFileName.lower() or ".dvi" in requestFileName.lower() or ".txt" in requestFileName.lower():
                    formattedCount += 1
                    formattedBytes += int(replySizeInBytes)
                elif "cgi-bin" in requestFileName.lower() or ".cgi" in requestFileName.lower() or ".pl" in requestFileName.lower():
                    dynamicCount += 1
                    dynamicBytes += int(replySizeInBytes)
                else:
                    othersCount += 1
                    if "-" not in replySizeInBytes:
                        othersBytes += int(replySizeInBytes)
        
            if counter == 0:
                self.startDate = datetime.strptime(timeStr, "%d/%b/%Y:%H:%M:%S")
                print(self.startDate)
            counter += 1
        self.endDate = datetime.strptime(timeStr, "%d/%b/%Y:%H:%M:%S")
        print(self.endDate)
        print((self.endDate - self.startDate))
        avgRequestPerDay = (counter / (self.endDate - self.startDate).days)
        print(counter, "requests")
        print(avgRequestPerDay, "average requests per day")
        print("")
        print(transferredBytes, "Bytes transferred")
        print("")
        print(transferredBytes/(self.endDate - self.startDate).days, "Bytes per day")
        print("")
        print("4")
        print("Successful:", succCount, "%.2f" % round(succCount / counter * 100, 2))
        print("Not modified:", notModiCount, "%.2f" % round(notModiCount / counter * 100, 2))
        print("Found:", foundCount, "%.2f" % round(foundCount / counter * 100, 2))
        print("Unuccessful:", unsuccCount, "%.2f" % round(unsuccCount / counter * 100, 2))
        print("Total:", succCount + notModiCount + foundCount + unsuccCount)
        print("")
        print("5")
        print("Local client request:", localClientCount, "%.2f" % round(localClientCount / succCount * 100, 2))
        print("Remote client request:", remoteClientCount, "%.2f" % round(remoteClientCount / succCount * 100, 2))
        print("Total client request:", localClientCount + remoteClientCount)
        print("")
        print("6")
        print("Local client bytes:", localClientBytes, "%.2f" % round(localClientBytes / (localClientBytes + remoteClientBytes) * 100, 2))
        print("Remote client bytes:", remoteClientBytes, "%.2f" % round(remoteClientBytes / (localClientBytes + remoteClientBytes) * 100, 2))
        print("Total successful bytes:", localClientBytes + remoteClientBytes)
        print("")
        print("7")
        print("HTML Count:", htmlCount, "%.2f" % round(htmlCount / succCount * 100, 2))
        print("Images Count:", imagesCount, "%.2f" % round(imagesCount / succCount * 100, 2))
        print("Sound Count:", soundCount, "%.2f" % round(soundCount / succCount * 100, 2))
        print("Video Count:", videoCount, "%.2f" % round(videoCount / succCount * 100, 2))
        print("Formatted Count:", formattedCount, "%.2f" % round(formattedCount / succCount * 100, 2))
        print("Dynamic Count:", dynamicCount, "%.2f" % round(dynamicCount / succCount * 100, 2))
        print("Others Count:", othersCount, "%.2f" % round(othersCount / succCount * 100, 2))
        print("Total Count:", htmlCount + imagesCount + soundCount + videoCount + formattedCount + dynamicCount + othersCount)
        print("")
        print("8")
        print("HTML Bytes:", htmlBytes, "%.2f" % round(htmlBytes / (localClientBytes + remoteClientBytes) * 100, 2))
        print("Images Bytes:", imagesBytes, "%.2f" % round(imagesBytes / (localClientBytes + remoteClientBytes) * 100, 2))
        print("Sound Bytes:", soundBytes, "%.2f" % round(soundBytes / (localClientBytes + remoteClientBytes) * 100, 2))
        print("Video Bytes:", videoBytes, "%.2f" % round(videoBytes / (localClientBytes + remoteClientBytes) * 100, 2))
        print("Formatted Bytes:", formattedBytes, "%.2f" % round(formattedBytes / (localClientBytes + remoteClientBytes) * 100, 2))
        print("Dynamic Bytes:", dynamicBytes, "%.2f" % round(dynamicBytes / (localClientBytes + remoteClientBytes) * 100, 2))
        print("Others Bytes:", othersBytes, "%.2f" % round(othersBytes / (localClientBytes + remoteClientBytes) * 100, 2))
        print("Total Bytes:", htmlBytes + imagesBytes + soundBytes + videoBytes + formattedBytes + dynamicBytes + othersBytes)
        print("")
        print("9")
        print("Average HTML transfer Bytes:", htmlBytes / htmlCount)
        print("Average Images transfer Bytes:", imagesBytes / imagesCount)
        print("Average Sound transfer Bytes:", soundBytes / soundCount)
        print("Average Video transfer Bytes:", videoBytes / videoCount)
        print("Average Formatted transfer Bytes:", formattedBytes / formattedCount)
        print("Average Dynamic transfer Bytes:", dynamicBytes / dynamicCount)
        print("Average Others transfer Bytes:", othersBytes / othersCount)
        print("")
        print("10")
        #[print(obj, count) for obj,count in uniqueObjDict.items() if count == 1]
        for obj,count in uniqueObjDict.items():
            if count == 1:
                accessedOnceCount += 1
                accessedOnceBytes += int(uniqueObjByteDict[obj])
        print("Percentage of unique objects accessed once:", "%.2f" % round(accessedOnceCount / uniqueObjCount * 100, 2))
        print("Percentage of Bytes accessed once:", "%.2f" % round(accessedOnceBytes / uniqueObjByteTotal * 100, 2))
    def getFileType(self, URI):
        if URI.endswith('/') or URI.endswith('.') or URI.endswith('..'):
            return 'HTML'
        filename = URI.split('/')[-1]
        if '?' in filename:
            return 'Dynamic'
        extension = filename.split('.')[-1].lower()
        if extension in self.fileTypeDict:
            return self.fileTypeDict[extension]
        return 'Others'

    def checkResCode(self, code):
        if code == '200' : return 'Successful'
        if code == '302' : return 'Found'
        if code == '304' : return 'Not Modified'   
        return None

if __name__ == '__main__':
    logfile = open('UofS_access_log', 'r', errors='ignore')
    logParser = Parser()
    logParser.parse(logfile)
    pass
