# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 21:30:18 2018

@author: saop0
"""
import requests
from bs4 import BeautifulSoup
import json
import time
import re
import os
import urllib.request
##http://blog.castman.net/%E6%95%99%E5%AD%B8/2016/12/19/python-data-science-tutorial-1.html
def get_web_page(url):
    time.sleep(0.5)
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
            if d.find('a'):
                href = d.find('a')['href']
                title = d.find('a').string
                articles.append({
                    'title': title,
                    'href': href,
                    'push_count': push_count
                    })
    return articles

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
    save_json(current_articles)
        
def save_json(current_articles):
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(current_articles, f, indent=2, sort_keys=True, ensure_ascii=False)

page = get_web_page('https://www.ptt.cc/bbs/Beauty/index.html')

if page:
    date = time.strftime("%m%d").lstrip('0') #today  drop 0 for ptt format
    date = ' '+date[0]+'/'+date[1:]
    current_articles = get_articles(page,date)
#    for post in current_articles:
#        print(post)
    
save_pic(current_articles) 
    
    
    
    
    
    
    