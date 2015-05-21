import math
from itertools import izip
import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer
import enchant
import re, math, collections
import os
import csv
import fnmatch

# tfIDF_0A45kt2U3U8_words.txt
def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            #print basename
            newbasename = basename.replace('_words.txt', '')
            newbasename = newbasename.replace('tfIDF', '')
            #print "new basename is :", newbasename
            #print "pattern is:", pattern
            if fnmatch.fnmatch(newbasename, pattern):
##                print "basename is:", newbasename
##                print "pattern is:", pattern
                filename = os.path.join(root, basename)
                return filename

def get_filename(fname):
    newname = fname.replace('_words.txt', '')
    newname = newname.replace('tfIDF_', '')
    #print newname
    directory = '/home/sbasu/VideoClustering/video srt files'
    file_path = find_files(directory, newname)
    #print file_path
    return file_path
##    print "File path is:"
##    print file_path

def get_dir_name(pathname):
    #print pathname
    if (pathname is None):
        directories = ["", "", "", "", "", "", ""]
    else:    
        directories = pathname.rsplit('/')
    #print directories[5]
    return directories[5]

def check_word_dictionary(all_tokens):
    list_tokens = []
    for token in all_tokens:
        if (enchant_dict.check(token)):
            #print d.check(token)
            list_tokens.append(token)
        else:
            #print token
            if (len(enchant_dict.suggest(token)) > 0):
                #print d.suggest(token)[0]
                list_tokens.append(enchant_dict.suggest(token)[0])
    #print list_tokens
    return list_tokens


def dot_product(v1, v2):
    return sum(map(lambda x: x[0] * x[1], izip(v1, v2)))

def cosine_measure(v1, v2):
    prod = dot_product(v1, v2)
    len1 = math.sqrt(dot_product(v1, v1))
    len2 = math.sqrt(dot_product(v2, v2))
    return prod / (len1 * len2)

def find_vector(file_name):
    v =[]
    vec1 =[]
    vec1.append( file_name.split("\n" ))
    #print v1
    #print type(vec1)
    try:
        for line in vec1:
            for lines in line:
                v.append(float(lines.split(" " )[2]))
    except:
        v.append(0.0)
    return v
    #print v    
        
def find_cosine_write_csv(d, files):
    files = files.replace(".txt", "")
    write_file = './all_cosine/' + files +'.csv'
    with open(write_file, 'a') as f_text:
    #writer = csv.writer(f_csv)
        f_text.write("Videos, Cosine \n")
        path = '/home/sbasu/Videopedia_MM/Videos_Tf-Idf/'
        for filename in os.listdir(path):
          #print filename
          file_open = path + filename
          f = open(file_open, 'r')
          text = f.read()
          #try:
          co_sim = cosine_measure(find_vector(d),find_vector(text))
          #except ValueError:
          #    co_sim= 0.0
          search_filename = filename.replace("_words.txt", "")
          infilePath = get_filename(search_filename)
          if (get_dir_name(infilePath) != None):
            infileDirName = get_dir_name(infilePath)
          else:
            infileDirName = " "
          print co_sim
          write_string = filename + ',' + str(co_sim) + "," + infileDirName + '\n'
          #print write_string
          f_text.write(write_string)
          #return write_string
        f_text.close()

##path_video = '/home/sbasu/Videopedia_MM/Videos_Tf-Idf/tfIDF_0A45kt2U3U8_words.txt'
##f_vid = open(path_video, 'r')
##d_vid = f_vid .read()
##
##
##path_wiki = '/home/sbasu/Videopedia_MM/Wikipedia pages/Tf-IDF/tfIDF_Academy_Awards.txt'
##f_wiki = open(path_wiki, 'r')
##d_wiki = f_wiki.read()

#find_vector(d_vid)
#print cosine_measure(find_vector(d_wiki),find_vector(d_vid))

path_wiki = '/home/sbasu/Videopedia_MM/Wikipedia pages/Tf-IDF/'
for files in os.listdir(path_wiki):
    file_to_open = path_wiki + files
    print files
    f = open(file_to_open, 'r')
    d = f.read()
    find_cosine_write_csv(d, files)
    
