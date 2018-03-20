#!/usr/bin/env python

import argparse
import pandas as pd
import re

# DEBUG mode?
DEBUG = False

# Default input & output file names
in_file = "data/example.xlsx"
out_file = "out.txt"

# All SWIFT codes, listed in a TXT file (one per line)
swift_file = "data/swift_codes.txt"

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


class BankAccount:
    """ Bank including account, CBU, IBAN, SWIFT, etc. """

    def __init__(self, bank, swiftcodes=None):
        self.bank = bank
        self.swiftcodes = swiftcodes
        self.parse(bank)

    def parse(self, bank):
        self.aba = self.parse_aba(bank)
        self.account = self.parse_account(bank)
        self.cbu = self.parse_cbu(bank)
        self.iban = self.parse_iban(bank)
        self.swift = self.parse_swift(bank)

    def parse_aba(self, s):
        """ Parse ABA number information """
        m = re.search(r"(aba|routing)(\-|\s+)?(code|number|num|no|nr|#)?(\.)?\s*(:)?\s*(\w+)", s, flags=re.I)
        if m:
            return m.group(6)

        return ''

    def parse_account(self, s):
        """ Parse Account number information """
        m = re.search(r"(account|acct|acc|cc|a/c)(\-|\s+)?(code|number|num|no|nr|#)?(\.)?\s*(:)?\s*(\w+)", s, flags=re.I)
        if m:
            return m.group(6)

        m = re.search(r"(^|\s+)(\d)+((\-|\.|/|\s)+\d+)*(\s|$)", s, flags=re.I)
        if m:
            digits = [c for c in m.group(0) if c.isdigit()]
            return ''.join(digits)

        return ''

    def parse_cbu(self, s):
        """ Parse CBU information """
        m = re.search(r"(cbu)(\-|\s+)?(code|number|num|no|nr|#)?(\.)?\s*(:)?\s*(\w+)", s, flags=re.I)
        if m:
            return m.group(6)

        return ''

    def parse_iban(self, s):
        """ Parse IBAN information """
        m = re.search(r"(iban)(-|\s+)?(code|number|num|no|nr|#)?(\.)?\s*(:)?\s*(\w+)", s, flags=re.I)
        if m:
            return m.group(6)

        return ''

    def parse_swift(self, s):
        """ Parse SWIFT information """
        # Check against a databse of all SWIFT codes
        if self.swiftcodes:
            for m in re.finditer(r"([A-Z]{6}[A-Z0-9]{2})([A-Z0-9]{3})?", s, flags=re.I):
                swift = m.group(0)
                if self.swiftcodes.has(swift):
                    return swift

        # Search using 'swift' keywords
        m = re.search(r"(swift|bic|code)(-|\s+)?(code|number|num|no|nr|#)?(\.)?(-|\s+)?(code|number|num|no|nr|#)?(\.)?\s*(:)?\s*(\w+)", s, flags=re.I)
        if m:
            return m.group(9)

        # Not found
        return ''

    def __str__(self):
        sa = self.swift  # Swift or ABA
        if not sa:
            sa = self.aba

        ica = ''  # IBAN, CBU or Account. Prepend a '/' to IBA/CBU/Account
        if self.iban:
            ica = '/' + self.iban
        elif self.cbu:
            ica = '/' + self.cbu
        elif self.account:
            ica = '/' + self.account

        return "{0}\t{1}".format(sa, ica)


class Payment:
    """ Represents one payment line (in the XLS) """
    def __init__(self, dfrow, cols, swiftcodes):
        self.swiftcodes = swiftcodes
        self.parse_line(dfrow, cols)

    def add(self, payment):
        if self.currency != payment.currency:
            raise Exception("Currencies do not match:\n\t{0}\n\t{1}".format(
                            self, payment))
        self.amount = self.amount + payment.amount

    def is_total(self):
        """ Is this a summary line? """
        return self.provider.lower().endswith(TOTAL_END_STRING)

    def key(self):
        return self.provider + '\t' + self.currency

    def parse_line(self, row, colnums):
        """ Extract values from a row, return a dictionary """
        rowdict = dict()
        for k in colnums.keys():
            i = colnums[k]
            rowdict[k.lower()] = row[i]

        # Convert 'NA' to empty strings
        self.provider = na2empty(rowdict[PROVIDER])
        self.provider2 = na2empty(rowdict[PROVIDER2])
        self.amount = na2zero(rowdict[AMOUNT])
        self.currency = rowdict[CURRENCY]

        self.bank = na2empty(rowdict[BANK])
        (binter, bbenef) = self.split_bank(self.bank)
        self.bank_intermediary = BankAccount(binter, self.swiftcodes)
        self.bank_beneficiary = BankAccount(bbenef, self.swiftcodes)

    def split_bank(self, s):
        """ Parse beneficiary bank """
        minter = re.search(r"(intermediary|interm) bank\s*(:?)\s*(.*)", s, flags=re.I)
        mbenef = re.search(r"(beneficiary|benef) bank\s*(:?)\s*(.*)", s, flags=re.I)

        if mbenef and minter:
            si = minter.start(1)
            sb = mbenef.start(1)
            if sb < si:
                benef = s[mbenef.end(2):si]
                inter = minter.group(3)
            else:
                inter = s[minter.end(2):sb]
                benef = mbenef.group(3)
            return (inter, benef)

        if mbenef:
            inter = s[:mbenef.start(1)]
            benef = mbenef.group(3)
            return (inter, benef)

        if minter:
            benef = s[:minter.start(1)]
            inter = minter.group(3)
            return (inter, benef)

        return ('', s)

    def __str__(self):
        return "{0} {1}\t{2:f}\t{3}\t{4}\t{5}\t{6}".format(
               self.provider, self.provider2, self.amount,
               self.bank_beneficiary, self.bank_intermediary,
               self.currency, self.bank)


class SwiftCodes:
    """ SWIFT codes 'database' (TXT file) """
    def __init__(self, swiftfile=swift_file):
        self.swiftfile = swiftfile
        self.load(swiftfile)

    def has(self, swift):
        return swift in self.swiftcodes

    def load(self, swiftfile):
        with open(swiftfile) as f:
            lines = f.readlines()
            self.swiftcodes = set([l.strip() for l in lines])

    def __str__(self):
        return str(self.swiftcodes)


class XlsFile:
    """
    Represent the data in an XLS file.
    Parse and create payment output file (tab separated txt)
    """

    def __init__(self, in_file, out_file, swiftcodes):
        self.in_file = in_file
        self.out_file = out_file
        self.swiftcodes = swiftcodes
        self.process()

    def process(self):
        """
        Process: Parse input file and create output file
        Args:
          in_file  : Input file name (file in 'Quiebra' format)
          out_file : Output file name (writen as tab-separated TXT file)
        """
        # Read file
        self.xls = pd.io.excel.read_excel(self.in_file, sheet_name=0)

        # Find and extract relevant column numbers
        self.data = self.remove_before_title(self.xls)
        self.titles = self.data.iloc[0].values.tolist()
        self.colnums = self.required_column_nums(self.titles)

        # Create summary
        self.byprovider = self.process_rows()

    def process_rows(self):
        """ Parse each row and return a dictionary with summary data by 'provider & currency' """
        byprovider = dict()
        for i in range(1, len(self.data)):
            line = self.data.iloc[i].values.tolist()
            payment = Payment(line, self.colnums, self.swiftcodes)

            if payment.is_total():
                pass  # Ignore 'total' lines
            else:
                prov = payment.key()
                if prov in byprovider:
                    byprovider[prov].add(payment)
                else:
                    byprovider[prov] = payment

        return byprovider

    def remove_before_title(self, df):
        """ Remove unwanted columns and rows """
        return df.iloc[TITLE_ROW:, FIRST_COLUMN:]

    def required_column_nums(self, titles):
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

    def write(self):
        """ Write output file """
        print("Writing output file '{0}'".format(self.out_file))
        with open(self.out_file, "w") as fout:
            fout.write(str(self))

    def __str__(self):
        # Title
        out = ("Number\tProvider\tAmount" +
               "\tSWIFT/ABA (Beneficiary)\tIBAN / CBU / Account (Beneficiary)" +
               "\tSWIFT/ABA (Intermediary)\tIBAN / CBU / Account (Intermediary)" +
               "\tCurrency\tBank (raw)\n")

        keys = list(self.byprovider.keys())
        keys.sort()
        idx = 1
        for k in keys:
            out += str(idx) + '\t' + str(self.byprovider[k]) + '\n'
            idx = idx + 1
        return out


def parse_commnad_line_args():
    """ Parse command line arguments """
    parser = argparse.ArgumentParser(description='Process input "Quibra" formatted files.')
    parser.add_argument('-i', '--infile', metavar='infile.txt', type=str, help='Input (txt) file', default=in_file)
    parser.add_argument('-o', '--outfile', metavar='outfile.txt', type=str, help='Output file', default=out_file)
    parser.add_argument('-s', '--swiftfile', metavar='swiftfile.txt', type=str, help='Swift codes file', default=swift_file)
    args = parser.parse_args()
    return (args.infile, args.outfile, args.swiftfile)

# ---
# Main
# ---
if __name__ == '__main__':
    (in_file, out_file, swift_file) = parse_commnad_line_args()  # Parse command line
    swiftcodes = SwiftCodes(swift_file)
    xls = XlsFile(in_file, out_file, swiftcodes)  # Create input file
    xls.process()  # Process file (parse input and write output file)
    print(xls)
    xls.write()
