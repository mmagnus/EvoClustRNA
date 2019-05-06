#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
[mm] rnas_half$ git:(master) ✗ python ../evoxv.py rp14 --replace --copy --run

  --copy create a structure of folders for this analysis
  --replace
  --run so for each mode run it evoxx.py --half -c

Hmm... but I don't need to re-run everything.

This is important:

gmp:tar
gmp:solution
AE000513.1/1919839-1919923:gxx
BA000004.3/387918-388001:gba
ABFD02000011.1/154500-154585:gbx
AE015927.1/474745-474827:gap

for trna, quick hack: mapping_ref.txt -> mapping_pk_ref.txt
"""
from __future__ import print_function

import argparse
import os
import shutil
import itertools


def get_parser():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-v", "--verbose", action="store_true", help="be verbose")
    parser.add_argument("--debug", action="store_true", help="be verbose for debugging")
    parser.add_argument("--copy", action="store_true", help="init (copy) folders for new runs")
    parser.add_argument("--replace", action="store_true", help="replace old mapping files")
    parser.add_argument("--run", action="store_true", help="run cmd")
    parser.add_argument('rna', help="", default="")
    return parser


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    # for i homolog
    rna = args.rna # shortcut
    d = args.debug
    cmd = 'evoxx.py --nvariant --half -c '
    for x in range(1,5):
        # copy folder to this
        # open a file
        newrun = args.rna + '_aln1_h' + str(x)
        print(newrun)

        if args.copy:
            os.system("rsync -rav --exclude 'out' " + rna + "/ " + newrun)

        homologs = open(args.rna + os.sep + 'mapping_pk_ref.txt').readlines()
        print(homologs)
        new_mapping = args.rna + ':solution\n' + \
                     args.rna + ':tar\n' + \
                     homologs[x + 1].strip()
        print(new_mapping)

        # open mapping file and write replace it with new mapping
        with open(newrun + os.sep + 'mapping_pk_ref.txt', 'w') as f:
            f.write(new_mapping)

        cmdfull = 'time ' + cmd + newrun
        print(cmdfull)
        if args.run:
            os.system(cmdfull)

    # for 2 homologs
    from itertools import product, combinations
    for comb in combinations([1, 2, 3, 4], 2):
        print(comb)
        a, b = comb
        newrun = args.rna + '_aln1_h' + str(a) + str(b)
        print(newrun)

        if args.copy:
            os.system("rsync -rav --exclude 'out' " + rna + "/ " + newrun)
            # shutil.copytree(args.rna, newrun)

        if args.replace:
            homologs = open(args.rna + os.sep + 'mapping_pk_ref.txt').readlines()
            print(homologs)
            new_mapping = args.rna + ':solution\n' + \
                         args.rna + ':tar\n' + \
                         homologs[a + 1] + \
                         homologs[b + 1].strip()
            print(new_mapping)

            # open mapping file and write replace it with new mapping
            with open(newrun + os.sep + 'mapping_pk_ref.txt', 'w') as f:
                f.write(new_mapping)

        cmdfull = 'time ' + cmd + newrun
        print(cmdfull)
        if args.run:
            os.system(cmdfull)


    from itertools import product, combinations
    for comb in combinations([1, 2, 3, 4], 3):
        print(comb)
        a, b, c = comb
        newrun = args.rna + '_aln1_h' + str(a) + str(b) + str(c)
        print(newrun)

        if args.copy:
            os.system("rsync -rav --exclude 'out' " + rna + "/ " + newrun)

        if args.replace:
            homologs = open(args.rna + os.sep + 'mapping_pk_ref.txt').readlines()
            print(homologs)
            new_mapping = args.rna + ':solution\n' + \
                         args.rna + ':tar\n' + \
                         homologs[a + 1] + \
                         homologs[b + 1] + \
                         homologs[c + 1].strip()

            print(new_mapping)

            # open mapping file and write replace it with new mapping
            with open(newrun + os.sep + 'mapping_pk_ref.txt', 'w') as f:
                f.write(new_mapping)

        cmdfull = 'time ' + cmd + newrun
        print(cmdfull)
        if args.run:
            os.system(cmdfull)
