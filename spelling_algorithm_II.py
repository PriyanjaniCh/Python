#!/usr/bin/python3

# Purpose:     Build summary tables from a real world dataset that will
#              be used to implement Kernigan's spelling algorithm.

# Execution:   ./spelling_algorithm_II.py misspelled word (one argument)

# Uses json-data.json from spelling_algorithm_I.py 

import sys
import os
import json
import string
import operator

sys.path.insert(0, '/home/python/spelling_algorithm/')
import tables

from Correction import *

print()
print('Number of arguments: ', len(sys.argv))
print('Argument List: ', str(sys.argv), '\n\n\n')

# Validating the arguments passed
words = []
if len(sys.argv) > 1:
    for i in range(1,len(sys.argv)):
        words.append(sys.argv[i])
else:
    print('Misspelled words not mentioned!\n\n')
    exit()


# Pruning the list with dictionary and eliminating the unknown values 
# Arguments:  Lists created after performing each operation
# Returns:    List with only the possible words

def prune_list(possible_list):
    final_list = [w for w in possible_list if w[0] in dictionary['words']]
    return final_list

# Process the words and print all the required values 
# Arguments:  One word from the list of arguments passed
# Returns:    Nothing

def process_words(word):

    # Checking whether the entered argument is alphabetic 
    if (word.isalpha() == False):
        print('\nEntered word has non-alphabetic characters!')
        exit()

    print('\nCurrent word being corrested is:', word)
    
    # Storing the lower case letters in a list
    letters = list(string.ascii_lowercase)
    
    
    # INSERTION operation on the misspelled word
    insert_list = [[str(word[:i]+word[i+1:]), 'I', i, '-', word[i], 
                  word[i-1:i+1]+'|'+word[i-1]] for i in range(len(word))]
    
    #Pruning list of words created after INSERTION
    insert_final = prune_list(insert_list)
    
    print('\nNo. of possible corrections using insertion ', len(insert_list))
    print('After pruning the list contains ', len(insert_final))
    
    # DELETION operation on the misspelled word
    delete_list = []
    for j in letters:
        new = [[str(word[:i]+j+word[i:]), 'D', i, j,'-', 
                word[i-1]+'|'+word[i-1]+j ] for i in range(len(word)+1)]
      
        delete_list.extend(new)
    
    #Pruning list of words created after DELETION
    delete_final = prune_list(delete_list)
    
    print('\nNo. of possible corrections using deletion ', len(delete_list))
    print('After pruning the list contains ', len(delete_final))
    
    # SUBSTITUTION operation on the misspelled word
    substitute_list = []
    for j in letters:
        new = [[str(word[:i]+j+word[i+1:]), 'S', i, j, word[i], 
                word[i]+'|'+j] for i in range(len(word)) if word[i]!= j]
        substitute_list.extend(new)
    
    #Pruning list of words created after SUBSTITUTION
    substitute_final = prune_list(substitute_list)
    
    print()
    print('No. of possible corrections using substitution ', len(substitute_list))
    print('After pruning the list contains ', len(substitute_final))
    
    # TRANSPOSE operation on the misspelled word
    transpose_list = []
    for i in range(len(word)-1):
        word_list = list(word)
        error = word_list[i]+word_list[i+1]
        word_list[i], word_list[i+1] = word_list[i+1], word_list[i]
        correct = word_list[i]+word_list[i+1]
        new = ''.join([k for k in word_list])
        new_list = [new, 'T', i, correct, error, error+'|'+correct]
        transpose_list.append(new_list)
    
    #Pruning list of words created after TRANSPOSITION
    transpose_final = prune_list(transpose_list)
    
    print()
    print('No. of possible corrections using transposition ', len(transpose_list))
    print('After pruning the list contains ', len(transpose_final))
      
    print()
    
    # List for storing values related to all the operations  
    final_list = []
    
    # p_x_word = P( x | word)
    # p_word = P(word)
    # Calculating probabilities for DELETION
    for delete in delete_final:
        p = delete[2]
        w_p_1 = delete[0][p-1]
        w_p = delete[0][p]
        X = letters.index(w_p_1)
        Y = letters.index(w_p)
        numerator = tables.del_table[X][Y+1]
        p_x_word = numerator/bigrams[w_p_1+w_p]
        p_word = dictionary['words'][delete[0]]/total_words
        final_prob = p_x_word*p_word*1000000000
        delete.append(p_x_word)
        delete.append(p_word)
        delete.append(final_prob)
        final_list.append(Correction(delete))
    
    # Calculating probabilities for INSERTION
    for insert in insert_final:
        p = insert[2]
        ins = insert[5][:2]
        X = letters.index(ins[0])
        Y = letters.index(ins[1])
        numerator = tables.add_table[X][Y+1]
        p_x_word = numerator/unigrams[ins[0]]
        p_word = dictionary['words'][insert[0]]/total_words
        final_prob = p_x_word*p_word*1000000000
        insert.append(p_x_word)
        insert.append(p_word)
        insert.append(final_prob)
        final_list.append(Correction(insert))
    
    # Calculating probabilities for SUBSTITUTION                  
    for substitute in substitute_final:
        subs = substitute[4]
        error = substitute[3]
        X = letters.index(subs)
        Y = letters.index(error)
        numerator = tables.sub_table[X][Y+1]
        p_x_word = numerator/unigrams[error]
        p_word = dictionary['words'][substitute[0]]/total_words
        final_prob = p_x_word*p_word*1000000000
        substitute.append(p_x_word)
        substitute.append(p_word)
        substitute.append(final_prob)
        final_list.append(Correction(substitute))
    
    # Calculating probabilities for TRANSPOSITION
    for transpose in transpose_final:
        p = transpose[2]
        trans = transpose[3]
        X = letters.index(trans[0])
        Y = letters.index(trans[1])
        numerator = tables.transpose_table[X][Y+1]
        p_x_word = numerator/bigrams[trans]
        p_word = dictionary['words'][transpose[0]]/total_words
        final_prob = p_x_word*p_word*1000000000
        transpose.append(p_x_word)
        transpose.append(p_word)
        transpose.append(final_prob)
        final_list.append(Correction(transpose))
    
    # Sorting the list based on final probability
    newlist = sorted(final_list, key=lambda x: x.initial_list[-1], reverse=True)
    
    # Formats for printing the table header and values
    format1 = '{:<12}{:<8}{:<8}{:<9}{:<9}{:<8}{:<15}{:<15}{:<7}'
    format2 = '{:<12s}{:<8s}{:<8d}{:<9s}{:<9s}{:<8s}{:<15.10f}{:<15.10f}{:<7.6f}'
    
    # Printing header
    print(format1.format('Candidate','Error','Error','Correct','Error','x|w',
                         'P(x|word)','P(word)','10^9'))
    print(format1.format('Correction','Type','Pos','Letter','Letter','','','',
                         'P(x|w)P(w)'))
    
    print()
    # Printing sorted values in the list
    for line in newlist:
        values = line.get_values()
        print(format2.format(*values))
    print()
    
    # Extra Credit
    
    actual_list = []
    remove = []          # for removing the repeated rows
    # Updating the calculated probabilities
    for i in range(len(newlist)-1):
        new = []
        row1 = newlist[i].get_values()
        if i < len(newlist)-1:
            row2 = newlist[i+1].get_values()
        if row1[0]==row2[0]:
            remove.append(i+1)
            final_prob = row1[8]+row2[8]
            new.append(row1[0])
            new.append(final_prob)            
        else:
            new.append(row1[0])
            new.append(row1[8])
        actual_list.append(new)
    # Removing the 
    for i in remove:
       del actual_list[i]

    actual = sorted(actual_list, key=operator.itemgetter(1), reverse=True) 
    print()
    
    # Format for printing the new list
    format4 = '{:<15s}{:<7.6f}'
    
    # Printing header
    print('Candidate    ','10^9 * P(x|w) P(w)')
    
    # Printing the sorted actual values
    print()
    for line in actual:
        print(format4.format(line[0], line[1]))
    print()
    print()


    


# End of process_words function

# Loading the json file
with open('json-data.json') as json_file:
    dictionary=json.load(json_file)

total_words = sum(dictionary['words'].values())
distinct_words = len(dictionary['words'])
unigrams = dictionary['unigrams']
bigrams = dictionary['bigrams']

print('\nNumber of words:{:18d}'.format(total_words))
print('Number of distinct words:{:9d}'.format(distinct_words))

for word in words:
    process_words(word)
        
