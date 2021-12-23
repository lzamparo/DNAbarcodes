import sys
import numpy as np
import numba
import time

str_to_num = {'A': 1, 'T': 2, 'G': 3, 'C': 4}
num_to_str = {1: 'A', 2: 'T', 3: 'G', 4: 'C'}

def _str_to_num(barcode):
    converted_list = [str_to_num[b] for b in barcode]
    return np.asarray(converted_list,dtype='int64')

def _num_to_str(array):
    converted_list = list(array)
    return [num_to_str[b] for b in converted_list]
    
def dna_to_numeric(batch):
    ''' convert list of barcode strings in batch to a numpy array '''
    numeric_batch = np.zeros((len(batch),barcode_len),dtype=np.int64)
    for i in range(len(batch)):
        numeric_batch[i,:] = _str_to_num(batch[i])
    return numeric_batch

def numeric_to_dna(numeric_batch):
    ''' convert numpy array of barcodes in batch to a list of strings '''
    batch = np.apply_along_axis(_num_to_str, axis=1, arr=numeric_batch)
    batch_list = batch.tolist()
    return [''.join(b) for b in batch_list]

def verify_mismatch_constraints(barcode, barcode_set, threshold=2):
    ''' test if the current barcode will be at least 2 mismatches away from any 
 element of the barcode set '''
    
    # broadcast substraction of barcode from each code in the barcode set
    if barcode_set.shape[0] > 0:
        mismatch_array = barcode_set - barcode
        mismatch_counts = np.count_nonzero(mismatch_array,axis=1)
        return mismatch_counts.min() >= threshold
    else:
        return True

def verify_content_constraints(barcode, low = 0.10, high = 0.90):
    ''' Make sure the GC content of the barcode lies in [low,high] 
    and also that there are no repetitive triples of any nucleotides '''
    gc_content = barcode[np.logical_or(barcode == 3, barcode == 4)].shape[0] / (1.0 * barcode_len)
    return (low < gc_content) & (gc_content < high)

@numba.jit(nopython=True)
def _verify_rep_constraint(barcode, run):
    for i in range((barcode.shape[0] - run.shape[0])+1):
        result = True
        for j in range(run.shape[0]):
                result = result and (barcode[i+j] == run[j])
        if result:
            return False    # found a run, reject this barcode
    return True             # did not find a run, accept this barcode

@numba.jit(nopython=True)
def verify_no_rep_constraints(barcode):
    ''' Ensure there are no runs of more than three consecutive bases '''
    result = True
    for i in range(1,5):
        result = result & _verify_rep_constraint(barcode, np.array([i,i,i]))
    return result

def process_batch(numeric_batch, barcodes, last_index=0, max_codes=80000):
    ''' apply validation rules to each potential barcode in the batch '''
    
    np.random.shuffle(numeric_batch)
    for barcode in numeric_batch:
        
        if last_index == max_codes:
            break
        
        if verify_mismatch_constraints(barcode, barcodes[0:last_index,:], mismatches) and \
           verify_content_constraints(barcode, gc_low, gc_high) and \
           verify_no_rep_constraints(barcode):
            barcodes[last_index,:] = barcode
            last_index += 1
            
    return last_index

            
# open the barcode file
all_barcodes_file = sys.argv[1]
validated_code_file = sys.argv[2]
max_codes = int(sys.argv[3])
barcode_len = int(sys.argv[4])
gc_low = float(sys.argv[5])
gc_high = float(sys.argv[6])
mismatches = float(sys.argv[7])

lines_per_batch = 10000

# bookkeeping for code array
last_index = 0

# grow the set of barcodes one by one, ensuring they are 3 mismatches apart
with open(all_barcodes_file,'r') as infile, open(validated_code_file,'w') as outfile:
    batch = []
    codes = np.empty((max_codes,barcode_len),dtype=np.int64)
    
    for line in infile:
        batch.append(line.strip())
        if len(batch) == lines_per_batch:
           
            if last_index >= max_codes:
                print("Found all codes, exiting")
                break
            
            print("beginning with ", last_index, " barcodes...")
            print("read ", len(batch), " lines")
            
            # convert to numpy
            batch_array = dna_to_numeric(batch)
            t0 = time.time()
            last_index = process_batch(batch_array, codes, last_index, max_codes)
            t1 = time.time()
            delta_t = t1 - t0
            batch = []
            print("result of batch processing is ", last_index, " qualified codes")
            print("time to process was: ", delta_t)
    
        
    # write out set of codes to outfile        
    str_codes = numeric_to_dna(codes[0:last_index,:])
    for code in str_codes:
        print(code, file=outfile)
