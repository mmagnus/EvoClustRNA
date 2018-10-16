#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
/home/magnus/rna-evo-malibu/ade # run here not up
"""
from __future__ import print_function
import os


def exe(cmd, dryrun=False):
    print(cmd)
    if not dryrun: os.system(cmd)

if __name__ == '__main__':
    modes = {
        #'simrna5x10rosetta5x10' : 'evox.py -s 10 -f 10 -e -p ade',
        #     'simrna5x50rosetta5x50' : 'evox.py -s 50 -f 50 -e -p ade',
        'simrna5x200rosetta5x200' : 'evox.py -s 200 -f 200 -e -p ade',
        'simrna5x300rosetta5x300' : 'evox.py -s 300 -f 300 -e -p ade',
        'simrna5x400rosetta5x400' : 'evox.py -s 400 -f 400 -e -p ade',
        'simrna5x500rosetta5x500' : 'evox.py -s 500 -f 500 -e -p ade',
        }

    root = os.getcwd()
    for m in modes:
        try: os.mkdir(m)
        except OSError: pass
        os.chdir(m)
        print('Run %s' % modes[m])
        exe(modes[m])
        os.chdir(root)
