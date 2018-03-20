# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 21:51:03 2018

@author: saop0
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
import os
import urllib

def get_web_page(url):
    time.sleep(0.5) #avoid ddos
    resp = requests.get(
        url=url,
        cookies={'over18': '1'}
    )
    if resp.status_code != 200:
        print('Invalid url:', resp.url)
        return None
    else:
        return resp.text
    
def get_articles(dom,date):
    soup = BeautifulSoup(dom,'html.parser')
    
    #get prev page
    paging_div = soup.find('div', 'btn-group btn-group-paging')
    prev_url = paging_div.find_all('a')[1]['href']
    
    articles = []
    divs = soup.find_all('div','r-ent')
    for d in divs:
        if d.find('div','date').string == date: #date of article correct
            #get number of push
            push_count = 0
            if d.find('div','nrec').string:
                try:
                    push_count = int(d.find('div','nrec').string)
                except ValueError:
                    pass
                
            #get href of article and title
            if d.find('a'): #haven't deleted yet
                href = d.find('a')['href']
                title = d.find('a').string
                author = d.find('div','author').string #author is my pratice
                articles.append({
                    'title': title,
                    'href': href,
                    'push_count': push_count,
                    'author': author
                    })
    return articles,prev_url

def parse(dom):
    soup = BeautifulSoup(dom, 'html.parser')
    links = soup.find(id='main-content').find_all('a')
    img_urls = []
    for link in links:
        #if link['href'].startswith('http://i.imgur.com'):
        if re.match(r'^https?://(i.)?(m.)?imgur.com',link['href']):
            img_urls.append(link['href'])
    return img_urls

def save(img_urls, title):
    if img_urls:
        try:
            dname = title.strip()  # 用 strip() 去除字串前後的空白
            os.makedirs(dname)
            for img_url in img_urls:
                if img_url.split('//')[1].startswith('m.'):
                    img_url = img_url.replace('//m.', '//i.')
                if not img_url.split('//')[1].startswith('i.'):
                    img_url = img_url.split('//')[0] + '//i.' + img_url.split('//')[1]
                if not img_url.endswith('.jpg'):
                    img_url += '.jpg'
                fname = img_url.split('/')[-1]
                urllib.request.urlretrieve(img_url, os.path.join(dname, fname))
        except Exception as e:
            print(e)

def save_pic(current_articles):
    PTT_URL = 'https://www.ptt.cc'
    for article in current_articles:
        page = get_web_page(PTT_URL + article['href'])
        if page:
            img_urls = parse(page)
            save(img_urls, article['title'])
            article['num_image'] = len(img_urls)

        
def save_json(current_articles):
    date = time.strftime("%Y%m%d")
    with open(date+'data.json', 'w', encoding='utf-8') as f:
        json.dump(current_articles, f, indent=2, sort_keys=True, ensure_ascii=False)

#main
PTT_URL = 'https://www.ptt.cc'
current_page = get_web_page(PTT_URL+'/bbs/Beauty/index.html')

if current_page:
    articles = []
    date = time.strftime("%m%d").lstrip('0') #today  drop 0 for ptt format
    date = ' '+date[0]+'/'+date[1:]
    current_articles, prev_url = get_articles(current_page,date)
    while current_articles: #if current_page have today article check prev_page
        articles += current_articles
        current_page = get_web_page(PTT_URL + prev_url)
        current_articles, prev_url = get_articles(current_page, date)
        
#    for post in articles:
#        print(post)
    
    save_pic(articles)
    save_json(articles)
    print('done')