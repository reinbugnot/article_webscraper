#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup

import urllib
from requests_html import HTML
from requests_html import HTMLSession

import os
import numpy as np


# In[2]:


def get_source(url):
    """Return the source code for the provided URL. 

    Args: 
        url (string): URL of the page to scrape.

    Returns:
        response (object): HTTP response object from requests_html. 
    """

    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)


# In[3]:


def scrape_google(query, i = 0):

    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.co.uk/search?q=articles+for+" + query + "&start=" + str(i * 10))

    links = list(response.html.absolute_links)
    google_domains = ('https://www.google.', 'https://google.')

    for url in links[:]:
        if url.startswith(google_domains):
            links.remove(url)
    return links


# In[4]:


def scrape_article(link):
    
    article_url = link.split("#")[0]
    article_content = article_url
    
    # Sending HTTP request
    req = requests.get(article_url)

    # Pulling HTTP data from internet
    article_soup = BeautifulSoup(req.text, "html.parser") 

    # Pull Title
    article_content += '\n\n' + article_soup.find_all('title')[0].text + '\n\n' 
    print('\nScraping Article: ' + article_soup.find_all('title')[0].text)
    
    # Pull Content
    for item in article_soup.find_all('body'):
        for content in item.find_all(['li','p', 'h2']):
            article_content += content.text + '\n\n'
            
    return article_content


# In[5]:


# Import Inputs
keywords = []
with open('keywords.txt', 'r') as f:
    keywords.append(f.readlines())
    
query_key = ' '
for word in keywords[0]:
    query_key += word + ' '

query_key = query_key.replace('\n', '')

with open('input_params.txt', 'r') as f:
    params = f.readlines()

min_word_count = int(params[0])
page = int(params[1]) -1


# In[14]:


for index, link in enumerate(scrape_google(query_key, page)[:7]):

    article_content = scrape_article(link)
    
    if len(article_content.split()) < min_word_count:
        print('SKIP: Article is below the minimum word count of ' + str(min_word_count))
        continue
        
    CHECK_FOLDER = os.path.isdir('output')

    # If folder doesn't exist, then create it.
    if not CHECK_FOLDER:
        os.mkdir('output')

    else:
        pass
    
    out = []
    out.append(article_content)
    out = np.array(out)


    del article_content

    np.savetxt('output/' + str(page) + "_" + str(index) + '.txt', out, fmt='%s', encoding="utf8")
    
    print('Saved contents to ' + str(page) + "_" + str(index) + '.txt')

    del out
    
print("\n Scraping Done!")


# In[ ]:





# In[ ]:




