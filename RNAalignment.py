#!/usr/bin/env python

"""RNAalignment

Example::

	# STOCKHOLM 1.0

	AACY023581040                --CGUUGGACU------AAA--------AGUCGGAAGUAAGC-----AAU-C------GCUGAAGCAACGC---
	AJ630128                     AUCGUUCAUUCGCUAUUCGCA-AAUAGCGAACGCAA--AAG------CCG-A-------CUGAAGGAACGGGAC
	target                       --CGUUGACCCAG----GAAA-----CUGGGCGGAAGUAAGGCCCAUUGCACUCCGGGCCUGAAGCAACGCG--
	#=GC SS_cons                 ::(((((,<<<<<<<.._____..>>>>>>>,,,,,,,,<<<<...._____.....>>>>,,,,)))))::::
	x                            --xxxxxxxxx-----------------xxxxxxxx--xxx------------------xxxxxxxxxxx----
	#=GC RF                      AUCGUUCAuCucccc..uuuuu..ggggaGaCGGAAGUAGGca....auaaa.....ugCCGAAGGAACGCguu
        //

x line is used to pick resides to calculate RMSD."""

import warnings
warnings.filterwarnings("ignore")

from Bio import AlignIO

class RNAalignment:
    """RNAalignemnt"""
    def __init__(self, fn):
        """Load the alignment in the Stockholm format using biopython"""
        self.alignment = AlignIO.read(open(fn), "stockholm")

    def get_range(self, seqid, offset=0):
        """Get a list of positions for selected residues based on the last line of the alignment!"""
        x = self.alignment.get_all_seqs()[-1].seq # ---(((((((----xxxxx--
        x_range = []
        for record in self.alignment:
            if record.id == seqid:
                spos = 0
                for xi, si in zip(x, record.seq):
                    if si != '-':
                        spos += 1
                    if xi != '-':
                        #print xi, si,
                        #print si, spos
                        x_range.append(spos + offset)
       #print len(x_range)
        if not x_range:
            raise Exception('Seq not found or wrong x line')
        return x_range


if __name__ == '__main__':
    ra = RNAalignment('test_data/rp13finalX.stk')
    print len(ra.get_range('rp13target', offset=0))
    print len(ra.get_range('cp0016', offset=0))
    print len(ra.get_range('NZ_ABBD01000528', offset=0))

    print ra.get_range('rp13target', offset=0)
    print ra.get_range('cp0016', offset=0)
    print ra.get_range('NZ_ABBD01000528', offset=0)


