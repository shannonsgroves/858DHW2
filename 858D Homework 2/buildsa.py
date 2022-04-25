import numpy as np
from pysuffixarray.core import SuffixArray
import sys
import pickle
import random
from time import process_time


preftab = False 
k = 0
referenceFile = ''
outputFile = ''

if len(sys.argv) == 5:
    preftab = True
    k = int(sys.argv[2])
    referenceFile = sys.argv[3]
    outputFile = sys.argv[4]
elif len(sys.argv) == 3:
    referenceFile = sys.argv[1]
    outputFile = sys.argv[2]

file1 = open(referenceFile, 'r')
lines = file1.readlines()
file1.close()

random_base = random.choice("ACGT")

reference = "".join(lines[1:]).replace("\n", "").upper().replace("N",random_base)
print("Reference is length {}".format(len(reference)))
t1_start = process_time()
sa = SuffixArray(reference)
sa = np.array(sa.suffix_array())

file = { 'string': reference, 'SA': sa}

if preftab == True:
    #create prefix table
    file['preftab'] = {}
    current_prefix = ''
    i =0
    j=0
    index_count =0
    
    for sa_index in sa:
        if len(reference[sa_index:]) >= k:
            if not current_prefix == reference[sa_index:sa_index +k]:
                if  not current_prefix == '':
                    file['preftab'][current_prefix] = (i,j-1)
                if index_count == len(sa)-1:
                    file['preftab'][reference[sa_index:sa_index +k]] = (index_count,index_count)
      
                #set original indices for i and j
                j = index_count
                i = index_count
                current_prefix = reference[sa_index:sa_index +k]
            if index_count == len(sa)-1:
                file['preftab'][reference[sa_index:sa_index +k]] = (i,index_count)
            #as long as it is the same prefix increase j    
            j +=1
          
        index_count += 1
    
t1_stop = process_time()
print("Elapsed build time {} seconds".format(round(t1_stop-t1_start, 2)))


f = open(outputFile, 'wb')
serial_grades = pickle.dump( file , f, pickle.HIGHEST_PROTOCOL)
f.close()

