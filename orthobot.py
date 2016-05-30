# -*- coding: utf-8 -*-

### ORTHOBOT main ###

# from OrthoBot_login2 import *
from OrthoBot_changecontent2 import *
from parser import *
from orthocheck import *

def main():
    section_name = u"Possibles fautes d'orthographe"
    orthochecker = Orthocheck(section_name)

    URL_done = []
    pagename_list = ['Henri_Dunant'] # usually given by OrthoBot_login
    print wiki_all_pagenames()
    # pagename_list = wiki_all_pagenames()
    # pagename_list = pagename_list[:10]
    # print pagename_list
    for pagename in pagename_list: #pagename_to_check:
        t = time.time()

        print "\nOrthoBot : traitement de la page " + pagename + '...'

        URL = "http://wikipast.world/wiki/index.php/" + pagename

        str1 = orthochecker.start_str
        str2 = orthochecker.stop_str
        removed_text = rm_content(pagename, str1, str2)

        print "\n==> Texte supprimé de la page " + pagename + ' : '
        print removed_text

        if removed_text != None:
            orthochecker.update_database(removed_text)

        words_parsed = clean_parse(URL)

        # update the Ortocheck object to the current page
        orthochecker.update_page(pagename, words_parsed)

        wiki_sec = orthochecker.wiki_section()

        print "\n==> Texte ajouté à la page " + pagename + ' : '
        print wiki_sec

        add_content(pagename, wiki_sec)

        delta_t = time.time() - t

        print "\n==> Temps écoulé (s) pour le traitement de la page " + pagename + ' : '
        print delta_t

        URL_done.append(URL)

    print "\nOrthoBot : les pages suivantes ont été vérifiées :"
    for url in URL_done:
        print url
    print '\n'


if __name__ == "__main__":
    main()