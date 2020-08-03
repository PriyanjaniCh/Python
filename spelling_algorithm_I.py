#!/usr/bin/python3

# Purpose:     Bulid a json file from a real world dataset that will
#              be used to implement Kernigan's spelling algorithm.

# Execution:   ./spelling_algorithm_I.py ap88.txt (one argument - not mandatory)

# The file ap88.txt contains 224M bytes of the AP ’88 corpus

import sys
import re
import time
import json
import operator
from string import punctuation
from collections import defaultdict

print('\nNumber of arguments: ', len(sys.argv))
print('Argument List: ', str(sys.argv), '\n\n\n')

# Validating the arguments passed
if len(sys.argv) > 2:
    print('Wrong number of arguments\n\n')
    exit()
if len(sys.argv) == 2:
    filename = sys.argv[1]
else:
    filename = '/home/python/spelling_algorithm/ap88.txt'
    
# Time before the start of file processing 
start_time = time.perf_counter()
start_cpu = time.process_time()

try:
    in_file = open(filename, 'r')
except IOError:
   print()
   print('Cannot open the file ', filename)
   print()
   exit()

# p = re.compile(r'^[AP]+\d*[-]+\d*')
   
# Initializing defaultdict's
unigram = defaultdict(int)
bigram = defaultdict(int)
words = defaultdict(int)

for line in in_file:
    # Replacing the tag
    line1 = re.sub(r'^[AP]+\d*[-]+\d*', '', line[:-1])
    # Replacing digits
    for i in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
        line1 = line1.replace(i, ' ')
    # Replacing punctuations
    for i in punctuation:
        line1 = line1.replace(i, ' ')
    # Changing the case of the line
    line1 = line1.lower()
    # Splitting the line
    for word in line1.split():
        words[word] += 1
        word1 = '<'+word+'>'
        # Adding keys and values into unigram defaultdict
        for letter in word1:
            unigram[letter]+=1
        # Adding keys and values into bigram defaultdict
        for i in range(len(word1)-1):
            bigram[word1[i:i+2]] += 1

# Closing the file
in_file.close()    
# Time after the end of file processing
stop_time = time.perf_counter()
stop_cpu = time.process_time() 

# Printing................

print('Number of unigrams:{:15d}'.format(len(unigram)))
print('Number of bigrams:{:16d}'.format(len(bigram)))
print()
print('Number of words:{:18d}'.format(sum(words.values())))
print('Number of distinct words:{:9d}'.format(len(words)))
print()

print('Top 10 words:')
# Sorting the words to print top 10 words
sorted_words = sorted(words.items(), key=operator.itemgetter(1), 
                                                        reverse = True)
for pair in sorted_words[:10]:
    print('{:10s} {:10d}'.format(pair[0], pair[1]))

elapsed_time = stop_time-start_time
cpu_time = stop_cpu-start_cpu
print()
print('Start time {:25.4f},  cpu time {:10.4f}'.format(start_time, start_cpu))
print('Stop time {:26.4f},  cpu time {:10.4f}'.format(stop_time, stop_cpu))
print('Total Elapsed time {:17.4f},  cpu time {:10.4f}'.format(
                                                    elapsed_time, cpu_time))
# Creating a final dictionary
final_dict = {}
final_dict['unigrams']=unigram
final_dict['bigrams']=bigram
final_dict['words']=words

# Dump the dictionary into a json file
with open('json-data.json', 'w') as file:
    json.dump(final_dict, file)
