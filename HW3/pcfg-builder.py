#Probability CFG builder
from __future__ import division
import tree


#Generate list of unique nonterminals from the training trees
def getNonterminals():
	for i in xrange(0, len(trainInput)):
		begin = None
		end = None
		if trainInput[i] == '(':
			end = i;
			for j in xrange(i - 1, 0, -1):
				if trainInput[j] == ' ' or trainInput[j] == '\n' or trainInput[j] == '(':
					begin = j + 1
					break

			nt = trainInput[begin : end]
			if nt not in nonterminals:
				nonterminals.append(trainInput[begin : end])

def getTerminals():
	for tree in trees:
		for leaf in tree.leaves():
			if leaf.label not in terminals:
				terminals.append(leaf.label)

def countRules(tree):
	global ruleCounts
	stack = []
	stack.append(tree.root)

	while(len(stack) > 0):
		parent = stack.pop()

		#This is a leaf node with no expansion, skip it
		if len(parent.children) == 0:
			continue

		stack.extend(parent.children)
		expansions = None #The sub dictionary with RHS expansions
		#Try getting a reference to the expansions dictionary for this nonterminal
		try:
			expansions = ruleCounts[parent.label]
		#This is the first time we're seeing this nonterminal, create a new 
		#expansions dict for it
		except KeyError, e:
			ruleCounts[parent.label] = {}
			expansions = ruleCounts[parent.label]
		
		childLabels = []
		for child in parent.children:
			childLabels.append(child.label)
		#Increment the number of occurences for this nonterminal -> RHS expansion
		try:
			expansions[tuple(childLabels)] += 1
		except KeyError, e:
			expansions[tuple(childLabels)] = 1

def generatePCFG():
	global pcfg

	for nonterminal in ruleCounts:
		total = 0
		for expansion in ruleCounts[nonterminal]:
			total += ruleCounts[nonterminal][expansion]

		for expansion in ruleCounts[nonterminal]:
			prob = (ruleCounts[nonterminal][expansion] + 1) / (pow(len(nonterminals) - 1, 2) + len(terminals))
			key = []
			key.append(nonterminal)
			key.extend(expansion)
			pcfg[tuple(key)] = prob

#Open the training file and get a list of lines
trainFile = open("train.trees")
trainLines = trainFile.readlines()
trainFile.seek(0)
trainInput = trainFile.read()
trainFile.close()

#A list of unique nonterminals from training
nonterminals = []
getNonterminals()

trees = []	#A list of Tree objects from training

#Iterate over the training examples and generate a tree for each line
for line in trainLines:
	if line.strip() == 0:
		continue

	parsedTree = tree.Tree.from_str(line)
	trees.append(parsedTree)

#A list of unique terminals (words) in training
terminals = []
getTerminals()

#print terminals

#A dictionary with key values: <nonterminal label>, and values: <dictionary>
#The sub-dictionary will have the right hand side of the rules (ie: (NN, VB)) as a keys
#and the count of nonterminal -> rhs in training.
ruleCounts = {} 

#Iterate over the generated parse trees and count the number of occurences for
#each expansion
for tree in trees:
	countRules(tree)

#The Probability Context Free Grammar. Key = ([nonterminal, expansion...])
#Value = laplace smoothed probability of using that nonterminal and expansion
pcfg = {}
generatePCFG()

top10 = []
# for rule in pcfg:
# 	if len(rule) < 3:
# 		continue

# 	for i in xrange(0, len(top10)):
# 		if pcfg[rule] > top10[i][-1]:
# 			entry = []
# 			entry.extend(rule)
# 			entry.append(pcfg[rule])
# 			top10.insert(i, entry)
# 			break

# 	if len(top10) < 10:
# 		entry = []
# 		entry.extend(rule)
# 		entry.append(pcfg[rule])
# 		top10.append(entry)

# 	if len(top10) == 11:
# 		top10.pop()

for lhs in ruleCounts:
	expansions = ruleCounts[lhs]
	for expansion in expansions:
		if len(expansion) < 2:
			continue
		for i in xrange(0, len(top10)):
			if expansions[expansion] > top10[i][-1]:
				entry = []
				entry.append(lhs)
				entry.extend(expansion)
				entry.append(expansions[expansion])
				top10.insert(i, entry)
				break
		
		if len(top10) < 10:
			entry = []
			entry.append(lhs)
			entry.extend(expansion)
			entry.append(expansions[expansion])
			top10.append(entry)
			break

		if len(top10) == 11:
			top10.pop()

for entry in top10:
	print "%-5s -> %-7s, %-10s| Frequency: %5d" % (entry[0], entry[1], entry[2], entry[3])

# for rule in pcfg:
# 	print "%-10s -> %-25s Prob: %.10f" % (rule[0], rule[1:], pcfg[rule])

# for nonterminal in ruleCounts:
# 	for rhs in ruleCounts[nonterminal]:
# 		print "%-10s -> %-15s Prob: %f" % (nonterminal, rhs, ruleCounts[nonterminal][rhs])

