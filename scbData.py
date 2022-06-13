# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 16:29:08 2021
@author: Chris
"""

import pandas as pd
import xml.etree.ElementTree as et

import numpy as np
import numpy.ma as ma

from datetime import datetime

import io

import os

from functools import reduce

# Read in the XML files as they were downloaded from the FHWA.  

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

# Parse the XML files for the individual years 

df2021=parse_XML("2021SC_ElementData.xml", ["FHWAED", "STATE", "STRUCNUM", "EN", "EPN", "TOTALQTY", "CS1", "CS2", "CS3", "CS4"])

df2020=parse_XML("2020SC_ElementData.xml", ["FHWAED", "STATE", "STRUCNUM", "EN", "EPN", "TOTALQTY", "CS1", "CS2", "CS3", "CS4"])

df2019=parse_XML("2019SC_ElementData.xml", ["FHWAED", "STATE", "STRUCNUM", "EN", "EPN", "TOTALQTY", "CS1", "CS2", "CS3", "CS4"])

df2018=parse_XML("2018SC_ElementData.xml", ["FHWAED", "STATE", "STRUCNUM", "EN", "EPN", "TOTALQTY", "CS1", "CS2", "CS3", "CS4"])

df2017=parse_XML("2017SC_ElementData.xml", ["FHWAED", "STATE", "STRUCNUM", "EN", "EPN", "TOTALQTY", "CS1", "CS2", "CS3", "CS4"])


""" the strucnum columns in the 2017 and 2018 sets were a total length of 13 digits, most of those are leading zeros, the two lambda fucntions below are placing additional zeros at the left hand side of the entries to merge those sets properly where the strucnum overlap """

df2018['STRUCNUM'] = df2018['STRUCNUM'].apply(lambda x: '{0:0>15}'.format(x))

df2017['STRUCNUM'] = df2017['STRUCNUM'].apply(lambda x: '{0:0>15}'.format(x))

# !!!

# MVP II is the Minimum Viable Product version II- or a program/data analysis that would supercede this one.  

# If I refer to "MVP II" and then comment out some code in that area I am referring to a functionality I have not achieved in this program and I would hope to make possible in a second version of this application were it to be updated.  

# !!!

# MVP II 
# Make the names of xml files be read into a column in the resulting dataframe as they are read from the files "automatically" rather than assigning the filename as I do below.  

""" import glob
import os.path

# Create a list of all XML files
files = glob.glob("*.xml")

# Create an empty list to append the df
filenames = []

for xml in files:
    df = pd.read_xml(xml)
    df['File Name'] = os.path.basename(xml)
    filenames.append(df)    

path = r'xml_in'
allFiles = glob.glob(path + '/*.xml')

