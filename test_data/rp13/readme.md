RNA-Puzzle 13
----------------------------------------------------------

1. Model 5 homologs with method of your choice.
2. Extract top100 models and put them into `structures`

-------------------------------------------------------------------------------

    [mm] evox$ git:(master) ✗ evoClustRNA.py -a ../rp13finalX_noSSperSeq_ref.sto -i structures -m ../mapping_ref.txt -f
     \_ evoClustRNA  Namespace(flat_dir=True, inf=False, input_dir='structures', mapping_fn='../mapping_ref.txt', matrix_fn='', output_dir='out', rna_alignment_fn='../rp13finalX_noSSperSeq_ref.sto', save=False, verbose=False)
    rp13finalX_noSSperSeq_ref_mapping_refX.matrix
     # of rnastruc: 6
     rnastruc: ['rp13:tar_', 'rp13:solution', 'cp0016:zcp', 'nc9445:znc', 'nc3295:zc3', 'nzaaox:zza']
      rp13 <-> tar_
       cutting out fragments ...
       analyzing... structures/*tar_*.pdb
       # of structures 200
      rp13 <-> solution
       cutting out fragments ...
       analyzing... structures/*solution*.pdb
       # of structures 1
      cp0016 <-> zcp
       cutting out fragments ...
       analyzing... structures/*zcp*.pdb
       # of structures 200
      nc9445 <-> znc
       cutting out fragments ...
       analyzing... structures/*znc*.pdb
       # of structures 200
      nc3295 <-> zc3
       cutting out fragments ...
       analyzing... structures/*zc3*.pdb
       # of structures 200
      nzaaox <-> zza
       cutting out fragments ...
       analyzing... structures/*zza*.pdb
       # of structures 200
     # of models: 1001
    matrix was created!  rp13finalX_noSSperSeq_ref_mapping_refX.matrix
    evoClustRNA.py -a ../rp13finalX_noSSperSeq_ref.sto -i structures -m ../mapping_ref.txt -f

copy models from structures to reps

    [mm] evox$ git:(master) ✗ evoClust_get_models.py -i structures/ *.out -u
    evoClust_get_models.py
    --------------------------------------------------------------------------------
    1_tar_min.out.1.pdb
    2_zcp_min.out.8.pdb
    3_tar_min.out.66.pdb
    4_tar_min.out.98.pdb
    5_tar_min.out.25.pdb
    = structures == out/structures/<files>===================
    cp -v structures//tar_min.out.1.pdb reps/c1_tar_min.out.1.pdb
    structures//tar_min.out.1.pdb -> reps/c1_tar_min.out.1.pdb
    cp -v structures//zcp_min.out.8.pdb reps/c2_zcp_min.out.8.pdb
    structures//zcp_min.out.8.pdb -> reps/c2_zcp_min.out.8.pdb
    cp -v structures//tar_min.out.66.pdb reps/c3_tar_min.out.66.pdb
    structures//tar_min.out.66.pdb -> reps/c3_tar_min.out.66.pdb
    cp -v structures//tar_min.out.98.pdb reps/c4_tar_min.out.98.pdb
    structures//tar_min.out.98.pdb -> reps/c4_tar_min.out.98.pdb
    cp -v structures//tar_min.out.25.pdb reps/c5_tar_min.out.25.pdb
    structures//tar_min.out.25.pdb -> reps/c5_tar_min.out.25.pdb
    = motif ==========================================
    out/motifs/tar_min.out.1.pdb -> reps_motifs/1_tar_min.out.1.pdb
    Missing motifs folder?
    out/motifs/zcp_min.out.8.pdb -> reps_motifs/2_zcp_min.out.8.pdb
    Missing motifs folder?
    out/motifs/tar_min.out.66.pdb -> reps_motifs/3_tar_min.out.66.pdb
    Missing motifs folder?
    out/motifs/tar_min.out.98.pdb -> reps_motifs/4_tar_min.out.98.pdb
    Missing motifs folder?
    out/motifs/tar_min.out.25.pdb -> reps_motifs/5_tar_min.out.25.pdb
    Missing motifs folder?

copy models from structures to reps_ns (this is where only models for the target sequences are stored, so no models of homologs):

    [mm] evox$ git:(master) ✗ evoClust_get_models.py -i structures/ *.out -n tar -u
    evoClust_get_models.py
    --------------------------------------------------------------------------------
    ['tar_min.out.1.pdb', '', 'tar_min.out.66.pdb', 'tar_min.out.98.pdb', 'tar_min.out.25.pdb']
    1_tar_min.out.1.pdb
    2_
    3_tar_min.out.66.pdb
    4_tar_min.out.98.pdb
    5_tar_min.out.25.pdb
    = structures == out/structures/<files>===================
    cp -v structures//tar_min.out.1.pdb reps_ns/c1_tar_min.out.1.pdb
    structures//tar_min.out.1.pdb -> reps_ns/c1_tar_min.out.1.pdb
    cp -v structures// reps_ns/c2_
    cp: structures// is a directory (not copied).
    cp -v structures//tar_min.out.66.pdb reps_ns/c3_tar_min.out.66.pdb
    structures//tar_min.out.66.pdb -> reps_ns/c3_tar_min.out.66.pdb
    cp -v structures//tar_min.out.98.pdb reps_ns/c4_tar_min.out.98.pdb
    structures//tar_min.out.98.pdb -> reps_ns/c4_tar_min.out.98.pdb
    cp -v structures//tar_min.out.25.pdb reps_ns/c5_tar_min.out.25.pdb
    structures//tar_min.out.25.pdb -> reps_ns/c5_tar_min.out.25.pdb
    = motif ==========================================
    out/motifs/tar_min.out.1.pdb -> reps_motifs_ns/1_tar_min.out.1.pdb
    Missing motifs folder?
    out/motifs/ -> reps_motifs_ns/2_
    Missing motifs folder?
    out/motifs/tar_min.out.66.pdb -> reps_motifs_ns/3_tar_min.out.66.pdb
    Missing motifs folder?
    out/motifs/tar_min.out.98.pdb -> reps_motifs_ns/4_tar_min.out.98.pdb
    Missing motifs folder?
    out/motifs/tar_min.out.25.pdb -> reps_motifs_ns/5_tar_min.out.25.pdb
    Missing motifs folder?


OK, so now we have two folders with models that we can compare to the reference structure.

Various methods can be used to do that. For `reps_ns` (so the models for the reference sequence) you can use full atom RMSD:

    [mm] evox$ git:(master) ✗ rna_calc_rmsd.py -t ..//*ref.pdb reps_ns/*.pdb
    method: all-atom-built-in
    # of models: 4
    c1_tar_min.out.1.pdb 6.34 1295
    c3_tar_min.out.66.pdb 11.6 1295
    c4_tar_min.out.98.pdb 15.1 1295
    c5_tar_min.out.25.pdb 14.34 1295
    # of atoms used: 1295
    csv was created!  rmsds.csv

For `reps`
