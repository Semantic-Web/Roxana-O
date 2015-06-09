# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 22:23:29 2015

@author: roxana
"""

import matplotlib.pyplot as plt
import numpy as np
import csv 


def open_with_csv(filename, d = ','):
    data= []
    with open(filename) as tsvin:
        reader= csv.reader(tsvin, delimiter = d)
        for line in reader:
            data.append(line)
    return data
#==============================================================================
#     Main program here : 
#==============================================================================

counts = dict()             
data_from_csv = open_with_csv('datagovdatasetsviewmetrics.csv')
for line in data_from_csv[2:]:
    counts[line[2]] = counts.get(line[2], 0) + int(line[3])

lst = list()
new_list_organ =list()
new_list_views = list()

for key, val in counts.items():
    lst.append((val, key))
    
lst.sort(reverse=True)
for val, key in lst[:10]:
    print key.format(),'       ', val
    new_list_views.append(val)
    new_list_organ.append(key)
fig, ax =  plt.subplots()

N=10
index = np.arange(N)
bar_width = 0.50
opacity = 0.4
error_config = {'ecolor': '1'}
rect = plt.bar(index+0.2, new_list_views , bar_width,
                 alpha=opacity,
                 color='b')

plt.xlabel('Organization')
plt.ylabel('Views')
plt.title('Views by Organization')
plt.xticks(index + bar_width, index+1 )
plt.tight_layout()
plt.show()

#n_groups = 10
#fig, ax = plt.subplots()
