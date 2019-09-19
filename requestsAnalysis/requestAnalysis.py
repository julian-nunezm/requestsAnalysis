import csv, json, datetime as dt, time
from pprint import pprint
from tensorflow.keras.preprocessing.text import text_to_word_sequence as ttws
csv.field_size_limit(500000)
#https://github.com/first20hours/google-10000-english/blob/master/20k.txt

#dataSource = "source/requests_data.csv"
dataSource = "../data/LastMonthRequests.csv"
commonWordslist = "../data/90.txt"
incidentNumberIndex = 0 #1
summaryIndex = 1 #4
tier1Index = 2 #9
tier2Index = 3 #10
tier3Index = 4 #11
paginationLimit = 100000
recordsLimit = [300000]
wordsCounter = 0
requestDict = {}
accessDict = {}
fileDict = {}
lotusDict = {}
outlookDict = {}
emailDict = {}
awsDict = {}
azureDict = {}
sqlDict = {}

def filterText (record, field):
    cleanWords = set(ttws(record[field]))
    for word in cleanWords:
        word = word.lower()
        if word not in mostCommonWords:
            if word in wordsDict:
                wordsDict[word] += 1
            else:
                wordsDict[word] = 1
            global wordsCounter
            wordsCounter += 1
        #else:
        #    print(word)

def addToDict(dictionary, key):
    if key in dictionary:
        dictionary[key] += 1
    else:
        dictionary[key] = 1

def lookForWord(word):
    print("Word: " + word + " - Times: " + str(wordsDict.get(word)))


def printDictionary(dictionary):
    print("Printing dictionary:")
    pprint(sorted(dictionary.items(), key=lambda i: i[1], reverse = True))

def printImportantWords():
    importantWords = ["access","create","change","remove","install","order","subscription","restore","backup"]
    for w in importantWords:
        lookForWord(w)

def printTopWords(limit):
    n = 0
    for k, v in sorted(wordsDict.items(), key=lambda i: i[1], reverse = True):
        print(k + "(" + str(v) + ")")
        n += 1
        if n > limit:
            break

def setElapsedTime (elapsed):
    if elapsed > 60:
        elapsed /= 60
        if elapsed > 60:
            return str(round(elapsed/60,2))+" hours"
        else:
            return str(round(elapsed,2))+" minutes"
    else:
        return str(round(elapsed,2))+" seconds"

try:
    start = time.time()
    records = dict()
    reg = dict()
    for lim in recordsLimit:
        i = 0
        #requests = 0
        #wordsDict = {}
        #Loading most common words in English
        #txtFile = open('90.txt', 'r', encoding="utf8")
        #mostCommonWords = txtFile.read().split(",")
        #txtFile.close()
        print(" ")
        print("Beginning to analyze "+ str(lim) +" records...")
        with open(dataSource, 'r', encoding="utf8") as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                record = {}
                try:
                    #print("Tier 1: " + row[tier1Index] + " - Number: " + row[incidentNumberIndex])
                    if i < lim:
                        #print("Tier 1: " + row[tier1Index])
                        if row[tier1Index] == "Request":
                            #print("Tier 1: " + row[tier1Index] + " - Number: " + row[incidentNumberIndex])
                            record['Incident_Number'] = row[incidentNumberIndex]
                            record['Summary'] = row[summaryIndex]
                            if "request" in record['Summary'].lower():
                                addToDict(requestDict, record['Summary'])
                            if "access" in record['Summary'].lower():
                                addToDict(accessDict, record['Summary'])
                            if "file" in record['Summary'].lower() or "folder" in record['Summary'].lower():
                                addToDict(fileDict, record['Summary'])
                            if "lotus" in record['Summary'].lower():
                                addToDict(lotusDict, record['Summary'])
                            if "outlook" in record['Summary'].lower():
                                addToDict(outlookDict, record['Summary'])
                            if "email" in record['Summary'].lower():
                                addToDict(emailDict, record['Summary'])
                            if "aws" in record['Summary'].lower():
                                addToDict(awsDict, record['Summary'])
                            if "azure" in record['Summary'].lower():
                                addToDict(azureDict, record['Summary'])
                            if "sql" in record['Summary'].lower():
                                addToDict(sqlDict, record['Summary'])
                            record['Operational_Categorization_Tier 1'] = row[tier1Index]
                            record['Operational_Categorization_Tier 2'] = row[tier2Index]
                            record['Operational_Categorization_Tier 3'] = row[tier3Index]
                            records[row[incidentNumberIndex]] = record
                            #filterText(record, "Summary")
                            #requests += 1
                            #if(requests%500==0):
                            #    print(f"{requests} requests loaded")
                        i += 1
                        if(i%paginationLimit==0):
                            print(f"{i} records loaded")
                    else:
                        break
                except Exception as e1:
                    print(f" - Error in row {i+1}: {str(e1)}")
                    #print(f" -> Incident Number: {incident['Incident_Number']}, Ini Date: {incident['Reported_Date']}, End Date: {incident['Resolved_Date']}")
                    print(f" -> Incident Number: {record['Incident_Number']}")
                    raise
        csvFile.close()
        print(f"There are {i} records read")
        #print(f"There are {requests} records read")

        print(" ")
        print("Analyzing records...")
        print(" ")

        #Loading most common words in English
        txtFile = open(commonWordslist, 'r', encoding="utf8")
        mostCommonWords = txtFile.read().split(",")
        txtFile.close()
        #Validate why is there a difference between having the filterText here or before
        wordsDict = {}
        i = 0
        for k, v in records.items():
            filterText(v, "Summary")
            i += 1
            if(i%paginationLimit==0):
                print(f"{i} records fields already checked")
        print(f"{i} records analyzed")
        print("----------------------------------------------")
        print("Results:")
        print("----------------------------------------------")
        print(f" - Total words analyzed: {wordsCounter}")
        print("----------------------------------------------")
    #printWords()
    print("Time: "+setElapsedTime(time.time() - start))
    #print("Please try printCommonWords(), printCenitexWords(), or printUncommonWords if you want to see any set of words.")
    """requestDict = {}
    accessDict = {}
    fileDict = {}
    lotusDict = {}
    outlookDict = {}
    emailDict = {}
    awsDict = {}
    azureDict = {}
    sqlDict = {}"""
except Exception as e2:
    print(f" - Error: {str(e2)}")
