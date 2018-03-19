#!/usr/bin/env python

import pandas as pd
import argparse

# Default input & output file names
in_file = "in.txt"
out_file = "out.txt"


def parse_commnad_line_args():
    """
    Parse command line arguments
    """
    parser = argparse.ArgumentParser(description='Process input "Quibra" formatted files.')
    parser.add_argument('-i', '--infile', metavar='infile.txt', type=str, help='Input (txt) file', default=in_file)
    parser.add_argument('-o', '--outfile', metavar='outfile.txt', type=str, help='Output file', default=out_file)
    args = parser.parse_args()
    return (args.infile, args.outfile)


def process(in_file, out_file):
    """
    Process: Parse input file and create output file
    Args:
      in_file  : Input file name (file in 'Quiebra' format)
      out_file : Output file name (writen as tab-separated TXT file)
    """
    df = pd.io.excel.read_excel(in_file, sheet_name=0)
    print("XLS:" + str(df))


# ---
# Main
# ---
(in_file, out_file) = parse_commnad_line_args()  # Parse command line
process(in_file, out_file)  # Process file (parse input and write output file)
