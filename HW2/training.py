#--------------------------
#Assignment 2
#Andrew Rosiclair
#109235970
#3/27/2016
#--------------------------

def getUniqueTags(train, test):
  tags = []

  for word in trainWords:
    tag = getTag(word)
    if tag not in tags:
      tags.append(tag)

  for word in testWords:
    tag = getTag(word)
    if tag not in tags:
      tags.append(tag)

  return tags

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
#and add them to the global transitionCount dictionary
def getTransCounts(inputWords):
  global transitionCount

  prev = getTag(inputWords[0])
  for i in xrange(1, len(inputWords)):
    current = getTag(inputWords[i])
    #Either increment the transition count or initialize it to 1
    try:
      transitionCount[(prev, current)] += 1
    except KeyError, e:
      transitionCount[(prev, current)] = 1

    prev = current

#--- BEGIN SCRIPT ---

#Read in the contents of both the training and test data
trainingInput = open("train.txt").read()
testInput = open("test.txt").read()

#Preprocess the input corpora into a list of words/tags with start tags inserted
trainWords = preprocess(trainingInput)
testWords = preprocess(testInput)

#Get a list of all unique tags used in both training and test corpora
uniqueTags = getUniqueTags(trainWords, testWords)

#A dictionary with keys (tag1, tag2) and values count(tag1,tag2)
transitionCount = {}
#Fill the dict with counts
getTransCounts(trainWords)
for key in transitionCount:
  print key, transitionCount[key]

