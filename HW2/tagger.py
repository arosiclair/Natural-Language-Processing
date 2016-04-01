#--------------------------
#Assignment 2
#Andrew Rosiclair
#109235970
#3/27/2016
#--------------------------

from pickle import load
from training import preprocess, getUniqueWords, getUniqueTags, getWord, getTag

#Load serialized objects
def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return load(f)

#Fill the tag count dictionary with counts from the training corpus
def getTagCounts():
  global tagCount

  for word in trainWords:
    tag = getTag(word)
    try:
      tagCount[tag] += 1
    except KeyError, e:
      tagCount[tag] = 1

#Iterate through the input sequence and generate a tag sequence that maximizes
#the laplace tag-word probability for each unigram in the input
def decodeTagSequence(inputSeq):
  tagPreds = []
  for token in inputSeq:
    word = getWord(token)
    #The tag that maximizes the probability and its probability
    argmax = ["", 0]
    for tag in uniqueTags:
      try:
        prob = laplaceEmissProbs[word, tag] * laplaceTagUnigramProbs[tag]
      #If a KeyError occurs, the word-tag bigram was unseen. Thus, the laplace
      #emission prob becomes the following constant
      except KeyError, e:
        prob = (1.0 / (tagCount[tag] + len(uniqueWords))) * laplaceTagUnigramProbs[tag]

      #Replace argmax if this tag performs better
      if prob > argmax[1]:
        argmax = [tag, prob]

    tagPreds.append(argmax[0])

  return tagPreds

#--- BEGIN SCRIPT ---
#Open and preprocess the test and training corpora
testFile = open("test.txt")
testInput = testFile.read()
testFile.close()
trainFile = open("train.txt")
trainInput = trainFile.read()
trainFile.close()

#List of word/tags with start tags inserted
testWords = preprocess(testInput)
trainWords = preprocess(trainInput)

#Lists of unique words and tags in training
uniqueWords = getUniqueWords()
uniqueTags = getUniqueTags()

#Dictionary with keys (tag) and values (count(tag))
tagCount = {}
getTagCounts()

#Open laplace-emissions and laplace-tag-unigrams probability files
laplaceEmissProbs = load_obj("laplace-emissions")
laplaceTagUnigramProbs = load_obj("laplace-tag-unigrams")

predictedTagSeq = decodeTagSequence(testWords)
for tag in predictedTagSeq:
  print tag