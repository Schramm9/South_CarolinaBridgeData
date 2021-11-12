# -*- coding: utf-8 -*-
"""
Created on Sun Sep 26 12:59:54 2021

@author: Chris
"""

import pandas as pd
import xml.etree.ElementTree as et

import numpy as np

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

df2020.index

df2020.dtypes

df2020.head

""" df20_17 is a comparison of the data for the bridge conditions of year 2020 and 2019 """

df20_17 = pd.merge(df2020, df2019, suffixes=['_20', '_19'], on=['STRUCNUM','EN'])
""" merge 2020 and 2019 datasets with common structure and element nos."""


""" df20_19a = pd.merge(df2020, df2019, on='EN', how='left') """

df2020.keys()    

"""grouped_obj = df2020.groupby(["STRUCNUM"])
for key, item in grouped_obj:
    print("Key is: " + str(key))
    print(str(item), "\n\n")"""
    
df2018=parse_XML("2018SC_ElementData.xml", ["FHWAED", "STATE", "STRUCNUM", "EN", "EPN", "TOTALQTY", "CS1", "CS2", "CS3", "CS4"])
    
"""df20_17 = df20_17.merge(df2018, how='right', suffixes=[None, '_18'], on=['STRUCNUM','EN'])"""

df2017=parse_XML("2017SC_ElementData.xml", ["FHWAED", "STATE", "STRUCNUM", "EN", "EPN", "TOTALQTY_17", "CS1_17", "CS2_17", "CS3_17", "CS4_17"])

df18_17 = pd.merge(df2018, df2017, suffixes=['_18', '_17'], on=['STRUCNUM','EN'])
""" merge 2018 and 2017 datasets with common structure and element nos."""

df18_17.tail()

df2020.tail()

df2019.tail()

df2018.tail()

df2017.tail()

df20_17['STRUCNUM']. value_counts()

""" STRUCNUM Length = 9153 """

df18_17['STRUCNUM']. value_counts()

""" STRUCNUM Length = 9091 """

df18_17['STRUCNUM'].value_counts(dropna=False)

df18_17.groupby('STRUCNUM').count()
""" looking for no. of unique STRUCNUM (structure numbers) for the 2018 and 2017 datasets"""

""" 9091 unique bridges between 2018 and 2017 """
""" This is expected given the number is <= 9117 which is the highest possible no. of matches betw. the two years """

df20_17.groupby('STRUCNUM').count() 
""" df20_17 is intended to hold all 4 years eventually but currently only 2020 and 2019"""
""" looking for no. of unique STRUCNUM (structure numbers) for the 2020 and 2019 datasets"""

""" 9153 unique bridges between 2020 and 2019 """
""" This is expected given the number is <= 9221 which is the highest possible no. of matches betw. the two years """

df2020.groupby('STRUCNUM').count()
""" reorders the rows for each bridge based on the EN """

""" 9221 unique bridges surveyed for 2020  """

df2019.groupby('STRUCNUM').count()

""" 9251 unique bridges surveyed for 2019  """

df2018.groupby('STRUCNUM').count()

""" 9160 unique bridges surveyed for 2018  """

df2017.groupby('STRUCNUM').count()

""" 9117 unique bridges surveyed for 2017  """

"""df18_17.drop_duplicates(inplace=True)"""

"""df18_17.drop_duplicates(subset ="STRUCNUM",
                     keep = False, inplace = True)"""

df18_17A = pd.merge(df2018, df2017, suffixes=['_18', '_17'], on=['STRUCNUM'], indicator= True)

"""df18_17B = pd.merge(df2018, df2017, suffixes=['_18', '_17'], on=['EN'], indicator= True)"""

"""df18_17C = pd.merge(df2018, df2017, suffixes=['_18', '_17'], on=['EPN'], indicator= True)"""

df2020.drop_duplicates(inplace = True)

df20_17.drop_duplicates(inplace=True)

df20_17.isnull().sum()/df20_17.shape[0]
""" Percentages of column values that ARE null"""

df18_17.isnull().sum()/df18_17.shape[0]
""" Percentages of column values that ARE null"""

""" df18_17O = pd.merge(df2018, df2017, suffixes=['_18', '_17'], on=['STRUCNUM','EN'], validate='m:1') """
""" merge 2018 and 2017 datasets with common structure and element nos."""

df2017A=df2017.drop_duplicates(subset=['EN'])

df18_17.drop_duplicates(inplace=True)

df2018=df2018[df2018.EPN.isnull()]
""" df18_17 was creating more entries than the original due to additional entries created when EN = EPN that also had CS1-CS4 data as well """

df2017=df2017[df2017.EPN.isnull()]
""" the two ...EPN.isnull() expressions above are required to merge 2017 and 2018 properly while resulting in a number of STRUCNUM """
""" smaller than 9117, that being the total number of possible matches between the two datasets  """

df18_17 = pd.merge(df2018, df2017, suffixes=['_18', '_17'], on=['STRUCNUM','EN'])

""" How to combine all the df's into one??? """

dftotal = pd.merge(df20_17, df18_17, on=['STRUCNUM', 'EN'])
""" merge 2020 and 2019 datasets with common structure and element nos."""

df2018['STRUCNUM'] = df2018['STRUCNUM'].apply(lambda x: '{0:0>15}'.format(x))

df2017['STRUCNUM'] = df2017['STRUCNUM'].apply(lambda x: '{0:0>15}'.format(x))

df2019.columns

df2018.columns

df19_18 = pd.merge(df2019, df2018, suffixes=['_19', '_19'], on=['STRUCNUM','EN'])
""" try above again but run groupby first"""


df20_19_18 = pd.merge(df20_17, df2018, on=['STRUCNUM', 'EN'])

df20_19_18 = df20_19_18.drop('FHWAED_19', 1)

df20_19_18 = df20_19_18.drop('FHWAED', 1)


df20_19_18_17 = pd.merge(df20_17, df2017, on=['STRUCNUM', 'EN'])

""" data_frames=[df2020, df2019, df2018, df2017] """

"""data_frames=[df20_17, df18_17]"""

""" df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['STRUCNUM', 'EN'],
                                            how='outer'), data_frames) """

"""https://stackoverflow.com/questions/52223045/merge-multiple-dataframes-based-on-a-common-column"""

df20_19_18_17 = df20_19_18_17.drop('FHWAED_19', 1)

df20_19_18_17 = df20_19_18_17.drop('FHWAED', 1)


