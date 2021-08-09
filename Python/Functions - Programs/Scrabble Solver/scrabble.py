# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 19:32:01 2021
@author: Viswanathan
Program: Scrabble helper
This program takes a Scrabble rack as a command-line argument and prints all 
"valid Scrabble English" words that can be constructed from that rack, along 
with their Scrabble scores, sorted by score. A Scrabble rack is made up 
of 2 to 7 characters. Only a maximum of two wildcards allowed on the rack with 
an individual limit of upto one of each "?" or "*" 
"""
import sys
import itertools

import wordscore


# Check if the rack is passed as an argument
# Check if the rack length is between 2 and 7 characters
if len(sys.argv) not in (2,3) or (len(sys.argv[1]) < 2 or len(sys.argv[1]) > 7):
    print('Plese provide a valid Scrabble rack of 2 to 7 characters as' \
          ' one arguement \nand if required a character and position number' \
          ' e.g. B3 as second optional argument')
    quit()

else:
    # Assign rack to wildrack
    wildrack = sys.argv[1].lower()  
    
    # Condition when two arguments with scrabble rack and
    # a character and position is input
    if len(sys.argv) == 3:
        # Get the argument for character and position
        userinput = sys.argv[2].lower()
        
        # Check if the argument is in form of B5 or D3 etc.
        try: 
            if (userinput[1].isdigit() 
                    and userinput[0].isalpha() 
                    and len(userinput) == 2):
                               
                # Assign alphabet and position 
                charposition = int(userinput[1])
                charinput = userinput[0].upper()
            else: 
                print('Positional alphabet argument should be in the form ' \
                  'of one alphabet and number')
                quit()        
        except:
            print('Positional argument example ' \
                  'like B3 or D4')
            quit()
            
    # Check if wilcard maximum is not exceeded 
    if wildrack.count('*') > 1 or wildrack.count('?') > 1:
        print("Only a maximum of 1 of each '?' or '*' wildcards are allowed")
        quit()
    
    # Count number of wildcards in the wildrack 
    wildcards = wildrack.count('?') +  wildrack.count('*')
    wildracklen = len(wildrack)
    
    # Create a cleanrack without wild cards and calculate length of clean rack
    cleanrack = wildrack.replace('*', '').replace('?', '')
    cleanracklen = len(cleanrack)
    
    # Check if all remaining characters in clean rack are alphabets
    if cleanrack.isalpha() == False and cleanrack != '':
        print("Only alphabets and valid wildcards '?' or '*' are allowed" \
              " for scrabble rack argument")
        quit()


# Initialize list for storing all possible word combinations of rack 
# Initialize list for storing all final validated words 
possible, final = [], []

# Open file with all valid words and store as list
with open("sowpods.txt","r") as infile:
    raw_input = infile.readlines()
    datalist = [datum.strip('\n') for datum in raw_input]

# If condition when only rack is provided   
if len(sys.argv) == 2:
    # Creat a list of all valid words which are less than or equal to 
    # rack characters
    validlist = [word for word in datalist if len(word) <= wildracklen]

# Else when rack and positional alphabet are provided    
else:
    # Creat a list of all valid words which are less than or equal to 
    # rack characters with matching alphabet in a position and the word is 
    # atleast the length of the position of fixed alphabet    
    validlist = [word 
                 for word in datalist 
                 if len(word) <= wildracklen 
                 and len(word) >= charposition 
                 and word[charposition-1] == charinput
                 ]
    
# Create a set of all valid words which are less than or equal to 
# rack characters
validset = {*validlist}

# The if block is executed if there are no wildcards in initial rack
# The if block is created as it is a little faster than else block for a rack 
# with no wildcards as validset is used to check words
if wildcards == 0:

    # Create a list of tuples of all possible permutations of the input rack 
    # alphabets    
    for i in range(2,8):
        possible.extend(list(itertools.permutations(cleanrack,i)))
    
    # Remove duplicates from all possible words list when rack contains 
    # repeated alphabets
    possible = list(set(possible))
        
    # Join the alphabets in the tuples and create a possible words list       
    for i in range(0,len(possible)):
        possible[i]=''.join(possible[i])
        
        # If the possible word formed is in the set of valid words, append 
        # word to final list
        if possible[i].upper() in validset and possible[i] not in final:
            final.append(possible[i])       
    
    try:
        # Call score_word function from wordscore module 
        # using the final words list and initial rack as arguments
        # Print the scored list of words
        for i in wordscore.score_word(final, wildrack):
            print('('+str(i[0])+', '+i[1]+')',end = '\n')       
                
        print('Total number of words:',len(final))
    
    except:
        print('Some unknown error, please try again')

else:    
    # The else block is executed if there are wildcards in initial rack
    # For each word in the full valid list of words compare if it can be 
    # created from rack letters       
    for word in validlist:                 
        testlist = list(cleanrack)
        
        # Compare if the valid word letters match the rack letter by popping 
        # rack letters
        for i in word.lower():
            for j in testlist:
                if i == j:
                    testlist.pop(testlist.index(j))
                    break
                
                else:
                    continue         
        
        # If there exists rack letters after popping and the number of letters 
        # is upto the 
        # number of wild cards on the rack (1 or 2)
        # Append each that word to final list 
        if len(word) - (cleanracklen - len(testlist)) <= wildcards:
            final.append(word.lower())        
    
    try:
        # Score the list of final words using score_word function in 
        # wordscore module
        result = wordscore.score_word(final, wildrack)
        
        # Format the result list      
        for i in range(len(result)):
            result[i] = '('+str(result[i][0])+', '+result[i][1]+')'     
        
        # Print the result list string
        print('\n'.join(map(str, result)))                       
        print('Total number of words:',len(final))
    
    except:
        print('Some unknown error, please try again')
