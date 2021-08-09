# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 13:57:32 2021
@author: Viswanathan
Module: Score words
This moduule has a score_word function that takes a list of words and the 
initial rack as arguments and scores the words. The function returns a sorted 
list of scored words.
"""
# Score of each alphabet
scores = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2,
         "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3,
         "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1,
         "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4,
         "x": 8, "z": 10}


def score_word(wordlist, wildrack):    
        
    # Create an empty dictionary to store words and scores
    scoredict = {}    
    
    # For each word in word list calculate score
    for word in wordlist:
        # Initialize score as 0
        sumi = 0
        # Remove all duplicates from the word to be scored and store in comp
        comp = list(set(word.lower()))
        
        # For each letter in comp check if the count of the letter is equal 
        # or less than count of same letter is rack.         
        # If condition is met calculate score of letter times the count of 
        # letter in word
        for i in comp:            
            if word.count(i)  <= wildrack.count(i):
                sumi += scores[i]*word.count(i)
            # If condition is not met calculate score of letter times the 
            # count of letter in rack
            # This is to account for not scoring words using wild cards 
            # from rack
            
            else:
                sumi += scores[i]*wildrack.count(i)
        
        # Add the score and word to the dictionary
        scoredict[word.lower()] = sumi 
    
    # Format, sort result into a list
    result = [(j,i) for i,j in scoredict.items()]
    result.sort(key = lambda x: (-x[0], x[1]))
    
    # Return the sorted and scored words list
    return result