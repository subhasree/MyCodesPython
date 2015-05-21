import re, math, collections
import os
import csv
import fnmatch

prob1 = []
prob2 = []

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

def find_probabilites(fileN):
    probabilities = []
    expressions = []
    lines = fileN.split('\n')
    for l in lines:
        #print l
        #print l.split('+')
        expressions = l.split('+')
        #print "Expression is:", expressions
        for exp in expressions:
            #print "exp is:", exp
            probs = exp.split('*')
            probabilities.append(probs[0])
    #print probabilities
    return probabilities
#for line in d:
#    print line
#print d

##for l in lines:
##    expressions = l.split('+')
##    #print expressions
##    for exp in expressions:
##        probs = exp.split('*')
##        probabilities.append(probs[0])

#def calc_kldiv(p1, p2):
def convert_float(list_string):
    list_float = []
    for i in list_string:
        if (i != '')and(i!= 'ack')and(not(any(c.isalpha() for c in i))):
            #print 'i is :', (i)
            list_float.append(float(i))
    return list_float
    
def kldiv(_s, _t):
    if (len(_s) == 0):
        return 1e33

    if (len(_t) == 0):
        return 1e33

    ssum = 0. + sum(i for i in _s)
    slen = len(_s)

    tsum = 0. + sum(i for i in _t)
    tlen = len(_t)

    #vocabdiff = set(_s.keys()).difference(set(_t.keys()))
    #lenvocabdiff = len(vocabdiff)
    lenvocabdiff = len(_s) + len(_t)
    """ epsilon """
    epsilon = min(min(_s)/ssum, min(_t)/tsum) * 0.001

    """ gamma """
    gamma = 1 - lenvocabdiff * epsilon

    # print "_s: %s" % _s
    # print "_t: %s" % _t

    """ Check if distribution probabilities sum to 1"""
    sc = sum([v/ssum for v in _s])
    st = sum([v/tsum for v in _t])

    if sc < 9e-6:
        print "Sum P: %e, Sum Q: %e" % (sc, st)
        print "*** ERROR: sc does not sum up to 1. Bailing out .."
        sys.exit(2)
    if st < 9e-6:
        print "Sum P: %e, Sum Q: %e" % (sc, st)
        print "*** ERROR: st does not sum up to 1. Bailing out .."
        sys.exit(2)

    div = 0.
    for  v in _s:
        pts = v / ssum
        t = _s.index(v)

        ptt = epsilon
        if t in _t:
            ptt = gamma * (_t[t] / tsum)
        try:
            ckl = (pts - ptt) * math.log(pts / ptt)
        except ZeroDivisionError:
            ckl = 0

        div +=  ckl

    return div
#end of kldiv

#print probabilities.values()

def find_kl_write_csv(d, files):
    files = files.replace(".txt_topics.txt", "")
    write_file = './all_ldas/all_ldas' + files +'.csv'
    with open(write_file, 'a') as f_text:
    #writer = csv.writer(f_csv)
        f_text.write("Videos, KL \n")
        path = '/home/sbasu/Videopedia_MM/writeLDA/'
        for filename in os.listdir(path):
          #print filename
          file_open = path + filename
          f = open(file_open, 'r')
          text = f.read()
          try:
              prob = find_probabilites(d)
              prob1 = find_probabilites(text)
              #print filename
              kl_div = (kldiv(convert_float(prob), convert_float(prob1)) + kldiv(convert_float(prob1), convert_float(prob)))/2
              #print kl_div
          except ValueError:
              kl_div= 0.0
          search_filename = filename.replace("_words.txt_topics.txt", "")
          infilePath = get_filename(search_filename)
          if (get_dir_name(infilePath) != None):
            infileDirName = get_dir_name(infilePath)
          else:
            infileDirName = " "
          write_string = filename + ',' + str(kl_div) + "," + infileDirName + '\n'
          #print write_string
          f_text.write(write_string)
          #return write_string
        f_text.close()


path_wiki = '/home/sbasu/Videopedia_MM/wikiwriteLDA/'

##file_to_open ="/home/sbasu/Videopedia_MM/wikiwriteLDA/Induction_motor_content.txt_topics.txt" 
##f = open(file_to_open, 'r')
##d = f.read()
##files = "Induction_motor_content.txt_topics.txt"
##find_kl_write_csv(d, files)

for files in os.listdir(path_wiki):
    file_to_open = path_wiki + files
    print files
    f = open(file_to_open, 'r')
    d = f.read()
    find_kl_write_csv(d, files)







