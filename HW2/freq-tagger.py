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

  for token in trainWords:
    tag = getTag(token)
    word = getWord(token)
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
        #prob = unknownWordTag(word, tag)

      #Replace argmax if this tag performs better
      if prob > argmax[1]:
        argmax = [tag, prob]

    tagPreds.append(argmax[0])

  return tagPreds

def unknownWordTag(word, tag):
  FEAT_CAPS = "FEATURE_CAPS"
  FEAT_NUM = "FEATURE_NUM"
  FEAT_ED = "FEATURE_ED"
  NFEAT_CAPS = "FEATURE_CAPS"
  NFEAT_NUM = "FEATURE_NUM"
  NFEAT_ED = "FEATURE_ED"

  #Get feature probabilities
  if word.istitle():
    titleProb = mleEmissProbs[FEAT_CAPS, tag]
  else:
    titleProb = mleEmissProbs[NFEAT_CAPS, tag]
  if any(char.isdigit() for char in word):
    numProb = mleEmissProbs[FEAT_NUM, tag]
  else:
    numProb = mleEmissProbs[NFEAT_NUM, tag]
  if word.endswith("ed") or word.endswith("ED"):
    edProb = mleEmissProbs[FEAT_ED, tag]
  else:
    edProb = mleEmissProbs[NFEAT_ED, tag]

  featProb = (1.0 / 3) * titleProb + (1.0 / 3) * numProb + (1.0 / 3) * edProb
  result = featProb * mleTagUnigramProbs[tag]
  return result

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
mleEmissProbs = load_obj("mle-emissions")
laplaceEmissProbs = load_obj("laplace-emissions")
laplaceTagUnigramProbs = load_obj("laplace-tag-unigrams")
mleTagUnigramProbs = load_obj("mle-tag-unigrams")

#Use the frequency based tagger method to predict a tag sequence and then write
#it to an output file
predictedTagSeq = decodeTagSequence(testWords)
outputFile = open("freq-tagger-output.txt", "w")
for tag in predictedTagSeq:
  if tag == "START":
    outputFile.write("\n" + tag + " ")
  else:
    outputFile.write(tag + " ")