for file_ in allFiles:   
    df = pd.read_csv(file_, header=0)
    df.name = file_
    print(df.name) """

# !!!

# MVP II- automate the steps below rather than inserting filename manually as is done below, but for now place the filename in a column in the dfs after parsing

df2017.insert(0, 'filename', '2017SC_ElementData.xml')

df2018.insert(0, 'filename', '2018SC_ElementData.xml')

df2019.insert(0, 'filename', '2019SC_ElementData.xml')

df2020.insert(0, 'filename', '2020SC_ElementData.xml')

df2021.insert(0, 'filename', '2021SC_ElementData.xml')



# b_17 thru b_21 just mean "bridge number" aka STRUCNUM for the corresponding years, making a variable that holds the STRUCNUM as an array for each year as it would be right after being parsed into a dataframe.  In other words the b_17 - b_21 variables will be larger in size (i.e. no. of rows) than the dataframes as seen below once the STRUCNUM not present in all years are removed.  

b_17 = df2017['STRUCNUM'].to_numpy()

b_18 = df2018['STRUCNUM'].to_numpy()

b_19 = df2019['STRUCNUM'].to_numpy()

b_20 = df2020['STRUCNUM'].to_numpy()

b_21 = df2021['STRUCNUM'].to_numpy()


# !!! THIS IS SUBJECT TO CHANGE: The assumption I will use is that the data for all bridges (denoted by STRUCNUM) that are common to all the years of data being analyzed (2017 - 2021 in this case) is to be considered, meaning that the data (condition states of individual bridge elements) associated with the bridges common across 5 years shall be used even if the data provided for a bridge one year is not provided for all the other years or is provided sporadically for other years (i.e. if the bridge components (EN) rated for condition state one year are not rated for all years - BUT some components of said bridge are rated for all years being considered and analyzed then those condition states for those elements can be used as part of the data).  For instance, a very common bridge component (or EN, element number) is a deck constructed of reinforced concrete, which I refer to as deck_rc, and this EN is number 12 as denoted by the Federal Highway Administration (FHWA) Specification for the National Bridge Inventory, Bridge Elements.  As such it may be that the number of observations across the years considered is not the same for that elemeent number (EN) each year- some years may include condition states associated with that element in some but not all years, but it is my intention to use as many observations as possible for as many bridge parts as possible to attempt to make the computer model accurate.  Again, ths is subject to change.  


# Determine the set of STRUCNUM common to all years observed.  

strucnum_in_all = list(set.intersection(*map(set, [b_17, b_18, b_19, b_20, b_21])))
# Sort the list so its contents will look more familiar to the user.
strucnum_in_all = sorted(strucnum_in_all)

# Remove STRUCNUM not present in all dfs

df2017 = df2017[np.isin(df2017['STRUCNUM'].to_numpy(), strucnum_in_all)]

df2018 = df2018[np.isin(df2018['STRUCNUM'].to_numpy(), strucnum_in_all)]

df2019 = df2019[np.isin(df2019['STRUCNUM'].to_numpy(), strucnum_in_all)]

df2020 = df2020[np.isin(df2020['STRUCNUM'].to_numpy(), strucnum_in_all)]

df2021 = df2021[np.isin(df2021['STRUCNUM'].to_numpy(), strucnum_in_all)]

# Then as a check, I make the STRUCNUM into sets for each newly modified dataframe strucnum_2017_mod 

strucnum_2017_mod = df2017['STRUCNUM'].unique()

strucnum_2018_mod = df2018['STRUCNUM'].unique()

strucnum_2019_mod = df2019['STRUCNUM'].unique()

strucnum_2020_mod = df2020['STRUCNUM'].unique()

strucnum_2021_mod = df2021['STRUCNUM'].unique()


# strucnum_2017_mod = strucnum_2018_mod = strucnum_2019_mod = strucnum_2021_mod = strucnum_2020_mod 



from array import *

strucnum_2017_mod.tolist()

strucnum_2018_mod.tolist()

strucnum_2019_mod.tolist()

strucnum_2020_mod.tolist()

strucnum_2021_mod.tolist()

import collections

if collections.Counter(strucnum_2021_mod) == collections.Counter(strucnum_2020_mod):
    print ("The lists are identical")
else :
    print ("The lists are not identical")






# !!!

# Is this the place where I go and make all the necessary dfs for each EN PER YEAR and then follow that with code to add the time component for each individual year so as to avoid having to ensure the number of observations per year is the same 

# Create EN dataframes for each year prior to concatenation of those dataframes (in this case that dataframe will be called deck_rc (note the lack of _year attached to the end) to facilitate inserting the time component individually for each bridge element for that year based on number of observations made that year.  

# !!! Of course the comment above is making me wonder if the idea that I should at least be able to infer that the same amount of time has passed between successive observations of said bridge element (EN) may cause inaccuracy which would be the case if the observations of a part of a bridge were made over successive years (e.g. if STRUCNUM = 000000000000004 is observed in all years being considered but a condition state for EN = 12 IS NOT recorded each year) it would be difficult to say that the same amount of time has passed between each observation of the bridge element (EN).  

qty_deck_rc_2017 = df2017['EN'].value_counts()[12]

# 1507 observations of deck_rc in 2017

qty_deck_rc_2018 = df2018['EN'].value_counts()[12]

# 1518 observations of deck_rc in 2018

qty_deck_rc_2019 = df2019['EN'].value_counts()[12]

# 1474 observations of deck_rc in 2019

qty_deck_rc_2020 = df2020['EN'].value_counts()[12]

# 1191 observations of deck_rc in 2020

qty_deck_rc_2021 = df2021['EN'].value_counts()[12]

# 1081 observations of deck_rc in 2021


# !!! Going to change the protocol for this analysis as follows:

#  a.	IF a bridge (STRUCNUM) is not present in all years being considered that STRUCNUM (bridge) is eliminated from the data.
#       i. 	IF a bridge element present in a bridge not meeting the criteria outlined in a. above (i.e. a bridge or STRUCNUM that is not eliminated from the data because that STRUCNUM IS present in all years under consideration) is not present and its condition state observed and recorded in all years being considered that bridge element (EN) is eliminated from the data.  (so eliminate the bridges first if they aren’t present in all the years then eliminate the elements from the bridges if the elements are not present in all the years for those bridges)




# !!!
""" date_rng_2017 = pd.date_range(start='1/1/2017', end='12/31/2017', freq='H')

