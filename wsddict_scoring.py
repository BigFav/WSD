#import os
from nltk.corpus import stopwords

SCALE = 2

def select_score(contextDefs, senseDefs):
    finalTally ={}
    tieBreaker ={}
    finalSense = 0
    currentMaxScore = 0
    currentMaxSense = 0
    for s_def in senseDefs:
        scorePerSense = []
        maxword = 0
        for word_defs in contextDefs.values():
	    for wordsense_def in word_defs: 
                countHash = compare_defs(wordsense_def,senseDefs[s_def])
                newScore = scale_score(countHash)
                scorePerSense.append(newScore[0])
                if newScore[1] > maxword: 
                    maxword = newScore[1]
                    tieBreaker[s_def] = maxword
        finalTally[s_def] = sum(scorePerSense)
    for sense, score in finalTally.items():
     #   print str(sense) + " : " + str(score)
        if score > currentMaxScore:
            currentMaxScore = score
            currentMaxSense = sense
        elif score == currentMaxScore:    
            if currentMaxSense ==0 or (sense in tieBreaker and tieBreaker[sense] > tieBreaker[currentMaxSense]):
                currentMaxSense = sense
    print currentMaxSense
    return currentMaxSense



def scale_score(wordCountHash):
    maxword = 0
    scorelist = []
    stop = stopwords.words('english')
    #remove singular stopwords
    for word,count in wordCountHash.items():
        sword = word.split()
        length = len(sword)
        if length == 1:
            scorelist.append(count+1)
        else:
            value = (length * count) + length
            scorelist.append(value)
        if length > maxword:
            maxword = length
    return [sum(scorelist), maxword]
        

def compare_defs(con1Def, sen1Def):
    currentStart = 0
    wordCountHash = {}
    contextDef = []
    conDef = con1Def + " "
    senDef = sen1Def + " " 
    #word appears multiple times in def
    contextDef.append(conDef)
    senseDef = senDef.split()
    remainsofcontextDef  = contextDef
    stop = stopwords.words('english')
    while currentStart < len(senseDef):
        updatedSense = senseDef[currentStart:]
        ngramSize= len(updatedSense)
        while ngramSize > 0:
            sense = "".join(str(e) + " " for e in updatedSense[:ngramSize])

#STOP WORD CHECK
            stopworded = False
            i = 0
            terms = sense.split(" ")
            if sense.strip() in stop:
                ngramSize = ngramSize -1
                continue

            while i+1 < len(terms):
                if (terms[i] in stop) and (terms[i+1] in stop):
                    stopworded = True
                    break
                else:
                    i = i+1

            if stopworded:
                ngramSize = ngramSize -1
                continue
    
            
#Check the contexts after splitting by words that overlapped
            updatedContext = []
            for con in remainsofcontextDef:
  #Check the splits for cases of the sense
                if sense in con:
                    conFreq = con.count(sense)
                    senFreq = senDef.count(sense)
                    if sense in wordCountHash:
                        wordCountHash[sense] = wordCountHash[sense]+(conFreq*senFreq)
                    else:
                        wordCountHash[sense] = conFreq*senFreq

#TODO optimize this segment
            updatedContext.append(con.split(sense))
            remainsofcontextDef = []
    #redefine contexts by splitting the previous context on the sense found
            for neocon in updatedContext:

                for segment in neocon:
                    remainsofcontextDef.append(segment)
            ngramSize = ngramSize -1

        currentStart = currentStart+1
 
    return wordCountHash


