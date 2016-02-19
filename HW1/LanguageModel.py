class LanguageModel:

  #Preprcess the corpus so that it is more easily scanned.
  def __init__(self, corpus):
    #Create instance variable of all lowercase input corpus
    self.corpus = corpus.lower()
    #Split string into sentences delimited by a period
    self.sentences = self.corpus.split(".")

    #Split sentences into a list of all words in the corpus, delimitted by a space
    #Start and end tokens are inserted at the start and end of sentences
    self.words = []
    for sentence in self.sentences:
      self.words.append("<s>")
      self.words.extend(sentence.split())
      self.words.append("</s>")

    #Scan the corpus for its vocabulary
    self.vocabulary = []
    self.vocabularySize = 0
    for word in self.words:
      if word not in self.vocabulary:
        self.vocabulary.append(word)
        self.vocabularySize += 1

    #Dictionaries that will save the count for words and bigrams we have already counted
    self.wordCount = {}
    self.bigramCount = {}

  #Returns the joint probability of a sequence of words 
  def getSequenceProb(self, wordList):
    #Start off with the MLE of the first word in the sequence
    result = self.getMLE(wordList[0])
    print result

    wordList.insert(0, "<s>")
    wordList.append("</s>")

    #Multiply the bigram probabilities of the next successive pairs of words in 
    #the sequence
    for i in xrange(1, len(wordList)):
      result *= self.getBigramProb(wordList[i - 1], wordList[i])
      print result

    return result

  #Returns the MLE conditional probability of the bigram "word1 word2"
  def getBigramProb(self, word1, word2):
    numBigrams = self.count(word1, word2)
    return float(numBigrams) / self.count(word1)

  #Returns the MLE conditional probability of the bigram "word1 word2" with 
  #Laplace smoothing
  def getSmoothedBigramProb(self, word1, word2):
    numBigrams = self.count(word1, word2)
    return float(numBigrams + 1) / (self.count(word1) + self.vocabularySize + 1)

  #Returns the probability of a bigram occuring using Katz Back-off method
  def katzBigramProb(self, word1, word2):
    #2 Part function: if the bigram is seen
    if self.count(word1, word2) > 0:
      return self.getADProb(word1, word2)

    #If the bigram is unseen
    elif self.count(word1, word2) == 0:
      return self.alpha(word1) * self.beta(word2)
    
  #Returns the Absolute Discounting probability of a bigram
  def getADProb(self, word1, word2 = None):
    #Unigram probability
    if word2 == None:
      if self.count(word) == 0:
        return 1.0 / self.vocabularySize
      else:
        return (self.count(word) - 0.5) / self.count(word)

    #Bigram probability
    else:
      return (self.count(word1, word2) - 0.5) / self.count(word1)


  #Returns the Maximum Likelihood Estimate for the occurence of a single word
  def getMLE(self, word):

    return float(self.count(word)) / len(self.words)

  #Get's the number of occurences for a word in the corpus. Saves it in the 
  #wordCount map for quick access
  def count(self, word1, word2 = None):
    #Only count the unigram
    if word2 == None:
      #Try to immediately retrieve the word count from the dictionary   
      try:
        return self.wordCount[word1]
      except KeyError, e:
        #We haven't counted this word yet so count now
        num = 0
        for sample in self.words:
          if sample == word1:
            num += 1

        #Save count to the dictionary and return
        self.wordCount[word1] = num
        return num
    #Count the bigram
    else:
      #Try to immediately retrieve the bigram count from the dictionary
      try:
        return self.bigramCount[(word1, word2)]
      except KeyError, e:
        #We haven't counted this bigram yet so count now
        count = 0
        prev = self.words[0]
        for word in self.words:
          if prev == word1 and word == word2:
            count += 1

          prev = word

        self.bigramCount[(word1, word2)] = count
        return count

  #Finds the amount of probability reserved for unseen bigrams beginning with word1
  def alpha(self, word1):
    remainingProb = 1.0

    for word in self.vocabulary:
      remainingProb -= self.getADProb(word1, word)

    return remainingProb

  def beta(self, word2):
    numerator = getADProb(word2)
    denominator = 0

    for word in self.vocabulary:
      denominator += getADProb(word)

    return numerator / denominator