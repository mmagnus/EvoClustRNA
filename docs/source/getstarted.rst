Get Started
===========================================

Modeling
-------------------------------------------

To get an initial set of structures, you might want to use ROSETTA/FARNA (https://www.rosettacommons.org/) and/or SimRNAweb (http://genesilico.pl/SimRNAweb/).

evoClustRNA
-------------------------------------------
Run::

    [mm] evoClustRNA git:(master) ✗   python evoClustRNA.py --rna_alignment_fn test_data/rp14sub.stk --output_dir test_out/rp14 --input_dir test_data --mapping 'target:rp14_farna_eloop_nol2fixed_cst|AACY023581040:aacy23_cst|AJ630128:aj63_cst' -x test_out/rp14_matrix.txt

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

This ``test_out/rp14_matrix.txt`` matrix keeps all-vs-all cores RMSD. Now it's time to cluster it to see what is the most common core in the pool.

Clustix
-------------------------------------------

Now you can cluster the obtained matrix of RMSD (``test_out/rp14_matrix.txt``)::

   ./clustix.py -m  test_out/rp14_matrix.txt -c 3
   cluster #1  curr the biggest cluster size  100.0
   rp14_farna_eloop_nol2fixed_cst.out.1.pdb rp14_farna_eloop_nol2fixed_cst.out.2.pdb rp14_farna_eloop_nol2fixed_cst   .out.5.pdb rp14_farna_eloop_nol2fixed_cst.out.7.pdb
   [..]
   60.pdb
   >> OK! The output is written to the output_cf3.out file

play with ``-c`` (cuttoff) to get 1/6  of your initial models in the first cluster.

TPP Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Do clustix.py and pick RMSD cutoff, to get 1/6 structures in the biggest cluster, for 4 homologs, we should have 100 structures per homolog, so 400 in total. 400 * 1/6 ~= 66)

The most common core in your pool is the first core is the first structure in the cluster #1::

  $ clustix.py -m matrix.txt -c 9.31
 cluster #1  curr the biggest cluster size  66
 tpp_min.out.2.pdb tpp_min.out.3.pdb tpp_min.out.4.pdb tpp_min.out.5.pdb tpp_min.out.6.pdb tpp_min.out.7.pdb tpp_min.out.8.pdb tpp_min.out.9.pdb tpp_min.out.10.pdb tpp_min.out.14.pdb tpp_min.out.17.pdb tpp_min.out.18.pdb tpp_min.out.20.pdb tpp_min.out.22.pdb tpp_min.out.23.pdb tpp_min.out.24.pdb tpp_min.out.25.pdb tpp_min.out.27.pdb tpp_min.out.28.pdb tpp_min.out.29.pdb tpp_min.out.30.pdb tpp_min.out.31.pdb tpp_min.out.32.pdb tpp_min.out.36.pdb tpp_min.out.37.pdb tpp_min.out.39.pdb tpp_min.out.42.pdb tpp_min.out.44.pdb tpp_min.out.45.pdb tpp_min.out.48.pdb tpp_min.out.49.pdb tpp_min.out.50.pdb tpp_min.out.53.pdb tpp_min.out.54.pdb tpp_min.out.58.pdb tpp_min.out.65.pdb tpp_min.out.66.pdb tpp_min.out.69.pdb tpp_min.out.70.pdb tpp_min.out.71.pdb tpp_min.out.72.pdb tpp_min.out.73.pdb tpp_min.out.77.pdb tpp_min.out.82.pdb tpp_min.out.84.pdb tpp_min.out.86.pdb tpp_min.out.87.pdb tpp_min.out.89.pdb tpp_min.out.90.pdb tpp_min.out.92.pdb tpp_min.out.93.pdb tpp_min.out.94.pdb tpp_min.out.95.pdb tpp_min.out.98.pdb tc5_min.out.29.pdb tc5_min.out.33.pdb tc5_min.out.45.pdb tc5_min.out.56.pdb tc5_min.out.66.pdb tc5_min.out.79.pdb tc5_min.out.83.pdb tae_min.out.18.pdb tae_min.out.23.pdb tae_min.out.26.pdb tae_min.out.75.pdb tae_min.out.83.pdb

now you can fetch the full structure for tpp_min.out.2.pdb in <output_fn>/structures/tpp_min.out.2.pdb . This is your final prediction :-)
