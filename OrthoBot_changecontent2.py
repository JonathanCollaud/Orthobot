#Orthobot

import urllib2
import json
import requests
from bs4 import BeautifulSoup
from OrthoBot_login import *
import string
import copy


# add new_content to the page
def add_content(pagename, new_content):
    # get the content
    result = requests.post(baseurl+'api.php?action=query&titles='+pagename+'&export&exportnowrap')
    soup = BeautifulSoup(result.text,'lxml')
    content = ''
    for primitive in soup.findAll("text"):
        content += primitive.string

    content += new_content

    # update the content
    headers = {'content-type':'application/x-www-form-urlencoded'}
    payload = {'action':'edit','assert':'user','format':'json','text':content,'title':pagename,'token':edit_token}
    r4 = requests.post(baseurl+'api.php',headers=headers,data=payload,cookies=edit_cookie)
    # print(r4.text)

# remove some text delimited by 'first' and 'last' words
def rm_content(pagename, first, last):
    # get the content
    result = requests.post(baseurl+'api.php?action=query&titles='+pagename+'&export&exportnowrap')
    soup = BeautifulSoup(result.text,'lxml')
    content = ''
    for primitive in soup.findAll("text"):
        content += primitive.string

    # split the text ...
    content_split = content.split('\n')
    new_content_split = copy.deepcopy(content_split) # mandatory deepcopy
    try:
        first_index = content_split.index(first)
    except:
        return None
    else:
        # ... to remove some parts of it ...
        removed_words = []
        removed_words.append(content_split[first_index])
        new_content_split.remove(content_split[first_index])
        index = first_index + 1
        while (index < len(content_split)) and (content_split[index] != last):
            # print content_split[index]
            removed_words.append(content_split[index])
            new_content_split.remove(content_split[index])
            index += 1
        removed_words.append(content_split[index])
        new_content_split.remove(content_split[index])

        # ... to finally join the splitted text with removed parts ...
        new_content = string.join(new_content_split, '\n')
        removed_str = string.join(removed_words, '\n')

        content = new_content
        
        # update page
        headers = {'content-type':'application/x-www-form-urlencoded'}
        payload = {'action':'edit','assert':'user','format':'json','text':content,'title':pagename,'token':edit_token}
        r4 = requests.post(baseurl+'api.php',headers=headers,data=payload,cookies=edit_cookie)
        # print(r4.text)

        return removed_str
