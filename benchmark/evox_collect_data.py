#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
example:

     [mm] evo$ ./evox_collect_data.py -p ade

"""
from __future__ import print_function

import argparse
import os
import glob
import pandas


def get_parser():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-d', "--dryrun",
                        action="store_true", help="dry run", default=False)

    #parser.add_argument('-p', '--path', help="", default='')
    parser.add_argument('paths', nargs='*', help="", default='')
    parser.add_argument('-c', '--case', help="only one case, for test")
    parser.add_argument("-v", "--verbose",
                        action="store_true", help="be verbose")

    return parser

def exe(cmd, dryrun):
    print(cmd)
    if not dryrun: os.system(cmd)

def main(dryrun, paths, case):
    root = os.getcwd()
    print(paths)
    for path in paths:
        print(path)
        if path in ['ade', 'gmp', 'rp06', 'rp13', 'rp14', 'rp17', 'thf', 'tpp', 'trna']:
            pass
        else:
            continue
        if path:
            os.chdir(path + '/evox/') # jump inside evox
        cases = glob.glob('*')
        # ade / evox / <type>
        rmsd_motif = None
        rmsds = None
        infs = None

        rmsd_motif = pandas.DataFrame()

        for c in cases: # simulation!
            # mode only for a specific case
            if case: # only if this is used
                if c != case:
                    print('!!! skip ' + c + '!!!')
                    continue

            if os.path.isdir(c):
                print('------------------------------')
                print ('  inside %s' % c)
                os.chdir(c) # go inside a folder
                print(os.getcwd())
                 # add column pdb case
                # collect motif rmsd
                fn = 'RMSD_motif.csv'
                print(fn)
                try:
                    df = pandas.read_csv(fn, index_col=None)
                except:
                    ## placeholder_fn = "/home/magnus/work/evo/rmsd_motif_fake.csv"
                    ## print('Insert placeholder')
                    ## df = pandas.read_csv(placeholder_fn, index_col=None)
                    os.chdir(root + '/' + path + '/evox/')
                    continue # skip

                df['pdb'] = path
                df['group_name'] = c

                print('fn', fn)
                print('df', df)

                rmsd_motif = rmsd_motif.append(df)
                print(rmsd_motif)

                ## try:
                ##     rmsd_motif.append(df)  # append to the df
                ##     print(rmsd_motif)
                ## except AttributeError:
                ##     rmsd_motif = df

                ## # add column pdb case
                ## # collect motif rmsd
                ## df = pandas.read_csv('rmsds.csv')
                ## df['group_name'] = case
                ## df['pdb'] = path
                ## if not rmsds:
                ##     rmsds = df
                ## else:
                ##     rmsds.append(df)  # append to the df

                ## # add column pdb case
                ## # collect motif rmsd
                ## df = pandas.read_csv('inf.csv')
                ## df['group_name'] = case
                ## df['pdb'] = path
                ## if not infs:
                ##     infs = df
                ## else:
                ##     infs.append(df)  # append to the df

                os.chdir(root + '/' + path + '/evox/') # root + '/' + case) # path + '/evox/')  # root)

        print(rmsd_motif)
        #print(rmsds)
        #print(infs)

        os.chdir(root)
        rmsd_motif.to_csv(path + '_rmsd_motf.csv', index=False)
        #rmsds.to_csv('rmsds.csv', index=False)
        #infs.to_csv('infs.csv', index=False)

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    main(args.dryrun, args.paths, args.case)
