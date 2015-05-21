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
                    
                    out=open("./metadata/meta-"+url1[1][0],"wb")
                    driver.get(url)
                    
                    title=driver.find_element_by_xpath("//*[@id='eow-title']")
                    des=driver.find_element_by_xpath("//*[@id='eow-description']")
                    subs=driver.find_element_by_xpath("//*[@class='yt-subscription-button-subscriber-count-branded-horizontal']")
                    views=driver.find_element_by_xpath("//*[@class='watch-view-count']")
                    likes=driver.find_element_by_xpath("//button[@id='watch-like']")
                    dislikes=driver.find_element_by_xpath("//button[@id='watch-dislike']")
                    cat=driver.find_element_by_xpath("//h4[@class='title']")
                    publish=driver.find_element_by_xpath("//*[@class='watch-time-text']")
                    #channel=driver.find_element_by_xpath("//*[@class="yt-uix-sessionlink     spf-link  g-hovercard"]")
                    description=driver.find_element_by_xpath("//meta[@name='description']")
                    keywords=driver.find_element_by_xpath("//meta[@name='keywords']")
                    videoTags=driver.find_elements_by_xpath("//meta[@property='og:video:tag']")
                    
                    
                    #comments
                    #comments=driver.find_element_by_xpath("//div[@class='comment-text-content']")
                    
                    out.write("<title>")
                    out.write(title.text.encode('utf-8'))
                    out.write('</title>')
                    
                    out.write('<des>')
                    out.write(des.text.encode('utf-8'))
                    out.write('</des>')
                    
                    out.write('<subs>')
                    out.write(subs.text.encode('utf-8'))
                    out.write('</subs>')
                    
                    out.write('<views>')
                    out.write(views.text.encode('utf-8'))
                    out.write('</views>')
                    
                    out.write('<likes>')
                    out.write(likes.text.encode('utf-8'))
                    out.write('</likes>')
                    
                    out.write('<dislikes>')
                    out.write(dislikes.text.encode('utf-8'))
                    out.write('</dislikes>')
                    
                    out.write('<publish>')
                    out.write(publish.text.encode('utf-8'))
                    out.write('</publish>')
                    
                    #out.write('<channel>')
                    #out.write(channel.text.encode('utf-8'))
                    #out.write('</channel>')
                    
                    
                    out.write('<description>')
                    out.write(description.get_attribute('content').encode('utf-8'))
                    out.write('</description>')
                    
                    
                    out.write('<keywords>')
                    out.write(keywords.get_attribute('content').encode('utf-8'))
                    out.write('</keywords>')
                    
                    out.write('<videoTags>')
                    for tag in videoTags:
                              out.write(tag.get_attribute('content'))
                              out.write(',')
                              out.write('</videoTags>')
          except:
                    print("error")
          out.close()
driver.close()


