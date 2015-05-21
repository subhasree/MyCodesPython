import sys
import random
import math
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer
import enchant
import re, math, collections
import os
import csv
import fnmatch

filewiki_to_open = '/home/sbasu/Videopedia_MM/Wikipedia pages/Content/Academy_Awards.txt' 
f1 = open(filewiki_to_open, 'r')
d1 = f1.read()

##filevideo_to_open = '/home/sbasu/Videopedia_MM/extractedWords/_1RFDkYS2QQ_words.txt' 
##f2 = open(filevideo_to_open, 'r')
##d2 = f2.read()  

def find_tf_idf(d, files):
    #files= files.replace(".txt", "")
    write_file = '/home/sbasu/Videopedia_MM/Videos_Tf-Idf/tfIDF_' + files 
    corpus = [d]
    try:
        vectorizer = TfidfVectorizer(min_df=1)
        X = vectorizer.fit_transform(corpus)
        idf = vectorizer._tfidf.idf_
        for elem in zip(vectorizer.get_feature_names(), idf):
            print elem
            with open(write_file, 'a') as f_text:
                try:
                    write_string = files + ' ' + str(elem[0]).encode("utf-8") + " " + str(elem[1]).encode("utf-8") + " " +'\n'
                    f_text.write(write_string)
                except:
                    write_string = ""
            f_text.close()
    except ValueError:
        print "error"
    #print vectorizer.get_feature_names()
    
#print dict(zip(vectorizer.get_feature_names(), idf))

path_wiki = '/home/sbasu/Videopedia_MM/extractedWords/'

for files in os.listdir(path_wiki):
    file_to_open = path_wiki + files
    print files
    f = open(file_to_open, 'r')
    d = f.read()
    find_tf_idf(d, files)
