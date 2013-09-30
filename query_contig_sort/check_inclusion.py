"""Given a csv file of blasts, check for blasts that mach the passed set and store the identity and DNA sequence associated with it"""

import csv
import os, sys
import re
from path import path
from collections import namedtuple

Identity = namedtuple('Identity', ['name','dna'])

# create unbuffered stdout so updates print nicely


re_query_contig = re.compile(r"^Query_contig_.+$")


def format_fasta(identity):
    sequence = identity.dna
    split_sequence = ["\n>" + identity.name]
    while sequence:
        split_sequence += [sequence[:79],]
        sequence = sequence[79:]
    return split_sequence


def check_inclusion(data_file, output_folder, verbose=False):
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
        match_list = []
        for num, line in enumerate(csv_reader):
            cur_percent = int((float(fd.tell()) / data_file_size) * 100)
            if cur_percent != last_percent:
                if verbose:
                    print "{0}%".format(cur_percent)
            last_percent = cur_percent

            # Is this a new Identity?
            blast_match = re_query_contig.search(line[0])
            if not blast_match:
                if data_column is None:
                    if len(line) > 2 and line[2]:
                        data_column = 2
                    else:
                        data_column = 1
                # Reset list on new idenity
                if identity_old != identity:
                    match_list = []
                identity_old = identity
                identity = Identity(line[0], line[data_column])
            else:
                query_name = line[0]
                if query_name in match_list:
                    continue
                else:
                    match_list.append(query_name)
                    # write line(s) to file
                    with open(output_folder / query_name + '.fasta','a') as output_fd:
                        output_fd.write('\n'.join(format_fasta(identity)))
                        output_fd.flush()


if __name__ == '__main__':
    from main import main
    main(sys.argv)
