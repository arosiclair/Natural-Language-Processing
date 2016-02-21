#Written in Python 2.7.11

#---BEGIN SCRIPT---

#Print app header
print "-" * 40
print "%32s" % "LANGUAGE MODEL EVALUATOR"
print "-" * 40

#Prompt for the filename of the training corpus
trainingFile = None
while True:
  print "\nEnter the file name for the training corpus"
  try:
    filename = raw_input("> ")
    trainingFile = open(filename)
    break
  except IOError, e:
    print "ERROR: Cannot open %r" % filename
    continue
