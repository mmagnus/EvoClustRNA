EvoClustRNA
============================================================================================================
Marcin Magnus & Rhiju Das

The Python implementation of a clustering routines of evolutionary conserved regions (helical regions) for RNA fold prediction. 

Results
-------------------------------------------------------------------------------

@plot here

Example: RNA Puzzle Challenge 13: ZMP riboswitch (#2 modeling in the ranking)
-------------------------------------------------------------------------------

@todo

    python rnastruc_evo_clustix.py --rna_alignment_fn test_data/rp14sub.stk \
       --output_dir test_out/rp14 \
       --input_dir test_data \
       --mapping 'target:rp14_farna_eloop_nol2fixed_cst|AACY023581040:aacy23_cst|AJ630128:aj63_cst' \
       -x test_out/rp14_matrix.txt

The results <http://ahsoka.u-strasbg.fr/rnapuzzles/Problem0013/13_index.php>

Example: RNA Puzzle Challenge 14: L-glutamine riboswitch (#1 modeling in the ranking)
-------------------------------------------------------------------------------
(bound sequence)

@todo

The results <http://ahsoka.u-strasbg.fr/rnapuzzles/Problem0014_Bound/14_index.php>

<http://ahsoka.u-strasbg.fr/rnapuzzles/problems_past.php>
