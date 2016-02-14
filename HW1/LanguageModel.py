class LanguageModel:

  #Constructor
  def __init__(self, corpus):
    #Instance variable to all lower case corpus
    self.corpus = corpus.lower()
    #Split string into sentences delimited by a period
    self.sentences = self.corpus.split(".")

    #Split sentences into a list of all words in the corpus, delimitted by a space
    self.words = []
    for sentence in self.sentences:
      self.words.extend(sentence.split(" "))

    #Count the number of unique words in the corpus for use with smoothing
    uniqueWords = []
    self.numUniqueWords = 0
    for word in self.words:
      if word not in uniqueWords:
        uniqueWords.append(word)
        self.numUniqueWords += 1

    #A dictionary that will save the count for words we have already counted
    self.wordCount = {}

  #Returns the joint probability of a sequence of words 
  def getSequenceProb(self, wordList):
    print wordList
    #Start off with the MLE of the first word in the sequence
    result = self.getMLE(wordList[0])
    print result

    #Multiply the bigram probabilities of the next successive pairs of words in 
    #the sequence
    for i in xrange(1, len(wordList)):
      result *= self.getBigramProb(wordList[i - 1], wordList[i])
      print result

    return result

  #Returns the MLE conditional probability of the bigram "word1 word2"
  def getBigramProb(self, word1, word2):
    bigramCount = 0

    prev = self.words[0]
    for word in self.words:
      if prev == word1 and word == word2:
        bigramCount += 1

      prev = word

    return float(bigramCount) / self.count(word1)

  #Returns the MLE conditional probability of the bigram "word1 word2" with 
  #Laplace smoothing
  def getSmoothedBigramProb(self, word1, word2):
    bigramCount = 0

    prev = self.words[0]
    for word in self.words:
      if prev == word1 and word == word2:
        bigramCount += 1

      prev = word

    return float((bigramCount + 1)) / (self.count(word1) + self.numUniqueWords)

  #Returns the Absolute Discounting probability of a bigram
  def getADProb(self, word1, word2):
    bigramCount = 0

    prev = self.words[0]
    for word in self.words:
      if prev == word1 and word == word2:
        bigramCount += 1

      prev = word

    #discount the bigramCount by 0.5
    return (bigramCount - 0.5) / self.count(word1)


  #Returns the Maximum Likelihood Estimate for the occurence of a single word
  def getMLE(self, word):

    return float(self.count(word)) / len(self.words)

  #Get's the number of occurences for a word in the corpus. Saves it in the 
  #wordCount map for quick access
  def count(self, word):
    #Try to immediately retrieve the word count from the dictionary  
    try:
      return self.wordCount[word]
    except KeyError, e:
      #We haven't counted this word yet so count now
      num = 0
      for sample in self.words:
        if sample == word:
          num += 1

      #Save count to the dictionary and return
      self.wordCount[word] = num
      return num
