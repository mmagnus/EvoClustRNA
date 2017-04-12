#!/usr/bin/env python

"""CLUSTIX - CLUSTering of matrIX :-)::

   ./clustix.py -m <matrix> -c <cuttoff>

Required: numpy

Authors: Marcin Magnus <magnus@genesilico.pl> Irina Tuszynska <irena@genesilico.pl>
"""

import sys
try:
    from numpy import array, zeros, loadtxt, nditer
except ImportError:
    try:
        import numpy
        print 'Something went wrong. Your numpy is in version: %s . Please upgrade! Clustix has been tested with numpy 1.7.1.!' % numpy.__version__
    except:
        print 'Something went wrong. Please, install numpy'
    sys.exit(1)

import os.path
import argparse

MIN_CLUSTER = 3

try:
    import lib.timex.timex as timex
    dont_use_timex = False
except ImportError:
    dont_use_timex = True


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m',
                         dest="matrix", required=True,
                         help="A txt file with a similarity matrix with column headers, See test_data/matrix.txt for more")
    parser.add_argument('-o',
                         dest="output",
                         help="See test_data/output.txt for more, don't type extension of the file")
    parser.add_argument('-c',type=float,
                         dest="cut_off",
                         default=5.0,
                         help="Cut_off of RMSD for the formation of a cluster")

    parser.add_argument("-v", "--verbose",
                    action="store_true", default=False, dest="verbose", help="be verbose")
    return parser


if __name__ == '__main__':

    parser = get_parser()
    opts = parser.parse_args()
    if not opts.matrix:
        parser.print_help()
        sys.exit(1)

    if not dont_use_timex: t = timex.Timex(); t.start()

    # main program
    cf = opts.cut_off
    mfn = opts.matrix
    verbose = opts.verbose

    # get struc_names
    struc_names = open(mfn).readline().rstrip().strip('#').split()

    # load matrix
    m = loadtxt(mfn)
    if verbose: print '> matrix:\n', m
    
    mshape = m.shape
    print 'There is ', mshape[0] ,'structures in your matrix. 1/6 of this is ', mshape[0] * 1/6
    # matrix for clustering, contain 0 for values > cf and 1 - for values from matri that are < cf
    mclust = zeros(mshape)

    index = nditer(m, flags =['multi_index'])
    while not index.finished:
        if index[0] < cf:
            mclust[index.multi_index[0], index.multi_index[1]] = 1
        else: mclust[index.multi_index[0], index.multi_index[1]] = 0
        index.iternext()

    if verbose: print '> matrix of neighbors:\n', mclust

    print opts.cut_off
    matrixfn = os.path.splitext(os.path.basename(opts.matrix))[0] # get only fn of matrix, remove extension
    if not opts.output:
        out_name = matrixfn + "_cf%.2f.out" %(opts.cut_off)
    else:
        out_name = opts.output + "_cf%.2f.out" %(opts.cut_off)
    print out_name
    output = open(out_name, "w")
    
    output.write( "CLUSTER_BAKER_cf%i_%s\n" %(int(cf), matrixfn))

    # find the biggest cluster
    # ... and the find the new biggest cluster
    # ... and the find the
    # ... till you reach no of elements in cluster less than MIN_CLUSTER
    c = 0
    while 1:
        no_neighbors_under_cf_of_struc = []

        for row in mclust:
            no_neighbors_under_cf = row.sum()
            no_neighbors_under_cf_of_struc.append(no_neighbors_under_cf)

        if verbose:print '> no_neighbors_under_cf_of_struc', no_neighbors_under_cf_of_struc # print no of neighbors

        curr_biggest_cluster = array(no_neighbors_under_cf_of_struc)
        curr_biggest_cluster_no_of_struc = curr_biggest_cluster.max()

        print 'cluster #' + str(c+1), " curr the biggest cluster size ", int(curr_biggest_cluster_no_of_struc)

        if curr_biggest_cluster_no_of_struc < MIN_CLUSTER: break

        index = no_neighbors_under_cf_of_struc.index(curr_biggest_cluster_no_of_struc)
        curr_biggest_cluster_row = mclust[index,:] # row of curr_biggest_cluster
        indexes = curr_biggest_cluster_row.nonzero()
        if verbose: print " indexes of elements in this cluster", str(indexes[0])

        output.write("%3.1f\n" %len(indexes[0]))

        struc_names_of_biggest_cluster = []
        for i in indexes[0]:
            struc_names_of_biggest_cluster.append(struc_names[i])
            nam = struc_names[i]
            print nam, # names of files
            output.write ("%s\n" %nam)
        print 
        mclust[:,indexes] = 0
        if c > 3:
            break
        c += 1
        
    print '>> OK! The output is written to the %s file' % out_name
    if not dont_use_timex: print t.end()

    output.close()
        
