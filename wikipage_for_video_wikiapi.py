from wikiapi import WikiApi
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re, math, collections
import os
import csv
import fnmatch
import urllib
import urllib2
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from pattern.web import Wikipedia

def wikipage_extract(article_handle_url):
    handle = article_handle_url.split("/")
    print handle[-1]
    article = Wikipedia(language="en").search(handle[-1], throttle=10)
    out_contents_file = "./Wikipedia pages/Content/" + handle[-1] + ".txt"
    out_contents = open(out_contents_file,"w")
    #out_contents.write(text1.encode('utf-8'))
    #print type(article.string)
    value = article.string
    #print value
    #print type(value)
    out_contents.write(value.encode('utf-8'))
    out_contents.close()

##    for text in article.string:
##        #print text
##        out_contents.write(text)
    
##    article = urllib.quote(handle[-1])
##    opener = urllib2.build_opener()
##    opener.addheaders = [('User-agent', 'Mozilla/5.0')] #wikipedia needs this
##    #print (opener.open(article_handle_url))
##    resource = opener.open(article_handle_url)
##    data = resource.read()
##    #print data
##    resource.close()
##    soup = BeautifulSoup(data)
##    links = soup.find_all('a')
##    for link in links:
##        textURL = link.get('href')
##        #text = link.get_text
##        text = link.text
##        #print text
##        #textfrombound = link.find_all('bound')
##        #print textfrombound.content
##        out_header_file = "./Wikipedia pages/" + handle[-1] + ".txt"
##        out_headers=open(out_header_file,"w")
##        out_headers.write(text.encode('utf-8'))
##        out_headers.close()
##        para_contents = soup.find_all('p')
##    for para in para_contents:
##        text = para.text
##        text1 = ' '
##        print text
        #textfrombound = link.find_all('bound')
        #print textfrombound.content
##        text1 = text1.join([word for word in text.split() if word not in (stopwords.words('english'))])
##        print text1
##    out_contents_file = "./Wikipedia pages/Content/" + handle[-1] + ".txt"
##    out_contents = open(out_contents_file,"w")
##    #out_contents.write(text1.encode('utf-8'))
##    print article.encode('utf-8')
##    out_contents.write(article.encode('utf-8'))
    #out_contents.close()

wiki = WikiApi()
wiki = WikiApi({ 'locale' : 'en'})

##results = wiki.find('Bose-Einstein Statistics')
##
##print results
##
##article = wiki.get_article(results[0])
##
##print article.url

for root, dirs, files in os.walk("/home/sbasu/Videopedia_MM/Topic Desc"):
    for file in files:
         print file
         file_to_open = "/home/sbasu/Videopedia_MM/Topic Desc/" + file
         f = open(file_to_open, 'r')
         d = f.readline()
         print d.split(' ')[2:]
         search_string = ""
         for k in d.split(' ')[2:]:
            search_string = search_string + " " + k
         print search_string
         try:
             results = wiki.find(search_string)
             print results
             article_handle = wiki.get_article(results[0])
             print article_handle.url
##             url_tosplit = article_handle.url
##             print url_tosplit.spilt('/')
             wikipage_extract(article_handle.url)
         except:
             print "error"
            
##f = open("/home/sbasu/Videopedia_MM/Topic Desc/ZHt9NTH6R_0", 'r')
##d = f.readline()
##print d.split(' ')[2:]
##search_string = ""
##for k in d.split(' ')[2:]:
##    search_string = search_string + " " + k
##print search_string
##try:
## results = wiki.find(search_string)
## print results
## article_handle = wiki.get_article(results[0])
## print article_handle.url
## wikipage_extract(article_handle.url)
##except:
## print "error"
