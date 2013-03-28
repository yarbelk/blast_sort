"""Given a csv file of blasts, check for blasts that mach the passed set and store the identity and DNA sequence associated with it"""
__author__ = 'yarbelk & kathysufy'

import csv
import os, sys
import re
from path import path
from collections import namedtuple

Identity = namedtuple('Identity', ['name','dna'])

# create unbuffered stdout so updates print nicely


re_identity = re.compile(r"^[\w_\d]+$")
re_blast_no = re.compile(r"^gi\|\d+\|\w+\|(?P<blast>\w{2,3}_?\d+)\.?\d*\|")

def format_fasta(identity):
    sequence = identity.dna
    if 'contig_245' in identity.name:
        pass
        #import ipdb; ipdb.set_trace()
    split_sequence = ["\n>" + identity.name]
    while sequence:
        split_sequence += [sequence[:79],]
        sequence = sequence[79:]
    return split_sequence

def check_inclusion(blast_set, data_file, output_folder, verbose=False):
    output_folder = path(output_folder)
    identity = None
    identity_old = None
    blast_no_old = None
    if verbose:
        print "Parsing {data_file}:".format(data_file=data_file)
    data_file_size = os.path.getsize(data_file)
    last_percent = 0
    with open(data_file, 'r') as fd:
        csv_reader = csv.reader(fd, dialect='excel')
        data_column = None
        for num, line in enumerate(csv_reader):
            cur_percent = int((float(fd.tell()) / data_file_size) * 100)
            if cur_percent != last_percent:
                if verbose:
                    print "{0}%".format(cur_percent)
            last_percent = cur_percent
            id_match = re_identity.search(line[0])
            if id_match:
                if data_column is None:
                    if len(line) > 2 and line[2]:
                        data_column = 2
                    else:
                        data_column = 1
                identity_old = identity
                identity = Identity(line[0], line[data_column])
            else:
                blast_match = re_blast_no.search(line[0])
                if blast_match:
                    blast_no = blast_match.groupdict('blast')['blast']
                    if blast_no.split('.',1)[0] in blast_set:
                        if blast_no != blast_no_old and identity.name != getattr(identity_old, 'name', None):
                            # write line(s) to file
                            with open(output_folder / blast_no + '.fasta','a') as output_fd:
                                output_fd.write('\n'.join(format_fasta(identity)))
                                output_fd.flush()
                        blast_no_old = blast_no


if __name__ == '__main__':
    from main import main
    main(sys.argv)
