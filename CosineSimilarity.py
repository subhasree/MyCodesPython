import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer
import enchant
import re, math, collections
import os
import csv
import fnmatch

enchant_dict = enchant.Dict("en_US")

stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            newbasename = basename.replace('_words.csv', '')
            newbasename = newbasename.replace('all_ldas', '')
##            print "new basename is :", newbasename
##            print "pattern is:", pattern
            if fnmatch.fnmatch(newbasename, pattern):
##                print "basename is:", newbasename
##                print "pattern is:", pattern
                filename = os.path.join(root, basename)
                return filename

def get_filename(fname):
    newname = fname.replace('_words.txt_topics.txt', '')
    #newname = newname.replace('all_ldas', '')
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


def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]

'''remove punctuation, lowercase, stem'''
def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english',min_df=1)
#vectorizer = TfidfVectorizer()

def cosine_sim(text1, text2):
    #print "text1 is :", text1
    #print "text2 is: ", text2
##    text1_list = [word for word in text1]
##    print text1_list
##    all_tokens = sum(text1_list, [])
##    text1_rev = check_word_dictionary(all_tokens)
    tfidf = vectorizer.fit_transform([text1, text2])
    #print tfidf
    return ((tfidf * tfidf.T).A)[0,1]

def find_words(fileN):
    #print "Inside"
    words = ""
    lines = fileN.split('\n')
    #f = open('./NPTEL_TheoryOfCS/ldas/Video1_content_lda.txt', 'r')
    #text = f.read()
    for l in lines:
        expressions = l.split('+')
        #print expressions
        for exp in expressions:
            word = exp.split('*')
            #print word[1]
            if (len(word)==2):
                #print word[1]
                word_1 = word[1]
                if (enchant_dict.check(word_1)):
                    words = words + word[1]
                    words = words + ' '
                else:
                    if (len(enchant_dict.suggest(word_1))>0):
                        word_sugg =enchant_dict.suggest(word_1)
                        #print word_sugg
                        words = words + word_sugg[0]
                        words = words + ' '
                    else:
                        words = words + ''    
            else :
                words = words + ''
    #print words            
    return words


def find_cosine_write_csv(d, files):
    files = files.replace(".txt", "")
    write_file = './all_cosine/' + files +'.csv'
    with open(write_file, 'a') as f_text:
    #writer = csv.writer(f_csv)
        f_text.write("Videos, Cosine \n")
        path = '/home/sbasu/VideoClustering/iVistopics/'
        for filename in os.listdir(path):
          print filename
          file_open = path + filename
          f = open(file_open, 'r')
          text = f.read()
          #try:
          co_sim = cosine_sim(find_words(d), find_words(text))
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

path_wiki = '/home/sbasu/VideoClustering/iVistopics'

for files in os.listdir(path_wiki):
    file_to_open = path_wiki + files
    print files
    f = open(file_to_open, 'r')
    d = f.read()
    find_cosine_write_csv(d, files)
    

