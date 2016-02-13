#Written in Python 2.7.11
from LanguageModel import LanguageModel

#---BEGIN SCRIPT---
#Open and read training corpus into a string
train = open("train.txt")
corpus = train.read()

#Create LanguageModel object using the training corpus
lm = LanguageModel(corpus)

print "The MLE conditional probability of a bigram 'and then' is: %f" % lm.getBigramProb("and", "then")