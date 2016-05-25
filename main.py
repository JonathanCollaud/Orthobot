#orthobot

from OrthoBot_login import *
from parser import *
from orthocheck import *

ortochecker = Orthocheck()

URL_list = ['Jules_Monnerat']
for pagename in URL_list: #pagename_to_check:
    URL = "http://wikipast.world/wiki/index.php/" + pagename
    # URL_list.append(URL)

    print URL
    
    # t = time.time()
    # print "Start time: " + str(t)

    words_parsed = clean_parse(URL)

    t = time.time()

    # update the Ortocheck object with current page
    ortochecker.update_page(pagename, words_parsed)

    # False to remove words numbers
    print ortochecker.wiki_section(False)
    print time.time() - t

    # result = requests.post(baseurl+'api.php?action=query&titles='+pagename+'&export&exportnowrap')
    # soup = BeautifulSoup(result.text,'html.parser')
    # content = ""
    # for primitive in soup.findAll("text"):
    #     content += primitive.string
    
    # content += ortochecker.wiki_section()
    # print(content)