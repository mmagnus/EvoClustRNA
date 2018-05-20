#!/usr/bin/env python
"""evoClust_get_models.py

Uses find in curr directory to find needed file.

This script creates:
- reps for top 5 clusters representative structures
- resp_motifs for top 5 clusters representative motifs

Add cutoff the name of reps, e.g. reps_c2.5

The script has the second mode right now::

    [mm] rosetta-5x$ evoClust_get_models.py -i structures/ ade_plus_ade_cleanup_mapping_pkX_*.out -n adepk
    evoClust_get_models.py
    --------------------------------------------------------------------------------
    ['adepk_min.out.10.pdb', 'adepk_min.out.5.pdb', '', 'adepk_min.out.1.pdb', '']
    1_adepk_min.out.10.pdb
    2_adepk_min.out.5.pdb
    3_
    4_adepk_min.out.1.pdb
    5_
    = structures == out/structures/<files>===================
    cp -v structures//adepk_min.out.10.pdb reps_ns/c1_adepk_min.out.10.pdb
    structures//adepk_min.out.10.pdb -> reps_ns/c1_adepk_min.out.10.pdb
    cp -v structures//adepk_min.out.5.pdb reps_ns/c2_adepk_min.out.5.pdb
    structures//adepk_min.out.5.pdb -> reps_ns/c2_adepk_min.out.5.pdb
    cp -v structures// reps_ns/c3_
    cp: structures// is a directory (not copied).
    cp -v structures//adepk_min.out.1.pdb reps_ns/c4_adepk_min.out.1.pdb
    structures//adepk_min.out.1.pdb -> reps_ns/c4_adepk_min.out.1.pdb
    cp -v structures// reps_ns/c5_
    cp: structures// is a directory (not copied).

first, the input is parsed to get borders of lines of clusters. These borders are used to select structures that come to a given cluster. For each cluster, there is a search if within it there is a structure that starts with a given name - defined with --NATIVE_SEQ_ONLY. If there is none, then to the reps list '' is appended.

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
    def __init__(self, fn, input_dir, output_prefix, skip_motifs, use_cutoff_for_names, native_seq_only):
        if output_prefix:
            output_prefix += '_'

        self.lines = open(fn).readlines()

        # get reps based on structures after numbers, such as
        # 8.0
        # adepk_min.out.10.pdb
        if not native_seq_only:
            reps = []
            for i, l in enumerate(self.lines):
                if is_number(l):
                    reps.append(self.lines[i + 1].strip())

        # get reps based on structures in a given cluster going from the top of that cluster
        if native_seq_only:
            clusters_borders = []
            for i,l in enumerate(self.lines):
                if is_number(l):
                    clusters_borders.append(i)

            clusters_borders.append(len(self.lines))  # at the end of the file
            reps = []
            for i in range(0,5): # for top 5 clusters
                # ['8.0\n', 'adepk_min.out.10.pdb\n', 'a04pk_min.out.2.pdb\n', 'a04pk_min.out.5.pdb\n', 'a04pk_min.out.6.pdb\n', 'a04pk_min.out.7.pdb\n', 'u51pk_min.out.2.pdb\n', 'u51pk_min.out.5.pdb\n', 'u51pk_min.out.10.pdb\n']
                cluster_lines = self.lines[clusters_borders[i] : clusters_borders[i + 1]]
                for cl in cluster_lines:
                    if cl.startswith(native_seq_only):
                        reps.append(cl.strip())
                        break
                else:
                    reps.append('')  # if not then 'None'
            print(reps)

        for i, r in enumerate(reps):
            print(str(i + 1) + '_' + r)

        # use cutoff for naming, instead of reps/ do reps_c2.6
        if use_cutoff_for_names:
            suffix = '_' + re.split('_', os.path.splitext(os.path.basename(fn))[0])[-1]  # rp14pk_n-155_n1-93_n2-33_n3-29_cf2.5.out
        else:
            suffix = ''

        # reps
        if native_seq_only:
            repsfolder = 'reps_ns'
        else:
            repsfolder = 'reps'
        try:
            os.mkdir(output_prefix + repsfolder + suffix)
        except OSError:
            pass

        # out in this case is input, for search reps and reps_motifs
        print '= structures == out/structures/<files>==================='

        for i, r in enumerate(reps):
            #cmd = "find . -iname " + r
            # commands.getoutput(cmd).split()[0].strip()

            if input_dir:
                rpath = input_dir + os.sep + r
            else:
                rpath = 'out/structures/' + r

            cmd = ('cp -v ' + rpath + ' ' +
                   output_prefix + repsfolder + suffix + '/c' + str(i + 1) + '_' + r)
            print cmd
            os.system(cmd)

        # motifs
        if not skip_motifs:
            if native_seq_only:
                reps_motifs_folder = 'reps_motifs_ns'
            else:
                reps_motifs_folder = 'reps_motifs'

            try:
                os.mkdir(output_prefix + reps_motifs_folder + suffix)
            except OSError:
                pass

            print '= motif =========================================='
            for i, r in enumerate(reps):
                print(input_dir + '/motifs/' + r + ' -> ' +
                      output_prefix + reps_motifs_folder + suffix + '/' + str(i + 1) + '_' + r)
                try:
                    shutil.copyfile(input_dir + '/motifs/' + r, output_prefix +
                                    reps_motifs_folder + suffix + '/c' + str(i + 1) + '_' + r)
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
    parser.add_argument('-n', '--native-seq-only')
    return parser


# main
if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    print(os.path.basename(__file__))
    print('-' * 80)
    ClustixResult(args.clustix_results_fn, args.input_dir, args.output_prefix, args.skip_motifs, args.use_cutoff_for_names, args.native_seq_only)
