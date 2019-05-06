#!/usr/bin/env python

"""

Size of the biggest cluster to quit, default 83 = 1/6 * 500, 300*1/6=50

rp17_rmGaps_ref_mapping_pk_refX_n1c39_cf3.50.out

"""
from __future__ import print_function

import os
import argparse
import subprocess
import sys
import re

LIMIT = 40

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('matrix',
                        help="A txt file with a similarity matrix with column headers, \
See test_data/matrix.txt for more . ! .txt is need to auto-removal system to work")
    parser.add_argument("--half", action="store_true", help="50% in 3 the biggest clusters")
    parser.add_argument("-v", "--verbose", action="store_true", help="")
    # parser.add_argument('-s', '--size',
    #                    help="size of the biggest cluster to quit, default 83 = 1/6 * 500, 300*1/6=50",
    #                    default=83)
    return parser


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    # get size from file
    size = len(open(args.matrix).readline().split()) - 1  # -1 to get 500 etc

    print ('# of struc %i' % size)

    c = 0
    while 1:
        if c > 40:
            print("You reached the limit, I'm quitting!")
            sys.exit(1)

        cmd = "evoClust_clustix.py " + args.matrix + " -c " + str(c)
        if args.half:
            cmd += " -o " + args.matrix.replace('.txt', '-half')

        print(cmd)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out = p.stdout.read().strip()
        err = p.stderr.read().strip()

        # print out
        if not args.half:
            for l in out.split('\n'):
                if 'cluster #1  curr the biggest cluster size' in l:
                    n = int(l.replace('cluster #1  curr the biggest cluster size', ''))
                    print('n: ', n)
                    if n >= int(size * 1 / 6):
                        sys.exit(0)
                    # clean matrix # hack
                    # this assume that a matrix is blebleble.matrix
                    cmd = 'rm ' + args.matrix.replace('.matrix', '') + \
                        '*cf' + str(c) + '*.out # auto-removal'
                    print(cmd)
                    os.system(cmd)
        else:
            # half mode
            # 50% in 3 clusters
            # start this procedure if you have even cluster #3
            if args.verbose: print(out)
            rn1 = re.compile("cluster #1  curr the biggest cluster size\s+(?P<n1>\d+)").search(out)
            if rn1:
                n1 = int(rn1.group('n1'))
            rn2 = re.compile("cluster #2  curr the biggest cluster size\s+(?P<n2>\d+)").search(out)
            if rn2:
                n2 = int(rn2.group('n2'))
            rn3 = re.compile("cluster #3  curr the biggest cluster size\s+(?P<n3>\d+)").search(out)
            if rn3:
                n3 = int(rn3.group('n3'))

            # summary
            if rn1 and rn2 and rn3:
                n = n1 + n2 + n3
                print('  # of structure in three the biggest clusters: ', n)

                if n >= int(size * 1/2):  # n (n1+n2+n3) > 1/6

                    cmd = 'mv ' + args.matrix.replace('.txt', '-half') + '*cf' + str(c) + '*.out ' + \
                      args.matrix.replace('.txt', '-half') + '_n-' + str(n) + '_n1-' + str(n1) + '_n2-' + str(n2) + '_n3-' + str(n3) + '_cf' + str(c) + '.out'
                    if args.verbose:
                        print(cmd)
                    os.system(cmd)

                    ## #txt = open(args.matrix.replace('.txt', '-half') + '_n1c' + str(n1) + '_cf' + str(c) + '.out').read()
                    ## with open(fn, 'w') as f:
                    ##     f.write(cmd + '\n')
                    ##     f.write('# of structure in three the biggest clusters: ' + str(n) + '\n')
                    ##     f.write(time.asctime())
                    ##     f.write(txt)

                    sys.exit(0)

            # clean matrix # hack
            cmd = 'rm ' + args.matrix.replace('.txt', '-half') + '*cf' + str(c) + '*.out # auto-removal'
            if args.verbose:
                print(cmd)
            os.system(cmd)

        # c += 0.05
        c += 0.5
