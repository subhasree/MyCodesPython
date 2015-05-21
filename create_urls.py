import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re, math, collections
import os
import csv
import fnmatch

driver = webdriver.Firefox()

for root, dirs, files in os.walk("/home/sbasu/VideoClustering/video srt files"):
    for file in files:
        new_url = "https://www.youtube.com/watch?v=" + file
        try:
                    url1=new_url.split('=')
                    url1[1]=url1[1].split('\n')
                    print url1[1][0]
                    open_file = "/home/sbasu/Videopedia_MM/Topic Desc/"+url1[1][0]
                    out=open(open_file,"a")
                    '''driver = webdriver.Firefox()'''
                    '''driver = webdriver.PhantomJS()'''
                    driver.get(new_url)
                    k=driver.find_element_by_xpath("//*[@id='eow-title']")
                    d=driver.find_element_by_xpath("//*[@id='eow-description']")
                    out.write(k.text.encode('utf-8'))
                    out.write('\n')
                    out.write(d.text.encode('utf-8'))
                    #print(k.text.encode('utf-8'))
  
        except:
                    print("error")

        out.close()
driver.close()

