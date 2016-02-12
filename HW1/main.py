#Written in Python 2.7.11

#---BEGIN SCRIPT---
train = open("train.txt")
corpus = train.read()

sentences = corpus.split(".")

print sentences