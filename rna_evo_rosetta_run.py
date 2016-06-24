#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
python run_rosetta.py  aacy28.fa

TODO helices as qsub..."""

import sys
import subprocess
import os
import copy

no_jobs = 96
MAX_TIME = 24

def hr(c='-'):
    print c * 80

def get_conserved_resi(cst_line):
    """get a list of conserved resi 

    ...c....c................c....................c.....................c..c............cc..........
    [4, 9, 26, 47, 69, 72, 85, 86]"""
    cst = []
    for i in range(0, len(cst_line)):
        if cst_line[i] == 'c':
            cst.append(i+1)
    return cst

def get_cst(f):
    txt = ''
    txt += '[ atompairs ]'
    f2 = copy.copy(f)
    f2.reverse()

    for i in f:
        for x in f2:
            if i !=  x:
                #print i,x
                txt +=  "C1' %s C1' %s FADE -25 25 10 -100 100\n" % (i, x)
    f2.pop()
    return txt.strip()

def prep_input(fn):
    print fn
    print ' prepare inputs...'

    try:
        os.mkdir(fn.replace('.fa',''))
    except OSError:
        pass

    lines = []
    for l in open(fn):
        if l.strip():
            if not l.startswith('#'):
                lines.append(l.strip())

    if len(lines) == 3:
        header, seq, ss = lines
        cst = None
    if len(lines) == 4:
        header, seq, ss, cst_line = lines
        cst = get_conserved_resi(cst_line)
        cst_text = get_cst(cst)
        # save seq.cst
        print '  cst made...'
 
    hr('#')
    print header
    print seq
    print ss
    if cst:
        print cst_line, cst
    hr('#')
    
    dir = fn.replace('.fa','')
    os.chdir(os.path.join(os.path.abspath(os.path.curdir), dir))
    print ' made:', os.getcwd()
    
    open('seq.fa','w').write(header + '\n' + seq + '\n')
    open('seq.ss','w').write(ss + '\n')
    if cst: open('seq.cst','w').write(cst_text + '\n')

def prep_helices():
    cmd =  'helix_preassemble_setup.py -secstruct seq.ss -fasta seq.fa' # 'helix_preassemble_setup.py -secstruct \'' + ss + '\' -fasta ' + seq 
    print cmd
    err = subprocess.call(cmd, shell=True)
    #if err == 0:
     #   print cmd, 'error'
        #sys.exit(1)

    new_file = open('CMDLINES_parallel','w')
    for l in open('CMDLINES'):
        if l.startswith('source'):
            l = l.strip() + ' & \n'
        new_file.write(l)

    print 
    print 'cd ' + fn.replace('.fa', '') + ' && source CMDLINES_parallel'
    #cmd = 'bash CMDLINES'
    #print cmd
    #subprocess.call(cmd, shell=True)

def prep_jobs():
    l = open('CMDLINES').read().split('\n')[-2].replace('# ','')
    #print l # -silent helix0.out helix1.out helix2.out helix3.out helix4.out helix5.out helix6.out helix7.out  -input_silent_res 6-10 102-106 17-24 29-36 38-41 64-67 43-45 61-63 46-50 55-59 70-71 100-101 74-83 88-97 108-113 118-123 
    if os.path.exists('seq.cst'):
        cmd = "rna_denovo_setup.py -fasta seq.fa -secstruct_file seq.ss  -cst_file seq.cst " + l
    else:
        cmd = "rna_denovo_setup.py -fasta seq.fa -secstruct_file seq.ss " + l

    err = subprocess.call(cmd, shell=True) 
    print cmd 

    f = open('README_FARFAR').read()
    f = f.replace('-minimize_rna true',  '-minimize_rna false')
    open('README_FARFAR_MIN_FALSE','w').write(f)

    for i in range(0,1000):
        if os.path.exists('r'+str(i)):
            pass
        else:
            out_dir = 'r'+str(i)
            break

    cmd = "rosetta_submit.py README_FARFAR_MIN_FALSE " + out_dir + " " + str(no_jobs) + " " + str(MAX_TIME) + " " + sys.argv[1].replace('.fa', '') + " > /tmp/rna_evo.log" # name
    print ' ', cmd
    err = subprocess.call(cmd, shell=True)

    print cmd
    print 'cd ' + fn.replace('.fa', '') + ' && source qsubMINI && cd ..'

    #subprocess.call('/home/oge/bin/lx24-amd64/qsub qsub_files//qsub0.sh', shell=True)
    #os.system('source qsubMINI')

    #cmd = "/home/oge/bin/lx24-amd64/qsub -cwd -l h_vmem=300M -l mem_free=500M -pe mpi 10 "+SimRNA_RUN_FILENAME

if __name__ == '__main__':
    
    try:
        fn = sys.argv[1]
        print 'rna_evo_rosetta_run.py'
        hr()
    except:
        print 'rna_evo_rosetta_run.py <seq.fa> [--helices] [--run]'
        sys.exit(1)
        
    prep_input(fn)

    if '--helices' in sys.argv:
        prep_helices() # warning!
    if '--run' in sys.argv:
        prep_jobs()
