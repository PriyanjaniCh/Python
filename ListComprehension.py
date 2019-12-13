#!/usr/bin/python3

# Purpose:     Practice w/ list comprehensions and dicts

# Execution:   ./driver.py in with calling these functions
#

def alnum_fn(x):
    ''' Returns (boolean) whether the input value is alphanumeric'''
    out = x.isalnum()
    return out

def is_noun(x):
    ''' Returns (boolean) whether the input value is a Noun'''
    if len(x) >= 2:
        if (x[0:2] == 'NN'):
            return True
        else:
            return False
    else:
        return False

def is_even(x):
    ''' Returns (boolean) whether the input value is even'''
    if x % 2 != 0:
        return False
    else:
        return True

def add_one(input):
    ''' Returns the list by adding 1 to all the elements'''
    out = list(map(lambda x : (x+1), input))
    return out

def drop_bad(input):
    ''' Returns a list of elements with only alphabets '''
    out = list(filter(lambda x : x.isalpha(), input))
    return out

def show_nouns(input):
    ''' Returns a list of elements which are nouns'''
    out = list(filter(lambda x: is_noun(x[1]), input))
    return out
    
def is_noun_in_list(input):
    ''' Returns True even if there's one noun in a list
        written to use it internally for show_nouns2 & 3 '''
    out1 = list(filter(lambda x : is_noun(x), input))
    if len(out1) >= 1:
        return True
    else:
        return False

def show_nouns2(input):
    ''' Returns a list of the same format
        containing only the nouns in the original list  '''
    out = list(filter(lambda x : is_noun_in_list(x[1]), input))
    return out
        
def show_nouns3(input):
    ''' Returns a simple list containing only the nouns '''
    out1 = list(filter(lambda x : is_noun_in_list(x[1]), input))
    out = list(map(lambda x : x[0], out1))
    return out
    
def select_numbers(v1):
    ''' Returns a list containing one greater than than each even number in the list'''
    out = list(map(lambda x : (x+1), filter(lambda x: (x%2 == 0), v1)))
    return out

def show_count(input):
    ''' Returns the total number of entries in the sublists'''
    out = sum(map(lambda x: len(x), input))
    return out

def show_totals(input):
    ''' Returns a list where each sublist has been summed'''
    out = list(map(lambda x: sum(x), input))
    return out

def show_total(input):
    ''' Returns the sum of the values in the sublists'''
    out = sum(map(lambda x: sum(x), input))
    return out

def dot_product(input):
    ''' Returns the dot product of sublists for the given list'''
    product = sum(x*y for x,y in zip(input[0], input[1]))
    return product

def remove_dot(input):
    ''' Returns a list of words without the final punctuation mark'''
    out = input[:-1]
    return out

def produce_lower(input):
    ''' Returns a list with same sentence in lower case'''
    out =  list(map(lambda x: x.lower(), input))
    return out

def count_words(input):
    ''' Returns the number of distinct words in the sentence'''
    input = input[:-1]
    out = set(input)
    return len(out)

def avg_grade(input):
    ''' Returns the average grade for HW1 '''
    total = sum(map(lambda x: x[2][0], input))
    length = len(input)
    return total/length

def ugrad_points(input):
    ''' Returns the total number of points earned on HW2 by undergraduates'''
    ugrad = list(filter(lambda x: x[1]=='u', input))
    total = sum(map(lambda x: x[2][1], ugrad))
    return total
