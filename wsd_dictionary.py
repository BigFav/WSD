import re
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords as stop
from nltk.stem.wordnet import WordNetLemmatizer as Lemma

from xml.etree import ElementTree as ET
from collections import OrderedDict, defaultdict
from operator import itemgetter


dictionary = {}
lmtzr = Lemma()
window_size = 2
rem_stop = True
use_sentences = False
lmtz_context = True


#TODO Discount definition-less words, fix POS tag, and regex / and ancronyms



def str_format(txt):
    """Removes punctuation, makes lowercase, and lemmatizes."""
    txt = re.sub("''", " ", txt)
    txt = re.sub('([\.\?\!\:\|,;`"\(\)]+)', ' ', txt).lower().split()
    return ' '.join(map(lmtzr.lemmatize, txt))

def get_definitions(prev_token, def_num, tag):
    word = prev_token[:-2]
    word_defs = []

    # if the word isn't in the dictionary xml file
    if not prev_token in dictionary.iterkeys():
        # first loop through, and only use matching tag
        for syn in wn.synsets(word):
            if syn.name.split('.')[1] == tag:
                word_defs.append((0,str_format(syn.definition)))
        # if empty, collect all defs
        if not word_defs:
            for syn in wn.synsets(word):
                word_defs.append((0,str_format(syn.definition)))
        
        return word_defs
    else:
        # if we know what sense it is
        if def_num:
            wordnet_nums = filter(bool, dictionary[prev_token][def_num][0])
            if wordnet_nums:
                for wordnet_num in wordnet_nums:
                    word_defs.append(str_format(wn.synset("%s.%s.%s" % (word, tag, wordnet_num)).definition))
                
                return word_defs
            else:
                word_defs = dictionary[prev_token][def_num][1]
                if use_sentences:
                    word_defs += ' ' + dictionary[prev_token][def_num][2]
                word_defs = [str_format(word_defs)]
            
                return word_defs
        else:
            wordnet_nums = []
            for i,sense in enumerate(dictionary[prev_token].iterkeys()):
                wordnet_nums.append((i+1,dictionary[prev_token][sense][0]))
            wordnet_nums = sorted([(i,define) for (i,define) in wordnet_nums if define[0]], \
                           key=itemgetter(0))

            # if there is at least one wordnet definition
            if len(wordnet_nums):
                for (sense,wordnet_lst) in wordnet_nums:
                    for wordnet_num in wordnet_lst:
                        defin = wn.synset("%s.%s.%s" % (word, tag, wordnet_num)).\
                                definition
                        word_defs.append((sense, str_format(defin)))
                return word_defs
            else:
                word_defs = []
                if use_sentences:
                    for sense in dictionary[prev_token].iterkeys():
                        word_defs.append((sense,dictionary[prev_token][sense][1]))
                        word_defs.append((sense,dictionary[prev_token][sense][2]))
                else:
                    for sense in dictionary[prev_token].iterkeys():
                        word_defs.append((sense,dictionary[prev_token][sense][1]))
            
                """ Can be optimized and/or removed
                if rem_stop:
                    #for i,word_def in enumerate(word_defs):
                    #    word_def = word_def.split()
                    #    word_defs[i] = ' '.join([w for w in word_def if w not in stopwords])
                    word_defs = [(' '.join([w for w in word_def.split() if w not in stopwords])) for word_def in word_defs]
                """
                return word_defs

def get_context_defs(word, tag):
    if tag:
        lst = get_definitions(word, 0, tag)
        return [defin for sense,defin in lst]
    
    defs = []
    for tag in ['a', 'n', 'r', 'v']:
        lst = get_definitions(word, 0, tag)
        if lst:
            defs.extend([defin for sense,defin in lst])
    # not sure if context definition order matters...but removes duplicates
    return list(set(defs))

# Initialize dictionary xml file as nested hashmap
doc = ET.parse('dictionary.xml').getroot()
for level in doc.findall('lexelt'):
    word = level.get('item')
    dictionary[word] = OrderedDict()
    for sense in level.findall('sense'):
        dictionary[word][int(sense.get('id'))] = (sense.get('wordnet').split(','), \
                                             str_format(sense.get('gloss')), \
                                             str_format(sense.get('examples')))

# Turns "%% word %%" into "____word____" to hack the tokenizer into not splitting it up
with open('training_data.data', 'r') as train:
    txt = re.sub(r"%%\s(.+)\s%%", r"____\1____", train.read())

#tries to remove punctuation
txt = re.sub("('')|(\.\.\.)", " ", txt)
txt = re.sub("\. ", " ", txt)
tokens = nltk.word_tokenize(re.sub('([\?\!\:,;`"\(\)]+)', ' ', txt).lower())

# Make the list a set for constant access in the lst comp
if rem_stop:
    stopwords = set(stop.words('english'))
    tokens = [w for w in tokens if not w in stopwords]

tag = ''
target = ''
target_defs = {} # To cache calculated definitions
context_defs = {}
lemma_word = ''
lemma_defs = []
for i,token in enumerate(tokens):
    # if token is a pipe, we know we split the word.tag and the def num
    if token is '|':
        if '.' in tokens[i-1]:
            target = tokens.pop(i-1)
            def_num = int(tokens.pop(i))
            tag = target[-1]

            if not target in target_defs.iterkeys():
                target_defs[target] = defaultdict(list)
                word_defs = get_definitions(target, def_num, tag)
                if def_num:
                    target_defs[target][def_num] = word_defs
                else:
                    for sense,word_def in word_defs:
                        target_defs[target][sense].append(word_def)
            elif not def_num in target_defs[target].iterkeys():
                word_defs = get_definitions(target, def_num, tag)
                if def_num:
                    target_defs[target][def_num] = word_defs
                else: 
                    for sense,word in word_defs:
                        target_defs[target][sense].append(word_def)
            
            # since I messed up the indices, it auto-skips the 2nd '|'
    # token is keyword in sentence
    if '____' in token:
        context = []
        beg_para = False
        end_para = False
        # Don't overun into another paragrph
        for j in range(window_size+1)[1:]:
            if tokens[i-j] == '|':
                beg_para = True 
            if not beg_para:
                if lmtz_context is True:
                    context.append(lmtzr.lemmatize(tokens[i-j]))
                else:
                    context.append(tokens[i-j])
            if tokens[i+j] in target_defs.iterkeys():
                end_para = True
            if not end_para:
                if lmtz_context is True:
                    context.append(lmtzr.lemmatize(tokens[i+j]))
                else:
                    context.append(tokens[i+j]) 
        
        # Get definitions for context words with weak POS-tag
        for i,word in enumerate(context):
            tag = nltk.pos_tag(word)[0][1].lower()
            if 'n' in tag:
                tag = 'n'
            elif 'v' in tag:
                tag = 'v'
            elif 'adj' in tag:
                tag = 'a'
            elif 'adv' in tag:
                tag = 'r'
            else:
                tag = ''
            if tag:
                word += ".%s" % (tag)
            context[i] = word
            if not word in context_defs.iterkeys():
                defs = get_context_defs(word, tag)
                context_defs[word] = defs
        # TODO Method that compares defs
