Adv
======================================================

Modeling
-----------------------------------------------------

See http://rna-pdb-tools.readthedocs.io/en/latest/utils.html#rosetta to read more how to use rna-pdb-tools to run ROSETTA.

RNAmodel
------------------------------------------------------

.. automodule:: RNAmodel
   :members:

RNAalignment
------------------------------------------------------

.. automodule:: RNAalignment
   :members:


evoClustRNA
------------------------------------------------------

.. argparse::
   :ref: evoClustRNA.get_parser
   :prog:  evoClustRNA.py

.. automodule:: evoClustRNA
   :members:

Clustix
------------------------------------------------------

.. argparse::
   :ref: clustix.get_parser
   :prog:  clustix.py

.. automodule:: clustix
   :members:
      
Tricks
-----------------------------------------------------

Get mapping from a file::

   evoClustRNA.py -a ../sub.sto -i simrnaweb -m `cat mapping.txt` -s -o out
   sub_matrix.txt
    # of rnastruc: 5
    rnastruc: ['ACCL02000010.1/116901-116991:tha', 'ACKX01000080.1/10519-10620:hak', 'AAQK01002704.1/947-1059:haq', 'CP001034.1/2651359-2651454:hcp', '4lVV:4lvv']
     ACCL02000010.1/116901-116991 <-> tha
      cutting out fragments ...
       # selected residues: 88
       saved to struc: out/structures/5f8916a8_ALL_100low-000001_AA.pdb
       saved to motifs: out/motifs//5f8916a8_ALL_100low-000001_AA.pdb
    
