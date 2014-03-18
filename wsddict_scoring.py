#import os
from nltk.corpus import stopwords
from collections import defaultdict

SCALE = 2

def select_score(contextDefs, senseDefs):
    finalTally = defaultdict(int)
    tieBreaker = defaultdict(int)
    finalSense = 0
    currentMaxScore = 0
    currentMaxSense = 0
    for s_def in senseDefs:
        scorelist = []
        maxword = 0
        for word_defs in contextDefs.values():
	    for wordsense_def in word_defs: 
                countHash = compare_defs(wordsense_def,senseDefs[s_def])
                newScore = scale_score(countHash)
                scorelist.append(newScore[0])
                if newScore[1] > maxword: 
                    maxword = newScore[1]
                    tieBreaker[s_def] = maxword
        finalTally[s_def] = sum(scorelist)
    for sense, score in finalTally.items():
        if score > currentMaxScore:
            currentMaxScore = score
            currentMaxSense = sense
        elif score == currentMaxScore:    
            if currentMaxSense ==0 or (sense in tieBreaker and tieBreaker[sense] > tieBreaker[currentMaxSense]):
                currentMaxSense = sense
#    print currentMaxSense
    with open('val_output.txt', 'a+') as out:
        out.write("%d\n" % currentMaxSense)

    return currentMaxSense



def scale_score(wordCountHash):
    maxword = 0
    scorelist = []
    stop = stopwords.words('english')
    #remove singular stopwords
    for word,count in wordCountHash.items():
        sword = word.strip()
        if not sword in stop:
            length = len(sword.split())
            if length == 1:
                scorelist.append(count)
            else:
                value = SCALE * length * count
                scorelist.append(value)
                if length > maxword:
                    maxword = length
    return [sum(scorelist), maxword]
        

def compare_defs(con1Def, sen1Def):
    currentStart = 0
    wordCountHash = {}
    conDef = con1Def + " "
    senDef = sen1Def + " "
    #word appears multiple times in def
    contextDef = conDef.split()
    senseDef = senDef.split()
    remainsofcontextDef  = contextDef
    while currentStart < len(senseDef):
        updatedSense = senseDef[currentStart:]
        ngramSize= len(updatedSense)
        while ngramSize > 0:
            context= "".join (str(e) + " " for e in remainsofcontextDef)
            sense = "".join(str(e) + " " for e in updatedSense[:ngramSize])
            if sense in context:
                conFreq = context.count(sense)
                senFreq = senDef.count(sense)
                if sense in wordCountHash:
                    wordCountHash[sense] = wordCountHash[sense]+(conFreq*senFreq)
                else:
                    wordCountHash[sense] = conFreq*senFreq
                updatedContext = context.replace(sense, " ")
                remainsofcontextDef = updatedContext.split()
            ngramSize = ngramSize -1

        currentStart = currentStart+1

    return wordCountHash
