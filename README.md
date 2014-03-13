http://www.it.iitb.ac.in/~esha/resources/firststage.pdf

http://www.inf.ed.ac.uk/teaching/courses/fnlp/Tutorials/7_WSD/tutorial.html

http://folk.uio.no/larsereb/informatikk/inf5820/NBWSD.pdf

http://nlp.stanford.edu/software/corenlp.shtml

http://nltk.googlecode.com/svn/trunk/doc/howto/wordnet.html



---------------------------------------------------------------------------------------------


General Wants
- Remove stop words and lemmatize


Naive Bayes

Wants
- Separate words into (word, part of speech, count) tuples
- Read, sentence count number of windows that words are in.
- Apply threshold to counts (use val set to pick optimal threshold; this is done later)

- Using probabilities, ignore differences in probabilities that are not stat significant across all definitions (~5%)
- Do naive bayes

----------------------------------------------------------------------------------------------------------------------

WSD Dictionary

Wants
- Read tokens
- POS tag original, carry over tag to the lemmatized
- Use tag to identify which definition to use (if the tag is noun, then use the noun definitions)
- Then look-up word
- Look up phrases large to small, removing matches in the context definitions
- Scoring will be done using this formula: (length of phrase)x(scale factor)x(frequency)
- May or may not use the example sentence along with the definitions.

----------------------------------------------------------------------------------------------------------------------

Questions

? Window size: Bayes, dict, or both?

? Stem vs. Lemmatize?

? Parsing WordNET dictionary, how?

? SenseVal?
