import re
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords as stop
from nltk.stem.wordnet import WordNetLemmatizer as Lemma

from xml.etree import ElementTree as ET


WORDNET_NUM = 0
GLOSS = 1
EXAMPLES = 2
dictionary = {}
lmtzr = Lemma()
window_size = 2
rem_stop = True
use_sentences = False


def str_format(txt):
    """
    Removes punctuation, and makes lowercase.
    """
    txt = re.sub("('')|(\.\.\.)", " ", txt)
    txt = re.sub("\. ", " ", txt)
    return re.sub('([\?\!\:,;`"\(\)]+)', ' ', txt).lower()

# TODO handle def_num == 0
def get_definitions(prev_token, def_num, tag):
    word = prev_token[:-2]
    word_defs = []
    wordnet_nums = dictionary[prev_token][def_num][0]
    if wordnet_nums[0]:
        # Since the given dictionary is extra trash
        for wordnet_num in wordnet_nums:
            try:
                word_defs.append(str_format(wn.synset("%s.%s.%s" % (word, tag, wordnet_num)).definition))
            except nltk.corpus.reader.wordnet.WordNetError:
                if len(wordnet_nums) > 1:
                    break
                else:
                    word_defs = dictionary[prev_token][def_num][1]
                    if use_sentences:
                        word_defs += ' ' + dictionary[prev_token][def_num][2]
                    word_defs = [str_format(word_defs)]
                    break
    else:
        word_defs = dictionary[prev_token][def_num][1]
        if use_sentences:
            word_defs += ' ' + dictionary[prev_token][def_num][2]
        word_defs = [str_format(word_defs)]
    if rem_stop:
        #for i,word_def in enumerate(word_defs):
        #    word_def = word_def.split()
        #    word_defs[i] = ' '.join([w for w in word_def if w not in stopwords])
        word_defs = [(' '.join([w for w in word_def.split() if w not in stopwords])) for word_def in word_defs]
    return (word, word_defs)

# TODO rest of method
def get_context_defs(word, tag):
    if tag:
        return get_definitions(word, 0, tag)


# Initialize dictionary xml file as nested hashmap
doc = ET.parse('dictionary.xml').getroot()
for level in doc.findall('lexelt'):
    word = level.get('item')
    dictionary[word] = {}
    for sense in level.findall('sense'):
        dictionary[word][sense.get('id')] = (sense.get('wordnet').split(','), \
                                             sense.get('gloss'), \
                                             sense.get('examples').lower())

# Turns "%% word %%" into "____word____" to hack the tokenizer into not splitting it up
with open('training_data.data', 'r') as train:
    txt = re.sub(r"%%\s(.+)\s%%", r"____\1____", train.read())

#tries to remove punctuation
txt = re.sub("('')|(\.\.\.)", " ", txt)
txt = re.sub("\. ", " ", txt)
tokens = nltk.word_tokenize(re.sub('([\?\!\:,;`"\(\)]+)', ' ', txt))

# Make the list a set for constant access in the lst comp
if rem_stop:
    stopwords = set(stop.words('english'))
    tokens = [w for w in tokens if not w in stopwords]

tag = ''
target = ''
target_defs = {} # To cache calculated definitions
lemma_word = ''
lemma_defs = []
for i,token in enumerate(tokens):
    # if token is a pipe, we know we split the word.tag and the def num
    if token is '|':
        if '.' in tokens[i-1]:
            prev_token = tokens.pop(i-1)
            def_num = tokens.pop(i)
            tag = prev_token[-1]
            if not prev_token in target_defs.iterkeys():
                (target, word_defs) = get_definitions(prev_token, def_num, tag)
                target_defs[prev_token] = {}
                target_defs[prev_token][def_num] = word_defs
            elif not def_num in target_defs[prev_token].iterkeys():
                (target, word_defs) = get_definitions(prev_token, def_num, tag)
                target_defs[prev_token][def_num] = word_defs
            # since I messed up the indices, it auto-skips the 2nd '|'

    # token is keyword in sentence
    if '____' in token:
        context = []
        beg_para = False
        end_para = False
        for j in range(window_size+1)[1:]:
            if tokens[i-j] == '|':
                beg_para = True 
            if not beg_para:
                context.append(tokens[i-j])
            if tokens[i+j] in target_defs.iterkeys():
                end_para = True
            if not end_para:
                context.append(tokens[i+j])
        # TODO Get definitions for context words with weak POS-tag
        context_defs = {word:{} for word in context}
        for word in context:
            tag = nltk.pos_tag(word).lower()
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
            word += ".%s" % (tag)
            (None, defs) = get_context_definitions(word, tag)
            context_defs[word] = defs
        # TODO Method that compares defs

