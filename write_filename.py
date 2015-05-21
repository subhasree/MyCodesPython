import os
import csv
import fnmatch


path_wiki = '/home/sbasu/Videopedia_MM/all_ldas/'

for files in os.listdir(path_wiki):
    file_to_open = "/home/sbasu/Videopedia_MM/PrecisionCalculation.csv"
    f = open(file_to_open, 'a')
    f.write(files)
    f.write("\n")
    f.close()
