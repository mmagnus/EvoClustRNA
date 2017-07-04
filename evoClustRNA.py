#!/usr/bin/env python

"""
When RNA models are loaded, models ending with 'template.pdb' are ignore.
"""

import Bio.PDB.PDBParser
import Bio.PDB.Superimposer
from Bio.PDB.PDBIO import Select
from Bio.PDB import PDBIO, Superimposer

import argparse
import sys
import math
import glob
import re
import os

import Bio.PDB.PDBParser
import Bio.PDB.Superimposer
from Bio.PDB.PDBIO import Select
from Bio.PDB import PDBIO, Superimposer

from RNAalignment import RNAalignment
from RNAmodel import RNAmodel

def get_rna_models_from_dir(directory, residues, save, output_dir):
    """@todo

    :param directory: 
    :param residues: 
    :param save: 
    :param output_dir: 
    :returns: 
    :rtype: 

    """
    
    """"""
    models = []
    if not os.path.exists(directory):
        raise Exception('Dir does not exist! ', directory)
    files = glob.glob(directory + "/*.pdb")
    files_sorted = sort_nicely(files)
    for f in files_sorted:
        ## ignore files that can be found in your folder
        ## be careful with this --magnus
        if f.endswith('template.pdb'):
            continue
        if 'clust01X' in f:
            continue
        if 'clust02X' in f:
            continue
        if 'clust03X' in f:
            continue
        models.append(RNAmodel(f, residues, save, output_dir))
    return models

def sort_nicely(l):
   """ Sort the given list in the way that humans expect.

   http://blog.codinghorror.com/sorting-for-humans-natural-sort-order/
   """
   convert = lambda text: int(text) if text.isdigit() else text
   alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
   l.sort( key=alphanum_key )
   return l

def parse_num_list(s):
    """ http://stackoverflow.com/questions/6512280/accept-a-range-of-numbers-in-the-form-of-0-5-using-pythons-argparse """
    m = re.match(r'(\d+)(?:-(\d+))?$', str(s))
    # ^ (or use .split('-'). anyway you like.)
    if not m:
        return s 
    start = m.group(1)
    end = m.group(2) or start
    return list(range(int(start,10), int(end,10)+1))

#def pair:
#    def __init__(self, f1, f2):
#        self.f1
#        self.f2
#    def calc_distance():
#        pass

def get_parser():
    """Get parser of arguments"""
        
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-a',"--rna_alignment_fn", help="rna alignemnt with the extra guidance line, e.g. test_data/rp14sub.stk")
    parser.add_argument('-o',"--output_dir", help="output folder where motifs and structures will be saved, e.g. test_out/rp14")
    parser.add_argument('-i',"--input_dir", help="input folder with structures, .e.g. test_data")
    parser.add_argument('-m',"--mapping", help="map folders on the drive with sequence names in the alignment (<name in the alignment>:<folder name>), use | to \
    for multiple seqs, e.g. 'target:rp14_farna_eloop_nol2fixed_cst|AACY023581040:aacy23_cst', use | as a separator")
    parser.add_argument('-x',"--matrix_fn", default="", help="output matrix with rmsds all-vs-all")
    parser.add_argument("-s", "--save", action="store_true", default=False, help="save motifs and structures to output_dir, this slows down the program")
    return parser

if __name__ == '__main__':
    parser = get_parser()
    opts = parser.parse_args()
    if not opts.rna_alignment_fn:
        parser.print_help()
        sys.exit(1)
        
    ra = RNAalignment(opts.rna_alignment_fn)

    global save # ugly hack!
    if opts.output_dir:
        save = True
    else:
        save = opts.save
    global output_dir  # ugly hack!
    output_dir = opts.output_dir
    input_dir = opts.input_dir
    if opts.matrix_fn:
        matrix_fn = opts.matrix_fn
    else:
        matrix_fn = os.path.splitext(os.path.basename(opts.rna_alignment_fn))[0] + '_matrix.txt'
    print matrix_fn

    rnastruc = opts.mapping.strip().split('|') # 'target:rp14_farna_eloop_nol2fixed_cst|X:X'
    print ' # of rnastruc:', len(rnastruc)
    print ' rnastruc:', rnastruc
    
    models = []

    for rs in rnastruc:
        try:
            rs_name_alignment, rs_name_dir = rs.split(':') # target:rp14_farna_eloop_nol2fixed_cst
        except ValueError:
            #if -m 'tpp|tpp_pdb|CP000050.1/ ..
            #rnastruc: ['tpp', 'tpp_pdb', 'CP000050.1/1019813-1019911:tc5_pdb', 'AE017180.1/640928-641029:tae_pdb', 'BX248356.1/234808-234920:tb2_pdb']
            #Traceback (most recent call last):
            #File "/home/magnus/work/src/evoClustRNA/evoClustRNA.py", line 100, in <module>
            #raise Exception("There is an error in your mapping, check all : and | carefully")
            #Exception: There is an error in your mapping, check all : and | carefully
            raise Exception("There is an error in your mapping, check all : and | carefully")

        print ' ', rs_name_alignment,'<->', rs_name_dir
        print '   cutting out fragments ... '
        models.extend( get_rna_models_from_dir(input_dir + os.sep + rs_name_dir, ra.get_range(rs_name_alignment), opts.save, opts.output_dir)[:] )        
    print ' # of models:', len(models)

    # prepare a matrix
    f = open(matrix_fn, 'w')
    t = '# '
    for r1 in models:
        #print r1,
        t += str(r1) + ' '
    #print
    t += '\n'

    if True:
        c = 1
        for r1 in models:
            for r2 in models:
                #print
                #print r1.fn, r2.fn, r1.get_rmsd_to(r2)#, 'tmp.pdb')
                rmsd = r1.get_rmsd_to(r2) #, 'tmp.pdb')
                #print rmsd
                t += str(rmsd) + ' '
                #break    
            #print
            t += '\n'
            
    f.write(t)
    f.close()

    #print t # matrix

    if True:
        print 'matrix was created! ', matrix_fn
    else:
        print 'matrix NOT was created!'
