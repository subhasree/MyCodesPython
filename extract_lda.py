from __future__ import print_function
import re, math, collections
import os
import os.path
import gensim
from gensim import corpora, models, similarities, utils
import enchant
import nltk
#import scheme as s

d = enchant.Dict("en_US")

documents=[]

#dict_documents = {file1: 'document 1'}
#print dict_documents[file1]

stoplist = set("a a's able about above according accordingly across actually after afterwards again against ain't all allow allows almost alone along already also although always am among amongst an and another any anybody anyhow anyone anything anyway anyways anywhere apart appear appreciate appropriate are aren't around as aside ask asking associated at available away awfully b be became because become becomes becoming been before beforehand behind being  believe below beside besides best better between beyond both brief but by c c'mon c's came can can't cannot cant cause causes certain certainly changes clearly co com come comes concerning consequently consider considering contain containing contains corresponding could couldn't course currently d definitely described despite did didn't different do does doesn't doing don't done down downwards during e each edu eg eight either else elsewhere enough entirely especially et etc even ever every everybody everyone everything everywhere ex exactly example except f far few fifth first five followed following follows for former formerly forth four from further furthermore g get gets getting given gives go goes going gone got gotten greetings h had hadn't happens hardly has hasn't have haven't having he he's hello help hence her here here's hereafter hereby herein hereupon hers herself hi him himself his hither hopefully how howbeit however i i'd i'll i'm i've ie if ignored immediate in inasmuch inc indeed indicate indicated indicates inner insofar instead into inward is isn't it it'd it'll it's its itself j just k keep keeps kept know knows known l last lately later latter latterly least less lest let let's like liked likely little look looking looks ltd m mainly many may maybe me mean meanwhile merely might more moreover most mostly much must my myself n name namely nd near nearly necessary need needs neither never nevertheless new next nine no nobody non none noone nor normally not nothing novel now nowhere o obviously of off often oh ok okay old on once one ones only onto or other others otherwise ought our ours ourselves out outside over overall own p particular particularly per perhaps placed please plus possible presumably probably  provides q que quite qv  r rather rd re really reasonably regarding regardless  regards relatively respectively  right s said same saw say saying says second secondly see seeing seem seemed seeming seems seen self selves sensible sent serious seriously seven several shall she should shouldn't since six so some somebody somehow someone something sometime sometimes somewhat somewhere soon sorry  specified specify specifying still sub such sup sure t t's take taken tell tends th than thank thanks thanx  that that's thats the their theirs them themselves then thence there there's thereafter thereby thereforetherein theres thereupon these they they'd they'll they're they've think third this thorough thoroughly those though three through throughout thru  thus to together too took toward towards tried tries truly try trying twice two u un under unfortunately unless unlikely until unto up upon us use used useful uses using usually uucp  v value various very via viz vs w want wants was wasn't way we we'd we'll we're we've welcome well went were weren't what what's whatever when whence whenever where where's whereafter whereas whereby wherein whereupon wherever whether  which while  whither who who's whoever whole whom whose why  will willing wish with within without won't wonder would would wouldn't x  y yes yet you you'd  you'll you're  you've your yours yourself yourselves z  zero".split())

def check_file_exists(file_path, filename):
    return 0
    
def process_srtfiles():
    for root, dirs, files in os.walk("/home/sbasu/Videopedia_MM/Wikipedia pages/Content"):
        for file in files:
