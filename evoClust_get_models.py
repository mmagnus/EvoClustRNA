#!/usr/bin/env python
"""evoClust_get_models.py

Uses find in curr directory to find needed file.

This script creates:
- reps for top 5 clusters representative structures
- resp_motifs for top 5 clusters representative motifs

Add cutoff the name of reps, e.g. reps_c2.5

OLD: It reads `out` folder created by evoclustRNA.py in structure such as:
- out/structures/<homologs>
"""
import argparse
import os
import shutil
import re


def is_number(s):
    # http://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-float-in-python
    try:
        float(s)
        return True
    except ValueError:
        return False


class ClustixResult(object):
    def __init__(self, fn, input_dir, output_prefix, skip_motifs, use_cutoff_for_names):
        if output_prefix:
            output_prefix += '_'

        self.lines = open(fn).readlines()
        reps = []
        for i, l in enumerate(self.lines):
            if is_number(l):
                reps.append(self.lines[i + 1].strip())

        for i, r in enumerate(reps):
            print(str(i + 1) + '_' + r)

        # use cutoff for naming, instead of reps/ do reps_c2.6
        if use_cutoff_for_names:
            suffix = '_' + re.split('_', os.path.splitext(os.path.basename(fn))[0])[-1]  # rp14pk_n-155_n1-93_n2-33_n3-29_cf2.5.out
        else:
            suffix = ''

        try:
            os.mkdir(output_prefix + 'reps' + suffix)
        except OSError:
            pass

        # out in this case is input, for search reps and reps_motifs
        print '= structures == out/structures/<files>==================='

        for i, r in enumerate(reps):
            #cmd = "find . -iname " + r
            # commands.getoutput(cmd).split()[0].strip()
            rpath = 'out/structures/' + r
            cmd = ('cp -v ' + rpath + ' ' +
                   output_prefix + 'reps' + suffix + '/c' + str(i + 1) + '_' + r)
            print cmd
            os.system(cmd)
        try:
            os.mkdir(output_prefix + 'reps_motifs' + suffix)
        except OSError:
            pass

        if not skip_motifs:
            print '= motif =========================================='
            for i, r in enumerate(reps):
                print(input_dir + '/motifs/' + r + ' -> ' +
                      output_prefix + 'reps_motifs' + suffix + '/' + str(i + 1) + '_' + r)
                try:
                    shutil.copyfile(input_dir + '/motifs/' + r, output_prefix +
                                    'reps_motifs' + suffix + '/c' + str(i + 1) + '_' + r)
                except IOError:
                    print 'Missing motifs folder?'


def get_parser():
    """Get parser of arguments"""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-i', "--input_dir",
                        help="input folder with structures, .e.g. test_data", default="out")
    parser.add_argument('-o', "--output_prefix",
                        help="output folder where motifs and structures will be saved, e.g. test_out/rp14", default='')
    parser.add_argument('clustix_results_fn', help="")
    parser.add_argument('-c', '--use-cutoff-for-names', action='store_true')
    parser.add_argument('-s', '--skip_motifs', action='store_true')
    return parser


# main
if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    print(os.path.basename(__file__))
    print('-' * 80)
    ClustixResult(args.clustix_results_fn, args.input_dir, args.output_prefix, args.skip_motifs, args.use_cutoff_for_names)
