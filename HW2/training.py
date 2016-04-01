#--------------------------
#Assignment 2
#Andrew Rosiclair
#109235970
#3/27/2016
#--------------------------

from pickle import dump, load, HIGHEST_PROTOCOL

def getUniqueTags():
  tags = []

  for word in trainWords:
    tag = getTag(word)
    if tag not in tags:
      tags.append(tag)

  return tags

def getUniqueWords():
  words = []

  for token in trainWords:
    word = getWord(token)
    if word not in words:
      words.append(token)

  return words

def getWord(word):
  prev = word[0]
  i = 0
  for char in word:
    if char == "/" and prev != "\\":
      return word[0:i]
    else:
      i += 1
      prev = char

def getTag(word):
  prev = word[0]
  i = 0
  for char in word:
    if char == "/" and prev != "\\":
      return word[i + 1:]
    else:
      i += 1
      prev = char


def preprocess(inputText):
  inputWords = []
  lines = inputText.split("\n")
  for line in lines:
    #Split the line into words and replace the line number at the beginning 
    #with <s>
    lineWords = line.split(" ")
    lineWords[0] = "<s>/START"
    inputWords.extend(lineWords)

  return inputWords

#Iterate through the input list to count all transitions of a tag i to tag j
#as well as all occurrences of a tag i.
#as well as all occurences of a word-tag bigram
def getCounts(inputWords):
  global tagBigramCount, tagCount, wordTagCount

  prev = getTag(inputWords[0])
  tagCount[prev] = 1

  firstword = getWord(inputWords[0])
  wordTagCount[(firstword, prev)] = 0

  for i in xrange(1, len(inputWords)):
    currentWord = getWord(inputWords[i])
    currentTag = getTag(inputWords[i])

    #Update tag count for current tag
    try:
      tagCount[currentTag] += 1
    except KeyError, e:
      tagCount[currentTag] = 1

    #Update bigram tag count
    try:
      tagBigramCount[(prev, currentTag)] += 1
    except KeyError, e:
      tagBigramCount[(prev, currentTag)] = 1

    #Update word-tag bigram count
    try:
      wordTagCount[(currentWord, currentTag)] += 1
    except KeyError, e:
      wordTagCount[(currentWord, currentTag)] = 1

    prev = currentTag

#Generate a dictionary for tag transition probabilities using MLE
def generateMLETrans():
  probabilities = {}
  for tagBigram in tagBigramCount:
    prob = float(tagBigramCount[tagBigram]) / tagCount[tagBigram[0]]
    probabilities[tagBigram] = prob

  #Serialize and save this object as a .pkl file
  save_obj(probabilities, "mle-transitions")

def generateMLEEmis():
  probabilities = {}
  for wordtag in wordTagCount:
    prob = float(wordTagCount[wordtag]) / tagCount[wordtag[1]]
    probabilities[wordtag] = prob

  #Serialize and save this object as a .pkl file
  save_obj(probabilities, "mle-emissions")

#Generate a dictionary for tag transition probabilities using MLE
def generateLaplaceTrans():
  probabilities = {}
  for tagBigram in tagBigramCount:
    prob = float(tagBigramCount[tagBigram] + 1) / (tagCount[tagBigram[0]] + len(uniqueTags))
    probabilities[tagBigram] = prob

  #Serialize and save this object as a .pkl file
  save_obj(probabilities, "laplace-transitions")

def generateLaplaceEmis():
  probabilities = {}
  for wordtag in wordTagCount:
    prob = float(wordTagCount[wordtag] + 1) / (tagCount[wordtag[1]] + len(uniqueWords))
    probabilities[wordtag] = prob

  #Serialize and save this object as a .pkl file
  save_obj(probabilities, "laplace-emissions")

def generateLaplaceTagUnigrams():
  probabilities = {}
  for tag in uniqueTags:
    prob = float(tagCount[tag] + 1) / (len(trainWords) + len(uniqueWords))
    probabilities[tag] = prob

  #Serialize and save this object as a .pkl file
  save_obj(probabilities, "laplace-tag-unigrams")

def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        dump(obj, f, HIGHEST_PROTOCOL)

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return load(f)

#--- BEGIN SCRIPT ---

#Read in the contents of the training data
trainingInput = open("train.txt").read()

#Preprocess the training corpus into a list of words/tags with start tags inserted
trainWords = preprocess(trainingInput)

#Get a list of all unique tags used in both training and test corpora
uniqueTags = getUniqueTags()
#Get a list of unique words used in training
uniqueWords = getUniqueWords()

#A dictionary with keys (tag1, tag2) and values count(tag1,tag2)
tagBigramCount = {}
#A dictionary with keys (word, tag) and values count(word/tag)
wordTagCount = {}
#A dictionary with keys (tag) and values count(tag)
tagCount = {}
#Fill the dicts with counts
getCounts(trainWords)

#Generate the MLE and Laplace transition files
generateMLETrans()
generateLaplaceTrans()
#Generate MLE and Laplace emission files
generateMLEEmis()
generateLaplaceEmis()
#Generate Laplace tag unigram file
generateLaplaceTagUnigrams()