# deck_rc_2017 - pd.DataFrame(date_rng_2017, columns=['date'] )
               ^ is the dash above supposed to be an = instead?

class df2017_EN:
    pass

element_df = df2017_EN() # element_df will hold all the variables (which will also be variables in the form of dataframes) to be created associated with the different bridge elements or  ENs.  

# Get the unique set of all EN common to all years being obsesrved/inventoried.  
elements = df2017['EN'].unique()


for element in elements:
    
    setattr(element_df, f"{element}", df2017[df2017['EN']==element].reset_index(drop=True))
    
for element in elements: #very important to keep the two for loops indented to the same spot! Second loop is not a nested loop!
        print(getattr(element_df, f"{element}"))

qty_deck_rc_2017 = df2017['EN'].value_counts()[12]

# 1507 observations of deck_rc in 2017

qty_deck_rc_2018 = df2018['EN'].value_counts()[12]

# 1518 observations of deck_rc in 2018

qty_deck_rc_2019 = df2019['EN'].value_counts()[12]

# 1474 observations of deck_rc in 2019

qty_deck_rc_2020 = df2020['EN'].value_counts()[12]

# 1191 observations of deck_rc in 2020

qty_deck_rc_2021 = df2021['EN'].value_counts()[12]

# 1081 observations of deck_rc in 2021 """


el_names = {'12': 'deck_rc',
            '13': 'deck_pc',
   	        '15': 'topFlg_pc',
   	        '16': 'topFlg_rc',
   	        '28': 'stDeck_og',
   	        '29': 'stDeck_cfg',
       	    '30': 'stDeck_corrOrtho',
            '31': 'deck_timb',
            	'38': 'slab_rc',
            	'39': 'slab_pc',
            	'54': 'slab_timb',
            	'60': 'deck_other',
            	'65': 'slab_other',
            	'102': 'cwBg_steel',
            	'103': 'cwBg_pc',
            	'105': 'cwBg_rc',
            '106': 'cwBg_other',
            '107': 'oGb_steel',
            '109': 'oGb_pc',
            '110': 'oGb_rc',
            '111': 'oGb_timb',
            '112': 'oGb_other',
            '113': 'stringer_steel',
            '115': 'stringer_pc',
            '116': 'stringer_rc',
            '117': 'stringer_timb',
            '118': 'stringer_other',
            '120': 'truss_steel',
            '135': 'truss_timb',
            '136': 'truss_other',
            '141': 'arch_steel',
            '142': 'arch_other',
            '143': 'arch_pc',
            '144': 'arch_rc',
            '145': 'arch_masonry',
            '146': 'arch_timb',
            '147': 'cbl_mSt',
            '148': 'cbl_secSt',
            '149': 'cbl_secOthr',
            '152': 'flrB_steel',
            '154': 'flrB_pc',
            '155': 'flrB_rc',
            '156': 'flrB_timb',
            '157': 'flrB_other',
            '161': 'spph',
            '162': 'sgp',
            '170': 'rrcf',
            '171': 'miscSS',
            '180': 'eqrcII',
            '181': 'eqrcC1',
            '182': 'eqrc_Othr',
            '202': 'col_st',
            	'203': 'col_othr',
            	'204': 'col_pc',
            	'205': 'col_rc',
            '206': 'col_timb',
            '207': 'twr_st',
            '208': 'tres_timb',
            '210': 'pw_rc',
            '211': 'pw_othr',
            '212': 'pw_timb',
            '213': 'pw_mas',
            	'215': 'abmt_rc',
            	'216': 'abmt_timb',
            	'217': 'abmt_mas',
            	'218': 'abmt_othr',
            	'219': 'abmt_steel',
            '220': 'pcf_rc',
            '225': 'pile_st',
            '226': 'pile_pc',
            '227': 'pile_rc',
            '228': 'pile_timb',
            '229': 'pile_othr',
            '231': 'pc_steel',
            	'233': 'pc_PrConc',
            	'234': 'pc_rc',
            '235': 'pc_timb',
            '236': 'pc_othr',
            '240': 'culv_st',
            '241': 'culv_rc',
            '242': 'culv_timb',
            '243': 'culv_othr',
            '244': 'culv_mas',
            '245': 'culv_pc',
            '250': 'tunnel',
            '251': 'pile_castSh',
            '252': 'pile_castDr',
            '254': 'cSh_stFH',
            '255': 'cSh_stPH',
            '256': 'slopeScP',
           	'300': 'joint_sse',
           	'301': 'joint_ps',
           	'302': 'joint_cs',
           	'303': 'joint_aws',
            '304': 'joint_oe',
            '305': 'joint_awo',
            '306': 'joint_othr',
            '307': 'joint_ap',
            '308': 'joint_ssp',
            '309': 'joint_sf',
            '310': 'brg_el',
            '311': 'brg_mov',
            '312': 'brg_ec',
            '313': 'brg_fxd',
            '314': 'brg_pot',
            '315': 'brg_dsk',
            '316': 'brg_othr',
            	'320': 'appSl_pc',
            '321': 'appSl_rc',
            	'330': 'br_m',
            '331': 'br_rc',
            '332': 'br_timb',
            '333': 'br_othr',
            '334': 'br_mas',
            	'510': 'dws_ac',
            	'511': 'dws_cp',
            	'512': 'dws_ep',
            '513': 'dws_timb',
            '515': 'spc_p',
            '516': 'spc_galv',
            '517': 'spc_ws',
            '520': 'rsps',
            '521': 'cpc',
            '522': 'deck_memb'
    }

