#!/usr/bin/env python

import argparse

# Default input & output file names
in_file = "in.txt"
out_file = "out.txt"

# Field numbers
page_start = 2
page_end = 6

amount_start = 25
amount_end = 42

name_start = 140
name_end = 189

country_start = 602
country_end = 604

swift_start = 700
swiftEnd = 710

account_start = 850
account_end = 865

# Get fiels into a Tuple List
fields = [(page_start, page_end), (amount_start, amount_end), (name_start, name_end), (country_start, country_end), (swift_start, swiftEnd), (account_start, account_end)]


def convert(l):
    """
    Convert input lines to output format
    Args:
       l (str) : Raw input line with fields delimited by positions in 'fields' tuples. Input line may contain trailing newline characters.
    Returns:
       str: A 'tab' delimited output string
    """
    lout = [extract(l, se) for se in fields]
    return '\t'.join(lout)


def extract(l, se):
    """
    Extract a field from an input line
    Args:
       l (str) : Raw input line with fields delimited by positions in 'fields' tuples. Input line may contain trailing newline characters.
       se (tuple): A tuple with the delimiting start and end coordinates to extract.
    Returns:
       str: A string to be used as output. Input whitespaces and newline characters are remvoved
    """
    return l[se[0]:se[1]].strip()


# ---
# Main
# ---

parser = argparse.ArgumentParser(description='Process input "Quibra" formatted files.')
parser.add_argument('-infile', metavar='infile.txt', type=str, help='Input (txt) file', default=in_file)
parser.add_argument('-outfile', metavar='outfile.txt', type=str, help='Output file', default=out_file)

args = parser.parse_args()
in_file = args.infile
out_file = args.outfile
print("Input file  : '%0s'\nOutput file : '%1s'" % (in_file, out_file))

# Open file and read lines
with open(in_file) as fin, open(out_file, 'w') as fout:
    # Read file and get a list of lines
    lines = fin.readlines()

    # Process each line, convert to output format and print result
    for l in lines:
        lout = convert(l)
        print(lout)
        fout.write(lout + '\n')
