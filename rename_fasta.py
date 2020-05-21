#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys


def main():
    """Main Fuction
    :returns: None

    """
    parser = argparse.ArgumentParser()
    parser.add_argument("dictionary", help="Dictionary of ids to translate "
                        "(from to)")
    parser.add_argument("fasta", help="Fasta file to translate (or use STDIN)",
                        nargs="?", default=None)
    args = parser.parse_args()

    if (args.fasta is not None):
        fasta = open(args.fasta)
    else:
        fasta = sys.stdin
    dictionary_file = open(args.dictionary)

    id_dict = {}
    for line in dictionary_file:
        (old, new) = line.strip().split("\t")
        id_dict[old] = new
    dictionary_file.close()

    for line in fasta:
        if line.startswith('>'):
            oldname = line[1:]
            if oldname not in id_dict:
                (oldname, desc) = oldname.split(" ", 1)
            if oldname in id_dict:
                newname = id_dict[oldname]
            else:
                newname = oldname
            sys.stdout.write(">%s\n" % newname)
        else:
            sys.stdout.write(line)

    fasta.close()
    if fasta is not sys.stdin:
        fasta.close()

if __name__ == "__main__":
    main()
