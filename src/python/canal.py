#!/usr/bin/env python

import pandas as pd
import argparse

# DEBUG mode?
DEBUG = True

# Default input & output file names
in_file = "data/example.xlsx"
out_file = "out.txt"

# Where the usefull information is
TITLE_ROW = 8  # Title
FIRST_ROW = TITLE_ROW + 1
FIRST_COLUMN = 1

# Columns that we should retrieve
BANK = "canal bancario"
PROVIDER = "fornecedor"
PROVIDER2 = "fornecedor 2"
AMOUNT = "valor"
CURRENCY = "moeda"
REQUIRED_COLUMNS = [PROVIDER, PROVIDER2, CURRENCY, AMOUNT, BANK]  # Make sure these values are lower case

# Summary 'total' lines end with this string
TOTAL_END_STRING = " total"


def is_total(name):
    """ Is this a summary line? """
    return name.lower().endswith(TOTAL_END_STRING)


def na2empty(v):
    """ Convert 'NA' to empty string """
    if pd.isna(v):
        return ''
    return v


def na2zero(v):
    """ Convert 'NA' to zero """
    if pd.isna(v):
        return 0
    return v


def parse_commnad_line_args():
    """ Parse command line arguments """
    parser = argparse.ArgumentParser(description='Process input "Quibra" formatted files.')
    parser.add_argument('-i', '--infile', metavar='infile.txt', type=str, help='Input (txt) file', default=in_file)
    parser.add_argument('-o', '--outfile', metavar='outfile.txt', type=str, help='Output file', default=out_file)
    args = parser.parse_args()
    return (args.infile, args.outfile)


def parse_line(row, colnums):
    """ Extract values from a row, return a dictionary """
    rowdict = dict()
    for k in colnums.keys():
        i = colnums[k]
        rowdict[k.lower()] = row[i]

    # Convert 'NA' to empty strings
    for k in [PROVIDER, PROVIDER2]:
        rowdict[k] = na2empty(rowdict[k])

    # Convert 'NA' to zeros
    for k in [AMOUNT]:
        rowdict[k] = na2zero(rowdict[k])

    return rowdict


def process(in_file, out_file):
    """
    Process: Parse input file and create output file
    Args:
      in_file  : Input file name (file in 'Quiebra' format)
      out_file : Output file name (writen as tab-separated TXT file)
    """
    # Read file
    df = pd.io.excel.read_excel(in_file, sheet_name=0)

    # Find and extract relevant column numbers
    df = remove_before_title(df)
    titles = df.iloc[0].values.tolist()
    colnums = required_column_nums(titles)

    # Create summary
    byprovider = process_rows(df, colnums)
    keys = list(byprovider.keys())
    keys.sort()
    for k in keys:
        print(k)


def process_rows(df, col_nums):
    """ Parse each row and return a dictionary with summary data by 'provider & currency' """
    byprovider = dict()
    for i in range(1, len(df)):
        row = parse_line(df.iloc[i].values.tolist(), col_nums)

        if is_total(row[PROVIDER]):
            pass  # Ignore 'total' lines
        else:
            prov = str(row[PROVIDER]) + "\t" + str(row[CURRENCY])
            if DEBUG:
                print("provider: '{0}'\tamount: {1:f}".format(prov, byprovider.get(prov, 0), row[AMOUNT]))
            byprovider[prov] = byprovider.get(prov, 0) + row[AMOUNT]

    return byprovider


def remove_before_title(df):
    """ Remove unwanted columns and rows """
    return df.iloc[TITLE_ROW:, FIRST_COLUMN:]


def required_column_nums(titles):
    """ Find column numbers from REQUIRED_COLUMN names, return a map """
    col_nums = [i for i in range(0, len(titles)) if str(titles[i]).lower() in REQUIRED_COLUMNS]
    if len(col_nums) != len(REQUIRED_COLUMNS):
        raise Exception(("Could not find all required columns in input XLS " +
                         "'{0!s}'\n\tRequired columns: {1!s}" +
                         "\n\tColumn titles: {2!s}" +
                         "\n\tFound: {3!s}").format(
                        in_file, REQUIRED_COLUMNS, titles, col_nums)
                        )

    # Create a dictionary
    colnum = dict()
    for i in col_nums:
        colnum[titles[i]] = i

    if DEBUG:
        print("titles: " + str(titles))
        print("col_nums: " + str(col_nums))

    return colnum


# ---
# Main
# ---
(in_file, out_file) = parse_commnad_line_args()  # Parse command line
process(in_file, out_file)  # Process file (parse input and write output file)
