# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 16:29:08 2021

@author: Chris
"""

import pandas as pd
import xml.etree.ElementTree as et

import numpy as np

import io

from functools import reduce

def parse_XML(xml_file, df_cols): 
    """Thanks to Roberto Preste Author From XML to Pandas dataframes,
    from xtree ... to return out_df
    https://medium.com/@robertopreste/from-xml-to-pandas-dataframes-9292980b1c1c
    """
    
    xtree = et.parse(xml_file)
    xroot = xtree.getroot()
    rows = []
    
    for node in xroot: 
        res = []
        res.append(node.attrib.get(df_cols[0]))
        for el in df_cols[1:]: 
            if node is not None and node.find(el) is not None:
                res.append(node.find(el).text)
            else: 
                res.append(None)
        rows.append({df_cols[i]: res[i] 
                     for i, _ in enumerate(df_cols)})
    
    out_df = pd.DataFrame(rows, columns=df_cols)
        
    return out_df

df2020=parse_XML("2020SC_ElementData.xml", ["FHWAED", "STATE", "STRUCNUM", "EN", "EPN", "TOTALQTY", "CS1", "CS2", "CS3", "CS4"])

df2019=parse_XML("2019SC_ElementData.xml", ["FHWAED", "STATE", "STRUCNUM", "EN", "EPN", "TOTALQTY", "CS1", "CS2", "CS3", "CS4"])

"""End Roberto Preste code From XML to Pandas dataframes,
    from xtree ... to return out_df
    https://medium.com/@robertopreste/from-xml-to-pandas-dataframes-9292980b1c1c
