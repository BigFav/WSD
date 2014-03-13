import re
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords as stop
from nltk.stem.wordnet import WordNetLemmatizer as Lemma


tokens = []
lmtzr = Lemma()
window_size = 2
# Turns "%%word%%" into "word%"
with open('training_data.data', 'r') as train:
    txt = re.sub(r"%%(.+)%%", r"\1%", train.read())
tokens = nltk.word_tokenize(txt)

# Make the list a set for constant access in the lst comp
stopwords = set(stop.words('english'))
tokens = [w for w in tokens if not w.lower() in stopwords]


for i in range(len(tokens)):
    if tokens[i] is '%':
        print tokens[i-1:i+2]

# remove punctuation?
tag = ''
word = ''
word_def = ''
lemma_word = ''
lemma_def = ''

prev_token = tokens[0]
for token in tokens[1:]:
    # token is either keyword, or def number
    if token is '|':
        if '.' in prev_token:
            word = prev_token[:-2]
            tag = prev_token[-1]
            lemma_word = "%s.%s" % (lmtzr.lemmatize(word, tag), tag)
        else:
            word_def = wn.synset("%s.%s.%s" % (word, tag, prev_token)).definition
            lemma_def = wn.synset("%s.%s" % (lemma_word, prev_token)).definition



    prev_token = token

