# -*- coding: utf-8 -*-
"""
Created on Mon May 23 19:15:53 2022

@author: Chris
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#create some data with Names column
data = pd.DataFrame({'Names': ['Joe', 'John', 'Jasper', 'Jez'] *4, 'Ob1' : np.random.rand(16), 'Ob2' : np.random.rand(16)})

#create unique list of names
UniqueNames = data.Names.unique()

#create a data frame dictionary to store your data frames
DataFrameDict = {elem : pd.DataFrame() for elem in UniqueNames}

for key in DataFrameDict.keys():
    DataFrameDict[key] = data[:][data.Names == key]