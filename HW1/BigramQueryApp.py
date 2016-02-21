from LanguageModel import LanguageModel

#---BEGIN SCRIPT---
#Written in Python 2.7.11

#Ask for input corpus
while True:
  #Print the header
  print "-" * 40
  print "%32s" % "BIGRAM QUERY APPLICATION"
  print "-" * 40

  inputFile = None
  while True:
    print "\n Enter the file name of the corpus"

    try:
      filename = raw_input("> ")
      inputFile = open(filename)
      break
    except IOError, e:
      print "ERROR: Cannot open %r" % filename
      continue

  inputText = inputFile.read()
  lm = LanguageModel(inputText)
  print "Input corpus has been successfully pre-processed.\n"
  break

while True:
  #Print the Main Menu
  print "-" * 40
  print "%24s" % "MAIN MENU"
  print "-" * 40

  print "Select the desired estimation method:"
  print "1) Maximum Likelihood Estimate"
  print "2) Laplace Smoothed Estimate"
  print "3) Absolute Discounted Estiamte"
  print "4) Katz Back-off Method"
  print "5) Quit"
  print "-" * 40

  #Get input number
  num = 0
  while True:
    option = raw_input("> ")
    try:
      int(option)
      if (0 < int(option) < 6):
        num = int(option)
        break
      else:
        raise ValueError(" error")
    except ValueError, e:
      print "ERROR: Please enter a valid integer between 1-5"
      continue

  #Handle input number:
  if(num == 1):
    while True:
      print "Enter the desired bigram:"
      bigram = raw_input("> ").split()
      if(len(bigram) == 2):
        print "The Maximum Likelihood Estimate for %r is: %f" % (bigram, 
                                                                lm.getMLEProb(bigram[0], bigram[1]))
        break
      else:
        print "ERROR: Invalid bigram. A bigram is a sequence of 2 words separated by whitespace."
        continue

  elif(num == 2):
    while True:
      print "Enter the desired bigram:"
      bigram = raw_input("> ").split()
      if(len(bigram) == 2):
        print "The Laplace Smoothed Estimate for %r is: %f" % (bigram, 
                                                                lm.getSmoothedProb(bigram[0], bigram[1]))
        break
      else:
        print "ERROR: Invalid bigram. A bigram is a sequence of 2 words separated by whitespace."
        continue

  elif(num == 3):
    while True:
      print "Enter the desired bigram:"
      bigram = raw_input("> ").split()
      if(len(bigram) == 2):
        print "The Absolute Discounted probability for %r is: %f" % (bigram, 
                                                                lm.getADProb(bigram[0], bigram[1]))
        break
      else:
        print "ERROR: Invalid bigram. A bigram is a sequence of 2 words separated by whitespace."
        continue

  elif(num == 4):
    while True:
      print "Enter the desired bigram:"
      bigram = raw_input("> ").split()
      if(len(bigram) == 2):
        print "The Katz Back-off probability for %r is: %f" % (bigram, 
                                                                lm.katzBigramProb(bigram[0], bigram[1]))
        break
      else:
        print "ERROR: Invalid bigram. A bigram is a sequence of 2 words separated by whitespace."
        continue
  elif(num == 5):
    quit()

