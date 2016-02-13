#Written in Python 2.7.11

def bigramProb(wordList):
  pass

#Returns the MLE conditional probability of the bigram "word1 word2"
def getBigramProb(word1, word2):
  global words
  bigramCount = 0

  prev = words[0]
  for word in words:
    if prev == word1 and word == word2:
      bigramCount += 1

    prev = word

  return float(bigramCount) / count(word1)

#Returns the MLE conditional probability of the bigram "word1 word2" with Laplace smoothing
def getSmoothedBigramProb(word1, word2):
  global words
  global numUniqueWords
  bigramCount = 0

  prev = words[0]
  for word in words:
    if prev == word1 and word == word2:
      bigramCount += 1

    prev = word

  return float((bigramCount + 1)) / (count(word1) + numUniqueWords)


#Returns the Maximum Likelihood Estimate for the occurence of a single word
def getMLE(word):
  global words

  return float(count(word)) / len(words)

#Get's the number of occurences for a word in the corpus. Saves it in the 
#wordCount map for quick access
def count(word):
  global wordCount
  global words

  #Try to immediately retrieve the word count from the dictionary  
  try:
    return wordCount[word]
  except KeyError, e:
    #We haven't counted this word yet so count now
    num = 0
    for sample in words:
      if sample == word:
        num += 1

    #Save count to the dictionary and return
    wordCount[word] = num
    return num

#---BEGIN SCRIPT---
#Open and read training corpus into a string
train = open("train.txt")
corpus = train.read()

#Split string into sentences delimited by a period
sentences = corpus.split(".")

#Split sentences into a list of all words in the corpus, delimitted by a space
words = []
for sentence in sentences:
  words.extend(sentence.split(" "))

#Count the number of unique words in the corpus
uniqueWords = []
numUniqueWords = 0
for word in words:
  if word not in uniqueWords:
    uniqueWords.append(word)
    numUniqueWords += 1



#A dictionary that will save the count for words we have already counted
wordCount = {}

print "The MLE conditional probability of a bigram 'and then' is: %f" % getBigramProb("and", "then")