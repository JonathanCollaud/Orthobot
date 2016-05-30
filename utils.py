# -*- coding: utf-8 -*-

# some functions (principally used by orthocheck)
## test if a word contains digits or uppercase letters
def digit_in(word):
    return any(char.isdigit() for char in word)
def upper_in(word):
    return any(char.isupper() for char in word)

## some functions to format word in the 'wiki way'
def wiki_text_bf(word):
    return "'''" + word + "'''"
def wiki_text_it(word):
    return "''" + word + "''"
def wiki_text_sec(word):
    return "== " + word + " =="
def wiki_text_ssec(word):
    return "=== " + word + " ==="

## simple binary search algorithm
def binary_search(val, tab):
    found = False
    i_i = 0
    i_f = len(tab)-1
    if tab[i_i] == val:
        return i_i
    elif tab[i_f] == val:
        return i_f
    while (not found) and ((i_f - i_i) > 1):
        i_m = (i_i + i_f) / 2
        # print i_m
        found = (tab[i_m] == val)
        # print found
        if tab[i_m] > val:
            i_f = i_m
        else:
            i_i = i_m
    if tab[i_i] == val:
        return i_i
    elif tab[i_f] == val:
        return i_f
    else:
        return -1
