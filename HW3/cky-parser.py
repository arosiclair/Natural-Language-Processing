#CKY Parser

from pickle import load
from math import log

#Load serialized objects
def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return load(f)

#Parsing algorithm
def parse(line):
	words = line.split(" ")	#the sequence of words

	score = initArray(words)
	back = initArray(words)

	for i in xrange(0, len(words)):
		begin = i
		end = i + 1

		#Add the POS tags for this word
		for j in xrange(0, len(nonterminals)):
			prob = 1 / (pow(len(nonterminals) - 1, 2) + len(terminals))
			try:
				nt = nonterminals[j]
				prob = pcfg[(nt, words[i])]
				score[begin][end][j] = prob
			except KeyError, e:
				continue

		#Add all unary rules that match
		addUnary(score, back, begin, end)

	for span in xrange(2, len(words)):
		for begin in xrange(0, len(words) - span):
			end = begin + span
			for split in xrange(begin + 1, end - 1):
				for triple in getTriples():
					aindex = nonterminals.index(triple[0])
					bindex = nonterminals.index(triple[1])
					cindex = nonterminals.index(triple[2])
					tripleProb = None
					try:
						tripleProb = pcfg[triple]
					except KeyError, e:
						continue

					prob = log(score[begin][split][bindex]) + log(scorescore[begin][split][cindex]) + log(tripleProb)
					if(prob > score[begin][end][aindex]):
						score[begin][end][aindex] = prob
						back[begin][end][aindex] = tuple([split, bindex, cindex])

				#Add all unary rules that match		
				addUnary(score, back, begin, end)

def initArray(words):
	result = [0] * (len(words) + 1)
	for i in xrange(0, len(result)):
		result[i] = [0] * (len(words) + 1)

	for i in xrange(0, len(result)):
		for j in xrange(0, len(result[i])):
			result[i][j] = [0] * len(nonterminals)

	return result

def addUnary(score, back, begin, end):
	added = True
	while added:
		for nt in nonterminals:
			for term in terminals:
				ruleProb = 1 / (pow(len(nonterminals) - 1, 2) + len(terminals))
				try:
					ruleProb = pcfg[(nt, term)]
				except KeyError, e:
					pass
				#TODO: This probability doesn't make sense.
				prob = log(ruleProb) + log(score[begin][end][len(nonterminals) + terminals.index(term)])

def getTriples():
	triples = []
	for A in nonterminals:
		for B in nonterminals:
			for C in nonterminals:
				triples.append(tuple([A, B, C]))

	return triples

#--- BEGIN SCRIPT ---
#Open and read each line of the test sequences
testFile = open("test.txt")
testLines = testFile.readlines()
testFile.close()

#Load the PCFG
pcfg = load_obj("pcfg")
#Load our set of nonterminals from training
nonterminals = load_obj("nonterminals")
terminals = load_obj("terminals")

for line in testLines:
	parse(line)