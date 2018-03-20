# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 02:29:16 2018

@author: saop0
"""

def test(img_urls):
    if img_urls:
        try:
            for img_url in img_urls:
                if img_url.split('//')[1].startswith('m.'):
                    img_url = img_url.replace('//m.', '//i.')
                if not img_url.split('//')[1].startswith('i.'):
                    img_url = img_url.split('//')[0] + '//i.' + img_url.split('//')[1]
                if not img_url.endswith('.jpg'):
                    img_url += '.jpg'
                fname = img_url.split('/')[-1]
                print(fname)
        except Exception as e:
            print('exception')
            print(e)

img_urls = ['http://i.imgur.com/sIdkDRV.jpg','https://i.imgur.com/amP6Y6K.jpg']
test(img_urls)