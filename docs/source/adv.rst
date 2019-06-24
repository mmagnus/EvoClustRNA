Adv
======================================================

RNA 3D structure prediction
-----------------------------------------------------

For each sequence chosen for folding, secondary structure predictions were generated based on the MSA. Two methods were used in this study: SimRNA and Rosetta. For Rosetta, a total of 10,000 decoys were generated for the target sequence and each homologous sequence using the Rosetta FARFAR protocol. For SimRNA prediction, SimRNAweb server was used using the default parameters.

Both modeling steps can be performed in a semi-automated way with rna-tools (M.M. et al., unpublished, software available for download at https://github.com/mmagnus/rna-tools) as well as the pipeline of tools facilitating modeling with Rosetta (https://rna-tools.readthedocs.io/en/latest/tools.html#rosetta) and SimRNA/SimRNAweb (https://rna-tools.readthedocs.io/en/latest/tools.html#simrnaweb).

evoClustRNA
-----------------------------------------------------

.. argparse::
   :ref: evoClustRNA.get_parser
   :prog:  evoClustRNA.py

.. automodule:: evoClustRNA
   :members:


evoClust_autoclustix.py
-----------------------------------------------------

.. argparse::
   :ref: evoClust_autoclustix.get_parser
   :prog: evoClust_autoclustix.py

.. automodule:: evoClust_autoclustix.py
   :members:

evoClust_autoclustix.py implements a simple interactive clustering. Technically, this script is a simple wrapper for evoClust_clustix.py.

.. argparse::
   :ref: evoClust_clustix.get_parser
   :prog:  evoClust_clustix.py

.. automodule:: evoClust_clustix.py
   :members:


evoClust_get_models.py
------------------------------------------------------

.. argparse::
   :ref: evoClust_get_models..get_parser
   :prog: evoClust_get_models.py



Python Classes used in the scripts
------------------------------------------------------

RNAmodel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: RNAmodel
   :members:

RNAalignment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: RNAalignment
   :members:
