# Nico JP

Scripts for Nico's JP processes

# Quiebra

### Power shell version

Split input files into required fields.
First version using PowerShell (yuck!)

### Python version

Python version accepts input/output files as command line arguments
```
$ python quiebra.py -h
usage: quiebra.py [-h] [-i infile.txt] [-o outfile.txt]

Process input "Quibra" formatted files.

optional arguments:
  -h, --help            show this help message and exit
  -i infile.txt, --infile infile.txt
                        Input (txt) file
  -o outfile.txt, --outfile outfile.txt
                        Output file

```

So, to run the example input file, you can do:
```
$ cd NicoJp
$ ./src/python/quiebra.py -i data/in.txt -o data/out.txt
PppP	AaaaaaaaaaaaaaaaA	NnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnN	CC	CccccccccC	AaaaaaaaaaaaaaA
PpP	AaaaaaaaaaA	NnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnN	C	CccccC	AaaaaA
PpP	AaaaaA	NnnnnnnnnnnnnnnnN	C	CcccC	AaaaaaaaaA
```

### Environment setpup

Currently using Python 3, if you have mutiple python verisons, you can create a virtual environment:

```
# Create virtual Env
cd NicoJp
virtualenv -p python3 .
```

To cativate the virtual environment, do the usual:
```
cd NicoJp
./bin/activate
```

# Canal (Python)

This programs parses a (messier) XLS file using only one cell for all bank data

### Requirements

Language
* Python 3

Pip moules:
* Pandas
* xlrd

### Parsing rules for Bank:

Parsing rules:
- If `IBAN` exists, no need for other data
- If no `IBAN` is present, then `Account` is required
- If `SWIFT` is present, then no other information is required
- If no `SWIFT` is present, then we need `ABA`
- If neither `SWIFT` nor `ABA` exists, then `Bank name` is required

### Input formats (Banks field):

* SWIFT: From 8 to 11 alphanumeric chars. Always starts with a letter,
Specifically, it refers to ISO-9362 (Bank Identification Codes / BIC): https://en.wikipedia.org/wiki/ISO_9362
e.g.:

```
Swift:CRESPI33S
Swift number:CRESPI33S
Swift num: CRESPI33S
Swift Code: CRESPI33S
Swift Code CRESPI33S
Bic Code CRESPI33S
Bic CRESPI33S
Swift Code nr. CRESPI33S
Code number:CRESPI33S
Bic-code:CRESPI33S
```

* IBAN : IBAN is up to 34 alphanumeric chars. The first two are always letters. e.g:
```
IBAN: AT3920029282727
IBAN-NR. AT3920029282727
IBAN NO. AT3920029282727
IBAN-CODE:AT3920029282727
```

* Account number examples:
```
ACC NO: 382826277272
ACCOUNT #382826277272
ACCOUNT NO: 382826277272
A/C NR. 382826277272
CC 382826277272
```

* ABA number examples: ABA is a 9 digit number
```
Routing number: 098765451
ABA 098765451
```
