#!/usr/bin/env python3

"""
Purpose: Split interleaved, paired reads into _1/2 files
Author: Ken Youens-Clark <kyclark@email.arizona.edu>
"""

import argparse
import os
import sys
from Bio import SeqIO

# --------------------------------------------------
def get_args():
    """get args"""
    parser = argparse.ArgumentParser(
        description='Split interleaved/paired reads',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('infile', metavar='FILE', nargs='+',
                        help='Input file(s)')

    parser.add_argument('-o', '--outdir', help='Output directory',
                        metavar='DIR', type=str, default='')

    parser.add_argument('-f', '--format', help='File format (fasta, fastq)',
                        metavar='str', type=str, default='fastq')

    return parser.parse_args()

# --------------------------------------------------
def main():
    """main"""
    args = get_args()
    infiles = args.infile
    out_dir = args.outdir
    file_format = args.format.lower()

    if out_dir and not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    valid_format = set(['fasta', 'fastq'])
    if not file_format in valid_format:
        print('Bad --format "{}" please choose from: {}'.format(
            file_format, ', '.join(valid_format)))
        sys.exit(1)

    for fnum, infile in enumerate(infiles):
        if not os.path.isfile(infile):
            print('"{}" is not a file'.format(infile))
            continue

        filename = os.path.basename(infile)
        base, ext = os.path.splitext(filename)
        dirname = out_dir if out_dir else os.path.dirname(os.path.abspath(infile))
        forward = open(os.path.join(dirname, base + '_1' + ext), 'wt')
        reverse = open(os.path.join(dirname, base + '_2' + ext), 'wt')

        print("{:3d}: {}".format(fnum + 1, filename))

        num_seqs = 0
        for i, rec in enumerate(SeqIO.parse(infile, file_format)):
            SeqIO.write(rec, forward if i % 2 == 0 else reverse, file_format)
            num_seqs += 1

        print('\tSplit {} sequences to {}'.format(num_seqs, dirname))

# --------------------------------------------------
if __name__ == '__main__':
    main()