"""

df2018=parse_XML("2018SC_ElementData.xml", ["FHWAED", "STATE", "STRUCNUM", "EN", "EPN", "TOTALQTY", "CS1", "CS2", "CS3", "CS4"])

df2017=parse_XML("2017SC_ElementData.xml", ["FHWAED", "STATE", "STRUCNUM", "EN", "EPN", "TOTALQTY", "CS1", "CS2", "CS3", "CS4"])

df2020.groupby('STRUCNUM').count()
""" reorders the rows for each bridge based on the EN """

""" 9221 unique bridges surveyed for 2020  """

df2019.groupby('STRUCNUM').count()

""" 9251 unique bridges surveyed for 2019  """

df2018.groupby('STRUCNUM').count()

""" 9160 unique bridges surveyed for 2018  """

df2017.groupby('STRUCNUM').count()

""" 9117 unique bridges surveyed for 2017  """

df2018=df2018[df2018.EPN.isnull()]
""" df18_17 was creating more entries than the original due to additional entries created when EN = EPN that also had CS1-CS4 data as well """

df2017=df2017[df2017.EPN.isnull()]
""" the two ...EPN.isnull() expressions above are required to merge 2017 and 2018 properly while resulting in a number of STRUCNUM """
""" smaller than 9117, that being the total number of possible matches between the two datasets  """

df2018['STRUCNUM'] = df2018['STRUCNUM'].apply(lambda x: '{0:0>15}'.format(x))

df2017['STRUCNUM'] = df2017['STRUCNUM'].apply(lambda x: '{0:0>15}'.format(x))

df20_19 = pd.merge(df2020, df2019, suffixes=['_20', '_19'], on=['STRUCNUM','EN'])
""" merge 2020 and 2019 datasets with common structure and element nos."""

df20_19_18 = pd.merge(df20_19, df2018, how= 'inner', on=['STRUCNUM', 'EN'])

df20_19_18 = df20_19_18.rename({"CS1":"CS1_18", "CS2":"CS2_18", "CS3":"CS3_18", "CS4":"CS4_18"}, axis='columns')

df20_19_18_17 = pd.merge(df20_19_18, df2017, on=['STRUCNUM', 'EN'])

df20_19_18_17 = df20_19_18_17.rename({"TOTALQTY_x":"TOTALQTY_18", "TOTALQTY_y":"TOTALQTY_17", "CS1":"CS1_17", "CS2":"CS2_17", "CS3":"CS3_17", "CS4":"CS4_17"}, axis='columns')

df20_19_18_17 = df20_19_18_17.drop(columns=['FHWAED_20', 'EPN_20', 'FHWAED_19', 'STATE_19', 'EPN_19', 'FHWAED_x', 'STATE_x', 'EPN_x', 'FHWAED_y', 'STATE_y', 'EPN_y'])

#Begin Exploration

# My hypothesis is that the condition state data consisting of CS1 through CS4 will increase with time

# How much do the condition state values change with time?  

# Can the bridges with the elements approaching CS4 (i.e. critical) be distinguished from the others?

df20_19_18_17.shape

#37085 Rows by 23 Columns

df20_19_18_17.head

#Data is sorted by STRUCNUM, numerically (low to high) 

df20_19_18_17.columns

df20_19_18_17.info()

# All data in the df20_19_18_17 dataframe is non-null object type

df20_19_18_17.describe()

df20_19_18_17.isnull().any

df20_19_18_17.isnull().sum()

df20_19_18_17.isnull().sum() / df20_19_18_17.shape[0]

df20_19_18_17.dtypes

#df20_19_18_17.type
#df20_19_18_17['type']

#df20_19_18_17.dtype.unique()

#df20_19_18_17.type.value_counts()

#df20_19_18_17.variable.unique()



df20_19_18_17['STATE_20'] = pd.to_numeric(df20_19_18_17['STATE_20'],errors='coerce')
df20_19_18_17 = df20_19_18_17.replace(np.nan, 0, regex=True)
df20_19_18_17['STATE_20'] = df20_19_18_17['STATE_20'].astype(int)


df20_19_18_17['STATE_20'] = pd.to_numeric(df20_19_18_17['STATE_20'],errors='coerce')
df20_19_18_17 = df20_19_18_17.replace(np.nan, 0, regex=True)
df20_19_18_17['STATE_20'] = df20_19_18_17['STATE_20'].astype(int)


# Spent a lot of time looking for a method to change data types efficiently, but I want to get this application in, so...

df20_19_18_17 = df20_19_18_17.astype({"STATE_20": 'int32', "STRUCNUM": 'int32', "EN": 'int32', "TOTALQTY_20": 'int32', "CS1_20": 'int32', "CS2_20": 'int32', "CS3_20": 'int32', "CS4_20": 'int32', "TOTALQTY_19": 'int32', "CS1_19": 'int32', "CS2_19": 'int32', "CS3_19": 'int32', "CS4_19": 'int32', "TOTALQTY_18": 'int32', "CS1_18": 'int32', "CS2_18": 'int32', "CS3_18": 'int32', "CS4_18": 'int32', "TOTALQTY_17": 'int32', "CS1_17": 'int32', "CS2_17": 'int32', "CS3_17": 'int32', "CS4_17": 'int32'})

# Apologies for the ugly brute force nature of line 151.

#cols = df20_19_18_17.select_dtypes(exclude=['int']).columns

#df20_19_18_17 = pd.to_numeric([cols], errors='coerce').fillna(0).astype(np.int64)

#cols = df20_19_18_17.select_dtypes(exclude=['int']).columns

#df20_19_18_17[cols] = df20_19_18_17[cols].apply(pd.to_numeric, downcast='int', errors='coerce')

#df20_19_18_17['CS1_17'] = df20_19_18_17['CS1_17'].astype('|S80')

#df20_19_18_17['CS1_17'].astype('float')

#df20_19_18_17['CS1_17'] = df20_19_18_17['CS1_17'].astype('float')

#df20_19_18_17['CS1_17'] = df20_19_18_17['CS1_17'].astype('str')

#df20_19_18_17['CS1_17'] = df20_19_18_17.CS1_17.astype(int())

#df20_19_18_17['CS1_18'] = df20_19_18_17['CS1_18'].astype('str') # #doesn't work

#df20_19_18_17['CS1_18'].dtype # still gives an object as dtype

#df20_19_18_17['CS1_18'].str.decode("utf-8")

df20_19_18_17.info()

#['CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']

#df20_19_18_17.CS4_20.sum().hist()


TotCS1_17 = df20_19_18_17['CS1_17'].sum()
df20_19_18_17.loc['TotCS1_17'] = pd.Series(df20_19_18_17['CS1_17'].sum(), index = ['CS1_17'])
TotCS2_17 = df20_19_18_17['CS2_17'].sum()
TotCS2_17 = int(TotCS2_17)
df20_19_18_17.loc['TotCS2_17'] = pd.Series(df20_19_18_17['CS2_17'].sum(), index = ['CS2_17'])
TotCS3_17 = df20_19_18_17['CS3_17'].sum()
TotCS3_17 = int(TotCS3_17)
df20_19_18_17.loc['TotCS3_17'] = pd.Series(df20_19_18_17['CS3_17'].sum(), index = ['CS3_17'])
TotCS4_17 = df20_19_18_17['CS4_17'].sum()
TotCS4_17 = int(TotCS4_17)
df20_19_18_17.loc['TotCS4_17'] = pd.Series(df20_19_18_17['CS4_17'].sum(), index = ['CS4_17'])

# TOTCS1_17 = 46489296

# TOTCS2_17 = 25322220

# TOTCS3_17 = 1521673

# TOTCS4_17 = 201358

TotCS1_18 = df20_19_18_17['CS1_18'].sum()
TotCS1_18 = int(TotCS1_18)
df20_19_18_17.loc['TotCS1_18'] = pd.Series(df20_19_18_17['CS1_18'].sum(), index = ['CS1_18'])
TotCS2_18 = df20_19_18_17['CS2_18'].sum()
TotCS2_18 = int(TotCS2_18)
df20_19_18_17.loc['TotCS2_18'] = pd.Series(df20_19_18_17['CS2_18'].sum(), index = ['CS2_18'])
TotCS3_18 = df20_19_18_17['CS3_18'].sum()
TotCS3_18 = int(TotCS3_18)
df20_19_18_17.loc['TotCS3_18'] = pd.Series(df20_19_18_17['CS3_18'].sum(), index = ['CS3_18'])
TotCS4_18 = df20_19_18_17['CS4_18'].sum()
TotCS4_18 = int(TotCS4_18)
df20_19_18_17.loc['TotCS4_18'] = pd.Series(df20_19_18_17['CS4_18'].sum(), index = ['CS4_18'])

# TOTCS1_18 = 45280654

# TOTCS2_18 = 26514152

# TOTCS3_18 = 1653895

# TOTCS4_18 = 230337

TotCS1_19 = df20_19_18_17['CS1_19'].sum()
TotCS1_19 = int(TotCS1_19)
df20_19_18_17.loc['TotCS1_19'] = pd.Series(df20_19_18_17['CS1_19'].sum(), index = ['CS1_19'])
TotCS2_19 = df20_19_18_17['CS2_19'].sum()
TotCS2_19 = int(TotCS2_19)
df20_19_18_17.loc['TotCS2_19'] = pd.Series(df20_19_18_17['CS2_19'].sum(), index = ['CS2_19'])
TotCS3_19 = df20_19_18_17['CS3_19'].sum()
TotCS3_19 = int(TotCS3_19)
df20_19_18_17.loc['TotCS3_19'] = pd.Series(df20_19_18_17['CS3_19'].sum(), index = ['CS3_19'])
TotCS4_19 = df20_19_18_17['CS4_19'].sum()
TotCS4_19 = int(TotCS4_19)
df20_19_18_17.loc['TotCS4_19'] = pd.Series(df20_19_18_17['CS4_19'].sum(), index = ['CS4_19'])

# TOTCS1_19 = 46242954

# TOTCS2_19 = 24646319

# TOTCS3_19 = 1400803

# TOTCS4_19 = 1018715

TotCS1_20 = df20_19_18_17['CS1_20'].sum()
TotCS1_20 = int(TotCS1_20)
df20_19_18_17.loc['TotCS1_20'] = pd.Series(df20_19_18_17['CS1_20'].sum(), index = ['CS1_20'])
TotCS2_20 = df20_19_18_17['CS2_20'].sum()
TotCS2_20 = int(TotCS2_20)
df20_19_18_17.loc['TotCS2_20'] = pd.Series(df20_19_18_17['CS2_20'].sum(), index = ['CS2_20'])
TotCS3_20 = df20_19_18_17['CS3_20'].sum()
TotCS3_20  = int(TotCS3_20)
df20_19_18_17.loc['TotCS3_20'] = pd.Series(df20_19_18_17['CS3_20'].sum(), index = ['CS3_20'])
TotCS4_20 = df20_19_18_17['CS4_20'].sum()
TotCS4_20 = int(TotCS4_20)
df20_19_18_17.loc['TotCS4_20'] = pd.Series(df20_19_18_17['CS4_20'].sum(), index = ['CS4_20'])

# TOTCS1_20 = 47434320

# TOTCS2_20 = 23145920

# TOTCS3_20 = 1881722

# TOTCS4_20 = 181230

# As it turns out these totals are meaningless because the dimensions of the Condition States vary depending on the EN.
# Going to attempt to discern how many different ENs there are in the 'EN' column and the quantity of each

EN_list = df20_19_18_17["EN"].tolist()

EN_list = list(df20_19_18_17.EN.value_counts())

s =  pd.value_counts(df20_19_18_17.EN)
s1 = pd.Series({'nunique': len(s), 'unique values': s.index.tolist()})
s.append(s1)

while s1 :
    
    while counter < len(s1):



import seaborn as sns

import matplotlib.pyplot as plt
#%matplotlib inline
sns.set_theme(style='darkgrid', color_codes=True)

sns.displot(data=df20_19_18_17, x=['2017','2018','2019','2020'], aspect=1.6, bins=30)
plt.title('Bridges w/ CS4 > 0 for 2017', fontsize=16)

x = ['2017','2018','2019','2020']



#column_name = "CS1_17"
#column_sum = df20_19_18_17[column_name].sum()


#def getSum(n):
     
 #   strr = str(n)
  #  column_name = list(map(int(float, strr.strip())))
   # return sum(column_name)

#print(getSum('CS1_17'))

#print(column_sum)

y1=np.array(['CS1_17'+'CS2_17'+'CS3_17'+'CS4_17'])
y2=np.array(['CS2_17'])



#y1=np.array(['CS1_17', 'CS2_17', 'CS3_17', 'CS4_17'])
#y2=np.array(['CS1_18', 'CS2_18', 'CS3_18', 'CS4_18'])


plt.bar(x, y1, color='r')
plt.bar(x, y2, bottom=y1, color='b')
plt.xlabel("Survey Year")

# Python program to find sum of elements in list
total = 0
# creating a list
list1 = ['CS1_17']
 
[float(i) for i in list]

np.array('CS_17', dtype=np.float32)

"""# Iterate each element in list
# and add them in variable total
for ele in range(0, len(list1)):
    total = total + list1[ele]

# printing total value
print("Sum of all elements in given list: ", total)

sum('CS1_17')

# Python program to find sum of elements in list
 
# creating a list
list1 = ['CS1_17']
"""
dataTypeSeries = df20_19_18_17.dtypes

print(df20_19_18_17.dtypes)
"""
total = df20_19_18_17['CS1_17'].sum()

sum(list1, 0)
df20_19_18_17.sum
# using sum() function
total = sum(list1)
 
# printing total value
print("Sum of all elements in given list: ", total)

""" 

"""# Python program to find sum of elements in list
total = 0
 
# creating a list
list1 = [11, 5, 17, 18, 23]
 
# Iterate each element in list
# and add them in variable total
for ele in range(0, len(list1)):
    total = total + list1[ele]
 
# printing total value
print("Sum of all elements in given list: ", total)"""