""" 06/07/22 """


# Make a dictionary of the keys and values of the bridge element numbers (EN) and the name I intend to give to the variable that will hold the number observations of that EN for that year using a dictionary comprehension.

qty_obs_2017 = {k : f'{v}_2017' for k, v in el_names.items()}



"""for key, value in el_names.items():

    add_string = "value" """
qty_deck_rc_2017 = df2017['EN'].value_counts()[12] 

    # 1507 observations of deck_rc in 2017

qty_deck_rc_2018 = df2018['EN'].value_counts()[12]

    # 1518 observations of deck_rc in 2018

qty_deck_rc_2019 = df2019['EN'].value_counts()[12]

    # 1474 observations of deck_rc in 2019

qty_deck_rc_2020 = df2020['EN'].value_counts()[12]

    # 1191 observations of deck_rc in 2020

qty_deck_rc_2021 = df2021['EN'].value_counts()[12]

    # 1081 observations of deck_rc in 2021
    


# !!!
# Hold off on the concatenation in the line below!  
# Concatenate the dataframes for all STRUCNUM present in all years observed

df17_18_19_20_21 =  pd.concat([df2017, df2018, df2019, df2020, df2021], axis=0)

# Define the columns of the dataframe that require conversion to numeric
cols = ['STRUCNUM', 'EN', 'TOTALQTY', 'CS1', 'CS2', 'CS3', 'CS4']

# Convert the columns to numeric
df17_18_19_20_21[cols] = df17_18_19_20_21[cols].apply(pd.to_numeric, errors='coerce')

# Divide the CS1 thru CS4 by TOTALQTY to make percentages of the total element per bridge
df17_18_19_20_21[['CS1','CS2','CS3','CS4']] = df17_18_19_20_21[['CS1','CS2','CS3','CS4']].div(df17_18_19_20_21.TOTALQTY, axis=0)

# Check the data types ofter performing the computations
df17_18_19_20_21.dtypes 


# Create the means to make the individual dataframes for each Element Number (EN) using getattr().

class df_names:
    pass

element_df = df_names() # element_df will hold all the variables (which will also be variables in the form of dataframes) to be created associated with the different bridge elements or  ENs.  

# Get the unique set of all EN common to all years being obsesrved/inventoried.  
elements = df17_18_19_20_21['EN'].unique()


for element in elements:
    
    setattr(element_df, f"{element}", df17_18_19_20_21[df17_18_19_20_21['EN']==element].reset_index(drop=True))
    
for element in elements: #very important to keep the two for loops indented to the same spot! Second loop is not a nested loop!
        print(getattr(element_df, f"{element}"))



# MVP II 
# dictionary of all the bridge elements possible in any bridge.  
# plan to use the dict below as a means to create dataframes for the element numbers (ENs) present in the concatenated dataframe using a loop if possible rather than just using getattr for all the numbers in the dict and possibly making empty dataframes in the process.
# Although doing this may require using glob (global variables) which from my investigation of the practice seems like a poor attempt at a solution.  

