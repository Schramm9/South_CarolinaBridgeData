# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 16:29:08 2021
@author: Chris
"""

import pandas as pd
import xml.etree.ElementTree as et

import numpy as np
import numpy.ma as ma

import io

import os

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
    

"""End Roberto Preste code From XML to Pandas dataframes,
    from xtree ... to return out_df

    https://medium.com/@robertopreste/from-xml-to-pandas-dataframes-9292980b1c1c
"""

df2021=parse_XML("2021SC_ElementData.xml", ["FHWAED", "STATE", "STRUCNUM", "EN", "EPN", "TOTALQTY", "CS1", "CS2", "CS3", "CS4"])
# 48562

df2020=parse_XML("2020SC_ElementData.xml", ["FHWAED", "STATE", "STRUCNUM", "EN", "EPN", "TOTALQTY", "CS1", "CS2", "CS3", "CS4"])
# 52619

df2019=parse_XML("2019SC_ElementData.xml", ["FHWAED", "STATE", "STRUCNUM", "EN", "EPN", "TOTALQTY", "CS1", "CS2", "CS3", "CS4"])
# 52036

df2018=parse_XML("2018SC_ElementData.xml", ["FHWAED", "STATE", "STRUCNUM", "EN", "EPN", "TOTALQTY", "CS1", "CS2", "CS3", "CS4"])
# 57830

df2017=parse_XML("2017SC_ElementData.xml", ["FHWAED", "STATE", "STRUCNUM", "EN", "EPN", "TOTALQTY", "CS1", "CS2", "CS3", "CS4"])
# 57624

df2021.groupby('STRUCNUM').count()

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
""" df18_17 was creating more entries than the original due to additional entries created when EN = EPN that also had cs1-cs4 data as well """

df2017=df2017[df2017.EPN.isnull()]
""" the two ...EPN.isnull() expressions above are required to merge 2017 and 2018 properly while resulting in a number of STRUCNUM """
""" smaller than 9117, that being the total number of possible matches between the two datasets  """

df2018['STRUCNUM'] = df2018['STRUCNUM'].apply(lambda x: '{0:0>15}'.format(x))

df2017['STRUCNUM'] = df2017['STRUCNUM'].apply(lambda x: '{0:0>15}'.format(x))

""" the STRUCNUM columns in the 2017 and 2018 sets were a total length of 13 digits, most of those are leading zeros, the two expressions above are placing additional zeros at the left hand side of the entries to merge those sets properly where the STRUCNUM overlap """


df20_19 = pd.merge(df2020, df2019, suffixes=['_20', '_19'], on=['STRUCNUM','EN']) # Keeping the observations that match by structure number (STRUCNUM) and that have the same element numbers (EN) wuthin that STRUCNUM.  

# df20_19c = pd.concat(df2020, df2019, on=['STRUCNUM','EN'])

# Axis 0 means rows, 1 means columns



""" merge 2020 and 2019 datasets with common structure (STRUCNUM) and element nos. (EPN) and the columns being distinguished by year via suffixes """

df20_19_18 = pd.merge(df20_19, df2018, how= 'inner', on=['STRUCNUM', 'EN'])

""" merge the 2018 dataframe into the already merged 2020 and 2019 dataframe """

df20_19_18 = df20_19_18.rename({"CS1":"CS1_18", "CS2":"CS2_18", "CS3":"CS3_18", "CS4":"CS4_18"}, axis='columns')

""" rename the column headings to distinguish the condition state (cs1-cs4) entries by year """

df20_19_18_17 = pd.merge(df20_19_18, df2017, on=['STRUCNUM', 'EN'])

""" merge the 2017 set into the other 3 years (could they all be merged at once?) """


df20_19_18_17 = df20_19_18_17.rename({"TOTALQTY_x":"TOTALQTY_18", "TOTALQTY_y":"TOTALQTY_17", "cs1":"CS1_17", "cs2":"CS2_17", "cs3":"CS3_17", "cs4":"CS4_17"}, axis='columns')

""" rename the column headings based on year """

df20_19_18_17 = df20_19_18_17.drop(columns=['FHWAED_20', 'EPN_20', 'FHWAED_19', 'STATE_19', 'EPN_19', 'FHWAED_x', 'STATE_x', 'EPN_x', 'FHWAED_y', 'STATE_y', 'EPN_y'])

""" removing superfluous columns """

# !!! 12/10

# Begin Exploration

# My hypothesis is that the condition state data consisting of CS1 through CS4 will increase with time, meaning that the condition of the bridge elements will deteriorate leading to the need for the measures of preservation, improvement and replacement.  

# How much do the condition state values change with time?  I'll explore this through regression analysis.  

# Can the bridges with the elements approaching CS4 (i.e. critical or severe) be distinguished from the others?  The CALTRANS Bridge Element Inspection Manual lays out the descriptions of the various condition states for each individual element and the conditions associated with cs4 are often distinguished from the others by prior knowledge of the bridge structure as would be information in the records of state and federal level engineering professionals but might not evident to inspectors in the field looking at the bridge itself.  Another description of the cs4 condition state for most of the elements inspected is the evidence of impact damage (the element has been struck by a vehicle or other moving object).  As a former engineer it is my opinion that making predictions about such possibilities is an analysis that requires other types of data regarding the bridge structure (clearances, average daily traffic, bridge size and location) and is not possible based solely on data of the sort provided by the datasets I have read into this analysis.  

# Data Exploration

df20_19_18_17.shape

# 
df20_19_18_17.groupby('STRUCNUM').count()

#37085 Rows by 23 Columns

df20_19_18_17.head

# Data is sorted by STRUCNUM, numerically (low to high) 

df20_19_18_17.columns

df20_19_18_17.info()

# All data in the df20_19_18_17 dataframe is non-null object type

df20_19_18_17.describe()

df20_19_18_17.isnull().any

df20_19_18_17.isnull().sum()

# !!! what computation is being done below? see video. (Ken Jee)

df20_19_18_17.isnull().sum() / df20_19_18_17.shape[0]

df20_19_18_17.dtypes



df20_19_18_17['STATE_20'] = pd.to_numeric(df20_19_18_17['STATE_20'],errors='coerce')
df20_19_18_17 = df20_19_18_17.replace(np.nan, 0, regex=True)
df20_19_18_17['STATE_20'] = df20_19_18_17['STATE_20'].astype(int)

# state does not change over time. 

# !!! make sure the statement below is just the same as the above copied over for unkown reasons.  
""" df20_19_18_17['STATE_20'] = pd.to_numeric(df20_19_18_17['STATE_20'],errors='coerce')
df20_19_18_17 = df20_19_18_17.replace(np.nan, 0, regex=True)
df20_19_18_17['STATE_20'] = df20_19_18_17['STATE_20'].astype(int) """


# Spent a lot of time looking for a method to change data types efficiently, but I want to get this application in, so...

df20_19_18_17 = df20_19_18_17.astype({"STATE_20": 'int32', "STRUCNUM": 'int32', "EN": 'int32', "TOTALQTY_20": 'int32', "CS1_20": 'int32', "CS2_20": 'int32', "CS3_20": 'int32', "CS4_20": 'int32', "TOTALQTY_19": 'int32', "CS1_19": 'int32', "CS2_19": 'int32', "CS3_19": 'int32', "CS4_19": 'int32', "TOTALQTY_18": 'int32', "CS1_18": 'int32', "CS2_18": 'int32', "CS3_18": 'int32', "CS4_18": 'int32', "TOTALQTY_17": 'int32', "CS1": 'int32', "CS2": 'int32', "CS3": 'int32', "CS4": 'int32'})

# Apologies for the ugly brute force nature of the expression above.

# !!! Delete between the checks?

# !!! Delete above to previous check?  


df20_19_18_17.info() # checking the types of the data in order to manipulate them

# make iterative process to come up with common strucnum

# Total number of years of data read in

# MVP II
# no_ofyrs = 


a = [1, 2, 3, 4]
b = [2, 3, 4, 5, 6]
c = [3, 4, 5, 6, 10, 12]
elements_in_all = list(set.intersection(*map(set, [a, b, c])))
elements_in_all




# !!! So it is safe to assume that the 4 dataframes can be concatenated without unexpected observations causing the analysis to be inaccurate.  But how can this be true if the original valuecounts code were giving correct results also?  Do I need to only merge first and then ....?

b_17 = df2017['STRUCNUM'].to_numpy()

print(b_17)

strUnique_17 =  pd.value_counts(b_17)

b_18 = df2018['STRUCNUM'].to_numpy()

print(b_18)

strUnique_18 =  pd.value_counts(b_18)

b_19 = df2019['STRUCNUM'].to_numpy()

print(b_19)

strUnique_19 =  pd.value_counts(b_19)

b_20 = df2020['STRUCNUM'].to_numpy()

print(b_20)

strUnique_20 =  pd.value_counts(b_20)

strUnique_20.equals(strUnique_19)

# strUnique_19 is the largest set:
    
set(strUnique_19).intersection(strUnique_20)

b_19_20 = set(b_19).intersection(b_20)

b_19_20 = sorted(b_19_20) #10151

b_17_18 = set(b_17).intersection(b_18)

b_17_18 = sorted(b_17_18)

# lambda function returns differences in sets

# l_func = lambda x, y: list((set(x)- set(y))) + list((set(y)- set(x))) 

# list_a = b_19
# list_b = b_20

# non_match = l_func(list_a, list_b) #  lists of strucnum for 2019 and 2020

# print("Non-match elements: ", non_match)

# list_func = lambda x, y: list((set(x)- set(y))) + list((set(y)- set(x))) 

# list_a = b_17
# list_b = b_18

# non_match1 = list_func(list_a, list_b) # lists of strucnum for 2017 and 2018

# print("Non-match elements: ", non_match)

strucnum_in_all = list(set.intersection(*map(set, [b_17, b_18, b_19, b_20])))
strucnum_in_all


df17 = df17[np.isin(df17['STRUCNUM'].to_numpy(), strucnum_in_all)]

df18 = df18[np.isin(df18['STRUCNUM'].to_numpy(), strucnum_in_all)]

df19 = df19[np.isin(df19['STRUCNUM'].to_numpy(), strucnum_in_all)]

df20 = df20[np.isin(df20['STRUCNUM'].to_numpy(), strucnum_in_all)]

# !!! left off here!

def non_match_elements(b_17, b_18, b_19, b_20):
    non_match = []
    for i in b_17:
        if i not in b_18:
            if i not in b_19:
                if i not in b_20:
                    non_match.append(i)
    return non_match
       

#list_a = [2, 4, 6, 8, 10, 12]
#list_b = [2, 4, 6, 8]

non_match = non_match_elements(b_17, b_18)
print("No match elements: ", non_match)



#!!!

list_func = lambda x, y: list((set(x)- set(y))) + list((set(y)- set(x))) 

list_a = b_17
list_b = b_20

non_match2 = list_func(list_a, list_b) # lists of strucnum for 2017 and 2020

print("Non-match elements: ", non_match)

#!!!

list_func = lambda x, y: list((set(x)- set(y))) + list((set(y)- set(x))) 

list_a = b_18
list_b = b_20

non_match3 = list_func(list_a, list_b) # lists of STRUCNUM for 2018 and 2020

print("Non-match elements: ", non_match)

#!!!

list_func = lambda x, y: list((set(x)- set(y))) + list((set(y)- set(x))) 

list_a = b_18
list_b = b_19

non_match4 = list_func(list_a, list_b) # lists of STRUCNUM for 2017 and 2020

print("Non-match elements: ", non_match)


intersection_19_20 = set(b_19).intersection(b_20)

intersection_20_19 = set(b_20).intersection(b_19)

intersection_19_20 = sorted(intersection_19_20)

intersection_20_19 = sorted(intersection_20_19)

intersection_20_19 == intersection_19_20 # returns true

intersection_17_18 = set(b_17).intersection(b_18)

intersection_18_17 = set(b_18).intersection(b_17)

intersection_17_18 == intersection_18_17 # returns true

intersection_17_20 = set(b_17).intersection(b_20)

intersection_20_17 = set(b_20).intersection(b_17)

intersection_17_20 == intersection_20_17 # returns true

intersection_18_20 = set(b_18).intersection(b_20)

intersection_20_18 = set(b_20).intersection(b_18)

intersection_18_20 == intersection_20_18 # returns true

intersection_17_19 = set(b_17).intersection(b_19)

intersection_19_17 = set(b_19).intersection(b_17)

intersection_17_19 == intersection_19_17 # returns true

#!!! https://stackoverflow.com/questions/64637774/how-to-compare-one-list-to-multiple-lists-in-python-to-see-if-there-are-any-matc

# lists_STRUCNUM = 






"""from collections import defaultdict

