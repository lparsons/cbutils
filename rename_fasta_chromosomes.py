#!/usr/bin/env python
''' Rename chromosomes in FASTA file based on specified chromosome map file'''

__version__ = "0.1"
__author__ = "Lance Parsons"
__author_email__ = "lparsons@princeton.edu"
__copyright__ = "Copyright 2011, Lance Parsons"
__license__ = "BSD 2-Clause License " \
    "http://www.opensource.org/licenses/BSD-2-Clause"


import sys
import os
import optparse
import fileinput


format_extensions = {
    'gff': 'tabular',
    'gtf': 'tabular',
    'bed': 'tabular',
    'txt': 'tabular',
    'tab': 'tabular',
    'tsv': 'tabular',
    'fa': 'fasta',
    'fasta': 'fasta'
}


def chromosome_map(mapfile=None):
    chromosome_map = dict()
    if mapfile is not None:
        fh = open(mapfile, 'rb')
        linenum = 1
        for line in fh:
            [k, v] = line.strip().split('\t')
            k = k.lstrip('>')
            if k in chromosome_map:
                raise DuplicateChromosomeError(k, linenum)
            else:
                chromosome_map[k] = v
            linenum += 1
    else:
        chromosome_map = {
            '1':  'chrI',
            '2':  'chrII',
            '3':  'chrIII',
            '4':  'chrIV',
            '5':  'chrV',
            '6':  'chrVI',
            '7':  'chrVII',
            '8':  'chrVIII',
            '9':  'chrIX',
            '10': 'chrX',
            '11': 'chrXI',
            '12': 'chrXII',
            '13': 'chrXIII',
            '14': 'chrXIV',
            '15': 'chrXV',
            '16': 'chrXVI',
            '17': 'chrMito',
            '18': '2-micron'
        }
    return chromosome_map


def main(argv=None):
    if argv is None:
        argv = sys.argv

    usage = "Usage: %prog [options] fasta_file [chromosome map file]"
    parser = optparse.OptionParser(usage=usage, version='%prog version ' +
                                   globals()['__version__'],
                                   description=globals()['__doc__'])
    parser.add_option('-f', '--format', default=None,
                      help="Force format to fasta or tabular. Default "
                      "is to use file extension.")
    parser.add_option('-c', '--column', default=1,
                      help="If tabular format, column number with id to "
                      "replace. [%default]")
    parser.add_option('-v', '--verbose',
                      action='store_true',
                      default=False, help='verbose output')
    try:
        (options, args) = parser.parse_args(argv[1:])
        if len(args) < 1:
            parser.error('Please specify fasta file')
    except SystemExit:  # Prevent exit when calling as function
        return 2

    try:
        if len(args) > 1:
            cmap = chromosome_map(args[1])
        else:
            cmap = chromosome_map()
    except DuplicateChromosomeError as e:
        sys.stderr.write("Invalid chromosome map file, duplicate chromosome "
                         "ids found in the first column\n%s\n" % e)
        return 3
    except Exception as e:
        sys.stderr.write("Problem parsing chromosome map file:\n%s\n" % e)
        return 4

    file_format = options.format
    if file_format is None:
        ext = os.path.splitext(args[0])[1].lstrip('.')
        file_format = format_extensions.get(ext)
    if file_format == 'fasta':
        replace_fasta_ids(args[0], cmap)
    elif file_format == 'tabular':
        replace_tabdelim_ids(args[0], cmap, options.column)
    else:
        sys.stderr.write("Unrecognized format or file extension: '%s'" %
                         file_format)

    return 1


def replace_fasta_ids(filename, cmap):
    '''Replace id string in fasta file using replace_keys dictionary'''
    for line in fileinput.input(filename):
        if line[0] == '>':
            old_id = line[1:].rstrip()
            new_id = cmap.get(old_id, old_id)
            line = '>%s\n' % new_id
        print line,


def replace_tabdelim_ids(filename, cmap, column_number=1):
    '''Replace id string in specified column of tab delimited
    file using replace_keys dictionary'''
    column_index = column_number - 1
    for line in fileinput.input(filename):
        line = line.rstrip()
        fields = line.split('\t')
        if (len(fields) >= column_number):
            fields[column_index] = cmap.get(fields[column_index],
                                            fields[column_index])
        print '%s\n' % '\t'.join(fields),


class DuplicateChromosomeError(Exception):
    """Exception raised when chromosome map contains duplicate keys.

    Attributes:
        chromosome -- chromosome id that is listed more than once
        linenum -- line number where the first duplicate appears
    """

    def __init__(self, chromosome, linenum):
        self.chromosome = chromosome
        self.linenum = linenum

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return("Duplicate Chromosome ID: "
               "%s found on line %i" % (self.chromosome, self.linenum))


if __name__ == '__main__':
    sys.exit(main())
