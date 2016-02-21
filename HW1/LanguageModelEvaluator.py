#Written in Python 2.7.11
from LanguageModel import LanguageModel
from math import log

#Helper function that preprocesses the test corpus in the same way the 
#LanguageModel constructor does and returns a list of tokens from the test corpus
def preProcessCorpus(corpusFile):
  #Create instance variable of all lowercase input corpus
  corpus = corpusFile.read().lower()
  #Split string into sentences delimited by a period
  sentences = corpus.split(".")

  #Split sentences into a list of all words in the corpus, delimitted by a space
  #Start and end tokens are inserted at the start and end of sentences
  words = []
  for sentence in sentences:

    if(sentence.split() != ""):
      words.append("<s>")
      words.extend(sentence.split())
      words.append("</s>")

  return words

#---BEGIN SCRIPT---

#Print app header
print "-" * 40
print "%32s" % "LANGUAGE MODEL EVALUATOR"
print "-" * 40

#Prompt for the filename of the training corpus
trainingFile = None
while True:
  print "\nEnter the file name for the training corpus"
  try:
    filename = raw_input("> ")
    trainingFile = open(filename)
    break
  except IOError, e:
    print "ERROR: Cannot open %r" % filename
    continue

lm = LanguageModel(trainingFile.read())
print "Training corpus has been pre-processed"

#Prompt for the filename of the test corpus
testFile = None
while True:
  print "\nEnter the file name for the test corpus"
  try:
    filename = raw_input("> ")
    testFile = open(filename)
    break
  except IOError, e:
    print "ERROR: Cannot open %r" % filename
    continue

#Preprocess the test corpus into a list of tokens
testTokens = preProcessCorpus(testFile)

#Calculate the perplexity of the MLE LM on the test corpus
logSum = 0
for i in xrange(1, len(testTokens)):
  if lm.getMLEProb(testTokens[i - 1], testTokens[i]) != 0:
    logSum += log(lm.getMLEProb(testTokens[i - 1], testTokens[i]), 2)

logSum = logSum * (1.0 / len(testTokens)) * -1

perplexity = 2.0 ** logSum

print "The perplexity of the MLE LanguageModel on the test corpus is: %f" % perplexity

#Calculate the perplexity of the Laplace LM on the test corpus
logSum = 0
for i in xrange(1, len(testTokens)):
  logSum += log(lm.getSmoothedProb(testTokens[i - 1], testTokens[i]), 2)

logSum = logSum * (1.0 / len(testTokens)) * -1

perplexity = 2.0 ** logSum

print "The perplexity of the Laplace LanguageModel on the test corpus is: %f" % perplexity

#Calculate the perplexity of the Katz Back-off LM on the test corpus
logSum = 0
for i in xrange(1, len(testTokens)):
  logSum += log(lm.katzBigramProb(testTokens[i - 1], testTokens[i]), 2)

logSum = logSum * (1.0 / len(testTokens)) * -1

perplexity = 2.0 ** logSum

print "The perplexity of the Katz Back-off LanguageModel on the test corpus is: %f" % perplexity

#Calculate the perplexity of the Unigram Absolute Discounting LM on the test corpus
logSum = 0
for token in testTokens:
  logSum += log(lm.getADProb(token), 2)

logSum = logSum * (1.0 / len(testTokens)) * -1

perplexity = 2.0 ** logSum

print "The perplexity of the unigram Absolute Discounting LanguageModel on the test corpus is: %f" % perplexity