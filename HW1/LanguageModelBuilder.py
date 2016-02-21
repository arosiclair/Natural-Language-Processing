#Written in Python 2.7.11
from LanguageModel import LanguageModel

#Prompt for input corpus
inputFile = None
while True:
  print "\n Enter the file name of the training corpus"

  try:
    filename = raw_input("> ")
    inputFile = open(filename)
    break
  except IOError, e:
    print "ERROR: Cannot open %r" % filename
    continue

inputFileText = inputFile.read()

lm = LanguageModel(inputFileText)
lm.buildLanguageModelFile()
print "Language model file output as: 'LanguageModel.txt'"

lm.buildTopBigramsFile()
print "Top bigrams file output as: 'TopBigrams.txt'"
