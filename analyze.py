# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 21:31:11 2018

@author: saop0
"""
import math
import json

with open('data.json', 'r', encoding='utf-8') as f:
    data_list = json.load(f)
    images = []
    pushes = []
    for d in data_list:
        images.append(d['num_image'])
        pushes.append(d['push_count'])

print('圖片數:', images, 'Max:', max(images), 'Min:', min(images))
print('推文數:', pushes, 'Max:', max(pushes), 'Min:', min(pushes))

def mean(x):
    return sum(x) / len(x)

print('平均圖片數:', mean(images), '平均推文數:', mean(pushes))

def de_mean(x):
    x_bar = mean(x)
    return [x_i - x_bar for x_i in x]


def variance(x):
    deviations = de_mean(x)
    variance_x = 0
    for d in deviations:
        variance_x += d**2
    variance_x /= len(x)
    return variance_x


def dot(x, y):
    dot_product = sum(v_i * w_i for v_i, w_i in zip(x, y))
    dot_product /= (len(x))
    return dot_product

def correlation(x, y):
    variance_x = variance(x)
    variance_y = variance(y)
    sd_x = math.sqrt(variance_x)
    sd_y = math.sqrt(variance_y)
    dot_xy = dot(de_mean(x), de_mean(y))
    return dot_xy/(sd_x*sd_y)

print('相關係數:', correlation(images, pushes))

def decile(num):  # 將數字十分位化
    return (num // 10) * 10

from collections import Counter
histogram = Counter(decile(push) for push in pushes)
print(histogram)
# Counter({0: 17, 10: 6, 20: 2, 30: 1})

from matplotlib import pyplot as plt

#histogram
#plt.bar([x-4 for x in histogram.keys()], histogram.values(), 8)
#plt.axis([-5, 35, 0, 20])
#plt.title('Pushes')
#plt.xlabel('# of pushes')
#plt.ylabel('# of posts')
#plt.xticks([10 * i for i in range(4)])
#plt.show()

#scatter plot
plt.scatter(images, pushes)
plt.title('# of image v.s. push')
plt.xlabel('# of image')
plt.ylabel('# of push')
plt.axis('equal')
plt.show()

















