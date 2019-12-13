#!/usr/bin/python3

# Purpose:     To implement the Henderson method

# Execution:   One argument for start number can be passed 
#

import sys

print('\nNumber of arguments: ', len(sys.argv))
print('Argument List: ', str(sys.argv), '\n\n\n')

# Validating the arguments passed
if len(sys.argv) > 2:
    print('Wrong number of arguments\n\n')
    exit()
elif len(sys.argv) > 1:
    if int(sys.argv[1]) < 0:
        print('Argument passed is Negative \n\n')
        exit()
    start_number = int(sys.argv[1])
else:
    start_number = 1000

count = 0
i = 1
total = 0               # total spoken numbers
increment = 0           # total number of increments
result = []             # list for the calculated output

initial = []            # list for first two rows
initial.append(['decrement','current','count',''])
initial.append(['',str(start_number),'',''])

number = start_number
while True:
    number = number-i
    count = count+1
    if number % 10 == 0 :
        print_count = '*'*count
        result.append([i, number, count, print_count])
        i = i+1
        count = 0
    if number-i < 0:
        print_count = '*'*count
        if number != 0:
            result.append([i, number, count, print_count])
        break

# formats for lists initial and result 
format1 = '{:>10s}{:>10s}{:>10s}{}{:<14s}'
format2 = '{:>10d}{:>10d}{:>10d}{}{:<14s}'
for j in range(len(initial)):
    print(format1.format(initial[j][0],initial[j][1],initial[j][2],
        ' ',initial[j][3]))
for j in range(len(result)):
    print(format2.format(result[j][0],result[j][1],result[j][2],
        ' ',result[j][3]))

# calculating total spoken words and increment 
increment = len(result)
for j in range(len(result)):
    total = total + result[j][2]

print("\n\nThere were", total,"numbers spoken with",
        increment,"different increments.")
print("Average cycles/incr = {:0.2f}.".format((total/increment)))

passed = start_number-number
print("\n\nThere were", passed, "numbers passed by with",
        increment, "different increments.")
print("Average numbers/incr = {:0.2f}.".format(passed/increment))