# !!! This may not be necessary given the syntax of the getattr() statement, can return the None object and eliminate the need to only create dataframes for the ENs that are present in the observations.  If NoneType object is returned the program can continue on to the next EN without throwing an error- there will be a variable of Type = NoneType in the output.  
# !!!

"""
el_names = {'12': 'deck_rc',
            '13': 'deck_pc',
   	        '15': 'topFlg_pc',
   	        '16': 'topFlg_rc',
   	        '28': 'stDeck_og',
   	        '29': 'stDeck_cfg',
       	    '30': 'stDeck_corrOrtho',
            '31': 'deck_timb',
            	'38': 'slab_rc',
            	'39': 'slab_pc',
            	'54': 'slab_timb',
            	'60': 'deck_other',
            	'65': 'slab_other',
            	'102': 'cwBg_steel',
            	'103': 'cwBg_pc',
            	'105': 'cwBg_rc',
            '106': 'cwBg_other',
            '107': 'oGb_steel',
            '109': 'oGb_pc',
            '110': 'oGb_rc',
            '111': 'oGb_timb',
            '112': 'oGb_other',
            '113': 'stringer_steel',
            '115': 'stringer_pc',
            '116': 'stringer_rc',
            '117': 'stringer_timb',
            '118': 'stringer_other',
            '120': 'truss_steel',
            '135': 'truss_timb',
            '136': 'truss_other',
            '141': 'arch_steel',
            '142': 'arch_other',
            '143': 'arch_pc',
            '144': 'arch_rc',
            '145': 'arch_masonry',
            '146': 'arch_timb',
            '147': 'cbl_mSt',
            '148': 'cbl_secSt',
            '149': 'cbl_secOthr',
            '152': 'flrB_steel',
            '154': 'flrB_pc',
            '155': 'flrB_rc',
            '156': 'flrB_timb',
            '157': 'flrB_other',
            '161': 'spph',
            '162': 'sgp',
            '170': 'rrcf',
            '171': 'miscSS',
            '180': 'eqrcII',
            '181': 'eqrcC1',
            '182': 'eqrc_Othr',
            '202': 'col_st',
            	'203': 'col_othr',
            	'204': 'col_pc',
            	'205': 'col_rc',
            '206': 'col_timb',
            '207': 'twr_st',
            '208': 'tres_timb',
            '210': 'pw_rc',
            '211': 'pw_othr',
            '212': 'pw_timb',
            '213': 'pw_mas',
            	'215': 'abmt_rc',
            	'216': 'abmt_timb',
            	'217': 'abmt_mas',
            	'218': 'abmt_othr',
            	'219': 'abmt_steel',
            '220': 'pcf_rc',
            '225': 'pile_st',
            '226': 'pile_pc',
            '227': 'pile_rc',
            '228': 'pile_timb',
            '229': 'pile_othr',
            '231': 'pc_steel',
            	'233': 'pc_PrConc',
            	'234': 'pc_rc',
            '235': 'pc_timb',
            '236': 'pc_othr',
            '240': 'culv_st',
            '241': 'culv_rc',
            '242': 'culv_timb',
            '243': 'culv_othr',
            '244': 'culv_mas',
            '245': 'culv_pc',
            '250': 'tunnel',
            '251': 'pile_castSh',
            '252': 'pile_castDr',
            '254': 'cSh_stFH',
            '255': 'cSh_stPH',
            '256': 'slopeScP',
           	'300': 'joint_sse',
           	'301': 'joint_ps',
           	'302': 'joint_cs',
           	'303': 'joint_aws',
            '304': 'joint_oe',
            '305': 'joint_awo',
            '306': 'joint_othr',
            '307': 'joint_ap',
            '308': 'joint_ssp',
            '309': 'joint_sf',
            '310': 'brg_el',
            '311': 'brg_mov',
            '312': 'brg_ec',
            '313': 'brg_fxd',
            '314': 'brg_pot',
            '315': 'brg_dsk',
            '316': 'brg_othr',
            	'320': 'appSl_pc',
            '321': 'appSl_rc',
            	'330': 'br_m',
            '331': 'br_rc',
            '332': 'br_timb',
            '333': 'br_othr',
            '334': 'br_mas',
            	'510': 'dws_ac',
            	'511': 'dws_cp',
            	'512': 'dws_ep',
            '513': 'dws_timb',
            '515': 'spc_p',
            '516': 'spc_galv',
            '517': 'spc_ws',
            '520': 'rsps',
            '521': 'cpc',
            '522': 'deck_memb'
    }
"""


