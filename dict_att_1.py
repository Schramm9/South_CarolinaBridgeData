# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 21:43:39 2021

@author: Chris
"""

import pandas as pd

import matplotlib.pyplot as plt

import xml.etree.ElementTree as et

import numpy as np

import matplotlib.pyplot as plt

import seaborn as sns

# Why was I using a dict?

# {'STRUCNUM' :'CS1'}
Bridges_17 = {'04' :'9', '08' :'14', '09' :'6', '16' :'21'}

# dfScatter_STRUCNUM is the dataframe that is meant to order the chronology of the observations on the x-axis by STRUCNUM increasing from lowest to highest STRUCNUM on a yearly basis.  

# How do I get the ENs out of the STRUCNUMs common to each set and then stack them in successive years?  Do I even need to?


# No EN associated 
# Can one be added to this format?
df17 = pd.DataFrame([{'STRUCNUM':'04','CS1':'14','Period':'03-31-2017'},
                   {'STRUCNUM':'08','CS1':'9','Period':'06-30-2017'},
                   {'STRUCNUM':'09','CS1':'21','Period':'09-30-2017'},
                   {'STRUCNUM':'11','CS1':'44','Period':'12-31-2017'}])

df['points']=df['points'].astype(float)
df['rebounds']=df['rebounds'].astype(float)
df['blocks']=df['blocks'].astype(float)
                   

# No EN associated 
# Can one be added to this format?
df18 = pd.DataFrame([{'STRUCNUM':'04','CS1':'34','Period':'03-31-2018'},
                   {'STRUCNUM':'08','CS1':'28','Period':'06-30-2018'},
                   {'STRUCNUM':'09','CS1':'40','Period':'09-30-2018'},
                   {'STRUCNUM':'11','CS1':'51','Period':'12-31-2018'}])
                

# No EN associated 
# Can one be added to this format?
df19 = pd.DataFrame([{'STRUCNUM':'04','CS1':'28','Period':'03-31-2019'},
                   {'STRUCNUM':'08','CS1':'12','Period':'06-30-2019'},
                   {'STRUCNUM':'09','CS1':'50','Period':'09-30-2019'},
                   {'STRUCNUM':'11','CS1':'39','Period':'12-31-2019'}])
                   

# No EN associated 
# Can one be added to this format?
df20 = pd.DataFrame([{'STRUCNUM':'04','CS1':'40','Period':'03-31-2020'},
                   {'STRUCNUM':'08','CS1':'24','Period':'06-30-2020'},
                   {'STRUCNUM':'09','CS1':'53','Period':'09-30-2020'},
                   {'STRUCNUM':'11','CS1':'48','Period':'12-31-2020'}])



df17.plot('Period', 'CS1')


dfScatter_STRUCNUM['Period'] = pd.to_datetime(dfScatter_STRUCNUM['Period'])

dfScatter_STRUCNUM = dfScatter_STRUCNUM.astype({"STRUCNUM": 'int32', "CS1": 'int32'})

dfScatter_STRUCNUM.sort_values(by=['STRUCNUM'])



# dfScatter_CSX is the dataframe that is meant to order the chronology of the observations on the x-axis by condition state (CSX, meaning the value of the condition state i.e. CS1, CS2 etc.) increasing from lowest to highest condition state value.  
dfScatter_CSX = pd.DataFrame([{'STRUCNUM':'04','CS1':'14','Period':'03-31-2017'},
                   {'STRUCNUM':'08','CS1':'9','Period':'06-30-2017'},
                   {'STRUCNUM':'09','CS1':'21','Period':'09-30-2017'},
                   {'STRUCNUM':'11','CS1':'44','Period':'12-31-2017'}])

dfScatter_STRUCNUM.plot('Period', 'CS1')

plt.scatter(dfScatter_STRUCNUM.Period, dfScatter_STRUCNUM.STRUCNUM.CS1)
