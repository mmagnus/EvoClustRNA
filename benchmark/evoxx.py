#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A mother script to run evox.py.

If no --case selected, it will be executed on all folder in the current directory or defined by --path.

Improvements:
- ln for structures, not copying any more!

"""
from __future__ import print_function

import argparse
import os
import glob
import sys
import time

def get_parser():
    """parser"""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-d', "--dryrun",
                        action="store_true", help="dry run", default=False)

    parser.add_argument('-p', '--path', help="", default='')
    parser.add_argument('-c', '--case', help="only one case, for test")
    parser.add_argument('--dont-copy-models', help="", action="store_true")
    parser.add_argument('--one-mode', help="Run the script for one mode only", action="store_true")
    parser.add_argument('--naln', help="New alignment, so run all modes, otherwise run only modes including diff homologs", action="store_true", default=False)
    parser.add_argument('--nvariant', help="new variant mode of homologs, so don't re-run top1000 and so on", action="store_true", default=False)

    parser.add_argument('--args', help="arguments for evox")
    parser.add_argument('--half', help="half mode, run autoclustering with half, dont get models, and do evoclust, it has to be there",
                        action="store_true")
    #parser.add_argument('-a', '--args', help=' -e -p or -a (see evox.py for more)', default=" -p -a ") # -a -p -e
    parser.add_argument('-t', '--test', help="short testing run, without -c it will go over all folders", action="store_true")
    parser.add_argument("-v", "--verbose",
                        action="store_true", help="be verbose")

    return parser

def exe(cmd, dryrun):
    """exe"""
    print(cmd)
    if not dryrun: os.system(cmd)


def main(dryrun, path, case, test, dont_copy_models, args, one_mode, half, naln, nvariant):
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
                # print('!!! skip ' + c + '!!!')
                continue

        # if not break ed, use this
        if os.path.isdir(c):
            print ('\_ inside folder: %s' % c)
            time.sleep(2)
            os.chdir(c) # go inside a folder
            ## # cmd
            ## #subcases = glob.glob('*.fa')
            ## #for sc in subcases:
            ## for i in [1000]: #
            if one_mode:
                args = ' --get-models -e -p --add-solution -m -g --half '
                #modes = {'simrna5x100farna5x100' : 'evox.py %s %s ' % (args, c),}
                modes = {'farna5x100' : 'evox.py %s %s ' % (args, c),}
            elif not test:
                args = ' -a -e -p -t -m -g  '
                #args = ' --process ' # process only
                #args = '-a -e -p -t -m -g '  # only if you want to get rmsd-all-structs
                # -m save motifs
                if half:
                    #args = " -e -p --autoclusthalf -t -c "
                    args = " --clean --evoclust --process --autoclusthalf --rmsd-all-structs --add-solution --calc-stats "
                    # keep this on only if you want to calc rmsds and infs
                    # args = " --calc-stats " # only calc
                    if nvariant:
                        print(" \_ new variant mode")
                        modes = {
                         'simrna5x100farna5x100' : 'evox.py %s %s ' % (args, c),
                         'simrna5x200' : 'evox.py %s %s ' % (args, c),
                         'farna5x100' : 'evox.py %s %s ' % (args, c), # x
                         'farna5x200' : 'evox.py %s %s ' % (args, c), # x
                         'simrna5x100' : 'evox.py %s %s ' % (args, c), # x

                         # with getting models
                         ## 'simrna5x100' : 'evox.py -s 100 -e %s %s ' % (args, c), # x
                        }

                    if naln:
                        print(" \_ new alingmnet mode [naln]")
                        modes = {
                        # these are not processed ;-)
                          'simrnatop1' : 'evox.py --calc-stats ' + c,
                          'simrnatop3' : 'evox.py --calc-stats ' + c,
                          'farnatop1' : 'evox.py --calc-stats ' + c,
                          'farnatop3' : 'evox.py --calc-stats ' + c,

                          'farna1000' : 'evox.py --target-only %s %s' % (args, c),
                          'simrna1000' : 'evox.py --target-only %s %s' % (args, c),

                         'simrna1x500farna1x500' : 'evox.py %s %s' % (args, c),
                         'simrna5x100farna5x100' : 'evox.py %s %s ' % (args, c),

                         'simrna5x200' : 'evox.py %s %s ' % (args, c),
                         'farna5x100' : 'evox.py %s %s ' % (args, c), # x
                         'farna5x200' : 'evox.py %s %s ' % (args, c), # x
                         'simrna5x100' : 'evox.py %s %s ' % (args, c), # x

                         # with getting models
                         ## 'simrna5x100' : 'evox.py -s 100 -e %s %s ' % (args, c), # x
                        }
                    else:  # this is by default ;-)
                        print(" \_ previous aln mode [no naln]")
                        modes = {
                         'simrna1x500farna1x500' : 'evox.py %s %s' % (args, c),
                         'simrna5x100farna5x100' : 'evox.py %s %s ' % (args, c),

                         'simrna5x200' : 'evox.py %s %s ' % (args, c),
                         'farna5x100' : 'evox.py %s %s ' % (args, c), # x
                         'farna5x200' : 'evox.py %s %s ' % (args, c), # x
                         'simrna5x100' : 'evox.py %s %s ' % (args, c), # x
                        }

                elif dont_copy_models:
                        modes = {
                            # required
                            'farna1000' : 'evox.py --target-only %s %s' % (args, c),
                            'simrna1000' : 'evox.py --target-only %s %s' % (args, c),
                            'simrna1x500farna1x500' : 'evox.py --target-only %s %s' % (args, c),
                            'simrna5x100farna5x100' : 'evox.py %s %s ' % (args, c),
                            'simrna5x200' : 'evox.py %s %s ' % (args, c),
                            'farna5x200' : 'evox.py %s %s ' % (args, c),
                            #'test' : 'evox.py --inf-all --target-only ' + args + c,
                            'farna1000' : 'evox.py  --target-only ' + args + c,
                            'simrna1000' : 'evox.py --target-only ' + args + c,
                            }
                        #'simrna1000' : 'evox.py -p ' + args + c,
                        #'simrna1x500farna1x500' : 'evox.py -p ' + args + c,
                        #'simrna5x100farna5x100' : 'evox.py -p ' + args + c,
                        #'simrna5x200' : 'evox.py -p  ' + args + c,
                        #'farna5x200' : 'evox.py -p  ' + args + c,
                else:
                    args = " --calc-stats " # only calc
                    modes = {
                        #'simrna5x10rosetta5x10' : 'evox.py -s 10 -f 10 -e -p ade',
                        #     'simrna5x50rosetta5x50' : 'evox.py -s 50 -f 50 -e -p ade',
                        # 1k # farna5x100  simrna5x100 done
                        # 'simrna5x10' : 'evox.py -s 10 -e -p ' + c,

                        ######## this is all required #######################################
                        'simrnatop1' : 'evox.py --calc-stats ' + c,
                        'simrnatop3' : 'evox.py --calc-stats ' + c,
                        'farnatop1' : 'evox.py --calc-stats ' + c,
                        'farnatop3' : 'evox.py --calc-stats ' + c,

                        # 'farnatop5' : 'evox.py --calc-stats ' + c,
                        # this is only for some calculactions

                        ## 'farna1000' : 'evox.py ' + args + ' ' + c,
                        ## 'simrna1000' : 'evox.py ' + args + ' ' + c,
                        ## 'simrna1x500farna1x500' : 'evox.py  ' + args + ' ' + c,
                        ## 'simrna5x100farna5x100' : 'evox.py ' + args + ' ' + c,
                        ## 'simrna5x200' : 'evox.py  ' + args + ' ' + c,
                        ## 'farna5x200' : 'evox.py  ' + args + ' ' + c,

                        # this is for full run
                        ## 'farna1000' : 'evox.py -f 1000 --target-only ' + args + ' ' + c,
                        ## 'simrna1000' : 'evox.py -s 1000 --target-only ' + args + ' ' + c,
                        ## 'simrna1x500farna1x500' : 'evox.py -s 500 -f 500 --target-only ' + args + ' ' + c,
                        ## 'simrna5x100farna5x100' : 'evox.py -s 100 -f 100 ' + args + ' ' + c,
                        ## 'simrna5x200' : 'evox.py -s 200  ' + args + ' ' + c,
                        ##  'farna5x200' : 'evox.py -f 200  ' + args + ' ' + c,
                        ## ############ end #####################################################
                        #'simrna5x10farna5x10' : 'evox.py -s 10 -f 10 -t ' + args + c,

                        #'simrna5x200farna5x200' : 'evox.py -s 200 -f 200 -e -p ' + c,
                        #'simrna5x400rosetta5x400' : 'evox.py -s 400 -f 400 -e -p ade',
                        #'simrna5x500rosetta5x500' : 'evox.py -s 500 -f 500 -e -p ade',
                        }
            else:
                args = ' -a -e -p -t -m -g  '
                n = 10
                modes = {
                    #'test' : 'evox.py -s 10 -f 10 -p -e -t ' + args + c, # for testing
                    'test' : 'evox.py -s ' + str(n) + ' -f ' + str(n) + ' ' + args + c, # for testing
                    #'farna1000' : 'evox.py -f 1000 --target-only ' + args + c,
                    #'farna10' : 'evox.py -f 10 --target-only ' + args + c,
                 }

            case_root = os.getcwd()

            for m in modes:
                print (m.rjust(23), modes[m].rjust(100))
            print('wating...')
            time.sleep(5)

            for m in modes:
                md = 'evox/' + m
                try:
                    os.mkdir(md)
                except OSError:
                    #os.system('trash ' + md)  # remove folder
                    #os.mkdir(md)
                    pass
                # go inside
                print (' \_ inside folder: %s' % md)
                time.sleep(2)
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
    main(args.dryrun, args.path, args.case, args.test, args.dont_copy_models, args.args, args.one_mode, args.half, args.naln, args.nvariant)
    print(args)
