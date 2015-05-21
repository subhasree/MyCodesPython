from gensim.models import word2vec
import logging

acad_words = " "
f_read = open("/home/sbasu/Videopedia_MM/academic_words_v1.txt", "rb")
meta_txt = f_read.read()
f_read.close()
          
acad_words = acad_words + meta_txt + meta_txt+ meta_txt + meta_txt + meta_txt
f= open("./academic_words.txt", 'a')
f.write(acad_words)
f.close()

