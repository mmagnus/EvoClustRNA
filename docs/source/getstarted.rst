Get Started
===========================================

Modeling
-------------------------------------------
First you have to use ROSETTA or SimRNA to get initial PDB models.

evoClustRNA
-------------------------------------------
Run::

    [mm] evoClustRNA git:(master) ✗   python rnastruc_evo_clustix.py --rna_alignment_fn test_data/rp14sub.stk --output_dir test_out/rp14 --input_dir test_data --mapping 'target:rp14_farna_eloop_nol2fixed_cst|AACY023581040:aacy23_cst|AJ630128:aj63_cst' -x test_out/rp14_matrix.txt

to perform a clustering.

The output should look like ::

    rnastruc_evo_clustix.py
    --------------------------------------------------------------------------------
     # of rnastruc: 3
     rnastruc: ['target:rp14_farna_eloop_nol2fixed_cst', 'AACY023581040:aacy23_cst', 'AJ630128:aj63_cst']
      target <-> rp14_farna_eloop_nol2fixed_cst
       cutting out fragments ...
      AACY023581040 <-> aacy23_cst
       cutting out fragments ...
      AJ630128 <-> aj63_cst
       cutting out fragments ...
     # of models: 300
    matrix was created!  test_out/rp14_matrix.txt

Clustix
-------------------------------------------

Now you can cluster the obtained matrix of RMSD (``test_out/rp14_matrix.txt``)::

   ./clustix.py -m  test_out/rp14_matrix.txt -c 3
   cluster #1  curr the biggest cluster size  100.0
   rp14_farna_eloop_nol2fixed_cst.out.1.pdb rp14_farna_eloop_nol2fixed_cst.out.2.pdb rp14_farna_eloop_nol2fixed_cst   .out.5.pdb rp14_farna_eloop_nol2fixed_cst.out.7.pdb
   [..]
   60.pdb
   >> OK! The output is written to the output_cf3.out file

play with ``-c`` (cuttoff) to get 1/6 of your initial models in the first cluster.
