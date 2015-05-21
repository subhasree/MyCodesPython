import re, math, collections
import os
import csv
import fnmatch

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

def tokenize(_str):
    stopwords = ['and', 'for', 'if', 'the', 'then', 'be', 'is', 'are', 'will', 'in', 'it', 'to', 'that']
    tokens = collections.defaultdict(lambda: 0.)
    for m in re.finditer(r"(\w+)", _str, re.UNICODE):
        m = m.group(1).lower()
        if len(m) < 2: continue
        if m in stopwords: continue
        tokens[m] += 1
    #print tokens
    return tokens
#end of tokenize

def kldiv(_s, _t):
    if (len(_s) == 0):
        return 1e33

    if (len(_t) == 0):
        return 1e33

    ssum = 0. + sum(_s.values())
    slen = len(_s)

    tsum = 0. + sum(_t.values())
    tlen = len(_t)

    vocabdiff = set(_s.keys()).difference(set(_t.keys()))
    lenvocabdiff = len(vocabdiff)

    """ epsilon """
    epsilon = min(min(_s.values())/ssum, min(_t.values())/tsum) * 0.001

    """ gamma """
    gamma = 1 - lenvocabdiff * epsilon

    # print "_s: %s" % _s
    # print "_t: %s" % _t

    """ Check if distribution probabilities sum to 1"""
    sc = sum([v/ssum for v in _s.itervalues()])
    st = sum([v/tsum for v in _t.itervalues()])

    if sc < 9e-6:
        print "Sum P: %e, Sum Q: %e" % (sc, st)
        print "*** ERROR: sc does not sum up to 1. Bailing out .."
        sys.exit(2)
    if st < 9e-6:
        print "Sum P: %e, Sum Q: %e" % (sc, st)
        print "*** ERROR: st does not sum up to 1. Bailing out .."
        sys.exit(2)

    div = 0.
    for t, v in _s.iteritems():
        pts = v / ssum

        ptt = epsilon
        if t in _t:
            ptt = gamma * (_t[t] / tsum)

        ckl = (pts - ptt) * math.log(pts / ptt)

        div +=  ckl

    return div
#end of kldiv

'''d1 = """Many research publications want you to use BibTeX, which better
organizes the whole process. Suppose for concreteness your source
file is x.tex. Basically, you create a file x.bib containing the
bibliography, and run bibtex on that file."""
d2 = """In this case you must supply both a \left and a \right because the
delimiter height are made to match whatever is contained between the
two commands. But, the \left doesn't have to be an actual 'left
delimiter', that is you can use '\left)' if there were some reason
to do it."""'''                                         

##f = open('./NPTEL_TheoryOfCS/Video1_content.txt', 'r')
##d = f.read()
###print d1
##
##path = '/home/sbasu/VideoTranscript/checkNS/'
##
##for filename in os.listdir(path):
##  #print filename
##  file_open = path + filename
##  f = open(file_open, 'r')
##  text = f.read()
##  with open(write_file, 'wb') as f_text:
##  print "KL-divergence for file", filename, " is:", (kldiv(tokenize(d), tokenize(text)) + kldiv(tokenize(text), tokenize(d)))/2

def find_kl_write_csv(d, files):
    write_file = './all_kl/all_kl' + files +'.csv'
    with open(write_file, 'wb') as f_text:
    #writer = csv.writer(f_csv)
        f_text.write("Videos, KL \n")
        path = '/home/sbasu/Videopedia_MM/extractedWords/'
        for filename in os.listdir(path):
          #print filename
          file_open = path + filename
          f = open(file_open, 'r')
          text = f.read()
          try:
##              prob = find_probabilites(d)
##              prob1 = find_probabilites(text)
              #print filename
              kl_div = (kldiv(tokenize(d), tokenize(text)) + kldiv(tokenize(text), tokenize(d)))/2
              print kl_div
          except ValueError:
              kl_div= 0.0
          search_filename = filename.replace("_words.txt", "")
          infilePath = get_filename(search_filename)
          if (get_dir_name(infilePath) != None):
            infileDirName = get_dir_name(infilePath)
          else:
            infileDirName = " "    
          write_string = filename + ',' + str(kl_div) + " ," + infileDirName + '\n'
          #print write_string
          f_text.write(write_string)
          #return write_string
        f_text.close()


path_wiki = '/home/sbasu/Videopedia_MM/Wikipedia pages/Content/'

for files in os.listdir(path_wiki):
    file_to_open = path_wiki + files
    f = open(file_to_open, 'r')
    d = f.read()
    find_kl_write_csv(d, files)

