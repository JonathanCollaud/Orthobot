#Orthobot

import urllib2
import json
import requests
from bs4 import BeautifulSoup
from OrthoBot_login import *

pagename='Ortobottest' #page de test, a changer par le reel pagename

#change content
result=requests.post(baseurl+'api.php?action=query&titles='+pagename+'&export&exportnowrap')
soup=BeautifulSoup(result.text,'lxml')
content=''
for primitive in soup.findAll("text"):
        content+=primitive.string
        print(content)
# content += '\n' + 'something new'
test = u"""
<code>== Possibles fautes d'orthographe ==
''par OrthoBot''
* genevois NOFAUTE
* Nestle
* Monnerat
* Vevey
* repreneurs
Si un mot n'est pas une faute d'orthographe : ajouter 'NOFAUTE' juste apres celui-ci.
Exemple : 'Lausanne' n'est pas une faute d'orthographe --> 'Lausanne NOFAUTE'</code>
"""
content += test
# content += ortochecker.wiki_section()
headers={'content-type':'application/x-www-form-urlencoded'}
payload={'action':'edit','assert':'user','format':'json','text':content,'title':pagename,'token':edit_token}
r4=requests.post(baseurl+'api.php',headers=headers,data=payload,cookies=edit_cookie)
print(r4.text)
