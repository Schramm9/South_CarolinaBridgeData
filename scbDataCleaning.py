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

# total of all CS1 thru CS4 with units of Square Feet

# df20_19_18_17['EN'] = np.where(df20_19_18_17['EN'].values >= 12) & (df20_19_18_17['EN'].values <= 65), sum('CS1_17')


# Units of Square Feet
# EN 12 - 65 dfDeckSlab refers to bridge elements decks and slabs with a Condition State measured in square feet
dfDeckSlab = df20_19_18_17.loc[(df20_19_18_17['EN'] >= 12) & (df20_19_18_17['EN'] <= 65), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17']]

# EN 320 - 321 dfApprSlabs refers to bridge elements approach slabs with a Condition State measured in square feet
dfApprSlabs = df20_19_18_17.loc[(df20_19_18_17['EN'] >= 320) & (df20_19_18_17['EN'] <= 321), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17']]

# EN 510 -522 dfWearSfc refers to bridge elements wearing surfaces with a Condition State measured in square feet
dfWearSfc = df20_19_18_17.loc[(df20_19_18_17['EN'] >= 510) & (df20_19_18_17['EN'] <= 522), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17']]


# Units of Linear Feet
# EN 102 - 112 dfGirders refers to bridge elements of the superstructure with a Condition State measured in linear feet
dfGirders = df20_19_18_17.loc[(df20_19_18_17['EN'] >= 102) & (df20_19_18_17['EN'] <= 112), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17']]

# EN 120 - 146 dfTrussArch trusses and arches Condition State measured in linear feet
dfTrussArch = df20_19_18_17.loc[(df20_19_18_17['EN'] >= 120) & (df20_19_18_17['EN'] <= 146), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17']]

# EN 113 - 118 dfStringers bridge stringers Condition State measured in linear feet
dfStringers = df20_19_18_17.loc[(df20_19_18_17['EN'] >= 113) & (df20_19_18_17['EN'] <= 118), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17']]

# EN 152 - 157 dfFlrBm floor beams Condition State measured in linear feet
dfFlrBm = df20_19_18_17.loc[(df20_19_18_17['EN'] >= 152) & (df20_19_18_17['EN'] <= 157), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17']]

# EN 147 - 149 dfMiscSup miscellaneous superstructure elements Condition State measured in linear feet
dfMiscSup = df20_19_18_17.loc[(df20_19_18_17['EN'] >= 147) & (df20_19_18_17['EN'] <= 149), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17']]

# EN 215 - 219 dfAbutments Abutment elements Condition State measured in linear feet
dfAbutments = df20_19_18_17.loc[(df20_19_18_17['EN'] >= 215) & (df20_19_18_17['EN'] <= 219), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17']]

# EN 231 - 236 dfPierCaps Pier Cap elements Condition State measured in linear feet
dfPierCaps = df20_19_18_17.loc[(df20_19_18_17['EN'] >= 231) & (df20_19_18_17['EN'] <= 236), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17']]

# EN 207 dfTwrSteel Tower Steel elements Condition State measured in linear feet
dfTwrSteel = df20_19_18_17.loc[(df20_19_18_17['EN'] == 207), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18']]

# EN 208 dfTresTimb Trestle elements made of Timber Condition State measured in linear feet
dfTresTimb = df20_19_18_17.loc[(df20_19_18_17['EN'] == 208), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17']]

# EN 210 - 213 dfPierWalls Pier Wall elements Condition State measured in linear feet
dfPierWalls = df20_19_18_17.loc[(df20_19_18_17['EN'] >= 210) & (df20_19_18_17['EN'] <= 213), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17']]

# EN 220 dfPCFRC Pile Cap/Footing - Reinforced Concrete elements Condition State measured in linear feet
dfPCFRC = df20_19_18_17.loc[(df20_19_18_17['EN'] == 220), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18']]

# EN 240 - 245 dfCulv Culvert elements Condition State measured in linear feet
dfCulv = df20_19_18_17.loc[(df20_19_18_17['EN'] >= 240) & (df20_19_18_17['EN'] <= 245), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17']]

# EN 250 dfTunnel Tunnel - Checking for this to be sure it is not present as the literature says it is no longer in purview
dfTunnel = df20_19_18_17.loc[(df20_19_18_17['EN'] == 250), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# EN 330 - 334 dfBrdgRail Varied Bridge Railing elements Condition State measured in linear feet (330 Metal, 331 RC, 332 Timb, 333 Other, 334 Masonry)
dfBrdgRail = df20_19_18_17.loc[(df20_19_18_17['EN'] >= 330) & (df20_19_18_17['EN'] <= 334), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17']]

# EN 300 - 309 dfJoints Varied Joint elements Condition State measured in linear feet
dfJoints = df20_19_18_17.loc[(df20_19_18_17['EN'] >= 300) & (df20_19_18_17['EN'] <= 309), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17']]

# EN 170 dfRRCF Rail Road Car Frame elements Condition State measured in linear feet
dfRRCF = df20_19_18_17.loc[(df20_19_18_17['EN'] == 170), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17']]


# Units of Each Below
# EN 161 dfPin Steel Pin and Pin hanger assembly elements Condition State measured in units of each
dfPin = df20_19_18_17.loc[(df20_19_18_17['EN'] == 161), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# EN 162 dfGusset Steel Gusset Plate elements Condition State measured in units of each
dfGusset = df20_19_18_17.loc[(df20_19_18_17['EN'] == 162), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# EN 171 dfSTEELMiscSup Miscellaneous Steel Superstructures elements Condition State measured in units of each
dfSTEELMiscSup = df20_19_18_17.loc[(df20_19_18_17['EN'] == 171), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# EN 180 dfEQRCII Earthquake Restrainer Cables Type II Condition State measured in units of each
dfEQRCII = df20_19_18_17.loc[(df20_19_18_17['EN'] == 180), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# EN 181 dfEQRCC1 Earthquake Restrainer Cables - C1 Condition State measured in units of each
dfEQRCC1 = df20_19_18_17.loc[(df20_19_18_17['EN'] == 181), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# EN 182 dfEQROther Earthquake Restrainer Cables - Other Condition State measured in units of each
dfEQROther = df20_19_18_17.loc[(df20_19_18_17['EN'] == 182), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# EN 202 - 206 Column elements Condition State measured in units of each

# Additionally it would be helpful for the number of each of the elements below PER BRIDGE were known- 



# EN 311 dfBrgMov Bearing Type - Moveable Bearing elements Condition State measured in units of each
dfBrgMov = df20_19_18_17.loc[(df20_19_18_17['EN'] == 311), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

dfBrgMov_20 = df20_19_18_17.loc[(df20_19_18_17['EN'] == 311), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]



# EN 312 dfBrgEC Bearing Type - Enclosed/Concealed Bearing elements Condition State measured in units of each
dfBrgEC = df20_19_18_17.loc[(df20_19_18_17['EN'] == 312), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# EN 313 dfBrgFixed Bearing Type - Fixed Bearing elements Condition State measured in units of each
dfBrgFixed = df20_19_18_17.loc[(df20_19_18_17['EN'] == 313), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# EN 314 dfBrgPot Bearing Type - Pot Bearing elements Condition State measured in units of each
dfBrgPot = df20_19_18_17.loc[(df20_19_18_17['EN'] == 314), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# EN 315 dfBrgDisk Bearing Type - Disk Bearing elements Condition State measured in units of each
dfBrgDisk = df20_19_18_17.loc[(df20_19_18_17['EN'] == 315), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# EN 316 dfBrgOther Bearing Type - Other Bearing elements Condition State measured in units of each
dfBrgOther = df20_19_18_17.loc[(df20_19_18_17['EN'] == 316), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]
# End Bearings


# EN 202 dfColSt Steel Column elements Condition State measured in units of each
dfColSt = df20_19_18_17.loc[(df20_19_18_17['EN'] == 202), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# EN 203 dfColOther Column elements of type Other Condition State measured in units of each
dfColOther = df20_19_18_17.loc[(df20_19_18_17['EN'] == 203), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# EN 204 dfColPrConc Prestressed Concrete Column elements Condition State measured in units of each
dfColPrConc = df20_19_18_17.loc[(df20_19_18_17['EN'] == 204), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# EN 205 dfColRfConc Reinforced Concrete Column elements Condition State measured in units of each
dfColRfConc = df20_19_18_17.loc[(df20_19_18_17['EN'] == 205), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# EN 206 dfColTimb Timber Column elements Condition State measured in units of each
dfColTimb = df20_19_18_17.loc[(df20_19_18_17['EN'] == 206), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# EN 225 dfPileSteel Pile - Steel Condition State measured in units of each
dfPileSteel = df20_19_18_17.loc[(df20_19_18_17['EN'] == 225), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# EN 226 dfPilePrConc Pile - Prestressed Concrete Condition State measured in units of each
dfPilePrConc = df20_19_18_17.loc[(df20_19_18_17['EN'] == 226), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# EN 227 dfPileRC Pile of Type - Reinforced Concrete Condition State measured in units of each
dfPileRC = df20_19_18_17.loc[(df20_19_18_17['EN'] == 227), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# EN 228 dfPileTimb Pile of Type - Timber Condition State measured in units of each
dfPileTimb = df20_19_18_17.loc[(df20_19_18_17['EN'] == 228), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# EN 229 dfPileOther Pile of Type - Other Condition State measured in units of each
dfPileOther = df20_19_18_17.loc[(df20_19_18_17['EN'] == 229), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# EN 251 dfPileCISS Pile- cast in steel shell Condition State measured in units of each
dfPileCISS = df20_19_18_17.loc[(df20_19_18_17['EN'] == 251), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# EN 252 dfPileCIDH Pile- cast in Drilled Hole Condition State measured in units of each
dfPileCIDH = df20_19_18_17.loc[(df20_19_18_17['EN'] == 252), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# EN 254 dfStSeisFH Steel Seismic Column Shells - Full Height Condition State measured in units of each
dfStSeisFH = df20_19_18_17.loc[(df20_19_18_17['EN'] == 254), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# EN 255 dfStSeisPH Steel Seismic Column Shells - Partial Height Condition State measured in units of each
dfStSeisPH = df20_19_18_17.loc[(df20_19_18_17['EN'] == 255), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# EN 256 dfSSP Slope/Scour Protection Condition State measured in units of each
dfSSP = df20_19_18_17.loc[(df20_19_18_17['EN'] == 256), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]



dfBrgDisk.boxplot('CS1_18','CS1_19')

# dfBrgDisk.hist('CS1_18')

# dfBrgDisk.plot(y='CS1_17', 'CS1_18', 'CS1_19', 'CS1_20’, x=’2017', '2018', '2019', '2020’)
# plt.show()

# dfBrgDisk.plot(y='CS1_17', 'CS1_18', 'CS1_19', 'CS1_20’, x=’year')

# Bearings (Brg)
# EN 310 dfBrgEl Bearing Type - Elastomeric Bearing elements Condition State measured in units of each
# Below start pulling out the entries in the merged df that are Elastomeric Bearings or ['EN'] == 310
dfBrgEl = df20_19_18_17.loc[(df20_19_18_17['EN'] == 310), ['STRUCNUM', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

dfBrgEl.insert(1, '2017', '2017')

dfBrgEl.insert(2, '2018', '2018')

dfBrgEl.insert(3, '2019', '2019')

dfBrgEl.insert(4, '2020', '2020')


# Elastomeric Bearings Yr 2020
dfBrgEl_20 = df20_19_18_17.loc[(df20_19_18_17['EN'] == 310), ['STRUCNUM', 'CS1_20', 'CS2_20',  'CS3_20', 'CS4_20']]

# Elastomeric Bearings Yr 2019
dfBrgEl_19 = df20_19_18_17.loc[(df20_19_18_17['EN'] == 310), ['STRUCNUM', 'CS1_19', 'CS2_19', 'CS3_19', 'CS4_19']]

# Elastomeric Bearings Yr 2018
dfBrgEl_18 = df20_19_18_17.loc[(df20_19_18_17['EN'] == 310), ['STRUCNUM', 'CS1_18', 'CS2_18', 'CS3_18', 'CS4_18']]

# Elastomeric Bearings Yr 2017
dfBrgEl_17 = df20_19_18_17.loc[(df20_19_18_17['EN'] == 310), ['STRUCNUM', 'CS1_17', 'CS2_17',  'CS3_17', 'CS4_17']]


# This was an attempt to make some plots- I believe I need to resample parts of my data for best results!
import matplotlib.pyplot as plt

# dfBrgEl.plot(kind='scatter', y=['CS1_20', 'CS2_20', 'CS3_20', 'CS4_20'], x= '2020')

arrData = np.array(dfBrgEl)

print(arrData.size)
print(arrData.shape)

dfBrgEl.plot(kind='scatter', y='CS1_20', x= '2020')
plt.show()

dfBrgEl.CS1_20.max()

dfBrgEl.plot(kind='scatter', y='CS2_20', x= '2020')
plt.show()

dfBrgEl.CS2_20.max()


# resample from yearly to monthly dfBrgEl_CS1 is the df I'm using for the purpose of linear regression Condition State 1

import datetime

# dfBrgEl_M is the dataframe to be converted to monthly intervals thru resample
index = pd.date_range('12/31/2017', periods=4, freq='Y')
dfBrgEl_M = pd.DataFrame(data=range(4), index=index, columns=['count'])
dfBrgEl_M

# Sum the number of elastomeric bearings in CS1
BrgElCS1_17 = dfBrgEl['CS1_17'].sum()

BrgElCS1_18 = dfBrgEl['CS1_18'].sum()

BrgElCS1_19 = dfBrgEl['CS1_19'].sum()

BrgElCS1_20 = dfBrgEl['CS1_20'].sum()

# Declare a list for the new column in dfBrgEl_M

BrgEl_CS1 = [dfBrgEl['CS1_17'].sum(), dfBrgEl['CS1_18'].sum(), dfBrgEl['CS1_19'].sum(), dfBrgEl['CS1_20'].sum()]

dfBrgEl_M['CS1'] = BrgEl_CS1

# Sum the number of elastomeric bearings in CS2

# Declare a list for the new column in dfBrgEl_M

BrgEl_CS2 = [dfBrgEl['CS2_17'].sum(), dfBrgEl['CS2_18'].sum(), dfBrgEl['CS2_19'].sum(), dfBrgEl['CS2_20'].sum()]

dfBrgEl_M['CS2'] = BrgEl_CS2
 
# Sum the number of elastomeric bearings in CS3

# Declare a list for the new column in dfBrgEl_M

BrgEl_CS3 = [dfBrgEl['CS3_17'].sum(), dfBrgEl['CS3_18'].sum(), dfBrgEl['CS3_19'].sum(), dfBrgEl['CS3_20'].sum()]

dfBrgEl_M['CS3'] = BrgEl_CS3

# Sum the number of elastomeric bearings in CS4

# Declare a list for the new column in dfBrgEl_M

BrgEl_CS4 = [dfBrgEl['CS4_17'].sum(), dfBrgEl['CS4_18'].sum(), dfBrgEl['CS4_19'].sum(), dfBrgEl['CS4_20'].sum()]

dfBrgEl_M['CS4'] = BrgEl_CS4

dfBrgEl_M.set_index(index).resample('M').bfill().reset_index()


dfBrgEl_M = df.insert




""" for node in xroot: 
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
    
return out_df """





while s1 :
    
    while counter < len(s1):



import seaborn as sns


+#%matplotlib inline
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

