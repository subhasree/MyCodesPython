import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re, math, collections
import os
import csv
import fnmatch


fp=open('url.txt')
urls=fp.readlines()
fp.close()
driver = webdriver.Firefox()

for url in urls:
        try:
                url1=url.split('=')
                url1[1]=url1[1].split('\n')
                print(url1[1][0])

                out=open(url1[1][0],"wb")
                '''driver = webdriver.Firefox()'''
                '''driver = webdriver.PhantomJS()'''
                driver.get(url)
                k=driver.find_element_by_xpath("//*[@id='eow-title']")
                d=driver.find_element_by_xpath("//*[@id='eow-description']")
                out.write(k.text.encode('utf-8'))
                out.write('\n')
                out.write(d.text.encode('utf-8'))
                print(k.text.encode('utf-8'))
  
                
        except:
                print("error")
        out.close()
driver.close()
        
