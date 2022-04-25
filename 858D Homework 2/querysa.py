import numpy as np
import sys
import pickle
from time import process_time

index = sys.argv[1]
queries = sys.argv[2]
queryMode = sys.argv[3]
output = sys.argv[4]

f = open(index, 'rb')
data = pickle.load(f)

reference = data['string']
reference += "$"
#print("Reference is {}".format(reference))
sa = data['SA']

preftab ={}
if 'preftab' in data.keys():
    preftab = data['preftab']

queryFile = open(queries, 'r')
lines = "".join(queryFile.readlines()).split(">")

queriesDictionary = {}
queriesOutput = {} 

for line in lines[1:]:
    name = line.split("\n")[0]
    sequence = line.split("\n")[1]
    queriesDictionary[name] = sequence


if queryMode == "naive":
    for name in queriesDictionary:
        t1_start = process_time() 
        sequence = queriesDictionary[name]
        print("Query length {}".format(len(sequence)))
        l =0
        r = len(reference) - 1
        
        if not preftab == {}:
            for prefix in preftab:
                if sequence.startswith(prefix):
                    l = preftab[prefix][0]
                    r = preftab[prefix][1]
        

        if sequence <= reference[sa[0]:] or sequence > reference[sa[len(reference)-1]:]:
            queriesOutput[sequence] = [0]
            #print("string {} appears 0 times".format(sequence))
        elif r-l == 0:
            queriesOutput[sequence] = [1, l, r]
            #print("string {} appears 1 time".format(sequence))
        elif r-l == 1:
            queriesOutput[sequence] = [2, l, r]
            #print("string {} appears 2 times".format(sequence))      
        else: 
            while r-l >1:
                c = int((l+r)/2)
                if sequence <= reference[sa[c]:] :
                    r = c
                else:
                    l =c
                
            string_left = r
            #print("string_left is {}".format(string_left))
            l =string_left
            r = len(reference)-1
            
            while r-l >1:
                c = int((l+r)/2)  
                if sequence <= reference[sa[c]:] :
                    r = c
                else:
                    l =c
        
            if not reference[sa[r]:].startswith(sequence):
                r = string_left
                
            queriesOutput[sequence] = [r-string_left+1, string_left, r]
            #print("string {} appears {} times".format(sequence, r-string_left+1))
        t1_stop = process_time()
        print("Elapsed query time {} seconds".format(round(t1_stop-t1_start, 2)))


def lcp(string1 , string2):
    i=0

    while i < min(len(string1), len(string2)):
        if string1[i] != string2[i]:
            break
        i = i+1
        
    return string1[:i]


if queryMode == 'simpaccel':
    
    for name in queriesDictionary:
        t1_start = process_time()
        sequence = queriesDictionary[name]
        print("Query length {}".format(len(sequence)))
        l = len(lcp(reference[sa[0]:], sequence))
        r = len(lcp(reference[sa[len(reference) -1]:], sequence))

        L = 0
        R = len(reference) -1
        m = 0

        if not preftab == {}:
            for prefix in preftab:
                if sequence.startswith(prefix):
                    L = preftab[prefix][0]
                    R = preftab[prefix][1]
        
        if sequence <= reference[sa[0]:] or sequence > reference[sa[len(reference)-1]:]:
            queriesOutput[sequence] = [0]
            #print("string {} appears 0 times".format(sequence))
        elif R-L == 0:
            queriesOutput[sequence] = [1, l, r]
            #print("string {} appears 1 time".format(sequence))
        elif R-L == 1:
            queriesOutput[sequence] = [2, l, r]
            #print("string {} appears 2 times".format(sequence))
        else: 

            while R - L > 1:
                M = int((L+R)/2)

                if l >= r:
                    
                    if len(lcp(reference[sa[M]:], reference[sa[L]:])) >= l:
                        m = l + len(lcp(reference[sa[M]+l:], sequence[l:]))
                    else:
                        m = len(lcp(reference[sa[M]:], reference[sa[l]:]))
                else:
                    if len(lcp(reference[sa[M]:], reference[sa[R]:])) >= r:
                        m = r +  len(lcp(reference[sa[M]+r:], sequence[r:]))
                    else:
                        m =  len(lcp(reference[sa[M]:], reference[sa[R]:]))

                if m == len(sequence) or sequence[m:] <= reference[sa[M] + m:]:
                    R = M
                    r =m
                else:
                    L = M
                    l =m

            string_left = R
            l =string_left
            r = len(reference)-1
            
            while r-l >1:
                c = int((l+r)/2)
                if sequence <= reference[sa[c]:] :
                    r = c
                else:
                    l =c
                    
            if not reference[sa[r]:].startswith(sequence):
                r = string_left

            queriesOutput[sequence] = [r-string_left+1, string_left, r]
            #print("string {} appears {} times".format(sequence, r-string_left+1))
        t1_stop = process_time()
        print("Elapsed query time {} seconds".format(round(t1_stop-t1_start, 2)))

outputFile = open(output, 'w')
string = ""

for name in queriesDictionary:
    string += name + " "
    sequence = queriesDictionary[name]
    string += str(queriesOutput[sequence][0]) + " "

    for x in range(0, queriesOutput[sequence][0]):
        string_left = queriesOutput[sequence][1]
        hit = string_left + x
        string += str(hit) + " "
        
    string += "\n"
    


outputFile.write(string)
    
            
                    






    
    



            

       
    




