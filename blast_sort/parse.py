"""
Parse the blast list into a set for comparsion with data sets
"""
__author__ = 'yarbelk & kathysufy'
import csv

def read_file(file_name):
    """Read the blast list csv file (excel dialect) and return it as a set"""
    blast_list = []

    with open(file_name, 'r') as fd:
        csv_reader = csv.reader(fd, dialect='excel')
        for line in csv_reader:
            blast_list = blast_list + line
    blast_set = set(blast_list)
    return blast_set

if __name__ == "__main__":
    import sys
    print sys.argv
    file_name = sys.argv[1]
    print read_file(file_name)