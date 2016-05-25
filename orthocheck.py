# -*- coding: utf-8 -*-

import codecs
import time
import csv
from bisect import bisect_left

# classes
class FrenchDict:
    """
    Attributs :
    - french dictionary as a list of words
    - names
    - names of cities
    - names of countries
    - names of cantons (from Switzerland)
    """
    def __init__(self):
        with codecs.open('gutenberg.txt', \
            encoding='mac_roman') as dwords:
            self.words = dwords.read().split('\r')
        # add some 1-char words and words containing 'œ' and 'æ'
        # to the dictionary
        one_chars = [u'c', u'l', u'd', u'y', u't', u's', u'n', u'qu']
        with codecs.open('liste_oe_ae.txt', encoding='utf-8') as oewords:
            oe_ae = oewords.read().split('\n')
        abrevs = [u'M', 'Mr', u'Mme', u'Ms', u'Mrs']
        self.words += one_chars + oe_ae + abrevs

        with codecs.open('liste_prenoms.txt', \
            encoding='mac_roman') as dwords:
            self.names = dwords.read().split('\n')

        self.countries = []
        cr = csv.reader(open('liste_pays.csv', 'rb'))
        for row in cr:
            self.countries.append(row[4].decode('utf-8'))

        self.cities = []
        cr = csv.reader(open('liste_villes_francaises.csv', 'rb'))
        for row in cr:
            self.cities.append(row[3].decode('utf-8'))

        with codecs.open('liste_cantons.txt', encoding='utf-8') as cwords:
            self.cantons = cwords.read().split('\n')

        self.symbols = [u'-', u'--']

class EnglishDict:
    """
    Attributs :
    - english dictionary as a list of words
    - for future version : proper names, surnames, etc...
    """
    def __init__(self):
        self.names = []
        with open('liste_names.txt', 'r') as nlist:
            for line in nlist:
                self.names.append(line[0:11].strip().lower().decode('utf-8'))

class MultiDict():
    def __init__(self):
        self.fdico = FrenchDict()
        self.edico = EnglishDict()
        self.fr_words = self.fdico.words
        self.all_words = self.fdico.words \
                       + self.fdico.names \
                       + self.fdico.countries \
                       + self.fdico.cities \
                       + self.fdico.cantons \
                       + self.fdico.symbols \
                       + self.edico.names

