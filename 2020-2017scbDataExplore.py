# -*- coding: utf-8 -*-
"""
Created on Sun Sep 26 12:59:54 2021

@author: Chris
"""

import pandas as pd
import xml.etree.ElementTree as et

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

""" df20_19 is a comparison of the data for the bridge conditions of year 2020 and 2019 """

df20_17 = pd.merge(df2020, df2019, suffixes=['_20', '_19'], on=['STRUCNUM','EN'])



""" df20_19a = pd.merge(df2020, df2019, on='EN', how='left') """

df2020.keys()    

"""grouped_obj = df2020.groupby(["STRUCNUM"])
for key, item in grouped_obj:
    print("Key is: " + str(key))
    print(str(item), "\n\n")"""
    
df2018=parse_XML("2018SC_ElementData.xml", ["FHWAED", "STATE", "STRUCNUM", "EN", "EPN", "TOTALQTY", "CS1", "CS2", "CS3", "CS4"])    
    
"""df20_17 = df20_17.merge(df2018, how='right', suffixes=[None, '_18'], on=['STRUCNUM','EN'])"""

df2017=parse_XML("2017SC_ElementData.xml", ["FHWAED", "STATE", "STRUCNUM", "EN", "EPN", "TOTALQTY", "CS1", "CS2", "CS3", "CS4"])    

df18_17 = pd.merge(df2018, df2017, suffixes=['_18', '_17'], on=['STRUCNUM','EN'])

df18_17.tail()

df2020.tail()

df2019.tail()

df2018.tail()

df2017.tail()

df18_17['STRUCNUM']. value_counts() 

df18_17['STRUCNUM'].value_counts(dropna=False)

df18_17.groupby('STRUCNUM').count() 

""" 9091 unique bridges between 2018 and 2017 """
""" This is expected given the number is <= 9117 which is the highest possible no. of matches betw. the two years """

df20_17.groupby('STRUCNUM').count() 

""" 9153 unique bridges between 2020 and 2019 """
""" This is expected given the number is <= 9221 which is the highest possible no. of matches betw. the two years """

df2020.groupby('STRUCNUM').count() 

""" 9221 unique bridges surveyed for 2020  """

df2019.groupby('STRUCNUM').count() 

""" 9251 unique bridges surveyed for 2019  """

df2018.groupby('STRUCNUM').count() 

""" 9160 unique bridges surveyed for 2018  """

df2017.groupby('STRUCNUM').count() 

""" 9117 unique bridges surveyed for 2017  """