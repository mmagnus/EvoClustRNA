#!/usr/bin/python

import Bio.PDB.PDBParser
import Bio.PDB.Superimposer
import math
import lib.rna_p_value.rna_p_value as pv
import glob
import re
import os

class rnamodel: 
    def __init__(self, fpath, residues):
        # parser 1-5 -> 1 2 3 4 5
        self.struc = Bio.PDB.PDBParser().get_structure('', fpath)
        self.residues = self.__parser_residues(residues)
        self.__get_atoms()
        self.fpath = fpath
        self.fn = os.path.basename(fpath)
        #self.atoms = []

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
        return self.fn

    def __repr__(self):
        return self.fn

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


def get_rna_models_from_dir(directory, residues):
    models = []
    files = glob.glob(directory + "/*.pdb")
    for f in files:
        print f
        models.append(rnamodel(f, residues))
    return models
        # print pv.get_p_value(3,10)#r.get_rmsd_to(r2), 3)

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
    #fn = "test_data/rp13cp0016.out.1.pdb"
    # 
    #r = rnamodel(fn, '1 4 5 10-15')
    #print r
    #if 1:
        #fn = "test_data/rp13prs_cst.out.1.pdb"
        #r2 = rnamodel(fn, '6 7 10-15 20')
        #print r2 
        #print 'rms', r.get_rmsd_to(r2)

        models = get_rna_models_from_dir('test_data/rp13cp0016',  '1-8')
        models.extend( get_rna_models_from_dir('test_data/rp13prs',  '6-13') )

        for r1 in models:
            for r2 in models:
                print r1.fn, r2.fn, r1.get_rmsd_to(r2, 'tmp.pdb')
                break    
