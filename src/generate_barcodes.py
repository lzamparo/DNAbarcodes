import sys

def allstrings(alphabet, length):
    """Find the list of all strings of 'alphabet' of length 'length'"""

    if length == 0: 
        return []

    c = [[a] for a in alphabet[:]]
    if length == 1: 
        return c

    c = [[x,y] for x in alphabet for y in alphabet]
    if length == 2: 
        return c

    for l in range(2, length):
        c = [[x]+y for x in alphabet for y in c]
        
    return c

if __name__ == "__main__":

    length = int(sys.argv[1])
    alphabet = ['A', 'C', 'G', 'T']
    outfile = sys.argv[2]

    my_strings = allstrings(alphabet, length)
    with open(outfile,'w') as barcodes:
        for s in my_strings:
            outstring = ''.join(s)
            print(outstring, file=barcodes)	