##            if file.endswith("_words.txt"):
##                file_path = os.path.join("/home/sbasu/Dropbox/MM_2015_MAterials/writeLDA", file)
##                file_path = file_path+"_topics.txt"
##                print (os.path.exists(file_path))
##                if ((os.path.exists(file_path)) == False):
                 with open(os.path.join(root, file)) as intxt_srt:
                     print(os.path.join(root, file))
                     data_srt = intxt_srt.read()
                     #print (len(data_srt))
                     text_srt = [[word for word in item.lower().split() if word not in stoplist] for item in data_srt.split('\t')]
                     all_tokens = sum(text_srt, [])
                     list_tokens = []
                     for token in text_srt:
                        if (d.check(token)):
                            #print (d.check(token))
                            list_tokens.append(token)
                        else:
                            #print token
                            if (len(d.suggest(token)) > 0):
                                #print d.suggest(token)[0]
                                list_tokens.append(d.suggest(token)[0])
                     list_tokenutf =[]
                     for items in list_tokens:
                         #print (items)
                         #print (gensim.utils.any2unicode(items, encoding='utf8', errors='strict'))
                         list_tokenutf.append(utils.to_utf8(items))
                     #print (list_tokenutf)
                     #print (type(list_tokenutf))
                     str_utf = ''.join(list_tokenutf)
                     srt_tokens = str_utf.split()
                     tokens = set(word for word in set(list_tokens))
                     tokens_once = set(word for word in set(list_tokens) if list_tokens.count(word) == 1)
                     #print tokens_once
                     texts = [[word for word in text if word not in tokens_once]
                                 for text in text_srt]
                     #print (type(texts[0]))
                     #print (texts[0][0])
                     dictionary = corpora.Dictionary(texts)
                     dictionary.save('/home/sbasu/Videopedia_MM/wikiwords_srt.dict') # store the dictionary, for future reference
                     #print (dictionary)
                     #print (dictionary.token2id)
                     corpus = [dictionary.doc2bow(text) for text in texts]
                     corpora.MmCorpus.serialize('words_srt.mm', corpus) # store to disk, for later use
                     #print (corpus) 
                     dictionary = corpora.Dictionary.load('/home/sbasu/Videopedia_MM/wikiwords_srt.dict')
                     corpus = corpora.MmCorpus('words_srt.mm')
                     try:
                         lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary,  update_every=1, chunksize=10000, passes=1)
                         root_write = "/home/sbasu/Videopedia_MM/wikiwriteLDA"
                         filename = os.path.join(root_write, file) + "_topics.txt"
                         for topic in lda.print_topics():
                              #print (topic)
                              with open(filename, 'a') as f_topics:
                                  print ("file open")
                                  f_topics.write(topic)
                                  f_topics.write("\n")
                              f_topics.close()
                     except ValueError:
                         pass
                         

#print  documents.items():
                  
#texts = [[word for word in document.lower().split() if word not in stoplist]
#              for document in documents]

## remove words that appear only once
##all_tokens = sum(texts, [])
##
##list_tokens = []
##
##for token in all_tokens:
##    if (d.check(token)):
##        #print d.check(token)
##        list_tokens.append(token)
##    else:
##        #print token
##        if (len(d.suggest(token)) > 0):
##            #print d.suggest(token)[0]
##            list_tokens.append(d.suggest(token)[0])
##            
##print list_tokens
##
##tokens = set(word for word in set(list_tokens))
##tokens_once = set(word for word in set(list_tokens) if list_tokens.count(word) == 1)
###print tokens_once
##texts = [[word for word in text if word not in tokens_once]
##             for text in texts]


##def write_srt(d, files):
##    write_file = './all_ldas/all_ldas' + files +'.csv'
##    with open(write_file, 'wb') as f_text:
##    #writer = csv.writer(f_csv)
##        f_text.write("Videos, KL \n")
##        path = '/home/sbasu/Dropbox/MM_2015_MAterials/checkldas/'
##        for filename in os.listdir(path):
##          #print filename
##          file_open = path + filename
##          f = open(file_open, 'r')
##          text = f.read()
##        f_text.close()

##for root, dirs, files in os.walk("/home/sbasu/Dropbox/MM_2015_MAterials"):
##    print (root)
##    for file in files:
##        if file.endswith(".srt"):
##             #print(os.path.join(root, file))
##             with open(os.path.join(root, file)) as intxt:
##                data = intxt.read()
##                x = re.findall('[aA-zZ]+', data)
##                print(x)
##                write_file = "/home/sbasu/Dropbox/MM_2015_MAterials/extractedWords/" + file + '_words.txt'
##                with open(write_file, 'wb') as f_text:
##                    #f_text.write( os.path.join(root, file))
##                    #f_text.write("\n")
##                    for string1 in x:
##                        f_text.write(string1)
##                        f_text.write("\t")
##                f_text.close()



##for root, dirs, files in os.walk("/home/sbasu/Videopedia_MM/extractedWords"):
##    print (dirs)
##    print (files)
##    for file in files:
##        if file.endswith(".txt"):
##             file_path = os.path.join("/home/sbasu/Dropbox/MM_2015_MAterials/writeLDA", file)
##             file_path = file_path+"_topics.txt"
##             print (os.path.exists(file_path))
##             write_file = "/home/sbasu/Videopedia_MM/file_handled.csv"
##             with open(write_file, 'a') as f_text:
##                    string1 = file + "," + str(os.path.exists(file_path))
##                    f_text.write(string1)
##                    f_text.write("\n")
##             f_text.close()
    

process_srtfiles()
