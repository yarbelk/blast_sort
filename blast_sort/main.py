import argparse
import sys, os
from path import path

from parse import read_file
from check_inclusion import check_inclusion

def main(argv):
    arg_parser = argparse.ArgumentParser(prog="blast_sort",
            description="A program to look up blast numbers and associated DNA/Protein data from a data file, check it against a list of blasts you want to compare, and save the output of all of the finds in fasta formated files named after the blast number")
    arg_parser.add_argument('--blast_file', '-b',
            required=True,
            help="csv lookup for blast nos")
    arg_parser.add_argument('--data_files', '-d', nargs='+',
            required=True,
            help="data files to search")
    arg_parser.add_argument('--output_folder', '-o',
            required=True,
            help="where to save the results")
    arg_parser.add_argument('--verbose', '-v', action='store_true',
            required=False,
            default=False, help="print status and completion rate")
    if len(argv) == 1:
        argv.append('--help')
    args = arg_parser.parse_args(argv[1:])
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w',0)
    output_folder = path(args.output_folder)
    # check that the output folder exists
    if not output_folder.exists():
        output_folder.mkdir()
    if not output_folder.isdir():
        print "{0} already exists and is not a directory.  please choose a directory or a new name"
        sys.exit(status=1)
    blast_set = read_file(args.blast_file)
    for data_file in args.data_files:
        check_inclusion(blast_set, data_file, output_folder, args.verbose)
    if args.verbose:
        print "\n\nDONE! :)"

