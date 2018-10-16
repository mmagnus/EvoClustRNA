#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import argparse
import shutil

#FARNA_ARCHIVE = '/Users/magnus/work/rosetta-archive/'
ROSETTA_ARCHIVE = "/home/magnus/work/rosetta-archive/"
TRASH = False # trash everything in ade/evox/<mode>


def get_parser():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-g', '--get-models', help="", action="store_true")
    parser.add_argument('-e', '--evoclust', action="store_true")
    parser.add_argument('-p', '--process', action="store_true")
    parser.add_argument('--target-only', action="store_true")
    parser.add_argument('-a', '--rmsd-all-structs', help="must be combined with -p",
                        action="store_true")
    parser.add_argument('-f', '--farna', help="", default="")
    parser.add_argument('-s', '--simrna', help="", default="")
    parser.add_argument('-t', '--add-solution', help="", default="")
    parser.add_argument("-v", "--verbose",
                        action="store_true", help="be verbose")
    parser.add_argument('case')
    return parser


def exe(cmd, dryrun=False):
    print(cmd)
    if not dryrun: os.system(cmd)

def get_farna(hs, n, case):
    """
    Collects the data based on these lists:
    hs = ['a04pk', 'a99pk', 'adepk', 'b28pk', 'u51pk']
    n = topX, e.g. top10
    """
    for h in hs:
        # cmd = "scp malibu:/home/magnus/rna-evo-malibu/ade/" + h + "/" + h + "_top" + n + "/* structures/"
        # /home/magnus/rna-evo-malibu/ade/a04pk
        try: os.mkdir(ROSETTA_ARCHIVE + case)
        except OSError: pass

        # ok, download trajectories files
        local_out_fn = ROSETTA_ARCHIVE + case + "/" + h + "_min.out"
        if not os.path.isfile(local_out_fn):
            cmd = "scp malibu:/home/magnus/rna-evo-malibu/" + case + "/" + h + "/" + h + "_min.out " + \
              local_out_fn
            exe(cmd)
        else:
            print('Exists ' + local_out_fn + ' [ok]')

        for i in range(1, int(n) + 1):
            # /Users/magnus/work/rosetta-archive/trna/trna_min.out.99.pdb
            pdb_fn = h + '_min.out.' + str(i) + '.pdb'
            lnfn = 'ln -s ' + ROSETTA_ARCHIVE + case + '/' + pdb_fn + ' ' + \
                            'structures/' + pdb_fn
            print(lnfn)
            exe(lnfn)

        # extract!
        dryrun = False
        # is this the code to get models for rp14?
        # off at the moment
        #if False:
        #    exe('mkdir %s_top%i' % (h, int(n)), dryrun)
        #    exe('extract_lowscore_decoys.py ' + local_out_fn + ' %i' % (int(n)), dryrun)
        #    exe('mv -v *min.out.*.pdb %s_top%i' % (h, int(n)), dryrun)
        #    exe('mv -v *min.out.*.pdb structures', dryrun)


def get_simrna(hs, n):
    """n=10
    trash structures
    mkdir structures

    mkdir ade_pk
    cd ade_pk
    rna_simrnaweb_download_job.py -c ade_pk-35b2a2c1 -n $n

    """
    SIMRNA_ARCHIVE = "/home/magnus//work/simrnaweb-archive/"
    root = os.getcwd()
    for h in hs.keys():
        job_id = hs[h]  # '{'ade_pk-35b2a2c1'
        print(job_id)
        # ~/work/simrnaweb-archive/_e614e4a0-0898-45f2-9964-52db07279965_ALL/
        #    e614e4a0-0898-45f2-9964-52db07279965_ALL-000001_AA.pdb
        for i in range(1, int(n) + 1):
            lnfn = 'ln -s ' + SIMRNA_ARCHIVE + '_' + job_id + '_ALL_top1000/' + \
              job_id + '_ALL_top1000-' + str(i).zfill(6) + '_AA.pdb ' + \
              'structures/' + h + '_' + job_id + '_ALL-' + str(i).zfill(6)+ '_AA.pdb'
            print(lnfn)
            exe(lnfn)

        # old test
        # exe("rna_simrnaweb_download_job.py --web-models -c " + job_id + " -n " + n)
        ## exe("cd _" + job_id + "_ALL_top" + n + "/ && rename 's/%s/%s_%s/' * " % (hs[h], h, hs[h]))
        ## exe("cp -v _" + job_id + "_ALL_top" + n + "/* ../structures")
        # os.chdir(root)
        #sys.exit()

