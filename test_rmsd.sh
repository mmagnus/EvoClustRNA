evoClust_calc_rmsd.py -a test_data/rp14/rp14sub.stk -t test_data/rp14/rp14_5ddp_bound_clean_ligand.pdb --mapping 'target:rp14_farna_eloop_nol2fixed_cst|AACY023581040:aacy23_cst|AJ630128:aj63_cst' -n 'target'  -o out.csv test_data/rp14/rp14_farna_eloop_nol2fixed_cst/*
#test_data/rp14/rp14_farna_eloop_nol2fixed_cst/rp14_farna_eloop_nol2fixed_cst.out.4.pdb  test_data/rp14/rp14_farna_eloop_nol2fixed_cst/rp14_farna_eloop_nol2fixed_cst.out.6.pdb

python evoClust_calc_rmsd.py -a test_data/test_rmsd/aln -t test_data/test_rmsd/4qk8_cl.pdb test_data/test_rmsd/4qlm_cl.pdb -n 4qk8_cl -m test_data/test_rmsd/mapping.txt
