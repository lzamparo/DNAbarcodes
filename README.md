# DNAbarcodes
### Simple generator of DNA barcodes for sequencing experiments

A pair of simple scripts to generate DNA barcodes with nice properties:
- arbitrary length of code
- a minimum Hamming distance between each code
- a GC content percentage upper and lower bound for each code
- a guarantee that no code will contain runs of longer than three of the same base

### Dependencies
- python 3.6 (though >3.4 may work)
- Numba 0.36
- Numpy > 1.12

Best best is to use an Anaconda python distribution.  Anaconda 5.0.1 of Python 3.6 worked out of the box for me.

### Usage

There are two scripts: `generate_barcodes.py` and `validate_barcodes.py`.  `generate_barcodes.py` takes a length and filename, and outputs all possible codes of that length:

```
$ python generate_barcodes <length> <output file>
```

Once the potential barcode strings have been generated, you can run `validate_barcodes.py` to get your barcodes by specifying the file of all possible codes, the name where your barcodes should be written, and how many barcodes you need:

```
$ python validate_barcodes <input file> <output file> <number of codes>
```
