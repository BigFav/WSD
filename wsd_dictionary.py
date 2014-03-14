import re
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords as stop
from nltk.stem.wordnet import WordNetLemmatizer as Lemma


tokens = []
lmtzr = Lemma()
window_size = 2
rem_stop = True
# Turns "%% word %%" into "____word____" to hack the tokenizer into not splitting it up
with open('training_data.data', 'r') as train:
    txt = re.sub(r"%%\s(.+)\s%%", r"____\1____", train.read())
tokens = nltk.word_tokenize(txt)

# Make the list a set for constant access in the lst comp
if rem_stop:
    stopwords = set(stop.words('english'))
    tokens = [w for w in tokens if not w.lower() in stopwords]

# remove punctuation?
tag = ''
word = ''
word_def = ''
lemma_word = ''
lemma_def = ''

for i,token in enumerate(tokens):
    # if token is a pipe, we know we split the word.tag and the def num
    if token is '|':
        if '.' in tokens[i-1]:
            prev_token = tokens.pop(i-1)
            def_num = tokens.pop(i)
            tag = prev_token[-1]
            word = prev_token[:-2]
            lemma_word = "%s.%s" % (lmtzr.lemmatize(word, tag), tag)
            word_def = wn.synset("%s.%s.%s" % (word, tag, def_num)).definition
            lemma_def = wn.synset("%s.%s" % (lemma_word, def_num)).definition
            if rem_stop:
                word_def = word_def.split()
                word_def = ' '.join([word for word in word_def if word not in stopwords])
                lemma_def = lemma_def.split()
                lemma_def = ' '.join([word for word in lemma_def if word not in stopwords])
            del tokens[i] # Remove sencond pipe aka '|'

    # token is keyword in sentence
    if '____' in token:
        context = []
        for j in range(window_size+1)[1:]:
            context.append(tokens[i+j])
            context.append(tokens[i-j])
        # TODO Method that compares defs
