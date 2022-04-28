# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 12:39:15 2022

@author: Chris
"""


import pandas as pd

import xml.etree.ElementTree as et

import numpy as np

import matplotlib.pyplot as plt

import seaborn as sns

from functools import reduce


# Here I'm first creating a period range, then creating a DataFrame with the period range as the index.
index = pd.period_range('1/1/2020', periods=3, freq='Q')
df = pd.DataFrame(data=range(1, 4), index=index, columns=['count'])
df
df

df.resample('M', convention='start').sum()

for STRUCNUM_20 in df2020:
if STRUCNUM_20 in df2019:
print STRUCNUM_20, df2019[STRUCNUM_20]

for STRUCNUM_20 in df2020:
        for STRUCNUM_19 in df2019:
            if STRUCNUM_20 == STRUCNUM_19:
                key = STRUCNUM_20, df2019[STRUCNUM_20]
                
                
"""myRDP = { 'Actinobacter': 'GATCGA...TCA', 'subtilus sp.': 'ATCGATT...ACT' }
myNames = { 'Actinobacter': '8924342' }

rdpSet = set(myRDP)
namesSet = set(myNames)

for name in rdpSet.intersection(namesSet):
    print name, myNames[name]

# Prints: Actinobacter 8924342"""
                
""" for key in myRDP:
        for jey in myNames:
            if key == jey:
                print key, myNames[key] """
                
for STRUCNUM_20 in df2020:
    if STRUCNUM_20 in df2019:
        print(STRUCNUM_20, df2019[STRUCNUM_20])
                
""" for key in myRDP:
    if key in myNames:
        print key, myNames[key] """