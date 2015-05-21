import urllib
import urllib2
from bs4 import BeautifulSoup
from nltk.corpus import stopwords

article= "Transformer"
article = urllib.quote(article)
out_headers=open("./Wikipedia pages/Transformer.txt","w")
out_contents = open("./Wikipedia pages/Content/Transformer_content.txt","w")
#print out_contents

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')] #wikipedia needs this

resource = opener.open("http://en.wikipedia.org/wiki/" + article)
data = resource.read()
resource.close()
soup = BeautifulSoup(data)
links = soup.find_all('a')
for link in links:
    textURL = link.get('href')
    #text = link.get_text
    text = link.text
    #print text
    #textfrombound = link.find_all('bound')
    #print textfrombound.content
    out_headers.write(text.encode('utf-8'))
#print soup.find('div',id="bodyContent").p.'span'.contents

out_headers.close()

#final_link = soup.p
#final_link.decompose()

para_contents = soup.find_all('p')

for para in para_contents:
    text = para.text
    text1 = ' '
    #print text
    #textfrombound = link.find_all('bound')
    #print textfrombound.content
    text1 = text1.join([word for word in text.split() if word not in (stopwords.words('english'))])
    print text1
    out_contents.write(text1.encode('utf-8'))

out_contents.close()


