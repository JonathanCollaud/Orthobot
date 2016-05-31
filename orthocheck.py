# -*- coding: utf-8 -*-

import codecs
import time
import csv
import re
from utils import *

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
    def __init__(self, section_name, botname = 'OrthoBot'):
        self.page_name1 = ''
        self.page_name2 = ''
        self.words = []
        self.dico = MultiDict()
        self.spewords_file = '_orthocheck_spewords.txt'
        self.spe_words = []
        with open(self.spewords_file) as swords:
            # self.spe_words = swords.read().split('\n')
            for word in swords:
                self.spe_words.append(word.strip().decode('utf-8'))
        self.DB_file = '_orthocheck_DB.txt'
        try:
            with open(self.DB_file, 'r') as dbwords: pass
        except IOError:
            # creates the database file is it doesn't exist
            with open(self.DB_file, 'w') as dbwords: pass
        self.DB_words = []
        with open(self.DB_file, 'r') as dbwords:
            # self.DB_words = dbwords.read().split('\n')
            for word in dbwords:
                self.DB_words.append(word.strip().decode('utf-8'))
        self.not_a_mistake = u'NOFAUTE'
        self.wiki_title = section_name
        self.wiki_author = botname.decode('utf-8')
        self.wiki_tuto = u"""Si un mot n'est pas une faute d'orthographe : ajouter '{no_mis}' juste après celui-ci dans la liste ci-dessus.
La prochaine fois que la page sera vérifiée, ce mot ne sera plus considéré comme une faute.
Exemple : 'Lausanne' n'est pas une faute d'orthographe --> 'Lausanne {no_mis}'.""".format(no_mis = self.not_a_mistake)
        self.wiki_no_mistake = u"cette page a été vérifiée, il semble n'y avoir aucune faute d'orthographe."
        self.html = ['<code>', '</code>']

        # here are two strings delimiting the 'zone' of orthocheck/orthobot in the wiki page
        self.start_str = wiki_text_sec(self.wiki_title)
        self.stop_str = self.html[1]

    def update_page(self, page_name, words_to_check):
        self.page_name1 = page_name.decode('utf-8')
        self.page_name2 = page_name.decode('utf-8').split('_')
        self.words = words_to_check

    def update_database(self, text_from_wiki):
        # words = re.findall(r"[\w'-]+", text_from_wiki)
        words = re.findall(r"[\w'-]+", text_from_wiki, re.UNICODE)
        with open(self.DB_file, 'a') as dbfile:
            for i in range(1, len(words)):
                if (words[i] == self.not_a_mistake) and (i > 0) \
                and not self.is_special(words[i-1]):
                    dbfile.write(words[i-1].encode('utf-8') + '\n')
            
        # update instance variable self.DB_words, just in case
        with open(self.DB_file, 'r') as dbfile:
            for word in dbfile:
                self.DB_words.append(word.strip().decode('utf-8'))

    def is_special(self, word):
        return word == self.page_name1 \
        or word in self.page_name2 \
        or word.lower() in self.spe_words \
        or word in self.DB_words

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
            return self.binary_compare() # mess with somewords...
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

    def wiki_section(self, with_numbers = False, htlm_code = True):
        """
        Returns the text ready to use to create a new section on wiki
        """
        if htlm_code:
            html = self.html
        else:
            html = ['', '']

        # wikitext = ['section title', 'section content']
        wikitext = '\n' + wiki_text_sec(self.wiki_title)
        wwords = self.compare_with_dico(4)
        if len(wwords) != 0:
            wikitext += '\n' + html[0] + ' par ' + wiki_text_it(self.wiki_author)
            i = 0
            while i < len(wwords):
                n = str(wwords[i]+1)
                w = wwords[i+1]
                if with_numbers:
                    wikitext += '\n* ' + w + ' (mot ' + n + ')'
                else:
                    wikitext += '\n* ' + w
                i += 2
            wikitext += '\n' + self.wiki_tuto + '\n' + html[1]
        else:
            wikitext += '\n' + html[0] + wiki_text_it(self.wiki_author) \
            + ' : ' + self.wiki_no_mistake + '\n' + html[1]
        return wikitext
    # ------------------------- #


# TESTS
def main():
    test = ['Skladowska', 'Lausanne', 'arbre', 'Varsovie', 'Genevois', 'CHF']

    print test

    # t = time.time()

    ortotest = Orthocheck()
    ortotest.update_page('test', test)

    # print time.time() - t

    # for w in test:
    #     print w
    #     print type(w)
    #     print ortotest.is_special(w)
    for w in ortotest.DB_words:
        print w
        print type(w)

if __name__ == "__main__":
    main()
