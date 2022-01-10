#! /bin/bash
### Qiyao modified a little bit based on modular cloning system in Thyer lab.
# Gonna filter cutting site for BsaI,BsmBI,AarI

### Shuffle the generated inputs, and apply simple rules to prune unwanted barcodes 
inputs=$1
outputs=$2

# Drop any barcodes with these substrings
BlpI="GCT[ACGT]{1}AGC"
BstXI="CCA[ACGT]{6}TGG"
BamHI="GGATCC"

gshuf $inputs | grep -v -E -e "$BlpI" -e "$BamHI" -e "$BstXI" > $outputs
