ALL PYTHON SCRIPTS ARE WRITTEN IN VERSION 2.7.11

1. pcfg-builder.py - This script processes the training data and builds a 
   probability context free grammar from it. The PCFG is a python dictionary
   object and is serialized and saved as 'pcfg.pkl'. The dictionary keys are the 
   rules in list form (ie: NP -> DT NN is keyd as [NP, DT, NN]) and the values 
   are the rule's laplace probability.

2. cky-parser.py - This script uses the PCFG as well as the set of terminals and
   nonterminals generated from training (Run the PCFG builder first!) to build a
   CKY parse table and generate optimal parse trees for the test sequences. The
   pseudocode from section 14.2 of the Speech and Language Processing was used
   as a reference for implementation. This script only parses the test sequences 
   from 'test.txt' in the same directory.

3. My brief report is in Report.txt