intersections = defaultdict(set)

lists = [
    ['b_17'],
    ['b_18'],
    ['b_19'],
    ['b_20']
]
for i in range(len(lists) - 1):
    for j in range(i + 1, len(lists)):
        intsec = set(lists[i]).intersection(lists[j])
        intersections[tuple(sorted(intsec))].add(tuple(lists[i]))
        intersections[tuple(sorted(intsec))].add(tuple(lists[i])) """
        
        
from collections import defaultdict
from copy import deepcopy
from operator import itemgetter


def srt(args):
    for ind, sub in enumerate(args, 1):
        sub.sort()
        yield ind, sub


list1 = ['b_17']
list2 = ['b_18']
list3 = ['b_19']
list4 = ['b_20']


d = defaultdict(defaultdict)
orig = [list1, list2, list3, list4]

all_best = defaultdict(int)

subs = sorted(srt(deepcopy(orig)), key=itemgetter(1))
for ind, ele in subs:
    best, partner = None, None
    for i2, ele2 in subs:
        if ind == i2:
            continue
        _int = len(set(ele).intersection(ele2))
        if best is None or best < _int:
            best = _int
            partner = i2
            if all_best[ind] < best:
                all_best[ind] = best
    d[ind][partner] = best
    d[partner][ind] = best

grouped = []

used = set()
for k, v in (d.items()):
    if all(val == all_best[_k] for _k, val in v.items()):
        best = [k] + list(v)
        if not any(s in used for s in best):
            grouped.append(best)
        used.update(best)

print(grouped)
print([[orig[ind - 1] for ind in grp] for grp in grouped])


# >>> a = [1, 2, 3, 4]
# >>> b = [2, 3, 4, 5, 6]
# >>> c = [3, 4, 5, 6, 10, 12]
# >>> elements_in_all = list(set.intersection(*map(set, [a, b, c])))
# >>> elements_in_all
# [3, 4]


# Making totals of the various conditon states (cs1 to cs4)

# 2017

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

# 2018

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

# 2019

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

# 2020

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


# Going to attempt to discern how many different STRUCNUMs there are in the 'STRUCNUM' column and the quantity of each

# !!!
STRUCNUMCount =  pd.value_counts(df20_19_18_17.STRUCNUM) 


# !!!
STRUClist = list(reduce(set.intersection, map(set, [df2017.STRUCNUM, df2018.STRUCNUM, df2019.STRUCNUM, df2020.STRUCNUM])))

# Compare the arrays (lists) of the ENs with each other and return matches
# !!! STRUClist_20 = 

# It would seem I have misinterpreted the possible number of STRUCNUM in common between the 4 datasets based on the above snippet- the number of possible bridges in all four sets is 9023.  The maximum possible is 9117 as seen above, but the number of 8992 is missing common STRUCNUM between all 4 dataframes.  Is it true that the originally merged dataframes were merged such that any elements (EN) not common between all four sets would have been eliminate during the merge?  The answer is yes.  

# !!!

# The dataframes for each year should probably be concatenated rather than merged one at a time because the method I used was dependant upon the assumption that the largest number of possibilities would be in the 2020 dataset- but this is a poor assumption because the total of STRUClist is larger than STRUCNUMCount 

STRUClist = [int(x) for x in STRUClist]
STRUClist.sort()

#  Above converts the list of strucnum to integer type and then sorts numerically, did that so I could see the order of the strucnum look a little more similar to the order of bridge numbers I had been seeing in the data right after the XML has been parsed.  

# elCount variable holding the counts of each element number (EN)  
elCount =  pd.value_counts(df20_19_18_17.EN)  

f# Returns a series and the series has a column heading with the name of the column you value counted-strange- the count of each en. returns a count of 7375 for the en 234 being the most observed and inspected element in the 4 years of data.  This makes sense as en==234 is a reinforced concrete pier cap and is very common in bridge construction.  The total possible number of bridge elements is 117 from looking in the CALTrans Bridge Element Inspection Manual.  

elCountList = pd.Series({'nunique': len(elCount), 'unique values': elCount.index.tolist()})
# returns the quantity of unique ENs and a list of the ENs found in the dataset

elCount.append(elCountList)

# show some of the output in the console

 # 60 unique ENs in the set
 # Total of 117 unique ENs possible


# Get the set of all the strucnum and en common across all 4 years of data in the form of an array.

merged_array = np.array(df20_19_18_17[['strucnum', 'en']])

# !!! # Get the rows for each strucnum en pair from the individual year dataframes.  Then concatenate.

# !!! df.loc[df['B'].isin([64, 15])]

# !!! extrasDF[(extrasDF.currentWorkspaceGuid.isin(workspacesDF.currentWorkspaceGuid))] workspacesDF - 1 column(currentWorkspaceGuid), and extrasDF - 4 columns (currentWorkspaceGuid, modelGuid, memoryUsage, lastModified) (show the values from the 2nd df(extrasDF) only if currentWorkspaceGuid exists in workspacesDF)

# !!! show the values of the rows only if the strucnum exists in the STRUClist

# !!! rpt[rpt['STK_ID'].isin(stk_list)]

df2020[~df2020['strucnum'].isin(STRUClist)] # showing the code for 2020, 2017 - 2019 were checked and returned the entire dataframe as well.  

# above line is used to check that there are no "extra" bridges in any of the dataframes, i.e. that the bridges observed each year are the same ones from year to year, that if a new bridge is observed over the years from 2017 to 2020 it would show up here.  All the dataframes are unchanged from when they are read in at the beginning of the file, so there are no extra bridges observed over this time period.  


df_ = df2018[df2018[df2018.columns[2]].isin(STRUClist)]


df2017[(df2017.strucnum.isin(STRUClist))]

df17 = df2017.loc[df2017['strucnum'].isin([STRUClist])]

new_df = df2017.loc[df2017['strucnum'].isin([4, 8])]





# Totals of condition states for different bridge elements begin below:

# Units of Square Feet generally the elements below, en= 12 thru 65, 320, 321, and 510 thru 522 are surfaces, roadway surface basically.  

# en 12 - 65 dfDeckSlab refers to bridge elements decks and slabs with a Condition state measured in square feet. Deck slab encompassed by the en 12 thru 65 are of many different possible material and construction.  

dfDeckSlab = df20_19_18_17.loc[(df20_19_18_17['en'] >= 12) & (df20_19_18_17['en'] <= 65), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17']]

# en 320 - 321 dfApprSlabs refers to bridge elements approach slabs with a Condition state measured in square feet

dfApprSlabs = df20_19_18_17.loc[(df20_19_18_17['en'] >= 320) & (df20_19_18_17['en'] <= 321), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17']]

# en 510 -522 dfWearSfc refers to bridge elements wearing surfaces with a Condition state measured in square feet

dfWearSfc = df20_19_18_17.loc[(df20_19_18_17['en'] >= 510) & (df20_19_18_17['en'] <= 522), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17']]


# Units of Linear Feet, these elements are mostly beams, girders, trusses to name a few, things that carry vertical loadings.

# The tricky nature of these elements is that their CS quantities are given in linear feet- which makes sense, however on a strucnum basis (bridge by bridge basis) merely being told that X Ft of a particular element is characterized by one of the condition states, being able to predict the amount of said element at said condition (cs1, cs2,..) may be possible, but the time series may point to an amount at a future date that is not possible because the total amount of that piece of the bridge is exceded by the amount predicted through univariate or multivariate analysis- basically, predicting that 400 feet of a bridge part will be at condition cs3 at a future date would be erroneous if the total length of that part is 300 feet, or just plain less than 400 feet.  Additionally, the idea that all or half, or any other significant proportion of the part of the bridge being at one of the upper condition states (e.g. cs3, cs4) characterized as "POOR" or "SEVERE" in the literature such as CAL Trans Bridge Element Inspection Manual or the SNBIBE (Specification for the National Bridge Inventory Bridge Elements) it is doubtful that such a significant portion of the bridge part could be in that condition and the overall bridge structure still be considered safe or even serviceable.  Additional data on the individual quantities of elements for each bridge should be sought.  

# en 102 - 112 dfGirders refers to bridge elements of the superstructure with a Condition state measured in linear feet, various possible materials (concrete, steel, prestressed, timber, etc.)

dfGirders = df20_19_18_17.loc[(df20_19_18_17['en'] >= 102) & (df20_19_18_17['en'] <= 112), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17']]

# en 120 - 146 dfTrussArch trusses and arches Condition state measured in linear feet, various materials

dfTrussArch = df20_19_18_17.loc[(df20_19_18_17['en'] >= 120) & (df20_19_18_17['en'] <= 146), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17']]

# en 113 - 118 dfStringers bridge stringers Condition state measured in linear feet, various materials

dfStringers = df20_19_18_17.loc[(df20_19_18_17['en'] >= 113) & (df20_19_18_17['en'] <= 118), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17']]

# en 152 - 157 dfFlrBm floor beams Condition state measured in linear feet, various materials

dfFlrBm = df20_19_18_17.loc[(df20_19_18_17['en'] >= 152) & (df20_19_18_17['en'] <= 157), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17']]

# en 147 - 149 dfMiscSup miscellaneous superstructure elements Condition state measured in linear feet, material: steel or other

dfMiscSup = df20_19_18_17.loc[(df20_19_18_17['en'] >= 147) & (df20_19_18_17['en'] <= 149), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17']]

# en 215 - 219 dfAbutments Abutment elements Condition state measured in linear feet, various materials (concrete mainly)

dfAbutments = df20_19_18_17.loc[(df20_19_18_17['en'] >= 215) & (df20_19_18_17['en'] <= 219), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17']]

# en 231 - 236 dfPierCaps Pier Cap elements Condition state measured in linear feet, various materials.  As mentioned earlier en 234 is the most prevalent element in the dataset.

dfPierCaps = df20_19_18_17.loc[(df20_19_18_17['en'] >= 231) & (df20_19_18_17['en'] <= 236), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17']]

# en 207 dfTwrSteel Tower Steel elements Condition state measured in linear feet

dfTwrSteel = df20_19_18_17.loc[(df20_19_18_17['en'] == 207), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18']]

# en 208 dfTresTimb Trestle elements made of Timber Condition state measured in linear feet

dfTresTimb = df20_19_18_17.loc[(df20_19_18_17['en'] == 208), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17']]

# en 210 - 213 dfPierWalls Pier Wall elements Condition state measured in linear feet

dfPierWalls = df20_19_18_17.loc[(df20_19_18_17['en'] >= 210) & (df20_19_18_17['en'] <= 213), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17']]

# en 220 dfPCFRC Pile Cap/Footing - Reinforced Concrete elements Condition state measured in linear feet
dfPCFRC = df20_19_18_17.loc[(df20_19_18_17['en'] == 220), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18']]

# en 240 - 245 dfCulv Culvert elements Condition state measured in linear feet, various materials

dfCulv = df20_19_18_17.loc[(df20_19_18_17['en'] >= 240) & (df20_19_18_17['en'] <= 245), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17']]

# en 250 dfTunnel Tunnel - Checking for this to be sure it is not present as the literature says it is no longer in purview

dfTunnel = df20_19_18_17.loc[(df20_19_18_17['en'] == 250), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# en 330 - 334 dfBrdgRail Varied Bridge Railing elements Condition state measured in linear feet (330 Metal, 331 RC, 332 Timb, 333 Other, 334 Masonry)

dfBrdgRail = df20_19_18_17.loc[(df20_19_18_17['en'] >= 330) & (df20_19_18_17['en'] <= 334), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17']]

# en 300 - 309 dfJoints Varied Joint elements Condition state measured in linear feet, various materials

dfJoints = df20_19_18_17.loc[(df20_19_18_17['en'] >= 300) & (df20_19_18_17['en'] <= 309), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17']]

# en 170 dfRRCF Rail Road Car Frame elements Condition state measured in linear feet

dfRRCF = df20_19_18_17.loc[(df20_19_18_17['en'] == 170), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17']]


# Units of Each Below

# en 161 dfPin Steel Pin and Pin hanger assembly elements Condition state measured in units of each

dfPin = df20_19_18_17.loc[(df20_19_18_17['en'] == 161), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# en 162 dfGusset Steel Gusset Plate elements Condition state measured in units of each

dfGusset = df20_19_18_17.loc[(df20_19_18_17['en'] == 162), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# en 171 dfSTEELMiscSup Miscellaneous Steel Superstructures elements Condition state measured in units of each

dfSTEELMiscSup = df20_19_18_17.loc[(df20_19_18_17['en'] == 171), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# en 180 dfEQRCII Earthquake Restrainer Cables Type II Condition state measured in units of each

dfEQRCII = df20_19_18_17.loc[(df20_19_18_17['en'] == 180), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# en 181 dfEQRCC1 Earthquake Restrainer Cables - C1 Condition state measured in units of each

dfEQRCC1 = df20_19_18_17.loc[(df20_19_18_17['en'] == 181), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# en 182 dfEQROther Earthquake Restrainer Cables - Other Condition state measured in units of each

dfEQROther = df20_19_18_17.loc[(df20_19_18_17['en'] == 182), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]



# Additionally it would be helpful for the number of each of the elements below PER BRIDGE were known- 


# en 202 - 206 Column elements Condition state measured in units of each

# en 202 dfColSt Steel Column elements Condition state measured in units of each

dfColSt = df20_19_18_17.loc[(df20_19_18_17['en'] == 202), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# !!! Start here 12/12/2021, continue getting totals for elements with units of each.  


# ColEls is a dict of Column Bridge elements 
ColEls = {'ColSt': 'dfColSt', 'ColOther' :'dfColOther', 'ColPrConc' :'dfColPrConc', 'ColRfConc' :'dfColRfConc', 'ColTimb' :'dfColTimb'}



for ColName in ColEls:
    ColEls[ColName] = pd.DataFrame()
    
#ColEls

# !!!

dist = {"name": "huzaifa", "age": 18, "skill": "programmer"}
print(dist)
for key, value in dist.items():
    print(f'Key: {key}')
    print(f'Value: {value}')
    
# !!!

# 
# for elEach, df in d.iteritems():

ColSt_CS1 = [dfColSt['CS1_17'].sum(), dfColSt['CS1_18'].sum(), dfColSt['CS1_19'].sum(), dfColSt['CS1_20'].sum()]

ColSt_CS2 = [dfColSt['CS2_17'].sum(), dfColSt['CS2_18'].sum(), dfColSt['CS2_19'].sum(), dfColSt['CS2_20'].sum()]

ColSt_CS3 = [dfColSt['CS3_17'].sum(), dfColSt['CS3_18'].sum(), dfColSt['CS3_19'].sum(), dfColSt['CS3_20'].sum()]

ColSt_CS4 = [dfColSt['CS4_17'].sum(), dfColSt['CS4_18'].sum(), dfColSt['CS4_19'].sum(), dfColSt['CS4_20'].sum()]

# en 203 dfColOther Column elements of type Other Condition state measured in units of each

dfColOther = df20_19_18_17.loc[(df20_19_18_17['en'] == 203), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# en 204 dfColPrConc Prestressed Concrete Column elements Condition state measured in units of each

dfColPrConc = df20_19_18_17.loc[(df20_19_18_17['en'] == 204), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# en 205 dfColRfConc Reinforced Concrete Column elements Condition state measured in units of each

dfColRfConc = df20_19_18_17.loc[(df20_19_18_17['en'] == 205), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# en 206 dfColTimb Timber Column elements Condition state measured in units of each

#dfColTimb = df20_19_18_17.loc[(df20_19_18_17['en'] == 206), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# End columns


# en 225 dfPileSteel Pile - Steel Condition state measured in units of each

dfPileSteel = df20_19_18_17.loc[(df20_19_18_17['en'] == 225), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# en 226 dfPilePrConc Pile - Prestressed Concrete Condition state measured in units of each

dfPilePrConc = df20_19_18_17.loc[(df20_19_18_17['en'] == 226), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# en 227 dfPileRC Pile of Type - Reinforced Concrete Condition state measured in units of each

dfPileRC = df20_19_18_17.loc[(df20_19_18_17['en'] == 227), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# en 228 dfPileTimb Pile of Type - Timber Condition state measured in units of each

dfPileTimb = df20_19_18_17.loc[(df20_19_18_17['en'] == 228), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# en 229 dfPileOther Pile of Type - Other Condition state measured in units of each

dfPileOther = df20_19_18_17.loc[(df20_19_18_17['en'] == 229), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# en 251 dfPileCISS Pile- cast in steel shell Condition state measured in units of each

dfPileCISS = df20_19_18_17.loc[(df20_19_18_17['en'] == 251), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# en 252 dfPileCIDH Pile- cast in Drilled Hole Condition state measured in units of each

dfPileCIDH = df20_19_18_17.loc[(df20_19_18_17['en'] == 252), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# en 254 dfStSeisFH Steel Seismic Column Shells - Full Height Condition state measured in units of each

dfStSeisFH = df20_19_18_17.loc[(df20_19_18_17['en'] == 254), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# en 255 dfStSeisPH Steel Seismic Column Shells - Partial Height Condition state measured in units of each

dfStSeisPH = df20_19_18_17.loc[(df20_19_18_17['en'] == 255), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# en 256 dfSSP Slope/Scour Protection Condition state measured in units of each

dfSSP = df20_19_18_17.loc[(df20_19_18_17['en'] == 256), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]


# Bearings (Brg)
# en 310 dfBrgEl Bearing Type - Elastomeric Bearing elements Condition state measured in units of each
# Below start pulling out the entries in the merged df that are Elastomeric Bearings or ['en'] == 310

dfBrgEl = df20_19_18_17.loc[(df20_19_18_17['en'] == 310), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]


# Elastomeric Bearings Yr 2020
dfBrgEl_20 = df20_19_18_17.loc[(df20_19_18_17['en'] == 310), ['strucnum', 'CS1_20', 'CS2_20',  'CS3_20', 'CS4_20']]

# Elastomeric Bearings Yr 2019
dfBrgEl_19 = df20_19_18_17.loc[(df20_19_18_17['en'] == 310), ['strucnum', 'CS1_19', 'CS2_19', 'CS3_19', 'CS4_19']]

# Elastomeric Bearings Yr 2018
dfBrgEl_18 = df20_19_18_17.loc[(df20_19_18_17['en'] == 310), ['strucnum', 'CS1_18', 'CS2_18', 'CS3_18', 'CS4_18']]

# Elastomeric Bearings Yr 2017
dfBrgEl_17 = df20_19_18_17.loc[(df20_19_18_17['en'] == 310), ['strucnum', 'CS1_17', 'CS2_17',  'CS3_17', 'CS4_17']]



# This was an attempt to make some plots- I believe I need to resample parts of my data for best results!



arrData = np.array(dfBrgEl)

print(arrData.size)
print(arrData.shape)


# !!!
dfBrgEl.plot(kind='scatter', y='CS1_20', x= '2020')
plt.show()

dfBrgEl.CS1_20.max()

dfBrgEl.plot(kind='scatter', y='CS2_20', x= '2020')
plt.show()
# !!!
dfBrgEl.CS2_20.max()

# resample from yearly to monthly dfBrgEl_CS1 is the df I'm using for the purpose of linear regression Condition state 1



BrgEl_CS1 = [dfBrgEl['CS1_17'].sum(), dfBrgEl['CS1_18'].sum(), dfBrgEl['CS1_19'].sum(), dfBrgEl['CS1_20'].sum()]

# s2!! dfBrgEl_M['cs1'] = BrgEl_CS1

# s2/dfBrgEl_M is the dataframe to be converted to monthly intervals thru resample
s2 = pd.Series(BrgEl_CS1, index=pd.period_range('2017-01-01',
                                            freq='A',
                                            periods=4))

# Change the frequency of observations from yearly to monthly
s2 = s2.resample('M', convention='start').asfreq()

s2 = s2.interpolate() # this is where the trend needs to start with the 'lowest' CS and be expected to trend upwards

dfBrgEl_M = s2.to_frame()

dfBrgEl_M.columns = ['cs1']

dfBrgEl_M.plot(y='cs1', use_index=True, kind='scatter')
plt.show()



# Declare a list for the new column in dfBrgEl_M

BrgEl_CS2 = [dfBrgEl['CS2_17'].sum(), dfBrgEl['CS2_18'].sum(), dfBrgEl['CS2_19'].sum(), dfBrgEl['CS2_20'].sum()]

# s2!! dfBrgEl_M['cs2'] = BrgEl_CS2
 
# Sum the number of elastomeric bearings in cs3

# Declare a list for the new column in dfBrgEl_M

BrgEl_CS3 = [dfBrgEl['CS3_17'].sum(), dfBrgEl['CS3_18'].sum(), dfBrgEl['CS3_19'].sum(), dfBrgEl['CS3_20'].sum()]

# s2!! dfBrgEl_M['cs3'] = BrgEl_CS3

# Sum the number of elastomeric bearings in cs4

# Declare a list for the new column in dfBrgEl_M

BrgEl_CS4 = [dfBrgEl['CS4_17'].sum(), dfBrgEl['CS4_18'].sum(), dfBrgEl['CS4_19'].sum(), dfBrgEl['CS4_20'].sum()]

# s2!! dfBrgEl_M['cs4'] = BrgEl_CS4

#dfBrgEl_M.index = dfBrgEl_M.index.to_period('M')

# CS1s en == 310 [34245, 33741, 49622, 40697]

# !!!

# ETFs = ETFs.resample(‘W’).agg([‘adjClose’ : ‘mean’, ‘high’ : ‘max’, ‘low’ : ‘min’, ‘volume’ : ‘sum’])

# !!!

#311
# en 311 dfBrgMov Bearing Type - Moveable Bearing elements Condition state measured in units of each
# Below start pulling out the entries in the merged df that are Moveable Bearings or ['en'] == 311

# en 311 dfBrgMov Bearing Type - Moveable Bearing elements Condition state measured in units of each

dfBrgMov = df20_19_18_17.loc[(df20_19_18_17['en'] == 311), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# Total each condition state

BrgMov_CS1 = [dfBrgMov['CS1_17'].sum(), dfBrgMov['CS1_18'].sum(), dfBrgMov['CS1_19'].sum(), dfBrgMov['CS1_20'].sum()]


# s2!! dfBrgEl_M['cs1'] = BrgEl_CS1

# s2/dfBrgEl_M is the dataframe to be converted to monthly intervals thru resample

s2 = pd.Series(BrgMov_CS1, index=pd.period_range('2017-01-01',
                                            freq='A',
                                            periods=4))

# Change the frequency of observations from yearly to monthly
# Using s2 as a "temp" variable that changes for each en and the CS (i.e. cs1 - cs4 to see if the resample trends up)

s2 = s2.resample('M', convention='start').asfreq()

s2 = s2.interpolate() # this is where the trend needs to start with the 'lowest' CS and be expected to trend upwards

dfBrgMov_M = s2.to_frame() #Result: trends upward until end of 2018

dfBrgMov_M.columns = ['cs1']


# after resample for cs1 for BrgMov

dfBrgMov_M['cs1'] = BrgMov_CS1

BrgMov_CS2 = [dfBrgMov['CS2_17'].sum(), dfBrgMov['CS2_18'].sum(), dfBrgMov['CS2_19'].sum(), dfBrgMov['CS2_20'].sum()]
s2 = pd.Series(BrgMov_CS2, index=pd.period_range('2017-01-01',
                                            freq='A',
                                            periods=4))

# Change the frequency of observations from yearly to monthly
# Using s2 as a "temp" variable that changes for each en and the CS (i.e. cs1 - cs4 to see if the resample trends up)

s2 = s2.resample('M', convention='start').asfreq()

s2 = s2.interpolate() # this is where the trend needs to start with the 'lowest' CS and be expected to trend upwards
#Result: trends downward until end of 2019
# dfBrgMov_M['cs2'] = BrgMov_CS2 

BrgMov_CS3 = [dfBrgMov['CS3_17'].sum(), dfBrgMov['CS3_18'].sum(), dfBrgMov['CS3_19'].sum(), dfBrgMov['CS3_20'].sum()]
s2 = pd.Series(BrgMov_CS3, index=pd.period_range('2017-01-01',
                                            freq='A',
                                            periods=4))

# Change the frequency of observations from yearly to monthly
# Using s2 as a "temp" variable that changes for each en and the CS (i.e. cs1 - cs4 to see if the resample trends up)

s2 = s2.resample('M', convention='start').asfreq()

s2 = s2.interpolate() # this is where the trend needs to start with the 'lowest' CS and be expected to trend upwards
#Result: trends upward until end of 2019

dfBrgMov_M['cs3'] = BrgMov_CS3

BrgMov_CS4 = [dfBrgMov['CS4_17'].sum(), dfBrgMov['CS4_18'].sum(), dfBrgMov['CS4_19'].sum(), dfBrgMov['CS4_20'].sum()]
s2 = pd.Series(BrgMov_CS3, index=pd.period_range('2017-01-01',
                                            freq='A',
                                            periods=4))

# Change the frequency of observations from yearly to monthly
# Using s2 as a "temp" variable that changes for each en and the CS (i.e. cs1 - cs4 to see if the resample trends up)

s2 = s2.resample('M', convention='start').asfreq()

s2 = s2.interpolate() # this is where the trend needs to start with the 'lowest' CS and be expected to trend upwards
#Result: trends upward until the end of 2019

dfBrgMov_M['cs4'] = BrgEl_CS4

dfBrgMov_M.plot(kind='scatter', y='CS1_20', x= '2020')
plt.show()

# 311

# 312 (None in the final dataset df20_19_18_17)

# 313
# en 313 dfBrgFixed Bearing Type - Fixed Bearing elements Condition state measured in units of each

dfBrgFixed = df20_19_18_17.loc[(df20_19_18_17['en'] == 313), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# Total each condition state

BrgFixed_CS1 = [dfBrgFixed['CS1_17'].sum(), dfBrgFixed['CS1_18'].sum(), dfBrgFixed['CS1_19'].sum(), dfBrgFixed['CS1_20'].sum()]

# s2/dfBrgFixed_M is the dataframe to be converted to monthly intervals thru resample
s2 = pd.Series(BrgFixed_CS1, index=pd.period_range('2017-01-01',
                                            freq='A',
                                            periods=4))

# Change the frequency of observations from yearly to monthly
# Using s2 as a "temp" variable that changes for each en and the CS (i.e. cs1 - cs4 to see if the resample trends up)

s2 = s2.resample('M', convention='start').asfreq()

#Result: trends upward until end of 2019

s2 = s2.interpolate() # this is where the trend needs to start with the 'lowest' CS and be expected to trend upwards

dfBrgFixed_M = s2.to_frame() 

dfBrgFixed_M.columns = ['cs1']


# after resample for cs1 for BrgFixed

dfBrgFixed_M['cs1'] = BrgFixed_CS1

BrgFixed_CS2 = [dfBrgFixed['CS2_17'].sum(), dfBrgFixed['CS2_18'].sum(), dfBrgFixed['CS2_19'].sum(), dfBrgFixed['CS2_20'].sum()]
s2 = pd.Series(BrgFixed_CS2, index=pd.period_range('2017-01-01',
                                            freq='A',
                                            periods=4))

# Change the frequency of observations from yearly to monthly
# Using s2 as a "temp" variable that changes for each en and the CS (i.e. cs1 - cs4 to see if the resample trends up)

s2 = s2.resample('M', convention='start').asfreq()

#Result: trends downward until end of 2019, then back up

s2 = s2.interpolate()

#Result: trends upward until end of 2019
# dfBrgFixed_M['cs2'] = BrgFixed_CS2 

BrgFixed_CS3 = [dfBrgFixed['CS3_17'].sum(), dfBrgFixed['CS3_18'].sum(), dfBrgFixed['CS3_19'].sum(), dfBrgFixed['CS3_20'].sum()]
s2 = pd.Series(BrgFixed_CS3, index=pd.period_range('2017-01-01',
                                            freq='A',
                                            periods=4))

# Change the frequency of observations from yearly to monthly
# Using s2 as a "temp" variable that changes for each en and the CS (i.e. cs1 - cs4 to see if the resample trends up)

s2 = s2.resample('M', convention='start').asfreq()

#Result: trends upward until end of 2019 (starts from 0)

s2 = s2.interpolate()

dfBrgFixed_M['cs3'] = BrgFixed_CS3

BrgFixed_CS4 = [dfBrgFixed['CS4_17'].sum(), dfBrgFixed['CS4_18'].sum(), dfBrgFixed['CS4_19'].sum(), dfBrgFixed['CS4_20'].sum()]
s2 = pd.Series(BrgFixed_CS3, index=pd.period_range('2017-01-01',
                                            freq='A',
                                            periods=4))

# Change the frequency of observations from yearly to monthly
# Using s2 as a "temp" variable that changes for each en and the CS (i.e. cs1 - cs4 to see if the resample trends up)

s2 = s2.resample('M', convention='start').asfreq()

#Result: Note: I suspect a mistake in the field when these observations were made, numbrs same as cs3 above.
# trends upward until end of 2019 (starts from 0)

s2 = s2.interpolate()

dfBrgFixed_M['cs4'] = BrgFixed_CS4
# 313


#314
# en 314 dfBrgPot Bearing Type - Pot Bearing elements Condition state measured in units of each

dfBrgPot = df20_19_18_17.loc[(df20_19_18_17['en'] == 314), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

BrgPot_CS1 = [dfBrgPot['CS1_17'].sum(), dfBrgPot['CS1_18'].sum(), dfBrgPot['CS1_19'].sum(), dfBrgPot['CS1_20'].sum()]

# s2/dfBrgPot_M is the dataframe to be converted to monthly intervals thru resample

s2 = pd.Series(BrgPot_CS1, index=pd.period_range('2017-01-01',
                                            freq='A',
                                            periods=4))

# Change the frequency of observations from yearly to monthly
# Using s2 as a "temp" variable that changes for each en and the CS (i.e. cs1 - cs4 to see if the resample trends up)

s2 = s2.resample('M', convention='start').asfreq()

#Result: Non-zero at start of 2017, trends downward until end of 2018, then up to end of 2019 then back down to end of 2020

s2 = s2.interpolate()

dfBrgPot_M = s2.to_frame() 

dfBrgPot_M.columns = ['cs1']

BrgFixed_CS2 = [dfBrgFixed['CS2_17'].sum(), dfBrgFixed['CS2_18'].sum(), dfBrgFixed['CS2_19'].sum(), dfBrgFixed['CS2_20'].sum()]
s2 = pd.Series(BrgFixed_CS2, index=pd.period_range('2017-01-01',
                                            freq='A',
                                            periods=4))

# Change the frequency of observations from yearly to monthly
# Using s2 as a "temp" variable that changes for each en and the CS (i.e. cs1 - cs4 to see if the resample trends up)

s2 = s2.resample('M', convention='start').asfreq()


# en 312 dfBrgEC Bearing Type - Enclosed/Concealed Bearing elements Condition state measured in units of each

dfBrgEC = df20_19_18_17.loc[(df20_19_18_17['en'] == 312), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# en 313 dfBrgFixed Bearing Type - Fixed Bearing elements Condition state measured in units of each

dfBrgFixed = df20_19_18_17.loc[(df20_19_18_17['en'] == 313), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# en 314 dfBrgPot Bearing Type - Pot Bearing elements Condition state measured in units of each

dfBrgPot = df20_19_18_17.loc[(df20_19_18_17['en'] == 314), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# en 315 dfBrgDisk Bearing Type - Disk Bearing elements Condition state measured in units of each

dfBrgDisk = df20_19_18_17.loc[(df20_19_18_17['en'] == 315), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# en 316 dfBrgOther Bearing Type - Other Bearing elements Condition state measured in units of each

dfBrgOther = df20_19_18_17.loc[(df20_19_18_17['en'] == 316), ['strucnum', 'CS1_20', 'CS1_19', 'CS1_18', 'CS1_17', 'CS2_20', 'CS2_19', 'CS2_18', 'CS2_17', 'CS3_20', 'CS3_19', 'CS3_18', 'CS3_17', 'CS4_20', 'CS4_19', 'CS4_18', 'CS4_17']]

# End Bearings




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






#%matplotlib inline
        sns.set_theme(style='darkgrid', color_codes=True)

    sns.displot(data=df20_19_18_17, x=['2017','2018','2019','2020'], aspect=1.6, bins=30)
    plt.title('Bridges w/ cs4 > 0 for 2017', fontsize=16)

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

