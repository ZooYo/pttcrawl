# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 16:49:36 2018

@author: saop0
"""

import requests
from bs4 import BeautifulSoup
import json
 
insta_url = 'https://www.ptt.cc/bbs/Beauty/M.1517487748.A.371.html'
 
res = requests.get(insta_url)
print(res.text)
soup = BeautifulSoup(res.text, "lxml")
#print(soup.text)
for img in soup.find_all('.richcontent'):
    print(img)
    #print(img.select('.imgur-embed-pub'))

#json_part = soup.find_all("script", type="text/javascript")[1].string
# 
## as json
#json_part = json_part[json_part.find('=')+2:-1]
#data = json.loads(json_part)
#image_url = data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['display_url']
# 
#img_data = requests.get(image_url).content
#print("Start downloading.")
#with open('download.jpg', 'wb') as handler:
#    handler.write(img_data)
#    print("Done.")