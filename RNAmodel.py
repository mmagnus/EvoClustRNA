#!/usr/bin/env python
from __future__ import print_function
__docformat__ = 'reStructuredText'
import os
import Bio.PDB.PDBParser
import Bio.PDB.Superimposer
from Bio.PDB.PDBIO import Select
from Bio.PDB import PDBIO
from Bio.SVDSuperimposer import SVDSuperimposer
from numpy import sqrt, array, asarray
from rna_pdb_tools.opt.BasicAssessMetrics.BasicAssessMetrics import *

class RNAmodel:
    """RNAmodel

    :Example:

        >>> rna = RNAmodel("test_data/rp14/rp14_5ddp_bound_clean_ligand.pdb", [1], False, None)
        >>> rna.get_report()
        "File:  rp14_5ddp_bound_clean_ligand.pdb  # of atoms: 1 \\nresi:  1  atom:  <Atom C3'> \\n"

    :param fpath: file path, string
    :param residues: list of residues to use (and since we take only 1 atom, C3', this equals to number of atoms.
    :param save: boolean, save to output_dir or not
    :param output_dir: string, if save, save segments to this folder
    """
    #:returns: None
    #:rtype: None
    #"""
    def __init__(self, fpath, residues, save=False, output_dir=""):

        # parser 1-5 -> 1 2 3 4 5
        self.struc = Bio.PDB.PDBParser().get_structure('', fpath)
        self.fpath = fpath
        self.fn = os.path.basename(fpath)
        self.residues = residues #self.__parser_residues(residues)
        self.__get_atoms()
        #self.atoms = []
        if save:
            self.save(output_dir) # @save

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
        self.atoms = []
        for res in self.struc.get_residues():
            if res.id[1] in self.residues:
                self.atoms.append(res["C3'"])
                #print res.id
                #ref_atoms.extend(, ref_res['P'])
            #ref_atoms.append(ref_res.get_list())
        if len(self.atoms) <= 0:
            raise Exception('problem: none atoms were selected!: %s' % self.fn)
        return self.atoms

    def __str__(self):
        return self.fn #+ ' # beads' + str(len(self.residues))

    def __repr__(self):
        return self.fn #+ ' # beads' + str(len(self.residues))

    def get_report(self):
        """Str a short report about rna model"""
        t = ' '.join(['File: ', self.fn, ' # of atoms:', str(len(self.atoms)), '\n'])
        for r, a in zip(self.residues, self.atoms):
            t += ' '.join(['resi: ', str(r), ' atom: ', str(a), '\n'])
        return t

    def get_rmsd_to(self, other_rnamodel, output='', dont_move=False):
        """Calc rmsd P-atom based rmsd to other rna model"""
        sup = Bio.PDB.Superimposer()

        if dont_move:
            # fix http://biopython.org/DIST/docs/api/Bio.PDB.Vector%27.Vector-class.html
            coords = array([a.get_vector().get_array() for a in self.atoms])
            other_coords = array([a.get_vector().get_array() for a in other_rnamodel.atoms])
            s = SVDSuperimposer()
            s.set(coords,other_coords)
            return s.get_init_rms()

        try:
            sup.set_atoms(self.atoms, other_rnamodel.atoms)
        except:
            print(self.fn, len(self.atoms),  other_rnamodel.fn, len(other_rnamodel.atoms))
            for a,b in zip(self.atoms, other_rnamodel.atoms):
                print(a.parent, b.parent)#a.get_full_id(), b.get_full_id())

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

    def get_inf_to(self, b, verbose=False):
        # @indev
        import string
        import random
        #job_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        job_id = '/home/magnus/Desktop/evoclust/'
        fn = self.save('/tmp/%s/' % job_id, verbose=verbose)
        fn2 = b.save('/tmp/%s/' % job_id, verbose=verbose)

        # rna-pdb-tools
        # required installed
        # https://github.com/mmagnus/rna-pdb-tools
        # renumber files in place
        fn_ren = fn.replace('.pdb', '') + '.renumber.pdb'
        fn2_ren = fn2.replace('.pdb', '') + '.renumber.pdb'

        os.system('rna_pdb_toolsx.py  --dont_report_missing_atoms --renumber_residues %s > %s' % (fn, fn_ren ))
        os.system('rna_pdb_toolsx.py  --dont_report_missing_atoms --renumber_residues %s > %s' % (fn2, fn2_ren))

        fn_inf = fn_ren.replace('.pdb', '') + '--' + fn2_ren.split('/')[-1].replace('.pdb', '') + '.infs'
        rmsd, DI_ALL, INF_ALL, INF_WC, INF_NWC, INF_STACK = interaction_network_fidelity(fn_ren, None, fn2_ren, None)
        return rmsd, DI_ALL, INF_ALL, INF_WC, INF_NWC, INF_STACK
        # clarna based
        ## # @indev
        ## import string
        ## import random
        ## #job_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        ## job_id = '/home/magnus/Desktop/evoclust/'
        ## fn = self.save('/tmp/%s/' % job_id, verbose=verbose)
        ## fn2 = b.save('/tmp/%s/' % job_id, verbose=verbose)

        ## # rna-pdb-tools
        ## # required installed
        ## # https://github.com/mmagnus/rna-pdb-tools
        ## # renumber files in place
        ## fn_ren = fn.replace('.pdb', '') + '.renumber.pdb'
        ## fn2_ren = fn2.replace('.pdb', '') + '.renumber.pdb'

        ## os.system('rna_pdb_toolsx.py  --dont_report_missing_atoms --renumber_residues %s > %s' % (fn, fn_ren ))
        ## os.system('rna_pdb_toolsx.py  --dont_report_missing_atoms --renumber_residues %s > %s' % (fn2, fn2_ren))

        ## fn_inf = fn_ren.replace('.pdb', '') + '--' + fn2_ren.split('/')[-1].replace('.pdb', '') + '.infs'
        ## quiet = ''
        ## if not verbose:
        ##     quiet = ' > /dev/null'
        ## # os.system('rna_calc_inf.py -t %s %s -o %s %s ' % (fn_ren, fn2_ren, fn_inf, quiet))

        ## import pandas as pd
        ## pd.set_option('display.width', 200)
        ## df = pd.read_csv(fn_inf)
        ## if verbose: print(df)
        ## return float(df['inf_all'])

    def save(self, output_dir, verbose=True):
        """Save structures and motifs """
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

        ## io.set_structure(self.struc)
        ## fn = folder_to_save + 'structures' + os.sep + self.fn #+ '.pdb'
        ## io.save(fn)
        ## if verbose:
        ##     print('    saved to struc: %s ' % fn)

        io = PDBIO()
        io.set_structure(self.struc)
        fn = folder_to_save +  'motifs/' + os.sep + self.fn #+ self.fn.replace('.pdb', '_motif.pdb')# #+ '.pdb'
        io.save(fn, BpSelect())
        if verbose:
            print('    saved to motifs: %s ' % fn)
        return fn

#main
if __name__ == '__main__':
    import doctest
    doctest.testmod()

    #rna = RNAmodel("test_data/rp14/rp14_5ddp_bound_clean_ligand.pdb", [1], False, Non3e)
    #print(rna.get_report())
    a = RNAmodel("test_data/GGC.pdb", [46, 47, 48])
    b = RNAmodel("test_data/GUC.pdb", [31, 32, 33])

    print(a.get_rmsd_to(b))
    print(a.get_rmsd_to(b, dont_move=True))

    print(a.get_inf_to(b))
