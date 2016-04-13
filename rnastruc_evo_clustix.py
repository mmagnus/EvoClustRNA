#!/usr/bin/python

import Bio.PDB.PDBParser
import Bio.PDB.Superimposer
from Bio.PDB.PDBIO import Select
from Bio.PDB import PDBIO, Superimposer

import optparse
import sys
import math
import glob
import re
import os

from RNAalignment import RNAalignment

class RNAmodel: 
    def __init__(self, fpath, residues):
        # parser 1-5 -> 1 2 3 4 5
        self.struc = Bio.PDB.PDBParser().get_structure('', fpath)
        self.residues = residues #self.__parser_residues(residues)
        self.__get_atoms()
        self.fpath = fpath
        self.fn = os.path.basename(fpath)
        #self.atoms = []
        if save:
            self.save() # @save

    def __parser_residues(self, residues):
        """Get string and parse it
        '1 4 5 10-15' -> [1, 4, 5, 10, 11, 12, 13, 14, 15]"""
        rs = []
        for r in residues.split():
            l = parse_num_list(r)
            for i in l:
                if i in rs:
                    raise Exception('You have this resi already in your list! See', residues)
            rs.extend(l)
        return rs

    def __get_atoms(self):
        self.atoms=[]
        for res in self.struc.get_residues():
            if res.id[1] in self.residues:
                self.atoms.append(res["C3'"])
                #print res.id
                #ref_atoms.extend(, ref_res['P'])
            #ref_atoms.append(ref_res.get_list())
        if len(self.atoms) <= 0:
            raise Exception('problem: none atoms were selected!')
        return self.atoms
    
    def __str__(self):
        return self.fn #+ ' # beads' + str(len(self.residues))

    def __repr__(self):
        return self.fn #+ ' # beads' + str(len(self.residues))

    def get_report(self):
        """Str a short report about rna model""" 
        t = ' '.join(['File: ', self.fn, ' # of atoms:', str(len(self.atoms)), '\n'])
        for r,a in zip(self.residues, self.atoms ):
            t += ' '.join(['resi: ', str(r) ,' atom: ', str(a) , '\n' ])
        return t

    def get_rmsd_to(self, other_rnamodel, output=''):
        """Calc rmsd P-atom based rmsd to other rna model"""
        sup = Bio.PDB.Superimposer()
        sup.set_atoms(self.atoms, other_rnamodel.atoms)
        rms = round(sup.rms, 3)
        if output:
            io = Bio.PDB.PDBIO()
            sup.apply(self.struc.get_atoms())
            io.set_structure( self.struc )
            io.save("aligned.pdb")

            io = Bio.PDB.PDBIO()
            sup.apply(other_rnamodel.struc.get_atoms())
            io.set_structure( other_rnamodel.struc )
            io.save("aligned2.pdb")
            
        return rms

    def save(self, verbose=True):
        folder_to_save =  output_dir + os.sep # ugly hack 'rp14/'
        try:
            os.makedirs(folder_to_save)
        except OSError:
            pass

        try:
            os.mkdir(folder_to_save + 'structures')
        except OSError:
            pass

        try:
            os.mkdir(folder_to_save + 'motifs')
        except OSError:
            pass

        RESI = self.residues
        if not self.struc:
            raise Exception('self.struct was not defined! Can not save a pdb!')
        class BpSelect(Select):
            def accept_residue(self, residue):
                if residue.get_id()[1] in RESI:
                    return 1
                else:
                    return 0

        io = PDBIO()
        io.set_structure(self.struc)
        fn = folder_to_save + 'structures' + os.sep + self.fn #+ '.pdb'
        io.save(fn)
        if verbose:
            print '    saved to struc: %s ' % fn

        io = PDBIO()
        io.set_structure(self.struc)
        fn = folder_to_save +  'motifs/' + os.sep + self.fn #+ self.fn.replace('.pdb', '_motif.pdb')# #+ '.pdb'
        io.save(fn, BpSelect())
        if verbose:
            print '    saved to motifs: %s ' % fn

def get_rna_models_from_dir(directory, residues):
    models = []
    if not os.path.exists(directory):
        raise Exception('Dir does not exist! ', directory)
    files = glob.glob(directory + "/*.pdb")
    files_sorted = sort_nicely(files)
    for f in files_sorted:
        #print f
        models.append(RNAmodel(f, residues))
    return models

def sort_nicely( l ):
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

if __name__ == '__main__':
    print 'rnastruc_evo_clustix.py'
    print '-' * 80
    
    optparser=optparse.OptionParser(usage="%prog [<options>]")
    optparser.add_option('-a',"--rna_alignment_fn", type="string",
                         dest="rna_alignment_fn",
                         default='',
                         help="")

    optparser.add_option('-o',"--output_dir", type="string",
                         dest="output_dir",
                         default='',
                         help="")

    optparser.add_option('-i',"--input_dir", type="string",
                         dest="input_dir",
                         default='',
                         help="")

    optparser.add_option('-m',"--mapping", type="string",
                         dest="mapping",
                         default='',
                         help="")

    optparser.add_option('-x',"--matrix_fn", type="string",
                         dest="matrix_fn",
                         default='matrix.txt',
                         help="")

    optparser.add_option("-s", "--save",
                     action="store_true", default=False, dest="save", help="")

    
    (opts, args)=optparser.parse_args()

    if len(sys.argv) == 1:
        print optparser.format_help() #prints help if no arguments
        sys.exit(1)

    ra = RNAalignment(opts.rna_alignment_fn)
    global save
    save = opts.save
    global output_dir  # ugly hack!
    output_dir = opts.output_dir
    input_dir = opts.input_dir
    matrix_fn = opts.matrix_fn
    rnastruc = opts.mapping.strip().split('|') # 'target:rp14_farna_eloop_nol2fixed_cst|X:X'
    print ' # of rnastruc:', len(rnastruc)
    print ' rnastruc:', rnastruc
    
    models = []

    for rs in rnastruc:
        rs_name_alignment, rs_name_dir = rs.split(':') # target:rp14_farna_eloop_nol2fixed_cst 
        print ' ', rs_name_alignment,'<->', rs_name_dir
        print '   cutting out fragments ... '
        models.extend( get_rna_models_from_dir(input_dir + os.sep + rs_name_dir, ra.get_range(rs_name_alignment))[:] )        

    print ' # of models:', len(models)

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