# main
if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    # rna_simrnaweb_download_job.py -n 1000 -c ade_pk-35b2a2c1
    # mv _XXX -> structures
    if args.farna or args.simrna:
        if TRASH:
            os.system('trash *')
        try:
            os.mkdir('structures')
        except OSError:
            shutil.rmtree('structures')
            os.mkdir('structures')

    if args.farna:
        # this is for rosetta
        # this is not ideal, but it works ;-)
        if args.case == 'ade' and args.target_only:
            hs = ['adepk']
        elif args.case == 'ade':
            hs = ['a04pk', 'a99pk', 'adepk', 'b28pk', 'u51pk'] # options for this I can have!

        if args.case == 'tpp' and args.target_only:
            hs = ['tpp']
        elif args.case == 'tpp':
            hs = 'tae  tal  tb2  tc5  tpp'.split()

        if args.case == 'gmp' and args.target_only:
            hs = ['gmp']
        elif args.case == 'gmp':
            hs = 'gapP  gbaP  gbx  gmp  gxx'.split()

        if args.case == 'thf' and args.target_only:
            hs = ['thf']
        elif args.case == 'thf':
            hs = 'hak  haqpk  hcppk  tha  thf'.split()

        if args.case == 'trna' and args.target_only:
            hs = ['trna']
        elif args.case == 'trna':
            hs = 'tab  taf  tm2  tm5  trna'.split()

        if args.case == 'rp17' and args.target_only:
            hs = ['rp17']
        elif args.case == 'rp17':
            hs = 'rp17   rp17hcf     rp17pistol  rp17s221    rp17s223'.split()

        if args.case == 'rp06' and args.target_only:
            hs = ['rp06']
        elif args.case == 'rp06':
            hs = 'rp06 rp06af193 rp06bx571'.split()

        if args.case == 'rp13' and args.target_only:
            hs = ['rp13']
        elif args.case == 'rp13':
            hs = 'rp13 rp13cp0016 rp13nc3295 rp13nc9445 rp13nzaaox'.split()
            # tutaj ten kod mozesz sobie uzyc jakbym kiedys chcial pracowac na modelach
            # pochodzacych z modelowania z więzami
            # hs = 'rp13cp0016cst nc3295cst rp13nc9445cst nzaaoxcst rp13prs_cst'.split()
            #hs = ''.split() # '

        if args.case == 'rp14' and args.target_only:
            hs = ['rp14']
        elif args.case == 'rp14':
            hs = 'rp14 rp14_aj63 rp14_aacy23'.split()

        get_farna(hs, args.farna, args.case)

    if args.simrna:

        if args.case == 'ade' and args.target_only:
            hs = {'ade_pk': 'ade_pk-35b2a2c1'}
        elif args.case == 'ade':
            hs = {'ade_pk': 'ade_pk-35b2a2c1',
                  'a04': '9c6339e0-591c-498d-9745-1a828f9ee81d',
                  'a99': '2e496700-b989-4044-883d-d34257b022ab',
                  'u51': 'e614e4a0-0898-45f2-9964-52db07279965',
                  'b28': '7bc1d432-eac8-47cf-a42e-aa3c89efc721'}

        if args.case == 'tpp' and args.target_only:
            hs = {'tpp': '16662ebf-cf31-42d1-98a3-2aae31f28087'}
        elif args.case == 'tpp':
            hs = {'tpp': '16662ebf-cf31-42d1-98a3-2aae31f28087',
                  'tc5': 'aed2c40b-bb70-44a7-846d-b133359fc6bd',
                  'tb2': '0abbb76e-9cda-482f-abb2-94557e91acd8',
                  'tae': '6bff10d7-d4ec-43ce-8f79-8f538fa1ae65',
                  'tal': 'd2609d4d-bd6f-49fd-acbe-0ab278e0166b'}

        if args.case == 'trna' and args.target_only:
            hs = {'trna': 'a9bc516d-e3da-489d-93ef-5eb20e3f13c3'}
        elif args.case == 'trna':
            hs = {'trna': 'a9bc516d-e3da-489d-93ef-5eb20e3f13c3',
                  'taf': '822df074-320e-4166-9fd1-8fbcf085908a',
                  'tm5': '613bcfcf-f513-4945-9cf4-6df7db04545e',
                  'tab': 'cf61bea5-88c4-4e82-8042-dc04ce5cadcf',
                  'tm2': '8ca21d4d-7ceb-4736-9619-7c1814c75637'
                      }

        if args.case == 'gmp' and  args.target_only:
            hs = {'gmp': 'faa97ed7'}
        elif args.case == 'gmp':
            hs = {'gmp': 'faa97ed7',
                      'gapP' : 'd9d225c5',
                      'gbx' : '00de79c8',
                      'gbaP' : 'd2b57aef',
                      'gxx' : '6bd26658' }

        if args.case == 'thf' and  args.target_only:
            hs = {'thf' : '7f0f8826'}
        elif args.case == 'thf':
            hs = {'thf' : '7f0f8826',
                  'tha' : '5f8916a8',
                  'hak' : 'cb6e7e4d',
                  'haq' : '497811c4',
                  'hcp' : 'hcp-pk-374cbbb1',
                  }

        if args.case == 'rp17' and  args.target_only:
            hs = {'rp17' : '948f56bb-ea7a-4619-9945-2fbfd6902c24'}
        elif args.case == 'rp17':
            hs = {'rp17' : '27b5093d',
                  'rp17hcfc' : '6d8062dd',
                  'rp17s223c' : '36828e10',
                  'rp17s221c' : '742b47e6',
                  'rp17pistol' : '336e0098'
                  }

        if args.case == 'rp13' and  args.target_only:
            hs = {'rp13' : '20569fa1'}
        elif args.case == 'rp13':
            hs = {'rp13' : '20569fa1',
                  'zcp' : '6537608a',
                  'znc' : 'a1ea6711',
                  'zbaa' : '684ef8ce',
                  'zaa'  : '6a68812b'
                  }

        if args.case == 'rp14' and  args.target_only:
            hs = {'rp14' : 'rp14+m+pk2-946da607'}
        elif args.case == 'rp14':
            hs = {
                'rp14' : 'rp14+m+pk2-946da607',
                'r14aj63' : 'r14aj63pk-2f5f0e3d',
                'r14aacy23' : 'r14aacy23+m+pk2-84f4be23',
                 }

        if args.case == 'rp06' and  args.target_only:
            hs = {'rp06' : '9d39f986'}
        elif args.case == 'rp06':
            hs = {'rp06' : '9d39f986',
                  'bx571' : '01621888',
                  'cp771' : 'cf8f8bb2',
                  'af193' : '545c05f8',
                  'am40'  : '9c6345c3'
                  }

        get_simrna(hs, args.simrna)

    # -t', '--add-solution'
    #exe('cp -v ../../*ref.pdb
    # -e', '--evoclust'
    if args.evoclust:
        # exe("evoClustRNA.py -a ../../ade_plus_ade_cleanup.sto -i structures -m ../../mapping_pk.txt -f")  # ade
        exe("evoClustRNA.py -a ../../" + args.case + "*ref.sto -i structures -m ../../*mapping*ref.txt -f")  # tpp<bleble>.sto
        exe("evoClust_autoclustix.py *mapping*X.txt")

    # '-a', '--rmsd-all-structs'
    if args.rmsd_all_structs:
         exe("evoClust_calc_rmsd.py -a ../../" + args.case + "*ref.sto -t ../../*ref.pdb -o rmsd_all_strucs.csv -n " + args.case + " -m ../../*mapping*ref.txt  structures/*.pdb")

    # '-p', '--process'
    if args.process:
        exe("evoClust_get_models.py -i structures/ *.out")
        exe("evoClust_get_models.py -i structures/ *.out -n '" + args.case + "_'")  # rp13_

        # pre-process structures to be compatible with the native
        if args.case == 'rp13': exe("cd reps_ns && rna_pdb_toolsx.py --delete 'A:46-56' --inplace *")
        if args.case == 'ade': exe("cd reps_ns && rna_pdb_toolsx.py --delete 'A:72' --inplace *")
        if args.case == 'tpp': exe("cd reps_ns && rna_pdb_toolsx.py --delete 'A:80' --inplace *")

        exe("evoClust_calc_rmsd.py -a ../../" + args.case + "*ref.sto -t ../../*ref.pdb -n " + args.case + " -m ../../*mapping*ref.txt -o rmsd_motif.csv reps/*.pdb")

        exe("rna_pdb_toolsx.py --inplace --get_rnapuzzle_ready reps_ns/*.pdb")
        if args.case == 'trna':
            exe("rna_calc_rmsd.py -m align -t ../../*ref.pdb reps_ns/*.pdb")
        else:
            exe("rna_calc_rmsd.py -t ../../*ref.pdb reps_ns/*.pdb")
        exe("rna_calc_inf.py -f -t ../../*ref.pdb reps_ns/*.pdb")
