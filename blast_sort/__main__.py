#!/usr/bin/env python
# encoding: utf-8

import argparse
import sys
from path import path

from parse import read_file
from check_inclusion import check_inclusion

def main(argv):
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--blast_file', '-b')
    arg_parser.add_argument('--data_files', '-d', nargs='+')
    arg_parser.add_argument('--output_folder', '-o')
    if len(argv) == 1:
        argv.append('--help')
    args = arg_parser.parse_args(sys.argv[1:])
    output_folder = path(args.output_folder)
    # check that the output folder exists
    if not output_folder.exists():
        output_folder.mkdir()
    if not output_folder.isdir():
        print "{0} already exists and is not a directory.  please choose a directory or a new name"
        sys.exit(status=1)
    blast_set = read_file(args.blast_file)
    for data_file in args.data_files:
        check_inclusion(blast_set, data_file, output_folder)
    print "\n\nDONE! :)"

main(sys.argv)