# Create dataframes for each individual EN to perform regression analysis for each possible part of a bridge

    # Deck and slabs, 13 elements

deck_rc = getattr(element_df, '12', None)

deck_pc = getattr(element_df, '13', None)

topFlg_pc = getattr(element_df, '15', None)

topFlg_rc = getattr(element_df, '16', None)

stDeck_og = getattr(element_df, '28', None)

stDeck_cfg = getattr(element_df, '29', None)

stDeck_corrOrtho = getattr(element_df, '30', None)

deck_timb = getattr(element_df, '31', None)

slab_rc = getattr(element_df, '38', None)

slab_pc = getattr(element_df, '39', None) # None in the data, MVP II

slab_timb = getattr(element_df, '54', None)

deck_other = getattr(element_df, '60', None) # None in the data, MVP II

slab_other = getattr(element_df, '65', None) # None in the data, MVP II

    # End deck and slabs

    # Superstructure, 38 elements
    
cwBg_steel = getattr(element_df, '102', None)

cwBg_pc = getattr(element_df, '103', None) # None in the data, MVP II

cwBg_rc = getattr(element_df, '105', None)

cwBg_other = getattr(element_df, '106', None) # None in the data, MVP II

oGb_steel = getattr(element_df, '107', None)

oGb_pc = getattr(element_df, '109', None)

oGb_rc = getattr(element_df, '110', None)

oGb_timb = getattr(element_df, '111', None)

oGb_other = getattr(element_df, '112', None) # None in the data, MVP II

stringer_steel = getattr(element_df, '113', None)

stringer_pc = getattr(element_df, '115', None)

stringer_rc = getattr(element_df, '116', None)

stringer_timb = getattr(element_df, '117', None)

stringer_other = getattr(element_df, '118', None) # None in the data, MVP II

truss_steel = getattr(element_df, '120', None)

truss_timb = getattr(element_df, '135', None) # None in the data, MVP II

truss_other = getattr(element_df, '136', None) # None in the data, MVP II

arch_steel = getattr(element_df, '141', None)

arch_other = getattr(element_df, '142', None) # None in the data, MVP II

arch_pc = getattr(element_df, '143', None)

arch_rc = getattr(element_df, '144', None)

arch_masonry = getattr(element_df, '145', None) # None in the data, MVP II

arch_timb = getattr(element_df, '146', None) # None in the data, MVP II

cbl_mSt = getattr(element_df, '147', None)

cbl_secSt = getattr(element_df, '148', None) # None in the data, MVP II

cbl_secOthr = getattr(element_df, '149', None) # None in the data, MVP II

flrB_steel = getattr(element_df, '152', None)

flrB_pc = getattr(element_df, '154', None)

flrB_rc = getattr(element_df, '155', None)

flrB_timb = getattr(element_df, '156', None)

flrB_other = getattr(element_df, '157', None) # None in the data, MVP II

spph = getattr(element_df, '161', None) # None in the data, MVP II

sgp = getattr(element_df, '162', None)

rrcf = getattr(element_df, '170', None) # None in the data, MVP II

miscSS = getattr(element_df, '171', None) # None in the data, MVP II

eqrcII = getattr(element_df, '180', None) # None in the data, MVP II

eqrcC1 = getattr(element_df, '181', None) # None in the data, MVP II

eqrc_Othr = getattr(element_df, '182', None) # None in the data, MVP II

    # End Superstructure
    
    # Substructure, 40 elements

col_st = getattr(element_df, '202', None)

col_othr = getattr(element_df, '203', None) # None in the data, MVP II

col_pc = getattr(element_df, '204', None)

col_rc = getattr(element_df, '205', None)

col_timb = getattr(element_df, '206', None)

twr_st = getattr(element_df, '207', None)

tres_timb = getattr(element_df, '208', None) # None in the data, MVP II

pw_rc = getattr(element_df, '210', None)

pw_othr = getattr(element_df, '211', None) # None in the data, MVP II

pw_timb = getattr(element_df, '212', None)

pw_mas = getattr(element_df, '213', None)

