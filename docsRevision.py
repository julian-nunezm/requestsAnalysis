import time, re
from pprint import pprint
from tensorflow.keras.preprocessing.text import text_to_word_sequence as ttws
#https://github.com/first20hours/google-10000-english/blob/master/20k.txt

#ToDo: Organize the structure to save the three totals for each document.
filepath = "data/comms/"
dataSources = ["5 x How to & user guides.txt",
               "10 x Cenitex Change Management Change Notifications.txt",
               "10 x insITe pages.txt",
               "10 x marketing_brochures material.txt",
               "11 Cenitex Bulletin examples.txt",
               "Service Catalogoe, Parts and Supplement in Plain word.txt"]
commonWordsSource = "data/20k.txt"
#paginationLimit = 1000
wordsCounter = 0
commonWordsDict = {}
uncommonWordsDict = {}

def filterText (line):
    cleanWords = set(ttws(line))#.replace("‘","").replace("’","")
    #cleanWords = line.split(" ")
    for word in cleanWords:
        #if not re.findall("^[0-9][0-9]$", word):
        if not re.findall("[0-9]+", word):
        #if re.findall("\D", word):
            word = word.lower()
            if word in mostCommonWords:
                if word in commonWordsDict:
                    commonWordsDict[word] += 1
                else:
                    commonWordsDict[word] = 1
            else:
                if word in uncommonWordsDict:
                    uncommonWordsDict[word] += 1
                else:
                    uncommonWordsDict[word] = 1
            global wordsCounter
            wordsCounter += 1
        #else:
        #    print(word)
            

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
    
    #Loading most common words in English
    txtFile = open(commonWordsSource, 'r')
    mostCommonWords = txtFile.read().split(",")
    #print(len(mostCommonWords))
    txtFile.close()

    #Reading all docs
    for doc in dataSources:
        print(f"\nFile: {doc}...")
        i = 0
        try:
            with open(filepath + doc, 'r', encoding='utf8') as docFile:
                for line in docFile:
                    filterText(line)
                    i += 1
                    #if(i%paginationLimit==0):
                    #    print(f"---> {i} lines printed...")
        except Exception as e1:
            print(f" - Error in line {i+1}: {str(e1)}")
            raise
        docFile.close()
        print(f"There were {i} lines.")
        
    print("----------------------------------------------")
    print("Results:")
    print("----------------------------------------------")
    print(f" - Total words analyzed: {wordsCounter}")
    print("----------------------------------------------")
    #printWords()
    print("Total words: " + str(wordsCounter))
    print("Time spent: "+setElapsedTime(time.time() - start))
    #print("Please try printCommonWords(), printCenitexWords(), or printUncommonWords if you want to see any set of words.")
except Exception as e2:
    print(f" - Error: {str(e2)}")
