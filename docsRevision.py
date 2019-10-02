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
threshold = 2000
#paginationLimit = 1000
wordsCounter = 0
docsDict = {}
commonWordsDict = {}
uncommonWordsDict = {}

def addWordtoDict (word, dictionary):
    if word in dictionary:
        dictionary[word] += 1
    else:
        dictionary[word] = 1
            

def lookForWord(word):
    print("------------------------------")
    print("")
    print("Looking for " + word)
    print("")
    for doc in dataSources:
        print("Doc: " + doc)
        print("-> Common Words Dict:")
        print("--> Word: " + word + " - Times: " + str(docsDict.get(doc)[0].get(word.lower())))
        print("-> Uncommon Words Dict:")
        print("--> Word: " + word + " - Times: " + str(docsDict.get(doc)[1].get(word.lower())))
        print("------------------------------")

def printDictionary(dictionary):
    print("Printing dictionary:")
    pprint(sorted(dictionary.items(), key=lambda i: i[1], reverse = True))

def printImportantWords():
    importantWords = ["access","create","change","remove","install","order","subscription","restore","backup"]
    for w in importantWords:
        lookForWord(w)

def printTopWords(limit):
    print("------------------------------")
    print("")
    print("Top " + str(limit) + " - Common Words")
    print("")
    n = 0
    for k, v in sorted(commonWordsDict.items(), key=lambda i: i[1], reverse = True):
        print(k + "(" + str(v) + ")")
        n += 1
        if n > limit:
            break
    print("")
    print("Top " + str(limit) + " - Uncommon Words")
    print("")
    n = 0
    for k, v in sorted(uncommonWordsDict.items(), key=lambda i: i[1], reverse = True):
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
    mostCommonWords = mostCommonWords[:threshold]
    #print(len(mostCommonWords))
    txtFile.close()

    #Reading all docs
    for doc in dataSources:
        print(f"\nFile: {doc}...")
        localCommonWords = {}
        localUncommonWords = {}
        localWordsCounter = 0
        #docsDict[doc] = [localCommonWords, localUncommonWords]
        #print(docsDict[doc][0])
        i = 0
        try:
            with open(filepath + doc, 'r', encoding='utf8') as docFile:
                for line in docFile:
                    #filterText(line)
                    cleanWords = set(ttws(line))#.replace("‘","").replace("’","")
                    for word in cleanWords:
                        if not re.findall("[0-9]+", word):
                            word = word.lower()
                            if word in mostCommonWords:
                                addWordtoDict(word, commonWordsDict)
                                addWordtoDict(word, localCommonWords)
                            else:
                                addWordtoDict(word, uncommonWordsDict)
                                addWordtoDict(word, localUncommonWords)
                            #global wordsCounter
                            wordsCounter += 1
                            localWordsCounter += 1
                    i += 1
                    #if(i%paginationLimit==0):
                    #    print(f"---> {i} lines printed...")
                docFile.close()
            docsDict[doc] = [localCommonWords, localUncommonWords]
            print("----------------------------------------------")
            print("Results [" + doc + "]:")
            print("----------------------------------------------")
            print(f" - Total words analyzed: {localWordsCounter}")
            print(f" - Total common words: {len(localCommonWords)}")
            print(f" - Total uncommon words: {len(localUncommonWords)}")
            print("----------------------------------------------")
        except Exception as e1:
            print(f" - Error in line {i+1}: {str(e1)}")
            raise
        print(f"There were {i} lines.")
        
    print("----------------------------------------------")
    print("Results:")
    print("----------------------------------------------")
    print(f" - Total words analyzed: {wordsCounter}")
    print(f" - Total common words: {len(commonWordsDict)}")
    print(f" - Total uncommon words: {len(uncommonWordsDict)}")
    print("----------------------------------------------")
    #printWords()
    print("Total words: " + str(wordsCounter))
    print("Time spent: " + setElapsedTime(time.time() - start))
    #print("Please try printCommonWords(), printCenitexWords(), or printUncommonWords if you want to see any set of words.")
    lookForWord('Cenitex')
    #printImportantWords()
    printTopWords(50)
except Exception as e2:
    print(f" - Error: {str(e2)}")