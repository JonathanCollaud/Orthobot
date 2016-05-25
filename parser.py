from lxml import html
import requests
import string
import re

##
# To parse page call clean_parse(url)
# To read the parsed html use array[i][0]
##

def parser (str):

    page = requests.get(str)
    tree = html.fromstring(page.content)

    span = tree.xpath('//span/text()') #get words from titles h2
    bio = tree.xpath('//li/text()') #get lines inside the list
    link = tree.xpath('//a/text()') #get words inside links
    garbage= tree.xpath('//p/text()') #get extended garbage

    bioClean = [] #bio with less garabage in it

    for i in range(len(bio)- 3): # -3 to remove useless information not related to bio
        if len(bio[i]) > 2: #remove shit of length 1 or 2 (" " and ". " mainly)
            bioClean.append(bio[i])

    parsed = bioClean

    for i in range(len(link) - 20):
        parsed.append(link[i]) #concatenation of both arrays

    for i in range(len(span)):
        parsed.append(span[i])

    for i in range(len(garbage)):
        parsed.append(garbage[i])
        
    return parsed

def split_bio(text):

    words = ""
    corr = []

    # split the text
    for i in range(len(text)):
        text[i] = re.sub(r'[^\w|^-]', ' ', text[i], flags=re.UNICODE)
        words += text[i] + " "

    corr += words.split(" ")

    return corr

def clean_space (words):
    ret=[]
    for i in range(len(words)):
        if(words[i] != ""):
            ret.append(words[i])
    return ret

def clean_shit (words):
    ret=[]
    for i in range(len(words)):
        #words[i] = re.sub(r'\W+', '', words[i],flags=re.UNICODE)
        words[i] = re.sub("\d+", "", words[i], flags=re.UNICODE)
    return words

def clean_parse(url):
    return clean_space(clean_space(split_bio(parser(url))))

#s = clean_parse('http://wikipast.world/wiki/index.php/George_Orwell')

#s = clean_parse('http://wikipast.world/wiki/index.php/Henri_Dunant')

#s = clean_parse('http://wikipast.world/wiki/index.php/Herbert_George_Wells')

#s = clean_parse('http://wikipast.world/wiki/index.php/Ortobottest')

#print(s)

#t =[]

#for i in range(len(s)):
#   t.append(s[i][0])

#for i in range(len(t)):
#    print(t[i])

#print("then :")
#print(t)
#for i in range(len(s)):
#    print(s[i][0])

