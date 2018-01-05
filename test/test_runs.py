import numpy as np

def _verify_rep_constraint(barcode, run):
    for i in range((barcode.shape[0] - run.shape[0])+1):
        result = True
        for j in range(run.shape[0]):
                result = result and (barcode[i+j] == run[j])
        if result:
            return False    # found a run, reject this barcode
    return True             # did not find a run, accept this barcode

def verify_no_rep_constraints(barcode):
    ''' Ensure there are no runs of more than three consecutive bases '''
    result = True
    for i in range(1,5):
        result = result & _verify_rep_constraint(barcode, np.array([i,i,i]))
    return result

fail_beginning = np.array([1, 1, 1, 2, 3, 4, 3, 2, 3, 4, 2, 3])
fail_end = np.array([1,2,3,4,4,3,2,1,1,3,3,3])
fail_middle = np.array([1, 2, 2, 2, 1, 2, 3, 4, 3, 4, 3, 4])
pass_wherever = np.array([1,2,3,4,3,2,3,4,3,2,1,2])

verify_no_rep_constraints(pass_wherever)

codes = [fail_beginning, fail_end, fail_middle]
results = [verify_no_rep_constraints(c) for c in codes]
for r in results:
    print(r)
    
    