class Orthocheck:
    """
    Object to find incorrect spelling mistakes from a list of words
    Can return the same list with wrong words highlighted 
    (bold, for a wiki),
    or return a ready-to-use wikipedia section 
    containing the list of wrong words and their number in the list
    """
    def __init__(self, botname = 'OrthoBot', spefile = 'orthocheck_spewords.txt'):
        self.page_name = ''
        self.words = []
        self.dico = MultiDict()
        with codecs.open(spefile, encoding='mac_roman') as swords:
            self.spe_words = swords.read().split('\n')
        self.no_mistake = 'NOFAUTE'
        self.wiki_title = "Possibles fautes d'orthographe"
        self.wiki_author = 'par ' + botname
        self.wiki_tuto = u"""Si un mot n'est pas une faute d'orthographe : ajouter '{NOM}' juste après celui-ci.
Exemple : 'Lausanne' n'est pas une faute d'orthographe --> 'Lausanne {NOM}'""".format(NOM = self.no_mistake)

    def update_page(self, page_name, words_to_check):
        self.page_name = page_name
        self.words = words_to_check

    # def update_database(self, text_from_wiki):
    #     words = text_from_wiki.split(' ')
    #     for i in range(len(words)-1):
    #         if (word[i] == self.no_mistake) and (i > 0):
                

    def is_special(self, word):
        return word == self.page_name or word.lower() in self.spe_words

    def is_good(self, word):
        """
        A 'good' word is a word :
        - without any uppercase letters (considered as )
        - without any digit
        - wich is not in the uniwords attributs of self.dico
        """
        # if not self.is_special(word) and not digit_in(word):
        #     if word not in self.
        return not self.is_special(word) and not digit_in(word)

    def basic_compare(self, with_sort):
        """
        Comparison with dictionary using 'basic' comparison

        Returns a list of the form :
        [index of wrong word 1, wrong word 1, 
         index of wrong word 2, wrong word 2,
         etc, ...]
        """
        if with_sort:
            words = sorted(self.words)
        else:
            words = self.words
        wrongs = []
        n_all = len(self.dico.all_words)
        n_fr = len(self.dico.fr_words)
        word_index = 0
        next_start = 0
        for word in words:
            if self.is_good(word):
                found = False
                i = next_start
                while (not found) and (i < n_all):
                    if word == self.dico.all_words[i]:
                        found = True
                        next_start = i if with_sort else 0
                    elif (word.lower() == self.dico.fr_words[i]) and (i < n_fr):
                        found = True
                        next_start = i if with_sort else 0
                    else:
                        i += 1
                if (not found) and (word not in wrongs):
                    wrongs.append(word_index)
                    wrongs.append(word)
            word_index += 1
        return wrongs

    def index_compare(self):
        """
        Comparison with dictionary using .index() function

        Returns a list of the form :
        [index of wrong word 1, wrong word 1, 
         index of wrong word 2, wrong word 2,
         etc, ...]
        """
        wrongs = []
        word_index = 0
        for word in self.words:
            if self.is_good(word):
                try:
                    self.dico.all_words.index(word)
                except:
                    try:
                        self.dico.fr_words.index(word.lower())
                    except:
                        if word not in wrongs:
                            wrongs.append(word_index)
                            wrongs.append(word)
                    else:
                        pass
                else:
                    pass
            word_index += 1
        return wrongs

    def in_compare(self):
        """
        Comparison with dictionary using 'in' operator

        Returns a list of the form :
        [index of wrong word 1, wrong word 1, 
         index of wrong word 2, wrong word 2,
         etc, ...]
        """
        wrongs = []
        word_index = 0
        for word in self.words:
            if self.is_good(word):
                if word not in self.dico.all_words:
                    if word.lower() not in self.dico.fr_words \
                    and (word not in wrongs):
                        wrongs.append(word_index)
                        wrongs.append(word)
            word_index += 1
        return wrongs

    def binary_compare(self):
        """
        Comparison with dictionary using binary search

        Returns a list of the form :
        [index of wrong word 1, wrong word 1, 
         index of wrong word 2, wrong word 2,
         etc, ...]
        """
        wrongs = []
        word_index = 0
        for word in self.words:
            if self.is_good(word):
                index = binary_search(word, self.dico.all_words)
                # index = binary_search2(self.dico.words, word.lower())
                if index == -1:
                    index = binary_search(word.lower(), self.dico.fr_words)
                    if index == -1 and (word not in wrongs):
                        wrongs.append(word_index)
                        wrongs.append(word)
            word_index += 1
        return wrongs

    def compare_with_dico(self, comparison_type):
        """
        Comparison with dictionary using :
           1 : basic comparison (with sorting)
           2 : basic comparison (without sorting)
           3 : binary search
           4 : list.index() function
           4 : 'in' operator

           From better to worst (time of execution) :
           3 << 4 < 5 << 1 < 2
           but 3 could lead to some unexpected results
        """
        if comparison_type == 1:
            return self.basic_compare(True)
        elif comparison_type == 2:
            return self.basic_compare(False)
        elif comparison_type == 3:
            return self.binary_compare()
        elif comparison_type == 4:
            return self.index_compare()
        elif comparison_type == 5:
            return self.in_compare()


    # ------------------------- #
    # FUNCIONS TO CALL IN MAIN.PY
    def words_with_wrongs(self):
        """
        Returns the initial list of words
        with wrong words in bold (in a wiki way)
        """
        wwords = self.compare_with_dico(4)
        new_words = self.words
        i = 0
        while i < len(wwords):
            new_words[wwords[i]] = wiki_text_bf(wwords[i+1])
            i += 2
        return new_words

    def wiki_section(self, with_numbers):
        """
        Returns the text ready to use to create a new section on wiki
        """
        wwords = self.compare_with_dico(4)
        wikitext = ''
        if len(wwords) != 0:
            wikitext += wiki_text_sec(self.wiki_title)
            wikitext += '\n' + wiki_text_it(self.wiki_author)
            i = 0
            while i < len(wwords):
                n = str(wwords[i]+1)
                w = wwords[i+1]
                if with_numbers:
                    wikitext += '\n* ' + w + ' (mot ' + n + ')'
                else:
                    wikitext += '\n* ' + w
                i += 2
        wikitext += '\n' + self.wiki_tuto
        return wikitext
    # ------------------------- #


#########

# other functions
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

def binary_search2(a, x, lo=0, hi=None):   # can't use a to specify default for hi
    hi = hi if hi is not None else len(a) # hi defaults to len(a)   
    pos = bisect_left(a,x,lo,hi)          # find insertion position
    return (pos if pos != hi and a[pos] == x else -1) # don't walk off the end


#########

# TESTS
def main():
    test = ['aga', 'zub', 'arbre', 'avion', '34', 'age45', 
            'imeuble', 'wagon', 't4re', 'monndes', 'avouer',
            'avérer', 'montrèrent', 'Alphonse', 'esSaitr', 'Paris']

    print test

    # t = time.time()

    ortotest = Orthocheck(test)

    # print time.time() - t

    print ortotest.wiki_section(True)

if __name__ == "__main__":
    main()
