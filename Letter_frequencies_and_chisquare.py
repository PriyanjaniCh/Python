#! /usr/bin/python3

# Purpose:    Letter frequencies in Unicode file

# Execution:  Two text files are passed as arguments;
#             pride.txt in english and swann.txt in french 
#


import sys
import os

print('\nNumber of arguments: ', len(sys.argv))
print('Argument List: ', str(sys.argv), '\n\n\n')

# Validating the arguments passed
if len(sys.argv) != 3:
    print('Wrong number of arguments\n\n')
    exit()
file1 = sys.argv[1]
file2 = sys.argv[2]

def handling_files(file_name):
    
    
    # Opening the file with utf-8 encoding
    file = open(file_name, encoding = "utf-8-sig")
    line_count = 0

    vowel_count = {'a':0, 'e':0, 'i':0, 'o':0, 'u':0, 'y':0,
                '\u00e9':0,
                '\u00e2':0, 
                '\u00ea':0, 
                '\u00ee':0,
                '\u00f4':0,
                '\u00fb':0, 
                '\u00e0':0,
                '\u00e8':0,
                '\u00f9':0,
                '\u00eb':0,
                '\u00ef':0,
                '\u00ff':0,
                '\u00fc':0,
                '\u00e6':0,
                '\u0153':0}
    cons_count = 0 

    replace_french = {
                '\u00e9':'e',
                '\u00e2':'a', 
                '\u00ea':'e', 
                '\u00ee':'i',
                '\u00f4':'o',
                '\u00fb':'u', 
                '\u00e0':'a',
                '\u00e8':'e',
                '\u00f9':'u',
                '\u00eb':'e',
                '\u00ef':'i',
                '\u00ff':'y',
                '\u00fc':'u',
                '\u00e6':'ae',
                '\u0153':'oe'
                }
    vowel_cnt_replace = dict(vowel_count)
    cons_cnt_replace = 0
    char_count = 0
    letter_count = 0
    
    # Reading the file by line
    for line in file:
        # Converting the text to lower case 
        lines = line.lower()
        line_count += 1
        for word in lines:
            char_count += len(word)
            # Calculating frequencies before replacing french vowels 
            alpha_count = 0
            v_count = 0
            for letter in word:
                if letter.isalpha():
                    alpha_count += 1
                if letter in vowel_count:
                    vowel_count[letter] += 1
                    v_count += 1
            letter_count += alpha_count
            cons_count += (alpha_count - v_count)
        # For replacing french vowels in each word
        for word in lines:
            for letter in word:
                r = replace_french.get(letter)
                if r != None:
                    word = word.replace(letter,r)
            # Calculating frequencies after replacing french vowels 
            for letter in word:
                if letter.isalpha():
                    alpha_count += 1
                if letter in vowel_cnt_replace:
                    vowel_cnt_replace[letter] += 1
                    v_count += 1
            cons_cnt_replace += (alpha_count - v_count)
            
    file.close()
    #Printing Book Information
    print("\nBook:", file_name)
    print("Number of lines       = {:7d}".format(line_count))
    print("Number of characters  = {:7d}".format(char_count))
    print("\nNumber of Vowels      = {:7d}".format(sum(vowel_count.values())))
    print("Number of Consonants  = {:7d}".format(cons_count))
    print("Number of letters     = {:7d}".format(letter_count))

    return vowel_count, cons_count, vowel_cnt_replace, cons_cnt_replace
   
# Calculating the expected contingency table
# Arguments:  Actual contingency table
# Returns:    Expected contingency table

def calculate_expected(actual):
    column_sum = [ x + y for x, y in zip(actual[0],actual[1])]
    total_sum = sum(column_sum)
    
    expected1 = list(map(lambda x:(sum(actual[0])*column_sum[x])/total_sum,
                         range(len(column_sum))))
    expected2 = list(map(lambda x:(sum(actual[1])*column_sum[x])/total_sum,
                         range(len(column_sum))))
    expected = [expected1, expected2]
    return expected

# Calculating the chi-square value and degrees of freedom
# Arguments:  Actual and expected contingency tables
# Returns:    Chi-squared statistic and degrees of freedom
    
def calculate_chi_square(actual, expected):
    chi_square = 0
    for i in range(len(expected)):
        chi_square += sum(map(lambda x:((x[0]-x[1])**2)/x[1], 
                                      zip(actual[i], expected[i])))
    df = (len(actual)-1)*(len(actual[0])-1)
    return chi_square, df

# Calculating the statistics for experiment01
# Arguments:  Vowel and consonant frequencies of 2 files
# Returns:    Expected contingency table, chi square and df

def calculate_statistics_exp1(vowel_cnt1, cons_cnt1, vowel_cnt2, cons_cnt2):
    vowel1 = sum(vowel_cnt1.values())
    vowel2 = sum(vowel_cnt2.values())
    first_row = [vowel1, cons_cnt1]
    second_row = [vowel2, cons_cnt2]
    actual = [first_row, second_row]
    expected = calculate_expected(actual)
    chi_square, df = calculate_chi_square(actual, expected)
    return actual, expected, chi_square, df

# Calculating the statistics for experiment02
# Arguments:  Vowel frequencies of 2 files
# Returns:    Expected contingency table, chi square and df

def calculate_statistics_exp2(vowel_cnt_repl1, vowel_cnt_repl2):
    vowel1 = [vowel_cnt_repl1[k] for k in sorted(vowel_cnt_repl1)[:6]]
    vowel2 = [vowel_cnt_repl2[k] for k in sorted(vowel_cnt_repl2)[:6]]
    actual = [vowel1, vowel2]
    expected = calculate_expected(actual)
    chi_square, df = calculate_chi_square(actual, expected)
    return actual, expected, chi_square, df  
    

#Reading and processing files
vowel_cnt1, consonant_cnt1,vowel_cnt_repl1,cons_repl1 = handling_files(file1)
vowel_cnt2, consonant_cnt2, vowel_cnt_repl2, cons_repl2= handling_files(file2)

# Calculating chi-square statistics

#Experiment 1
print("\nExperiment 1")
actual1, expected1, chi_square1, df1 = calculate_statistics_exp1(vowel_cnt1, 
                                consonant_cnt1, vowel_cnt2, consonant_cnt2)
# Printing values for Experiment 1

print("\nActual:")
print("Book           Vowels     Consonants")
print("{:9}{:12d}{:12d}".format(file1, *actual1[0]))
print("{:9}{:12d}{:12d}".format(file2, *actual1[1]))

print("\nExpected:")
print("Book           Vowels     Consonants")
print(("{:9}   "+2*"{:12.2f}").format(file1, *expected1[0]))
print(("{:9}   "+2*"{:12.2f}").format(file2, *expected1[1]))

print("\nchi-square = {:.2f} with df = {:d}".format(chi_square1,df1))

#Experiment 2
print("\n\nExperiment 2")
actual2, expected2, chi_square2, df2 = calculate_statistics_exp2(
                                           vowel_cnt_repl1, vowel_cnt_repl2)

# Printing values for Experiment 2
print("\nActual:")
print(
"Book            a           e          i         o          u           y")
print(("{:9}"+6*"{:11d}").format(file1, *actual2[0]))
print(("{:9}"+6*"{:11d}").format(file2, *actual2[1]))

print("\nExpected:")
print(
"Book            a           e          i         o          u           y")
print(("{:9} "+6*"{:11.2f}").format(file1, *expected2[0]))
print(("{:9} "+6*"{:11.2f}").format(file2, *expected2[1]))

print("\nchi-square = {:.2f} with df = {:d}".format(chi_square2,df2))
