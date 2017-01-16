.. geekbook documentation master file, created by
   sphinx-quickstart on Fri Nov 15 13:28:22 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to EvoClustRNA documentation!
================================

Marcin Magnus & Rhiju Das

The code of the project can be found at GitHub (https://github.com/mmagnus/EvoClustRNA)

The Python implementation of a clustering routines of evolutionary conserved regions (helical regions) for RNA fold prediction.

The understanding of the importance of RNA has dramatically changed over the recent years. As in the case of proteins, the function of an RNA molecule is encoded in its tertiary structure, which in turn is determined by the molecule's sequence. The prediction of tertiary structures of complex RNAs is still a challenging task. Using the observation that RNA sequences from the same RNA family fold into highly conserved structure, we make an assumption that similar process can be observed in in silico modeling and can be used to detect global helical arrangements for the target sequence based on the arrangements within a subset of homologs. 

**Thus this work explores the use of multiple sequence alignment information and parallel modeling of RNA homologs to improve ab initio RNA structure prediction method.**

To build a structural model of the target sequence, a multi-step modeling process is performed. First, for the target sequence, a subset of homologous sequences is selected using the RFAM database. Subsequently, independent folding simulations using ROSETTA/FARNA are carried out. Structural fragments corresponding to the evolutionary conserved regions (helical regions) - determined from the alignment - are extracted from all obtained models and clustered. The model of the target sequence is selected based on the most common structural arrangement of helical. In order to increase the accuracy of RNA structure prediction, we also explore a way to constrain simulation keeping conserved residues identified by on the alignment in close spatial proximity. 

We tested our approach on the testing dataset of RNA of known structures and on two RNA Puzzles challenges. In blind prediction of ZMP riboswitch, the final model obtained with the described methodology was scored as the 2nd and in blind prediction of L-glutamine riboswitch (bound form) the model was scored as the 1st in the ranking of all submissions in terms of the RMSD to the native structure.
Through this combination of parallel modeling of homologous sequences, constraints on conserved residues, and selecting the final model based on the clustering of conserved fragments, we increase the performance of RNA structure prediction.


Contents:

.. toctree::
   :maxdepth: 3

   install
   getstarted
   
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
