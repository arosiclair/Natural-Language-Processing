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

      if(sentence.split() != ""):
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
    result = 1

    wordList.insert(0, "<s>")
    wordList.append("</s>")

    #Multiply the bigram probabilities of the next successive pairs of words in 
    #the sequence
    for i in xrange(1, len(wordList)):
      result *= self.getBigramProb(wordList[i - 1], wordList[i])

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
      if self.count(word1) == 0:
        return 1.0 / self.vocabularySize
      else:
        return (self.count(word1) - 0.5) / len(self.words)

    #Bigram probability
    else:
      return (self.count(word1, word2) - 0.5) / self.count(word1)


  #Returns the Maximum Likelihood Estimate for the occurence of a single word
  def getMLE(self, word):
    return float(self.count(word)) / len(self.words)

  def getSmoothedUnigramProb(self, word):
    return float(self.count(word) + 1) / (len(self.words) + self.vocabularySize)

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
    numerator = self.getADProb(word2)
    denominator = 0

    for word in self.vocabulary:
      denominator += self.getADProb(word)

    return numerator / denominator

  def buildLanguageModelFile(self):
    bigramsOutput = open("LanguageModel.txt", 'w')

    #Iterate through each succesive bigram in the corpus, keeping track of counts 
    #in the bigrams dictionary
    prev = self.words[0]
    for i in xrange(1, len(self.words)):
      word = self.words[i]
      try:
        num = self.bigramCount[(prev, word)]
        self.bigramCount[(prev, word)] = num + 1
      except KeyError, e:
        self.bigramCount[(prev, word)] = 1

      prev = word

    #File header
    bigramsOutput.write("-" * 85 + "\n")
    bigramsOutput.write("%49s" % "LANGUAGE MODEL" + "\n")
    bigramsOutput.write("-" * 85 + "\n")
    bigramsOutput.write("%-40s%15s%15s%15s" % ("Bigram", "Frequency", "MLE", "Katz") + "\n")
    bigramsOutput.write("-" * 85 + "\n")

    #Print all bigrams seen in training along wit their frequency, MLE and Katz
    #estimations
    for bigram in self.bigramCount.keys():
      bigramsOutput.write("%-20s%-20s%15s" % (bigram[0], bigram[1], self.bigramCount[bigram]))
      bigramsOutput.write("%15.10f%15.10f\n" % (self.getBigramProb(bigram[0], bigram[1]),
                                        self.katzBigramProb(bigram[0], bigram[1])))
    bigramsOutput.write("-" * 85 + "\n")

    #Header for unigram frequencies
    bigramsOutput.write("\n%-20s%9s\n" % ("Unigram", "Frequency"))
    bigramsOutput.write("-" * 85 + "\n")

    #Print all unigrams seen in training along with their frequency
    for word in self.vocabulary:
      bigramsOutput.write("%-20s%9s\n" % (word, self.count(word)))

  def buildTopBigramsFile(self):
    output = open("TopBigrams.txt", 'w')

    self.writeTopMLE(output)
    self.writeTopLaplace(output)
    self.writeTopAD(output)
    self.writeTopKatz(output)


  def writeTopMLE(self, output):
    #List of top 20 MLE bigrams
    top20MLE = []

    for bigram in self.bigramCount.keys():
      #The joint MLE probability
      prob = self.getBigramProb(bigram[1], bigram[0]) * self.getMLE(bigram[0])

      #Insert bigrams and probability as a 3 element list into the top20MLE list
      for i in xrange(0, 20):
        if i == len(top20MLE) and i < 20:
          top20MLE.append([bigram[0], bigram[1], prob])
        if prob > top20MLE[i][2]:
          top20MLE.insert(i, [bigram[0], bigram[1], prob])
          if len(top20MLE) == 21:
            top20MLE.remove(top20MLE[20])
          break

    #Top 20 MLE Header
    output.write("-" * 60 + "\n")
    output.write("%39s\n" % "TOP 20 MLE BIGRAMS") 
    output.write("-" * 60 + "\n")
    output.write("%-40s%20s\n" % ("Bigram", "Joint Probability")) 
    output.write("-" * 60 + "\n")

    #Print the top 20
    i = 1
    for bigram in top20MLE:
      output.write("%-3d%-17s%-20s%20.10f\n" % (i, bigram[0], bigram[1], bigram[2])) 
      i += 1

  def writeTopLaplace(self, output):
    top20Laplace = []
    #Top 20 Laplace Smoothing
    for bigram in self.bigramCount.keys():
      #The joint MLE probability
      prob = self.getSmoothedBigramProb(bigram[1], bigram[0]) * self.getSmoothedUnigramProb(bigram[0])

      #Insert bigrams and probability as a 3 element list into the top20Laplace list
      for i in xrange(0, 20):
        if i == len(top20Laplace) and i < 20:
          top20Laplace.append([bigram[0], bigram[1], prob])
        if prob > top20Laplace[i][2]:
          top20Laplace.insert(i, [bigram[0], bigram[1], prob])
          if len(top20Laplace) == 21:
            top20Laplace.remove(top20Laplace[20])
          break

    #Top 20 MLE Header
    output.write("-" * 60 + "\n")
    output.write("%41s\n" % "TOP 20 LAPLACE BIGRAMS") 
    output.write("-" * 60 + "\n")
    output.write("%-40s%20s\n" % ("Bigram", "Joint Probability")) 
    output.write("-" * 60 + "\n")

    #Print the top 20
    i = 1
    for bigram in top20Laplace:
      output.write("%-3d%-17s%-20s%20.10f\n" % (i, bigram[0], bigram[1], bigram[2])) 
      i += 1

  def writeTopAD(self, output):
    top20AD = []
    #Top 20 Absolute Discounting
    for bigram in self.bigramCount.keys():
      #The joint probability
      prob = self.getADProb(bigram[1], bigram[0]) * self.getADProb(bigram[0])

      #Insert bigrams and probability as a 3 element list into the top20AD list
      for i in xrange(0, 20):
        if i == len(top20AD) and i < 20:
          top20AD.append([bigram[0], bigram[1], prob])
        if prob > top20AD[i][2]:
          top20AD.insert(i, [bigram[0], bigram[1], prob])
          if len(top20AD) == 21:
            top20AD.remove(top20AD[20])
          break

    #Top 20 MLE Header
    output.write("-" * 60 + "\n")
    output.write("%47s\n" % "TOP 20 ABSOLUTE DISCOUNTED BIGRAMS")
    output.write("-" * 60 + "\n")
    output.write("%-40s%20s\n" % ("Bigram", "Joint Probability")) 
    output.write("-" * 60 + "\n")

    #Print the top 20
    i = 1
    for bigram in top20AD:
      output.write("%-3d%-17s%-20s%20.10f\n" % (i, bigram[1], bigram[0], bigram[2]))
      i += 1

  def writeTopKatz(self, output):
    top20Katz = []
    #Top 20 Absolute Discounting
    for bigram in self.bigramCount.keys():
      #The joint probability
      prob = self.getADProb(bigram[1], bigram[0]) * self.getADProb(bigram[0])

      #Insert bigrams and probability as a 3 element list into the top20Katz list
      for i in xrange(0, 20):
        if i == len(top20Katz) and i < 20:
          top20Katz.append([bigram[0], bigram[1], prob])
        if prob > top20Katz[i][2]:
          top20Katz.insert(i, [bigram[0], bigram[1], prob])
          if len(top20Katz) == 21:
            top20Katz.remove(top20Katz[20])
          break

    #Top 20 MLE Header
    output.write("-" * 60 + "\n")
    output.write("%44s\n" % "TOP 20 KATZ BACK-OFF BIGRAMS") 
    output.write("-" * 60 + "\n")
    output.write("%-40s%20s\n" % ("Bigram", "Joint Probability")) 
    output.write("-" * 60 + "\n")

    #Print the top 20
    i = 1
    for bigram in top20Katz:
      output.write("%-3d%-17s%-20s%20.10f\n" % (i, bigram[0], bigram[1], bigram[2]))
      i += 1