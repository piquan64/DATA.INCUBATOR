#!/usr/bin/env python3
"""Add sample name to FASTQ headers"""

import argparse
import csv
import os
import sys
from Bio import SeqIO

# --------------------------------------------------
def get_args():
    """get args"""
    parser = argparse.ArgumentParser(
        description='Add sample name to FASTQ',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('fastq', metavar='FASTQ', help='FASTQ file(s)',
                        nargs='+')

    parser.add_argument('-m', '--barcode_file', help='Barcode map file',
                        metavar='str', type=str, default='')

    parser.add_argument('-o', '--outdir', help='Output directory',
                        metavar='str', type=str, default=os.getcwd())

    return parser.parse_args()

# --------------------------------------------------
def main():
    """main"""
    args = get_args()
    barcode_file = args.barcode_file
    out_dir = args.outdir

    if not os.path.isfile(barcode_file):
        print('-m "{}" is not a file'.format(barcode_file))
        sys.exit(1)

    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    barcode_to_sample = {}
    with open(barcode_file) as fh:
        reader = csv.DictReader(fh, delimiter='\t')
        for row in reader:
            barcode_to_sample[row['BarcodeSequence']] = row['SampleID'] + '_'

    #print(barcode_to_sample)

    for fnum, fastq in enumerate(args.fastq):
        if not os.path.isfile(fastq):
            print('-f "{}" is not a file'.format(fastq))
            sys.exit(1)

        basename = os.path.basename(fastq)
        out_file = os.path.join(out_dir, basename)
        out_fh = open(out_file, 'wt')

        print('{:3}: {}'.format(fnum+1, basename))

        with open(fastq, "rU") as handle:
            for record in SeqIO.parse(handle, 'fastq'):
                desc = record.description
                parts = desc.split(':')
                barcode = parts[-1]
                if barcode in barcode_to_sample:
                    sample_name = barcode_to_sample[barcode]
                    record.id = ':'.join([sample_name, desc])
                    SeqIO.write(record, out_fh, 'fastq')

    print('Done, see outdir "{}"'.format(out_dir))

# --------------------------------------------------
if __name__ == '__main__':
    main()
