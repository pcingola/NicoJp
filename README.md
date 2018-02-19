# Nico JP

Scripts for Nico's JP processes

### Quiebra

Split input files into required fields.

- First version using PowerShell (yuck!)
- Python version


# Python version

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

# Environment setpup

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
