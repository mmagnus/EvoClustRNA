#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
from __future__ import print_function
import os
import argparse


def get_parser():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-g', '--get-models', help="", action="store_true")
    parser.add_argument('-e', '--evoclust', action="store_true")
    parser.add_argument('-p', '--process', action="store_true")
    parser.add_argument('-f', '--farna', help="", default="")
    parser.add_argument('-s', '--simrna', help="", default="")
    parser.add_argument("-v", "--verbose",
                        action="store_true", help="be verbose")
    parser.add_argument('case')
    return parser


def exe(cmd, dryrun=False):
    print(cmd)
    if not dryrun: os.system(cmd)

def get_farna(hs, n, case):
    """
    n = topX, e.g. top10
    """
    for h in hs:
        # cmd = "scp malibu:/home/magnus/rna-evo-malibu/ade/" + h + "/" + h + "_top" + n + "/* structures/"
        # /home/magnus/rna-evo-malibu/ade/a04pk
        try: os.mkdir("/home/magnus/work/rosetta-archive/" + case + "/")
        except OSError: pass

        # ok, download trajectories files
        local_out_fn = "/home/magnus/work/rosetta-archive/" + case + "/" +  h + "_min.out"
        if not os.path.isfile(local_out_fn):
            cmd = "scp malibu:/home/magnus/rna-evo-malibu/ade/" + h + "/" + h + "_min.out " + \
              local_out_fn
            exe(cmd)
        else:
            print('Exists ' + local_out_fn + ' [ok]')

        # extract!
        dryrun = False
        # exe('mkdir %s_top%i' % (h, int(n)), dryrun)
        exe('extract_lowscore_decoys.py ' + local_out_fn + ' %i' % (int(n)), dryrun)
        # exe('mv -v *min.out.*.pdb %s_top%i' % (h, int(n)), dryrun)
        exe('mv -v *min.out.*.pdb structures', dryrun)

def get_simrna(hs, n):
    """n=10
    trash structures
    mkdir structures

    mkdir ade_pk
    cd ade_pk
    rna_simrnaweb_download_job.py -c ade_pk-35b2a2c1 -n $n

    """
    root = os.getcwd()
    for h in hs.keys():
        try: os.mkdir(h)
        except OSError: pass
        os.chdir(h)
        job_id = hs[h]  # '{'ade_pk-35b2a2c1'
        exe("rna_simrnaweb_download_job.py -c " + job_id + " -n " + n)
        exe("cd _" + job_id + "_ALL_top" + n + "/ && rename 's/%s/%s_%s/' * " % (hs[h], h, hs[h]))
        exe("cp -v _" + job_id + "_ALL_top" + n + "/* ../structures")
        os.chdir(root)


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    # rna_simrnaweb_download_job.py -n 1000 -c ade_pk-35b2a2c1
    # mv _XXX -> structures
    if args.farna:
        # this is for rosetta
        # this is not ideal, but it works ;-)
        try:
            os.mkdir('structures')
        except OSError: pass

        if args.case == 'ade':
            hs = ['a04pk', 'a99pk', 'adepk', 'b28pk', 'u51pk'] # options for this I can have!
            get_farna(hs, args.farna, args.case)

    if args.simrna:
        try:
            os.mkdir('structures')
        except OSError: pass

        if args.case == 'ade':

            hs = {'ade_pk': 'ade_pk-35b2a2c1',
                  'a04': '9c6339e0-591c-498d-9745-1a828f9ee81d',
                  'a99': '2e496700-b989-4044-883d-d34257b022ab',
                  'u51': 'e614e4a0-0898-45f2-9964-52db07279965',
                  'b28': '7bc1d432-eac8-47cf-a42e-aa3c89efc721'}
            get_simrna(hs, args.simrna)

    if args.evoclust:
        exe("evoClustRNA.py -a ../../ade_plus_ade_cleanup.sto -i structures -m ../../mapping_pk.txt -f")
        exe("evoClust_autoclustix.py ade_plus_ade_cleanup_mapping_pkX.txt")

    if args.process:
        exe("evoClust_get_models.py -i structures/ ade_plus_ade_cleanup_mapping_pkX_*.out")
        exe("evoClust_get_models.py -i structures/ ade_plus_ade_cleanup_mapping_pkX_*.out -n 'ade'")

        exe("evoClust_calc_rmsd.py -a ../../ade_plus_ade_cleanup.sto -t ../../reference*.pdb -n ade -m ../../mapping_pk.txt reps/*.pdb -o rmsd_motif.csv")

        exe("rna_pdb_toolsx.py --inplace --get_rnapuzzle_ready reps_ns/*.pdb")
        exe("rna_calc_inf.py -f -t ../../reference*.pdb reps_ns/*.pdb")
        exe("rna_calc_rmsd.py -t ../../reference*.pdb reps_ns/*.pdb")
