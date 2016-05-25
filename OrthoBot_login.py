#orthobot

import urllib2
import json
import requests
from bs4 import BeautifulSoup

#Login

# Login params
user='Orthobot'
passw=urllib2.quote('Orthy')
baseurl='http://wikipast.world/wiki/'
login_params='?action=login&lgname=%s&lgpassword=%s&format=json'% (user,passw)

# Login request
r1=requests.post(baseurl+'api.php'+login_params)
login_token=r1.json()['login']['token']

#login confirm
login_params2=login_params+'&lgtoken=%s'% login_token
r2=requests.post(baseurl+'api.php'+login_params2,cookies=r1.cookies)

#get edit token2
params3='?format=json&action=query&meta=tokens&continue='
r3=requests.get(baseurl+'api.php'+params3,cookies=r2.cookies)
edit_token=r3.json()['query']['tokens']['csrftoken']

edit_cookie=r2.cookies.copy()
edit_cookie.update(r3.cookies)
    

#get all pages

#get the first 500 pages
result=requests.post(baseurl+'api.php?action=query&list=allpages&aplimit=500&format=xml')
soup=BeautifulSoup(result.text,'lxml')
#print(result.text)

#print names 
#find all p
pagename_to_check = []
for primitive in soup.findAll('p'):
    #print(primitive['title'])
    pagename_to_check.append(primitive['title'])
    newx=primitive['title']
        
#get all the other pages   
while True:
    result=requests.post(baseurl+'api.php?action=query&list=allpages&apfrom='+newx+'&aplimit=20&format=xml')
        #print(newx)
    soup=BeautifulSoup(result.text,'lxml')
        #print(result.text)

        #print names of all pages
        #find all p
    x=newx
    for primitive in soup.findAll('p'):
        #print(primitive['title'])
        pagename_to_check.append(primitive['title'])
        newx=primitive['title']
        #print(newx)
               
    if x==newx:
            break

