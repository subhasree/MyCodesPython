from wikiapi import WikiApi

wiki = WikiApi()
wiki = WikiApi({ 'locale' : 'en'})

results = wiki.find('Bose-Einstein Statistics')

print results

article = wiki.get_article(results[0])

print article.url