abmt_rc = getattr(element_df, '215', None)

abmt_timb = getattr(element_df, '216', None)

abmt_mas = getattr(element_df, '217', None)

abmt_othr = getattr(element_df, '218', None)

abmt_steel = getattr(element_df, '219', None)

pcf_rc = getattr(element_df, '220', None)

pile_st = getattr(element_df, '225', None)

pile_pc = getattr(element_df, '226', None)

pile_rc = getattr(element_df, '227', None)

pile_timb = getattr(element_df, '228', None)

pile_othr = getattr(element_df, '229', None)

pc_steel = getattr(element_df, '231', None)

pc_PrConc = getattr(element_df, '233', None)

pc_rc = getattr(element_df, '234', None)

pc_timb = getattr(element_df, '235', None)

pc_othr = getattr(element_df, '236', None) # None in the data, MVP II

culv_st = getattr(element_df, '240', None)

culv_rc = getattr(element_df, '241', None)

culv_timb = getattr(element_df, '242', None) # None in the data, MVP II

culv_othr = getattr(element_df, '243', None)

culv_mas = getattr(element_df, '244', None)

culv_pc = getattr(element_df, '245', None)

tunnel = getattr(element_df, '250', None) # None in the data, MVP II

pile_castSh = getattr(element_df, '251', None) # None in the data, MVP II

pile_castDr = getattr(element_df, '252', None) # None in the data, MVP II

cSh_stFH = getattr(element_df, '254', None) # None in the data, MVP II

cSh_stPH = getattr(element_df, '255', None) # None in the data, MVP II

slopeScP = getattr(element_df, '256', None) # None in the data, MVP II

    # End Substructure
    
    # Joints, 10 elements

joint_sse = getattr(element_df, '300', None)

joint_ps = getattr(element_df, '301', None)

joint_cs = getattr(element_df, '302', None)

joint_aws = getattr(element_df, '303', None)

joint_oe = getattr(element_df, '304', None)

joint_awo = getattr(element_df, '305', None)

joint_othr = getattr(element_df, '306', None)

joint_ap = getattr(element_df, '307', None) # None in the data, MVP II

joint_ssp = getattr(element_df, '308', None) # None in the data, MVP II

joint_sf = getattr(element_df, '309', None) # None in the data, MVP II

    # End Joints
    
    # Bearings, 7 elements

brg_el = getattr(element_df, '310', None)

brg_mov = getattr(element_df, '311', None)

brg_ec = getattr(element_df, '312', None)

brg_fxd = getattr(element_df, '313', None)

brg_pot = getattr(element_df, '314', None)

brg_dsk = getattr(element_df, '315', None)

brg_othr = getattr(element_df, '316', None)

    # End Bearings
    
    # Approach Slabs, 2 elements

appSl_pc = getattr(element_df, '320', None) # None in the data, MVP II

appSl_rc = getattr(element_df, '321', None) # None in the data, MVP II

    # End Approach Slabs
    
    # Railings, 5 elements
    
br_m = getattr(element_df, '330', None)

br_rc = getattr(element_df, '331', None)

br_timb = getattr(element_df, '332', None)

br_othr = getattr(element_df, '333', None)

br_mas = getattr(element_df, '334', None)

    # End Railings
    
    # Wearing Surfaces, 10 elements
    
dws_ac = getattr(element_df, '510', None)

dws_cp = getattr(element_df, '511', None) # None in the data, MVP II

dws_ep = getattr(element_df, '512', None) # None in the data, MVP II

dws_timb = getattr(element_df, '513', None) # None in the data, MVP II

spc_p = getattr(element_df, '515', None)

spc_galv = getattr(element_df, '516', None) # None in the data, MVP II

spc_ws = getattr(element_df, '517', None) # None in the data, MVP II

rsps = getattr(element_df, '520', None) # None in the data, MVP II

cpc = getattr(element_df, '521', None) # None in the data, MVP II

deck_memb = getattr(element_df, '522', None) # None in the data, MVP II

    # End Wearing Surfaces
    
    # End Elements


# Make the required dfs and then make plots and perform regression.  
# Create time column for the plots.  
# Create a column to compute the percentage of each CS (condition state) as means to determine when that CS might overtake all of the elements to which it pertains.  
# Make the total number of observations of each bridge element spread evenly across the total number of years inventoried.  Or should it be spread the observations evenly across the year for which the observations have been made?  

deck_rc = 