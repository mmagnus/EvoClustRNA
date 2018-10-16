#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A mother script to run evox.py.

Improvements:
- ln for structures, not copying any more!

"""
from __future__ import print_function

import argparse
import os
import glob
import sys


def get_parser():
    """parser"""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-d', "--dryrun",
                        action="store_true", help="dry run", default=False)

    parser.add_argument('-p', '--path', help="", default='')
    parser.add_argument('-a', '--args', help=' -e -p or -a (see evox.py for more)', default=" -p -a ") # -a -p -e
    parser.add_argument('-c', '--case', help="only one case, for test")
    parser.add_argument('-t', '--test', help="short testing run, without -c it will go over all folders", action="store_true")
    parser.add_argument("-v", "--verbose",
                        action="store_true", help="be verbose")

    return parser

def exe(cmd, dryrun):
    """exe"""
    print(cmd)
    if not dryrun: os.system(cmd)


def main(dryrun, path, case, test, args):
    """

    """
    if path:
        os.chdir(path)
    root = os.getcwd()
    cases = glob.glob('*')

    for c in cases:
        if c.startswith('_'):
            continue
        # print('Case: ', c)
        # mode only for a specific case
        if case: # only if this is used
            if c != case:
                print('!!! skip ' + c + '!!!')
                continue

        # if not break ed, use this
        if os.path.isdir(c):
            print ('[%s]' % c)
            os.chdir(c) # go inside a folder
            ## # cmd
            ## #subcases = glob.glob('*.fa')
            ## #for sc in subcases:
            ## for i in [1000]: #
            if not test:
                args = ' -a -p '  # only if you want to get rmsd-all-structs
                modes = {
                    #'simrna5x10rosetta5x10' : 'evox.py -s 10 -f 10 -e -p ade',
                    #     'simrna5x50rosetta5x50' : 'evox.py -s 50 -f 50 -e -p ade',
                    # 1k # farna5x100  simrna5x100 done
                    # 'simrna5x10' : 'evox.py -s 10 -e -p ' + c,

                    ######## this is all required #######################################
                    #'farna1000' : 'evox.py -f 1000 --target-only ' + args + c,
                    #'simrna1000' : 'evox.py -s 1000 --target-only ' + args + c,
                    #'simrna1x500farna1x500' : 'evox.py -s 500 -f 500 --target-only ' + args + c,
                    #'simrna5x100farna5x100' : 'evox.py -s 100 -f 100 ' + args + c,
                    #'simrna5x200' : 'evox.py -s 200 ' + args + c,
                    #'farna5x200' : 'evox.py -f 200  ' + args + c,
                    ############ end #####################################################

                    #'simrna5x200farna5x200' : 'evox.py -s 200 -f 200 -e -p ' + c,
                    #'simrna5x400rosetta5x400' : 'evox.py -s 400 -f 400 -e -p ade',
                    #'simrna5x500rosetta5x500' : 'evox.py -s 500 -f 500 -e -p ade',
                    }
            else:
                args = ' -a '
                modes = {
                    'test' : 'evox.py -s 10 -f 10 -p -e -t ' + args + c, # for testing
                    #'farna1000' : 'evox.py -f 1000 --target-only ' + args + c,
                    #'farna10' : 'evox.py -f 10 --target-only ' + args + c,
                 }

            case_root = os.getcwd()
            for m in modes:
                md = 'evox/' + m
                try:
                    os.mkdir(md)
                except OSError:
                    os.system('trash ' + md)  # remove folder
                    os.mkdir(md)
                # go inside
                os.chdir(md)
                print(' %s in %s' % (modes[m], md))
                exe(modes[m], False)
                os.chdir(case_root)
                #simrna5x100farna5x100
                #evox.py  -p thf

                ##     exe('rm *min.out.*.pdb', dryrun)
                ##     exe('mkdir %s_top%i' % (c, i), dryrun)
                ##     exe('extract_lowscore_decoys.py *min.out %i' % (i), dryrun)
                ##     exe('mv -v *min.out.*.pdb %s_top%i' % (c, i), dryrun)
            os.chdir(root)
            # sys.exit(1)  # after ade

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    #os.system('mdimport /home/magnus/work')
    #os.system('mdimport /home/magnus/')
    main(args.dryrun, args.path, args.case, args.test, args.args)
