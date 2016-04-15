#--------------------------
#Assignment 2
#Andrew Rosiclair
#109235970
#3/27/2016
#--------------------------

from pickle import load
from training import preprocess, getWord, getTag
from math import log

#Load serialized objects
def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return load(f)

def preprocess(inputText):
  lineArrays = []
  lines = inputText.split("\n")
  for line in lines:
    if line == "":
      break
    lineWords = line.split(" ")
    firstWord = lineWords[0].split("\t")[1]
    lineWords[0] = firstWord
    lineArrays.append(lineWords)

  return lineArrays

def getUniqueWords():
  words = []
  for line in trainLines:
    for token in line:
      word = getWord(token)
      if word not in words:
        words.append(word)

  return words

def getUniqueTags():
  tags = []
  for line in trainLines:
    for token in line:
      tag = getTag(token)
      if tag not in tags:
        tags.append(tag)

  tags.append("START")
  return tags

def getTagCounts():
  global tagCount

  for line in trainLines:
    for word in line:
      tag = getTag(word)
      try:
        tagCount[tag] += 1
      except KeyError, e:
        tagCount[tag] = 1

#Viterbi Algorithm
def decodeTagSequence(inputSeq):
  #Iterate through each line in test corpus
  for line in testLines:
    predTags = [] #resulting predicted tag sequence

    #initialization
    scores = [[0] * (len(uniqueTags) - 1)] * len(line)
    backpointers = [[0] * (len(uniqueTags) - 1)] * len(line)

    #Initialize scores and backpointers for the first word in sentence
    for i in xrange(0, len(uniqueTags) - 1):
      try:
        transProb = laplaceTransProbs[("START", uniqueTags[i])]
      except KeyError, e:
        transProb = laplaceUnkTransitionProb
      try:
        emissProb = laplaceEmissProbs[(getWord(line[0]), uniqueTags[i])]
      except KeyError, e:
        emissProb = laplaceUnkEmissProb

      scores[0][i] = transProb * emissProb
   
      
      backpointers[0][i] = uniqueTags.index("START")

    #Forward pass
    for i in xrange(1, len(line)):
      for j in xrange(0, len(uniqueTags) - 1):
        argmax = maxTransProb(scores[i - 1], line, i, j)
        scores[i][j] = argmax[1]

        backpointers[i][j] = argmax[0]

    #Backtrace
    predTags.append(getMaxIndex(scores[len(line) - 1]))
    for i in xrange(len(line) - 2, 0, -1):
      predTags.insert(0, backpointers[i + 1][predTags[0]])

    #Write predicted tag sequence to output
    for tagIndex in predTags:
      outputFile.write(uniqueTags[tagIndex] + " ")
    outputFile.write("\n")


def maxTransProb(prevScores, line, wordIndex, tagIndex):
  #First entry = the tag index (for uniqueTags[]) that maximizes this transition and
  #Second entry = maximized probability
  argmax = [0 , 0]
  for i in xrange(0, len(prevScores)):
    try:
      transProb = laplaceTransProbs[(uniqueTags[i], uniqueTags[tagIndex])]
    except KeyError, e:
      transProb = laplaceUnkTransitionProb
    try:
      emissProb = laplaceEmissProbs[getWord(line[wordIndex]), uniqueTags[tagIndex]]
    except KeyError, e:
      emissProb = laplaceEmissProbs

    prob = prevScores[i] + log(transProb) + log(laplaceUnkEmissProb)
    
    if prob > argmax[1]:
      argmax = [i, prob]

  return argmax

def getMaxIndex(array):
  argmax = [0, 0]
  for i in xrange(0, len(array) - 1):
    if array[i] > argmax[1]:
      argmax = [i, array[i]]

  return argmax[0]
#--- BEGIN SCRIPT ---
#Open and preprocess the test and training corpora
testFile = open("test.txt")
testInput = testFile.read()
testFile.close()
trainFile = open("train.txt")
trainInput = trainFile.read()
trainFile.close()

#List of word/tags with start tags inserted
testLines = preprocess(testInput)
trainLines = preprocess(trainInput)

#Lists of unique words and tags in training
uniqueWords = getUniqueWords()
uniqueTags = getUniqueTags()

#Dictionary with keys (tag) and values (count(tag)) from training
tagCount = {}
getTagCounts()

#Load MLE and Laplace transition and emission dictionaries
mleTransProbs = load_obj("mle-transitions")
laplaceTransProbs = load_obj("laplace-transitions")
mleEmissProbs = load_obj("mle-emissions")
laplaceEmissProbs = load_obj("laplace-emissions")
laplaceTagUnigramProbs = load_obj("laplace-tag-unigrams")

laplaceUnkTransitionProb = load_obj("laplace-transitions-unknown")
laplaceUnkEmissProb = load_obj("laplace-emissions-unknown")

outputFile = open("hmm-tagger-output.txt", "w")
decodeTagSequence(testLines)