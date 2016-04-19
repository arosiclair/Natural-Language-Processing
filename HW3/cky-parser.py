# CKY Parser
from __future__ import division
from pickle import load
from math import log
from tree import Tree, Node


# Load serialized objects
def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return load(f)


# Parsing algorithm
def parse(inputLine):
    inputLine = inputLine.strip()
    words = inputLine.split(" ")  # the sequence of words

    score = initArray(words)
    back = initArray(words)

    # Iterate over each column in the table
    for j in xrange(0, len(words)):

        # Add the POS tag probabilities to the bottom entry of this column
        for i in xrange(0, len(nonterminals)):
            prob = -1
            try:
                nt = nonterminals[i]
                prob = pcfg[(nt, words[j])]
            except KeyError, e:
                prob = 1 / (pow(len(nonterminals) - 1, 2) + len(terminals))

            score[j][j][i] = log(prob)

        # Iterate over the rest of the rows above in the column.
        for i in xrange(j - 1, -1, -1):
            #Try every splitting index for this entry
            for k in xrange(i, j):
                for rule in pcfg:
                    if len(rule) == 2:
                        continue
                    aindex = nonterminals.index(rule[0])
                    bindex = nonterminals.index(rule[1])
                    cindex = nonterminals.index(rule[2])
                    if score[i][k][bindex] != 0 and score[k + 1][j][cindex] != 0:
                        ruleProb = -1
                        try:
                            ruleProb = pcfg[rule]
                        except KeyError, e:
                            ruleProb = 1 / (pow(len(nonterminals) - 1, 2) + len(terminals))
                        prob = log(ruleProb) + score[i][k][bindex] + score[k + 1][j][cindex]
                        if prob > score[i][j][aindex] or score[i][j][aindex] == 0:
                            score[i][j][aindex] = prob
                            back[i][j][aindex] = (k, bindex, cindex)

    #printArray(score)

    return buildTree(score, back, words, len(words))


def buildTree(score, back, words, wordsLength):
    # Create the root tree
    rootTree = Tree(None)

    # Find the highest probability nonterminal to use for the root node
    maxIndex = getMax(score[0][wordsLength - 1])

    # Get the backpointer corresponding to this nonterminal
    triple = back[0][wordsLength - 1][maxIndex]
    leftChild = Node(nonterminals[triple[1]], [])
    rightChild = Node(nonterminals[triple[2]], [])

    # Create the root node and attach it's children
    rootNode = Node(nonterminals[maxIndex], [leftChild, rightChild])
    rootTree.root = rootNode

    begin = 0
    end = wordsLength - 1
    split = triple[0]  # The splitting index

    # Start by pushing the root's children onto the stack
    # The subsequence that each child represents is also pushed with them.
    stack = []
    stack.append([rightChild, split + 1, end])
    stack.append([leftChild, begin, split])

    # Continue processing sub trees on the stack
    while len(stack) > 0:
        #print "STACK LENGTH:", len(stack)
        nodeList = stack.pop()
        parent = nodeList[0]
        ntIndex = nonterminals.index(parent.label)
        begin = nodeList[1]
        end = nodeList[2]

        # If this is a subsequence of multipe words, get the left and right constituents
        if (end - begin) > 0:
            # Get the left and right constituents of the subsequence [i:j]
            triple = back[begin][end][ntIndex]
            leftChild = Node(nonterminals[triple[1]], [])
            rightChild = Node(nonterminals[triple[2]], [])
            split = triple[0]

            # Attach these new children to the parent node
            parent.append_child(leftChild)
            parent.append_child(rightChild)

            # Push these new children onto the stack
            stack.append([rightChild, split + 1, end])
            stack.append([leftChild, begin, split])

        # Otherwise this is a subsequence of 1 word, attach the word as a child
        # to the parent, which is a POS tag
        else:
            terminal = Node(words[begin], [])
            parent.append_child(terminal)
    
    return rootTree

def outputTree(node):

    if len(node.children) == 0:
        return node.label
    elif len(node.children) == 1:
        return node.label + "(" + outputTree(node.children[0]) + ") "
    else:
        return node.label + "(" + outputTree(node.children[0]) + outputTree(node.children[1]) + ") "

def printArray(array):
    for i in xrange(0, len(array)):
        for j in xrange(0, len(array[i])):
            print "\nFOR ENTRY [%d][%d]:" % (i, j)
            for k in xrange(0, len(array[i][j])):
                print array[i][j][k], ",",


# Get the index of the entry in this list with the max probability
def getMax(list):
    maxIndex = 0
    maxProb = 0
    for i in xrange(0, len(list)):
        if list[i] > maxProb:
            maxProb = list[i]
            maxIndex = i

    return maxIndex


def initArray(words):
    result = [0] * (len(words))
    for i in xrange(0, len(result)):
        result[i] = [0] * (len(words))

    for i in xrange(0, len(result)):
        for j in xrange(0, len(result[i])):
            result[i][j] = [0] * len(nonterminals)

    return result


def addUnary(score, back, begin, end):
    added = True
    while added:
        added = False
        for nt in nonterminals:
            for term in terminals:
                aindex = nonterminals.index(nt)
                bindex = len(nonterminals) + terminals.index(term)
                ruleProb = 1 / (pow(len(nonterminals) - 1, 2) + len(terminals))
                try:
                    ruleProb = pcfg[(nt, term)]
                except KeyError, e:
                    pass
                # TODO: This probability doesn't make sense.
                prob = log(ruleProb) + log(score[begin][end][bindex])
                if prob > score[begin][end][aindex]:
                    score[begin][end][aindex] = prob
                    back[begin][end][aindex] = (-1, bindex, None)
                    added = True


def getTriples():
    result = []
    for A in nonterminals:
        for B in nonterminals:
            for C in nonterminals:
                result.append(tuple([A, B, C]))

    return result


# --- BEGIN SCRIPT ---
# Open and read each line of the test sequences
testFile = open("test.txt")
testLines = testFile.readlines()
testFile.close()

outputFile = open("output.trees", "w")

# Load the PCFG
pcfg = load_obj("pcfg")
# Load our set of nonterminals from training
nonterminals = load_obj("nonterminals")
terminals = load_obj("terminals")

triples = getTriples()

parsedTrees = []
for line in testLines:
    parsedTrees.append(parse(line))
    #print "LINE PARSED"

for tree in parsedTrees:
    output = outputTree(tree.root) + "\n"
    outputFile.write(output)

print "Output tree file produced: 'output.trees'"