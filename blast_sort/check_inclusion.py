"""Given a csv file of blasts, check for blasts that mach the passed set and store the identity and DNA sequence associated with it"""

import csv
import os, sys
import re
from path import path
from collections import namedtuple

Identity = namedtuple('Identity', ['name','dna'])

# create unbuffered stdout so updates print nicely


re_identity = re.compile(r"^[\w_\d]+$")
re_blast_no = re.compile(r"^gi\|\d+\|\w+\|(?P<blast>\w{2,3}_?\d+)\.?\d*\|")

re_gi = re.compile(r"^gi\|\d+\|(?P<type>\w+)")
re_refseq = re.compile(r"ref\|(?P<accession>[\w\d_]+)(\.\d+)?\|(?P<name>[\w\d_]*)")
re_genbank = re.compile(r"gb\|(?P<accession>[\w\d_]+)(\.\d+)?\|(?P<locus>[\w\d]*)")
re_embl = re.compile(r"emb\|(?P<accession>[\w\d_]+)(\.\d+)?\|(?P<locus>[\w\d]*)")
re_pir = re.compile(r"pir\|(?P<accession>[\w\d_]*)\|(?P<name>[\w\d_]*)")  # Doesn't seem to have accession numbers
re_ddbj = re.compile(r"djb\|(?P<accession>[\w\d_]*)(\.\d+)?\|(?P<locus>[\w\d_]*)")
re_prf = re.compile(r"prf\|(?P<accession>[\w\d_]*)(\.\d+)?\|(?P<locus>[\w\d_]*)")  # Doesn't seem to have accession numbers

re_dict = {
    'ref': re_refseq,
    'gb' : re_genbank,
    'emb': re_embl,
    'pir': re_pir,
    'djb': re_ddbj,
    'prf': re_prf,
    }

def get_blast_dict(data):
    gi_search = re_gi.search(data)
    if gi_search:
        try:
            blast_type = gi_search.groupdict()['type']
            test_re = re_dict[blast_type]
            data_search = test_re.search(data)
            if data_search:
                found = data_search.groupdict()
                blast = found['accession'] if found['accession'] else found['name']
                ret_data = {
                        'blast_type' : blast_type,
                        'blast'      : blast.split('.')[0],
                        'name'       : found.get('name'),
                        'locus'      : found.get('locus'),
                        }
                return ret_data
            return None
        except KeyError:
            return None
    return None

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
                blast_match = get_blast_dict(line[0])
                if blast_match:
                    blast_no = blast_match['blast']
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
