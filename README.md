sepsid_transcriptomes
=====================

Given a list of blast numbers (DNA and Proteins), and a set of data files
containing the data for various species (one species per datafile),
create output files (fasta format) for each blast number that contains all
the matching blasts from the supplied data files.

To install this as a command line program, check out the repo and install with:

    python setup.py install

This installs command line interface `blast_sort`.  use this by typing

    blast_sort --help

which will give you usage instructions.

remember, all data files must be in `.csv` format, not excel formats.


Changes
-------

#### 0.1.2
added nosetests for the blast number regex.
added -v --verbose tags for printing status (printing slows it down)
resturctured the main.py, added description and help to the options
made the options -b, -d, and -o required so the usage information is displayed
better support for finding blast numbers - the regex was limited to one type:
`gi|386767918|ref|NM_001259384.1|` (eg, ref, and requiring an underscore).
