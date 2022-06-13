# -*- coding: utf-8 -*-
"""
Created on Sun May  8 11:57:20 2022

@author: Chris
"""

import pandas as pd

import matplotlib.pyplot as plt

import xml.etree.ElementTree as et

import numpy as np

import matplotlib.pyplot as plt

import seaborn as sns


df17 = pd.DataFrame([{'strucnum':'000000000000004', 'EN': '12', 'EPN': 'None', 'TOTALQTY': '21855', 'CS1':'20544', 'CS2': '1311', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000004', 'EN': '110', 'EPN': 'None', 'TOTALQTY': '3270', 'CS1':'0', 'CS2': '2616', 'CS3': '458', 'CS4': '196'},
                     {'strucnum':'000000000000004', 'EN': '202', 'EPN': 'None', 'TOTALQTY': '84', 'CS1':'0', 'CS2': '67', 'CS3': '17', 'CS4': '0'},
                     {'strucnum':'000000000000004', 'EN': '210', 'EPN': 'None', 'TOTALQTY': '171', 'CS1':'0', 'CS2': '125', 'CS3': '46', 'CS4': '0'},
                     {'strucnum':'000000000000004', 'EN': '234', 'EPN': 'None', 'TOTALQTY': '695', 'CS1':'0', 'CS2': '500', 'CS3': '195', 'CS4': '0'},
                     {'strucnum':'000000000000004', 'EN': '331', 'EPN': 'None', 'TOTALQTY': '1410', 'CS1':'0', 'CS2': '1325', 'CS3': '85', 'CS4': '0'},                     
                     {'strucnum':'000000000000008', 'EN': '12', 'EPN': 'None', 'TOTALQTY': '5922', 'CS1':'5626', 'CS2': '296', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000008', 'EN': '110', 'EPN': 'None', 'TOTALQTY': '5922', 'CS1':'0', 'CS2': '5922', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000008', 'EN': '204', 'EPN': 'None', 'TOTALQTY': '16', 'CS1':'0', 'CS2': '16', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000008', 'EN': '205', 'EPN': 'None', 'TOTALQTY': '12', 'CS1':'0', 'CS2': '12', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000008', 'EN': '234', 'EPN': 'None', 'TOTALQTY': '188', 'CS1':'0', 'CS2': '188', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000008', 'EN': '301', 'EPN': 'None', 'TOTALQTY': '94', 'CS1':'0', 'CS2': '94', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000008', 'EN': '333', 'EPN': 'None', 'TOTALQTY': '252', 'CS1':'0', 'CS2': '252', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000018', 'EN': '12', 'EPN': 'None', 'TOTALQTY': '924', 'CS1':'924', 'CS2': '0', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000018', 'EN': '38', 'EPN': 'None', 'TOTALQTY': '836', 'CS1':'836', 'CS2': '0', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000018', 'EN': '110', 'EPN': 'None', 'TOTALQTY': '176', 'CS1':'0', 'CS2': '109', 'CS3': '44', 'CS4': '23'},
                     {'strucnum':'000000000000018', 'EN': '204', 'EPN': 'None', 'TOTALQTY': '12', 'CS1':'12', 'CS2': '0', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000018', 'EN': '210', 'EPN': 'None', 'TOTALQTY': '63', 'CS1':'0', 'CS2': '63', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000018', 'EN': '234', 'EPN': 'None', 'TOTALQTY': '120', 'CS1':'120', 'CS2': '0', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000018', 'EN': '331', 'EPN': 'None', 'TOTALQTY': '88', 'CS1':'88', 'CS2': '0', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000019', 'EN': '12', 'EPN': 'None', 'TOTALQTY': '4092', 'CS1':'3846', 'CS2': '246', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000019', 'EN': '110', 'EPN': 'None', 'TOTALQTY': '528', 'CS1':'0', 'CS2': '528', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000019', 'EN': '204', 'EPN': 'None', 'TOTALQTY': '14', 'CS1':'0', 'CS2': '14', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000019', 'EN': '205', 'EPN': 'None', 'TOTALQTY': '14', 'CS1':'0', 'CS2': '14', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000019', 'EN': '234', 'EPN': 'None', 'TOTALQTY': '217', 'CS1':'0', 'CS2': '217', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000019', 'EN': '301', 'EPN': 'None', 'TOTALQTY': '155', 'CS1':'0', 'CS2': '155', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000022', 'EN': '12', 'EPN': 'None', 'TOTALQTY': '264', 'CS1':'0', 'CS2': '264', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000022', 'EN': '110', 'EPN': 'None', 'TOTALQTY': '264', 'CS1':'0', 'CS2': '264', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000022', 'EN': '331', 'EPN': 'None', 'TOTALQTY': '264', 'CS1':'0', 'CS2': '264', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000031', 'EN': '16', 'EPN': 'None', 'TOTALQTY': '264', 'CS1':'0', 'CS2': '264', 'CS3': '0', 'CS4': '0'}])


df18 = pd.DataFrame([{'strucnum':'000000000000004', 'EN': '12', 'EPN': 'None', 'TOTALQTY': '21855', 'CS1':'20544', 'CS2': '1311', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000004', 'EN': '110', 'EPN': 'None', 'TOTALQTY': '3270', 'CS1':'0', 'CS2': '2616', 'CS3': '458', 'CS4': '196'},
                     {'strucnum':'000000000000004', 'EN': '202', 'EPN': 'None', 'TOTALQTY': '84', 'CS1':'0', 'CS2': '67', 'CS3': '17', 'CS4': '0'},
                     {'strucnum':'000000000000004', 'EN': '210', 'EPN': 'None', 'TOTALQTY': '171', 'CS1':'0', 'CS2': '125', 'CS3': '46', 'CS4': '0'},
                     {'strucnum':'000000000000004', 'EN': '234', 'EPN': 'None', 'TOTALQTY': '695', 'CS1':'0', 'CS2': '500', 'CS3': '195', 'CS4': '0'},
                     {'strucnum':'000000000000004', 'EN': '331', 'EPN': 'None', 'TOTALQTY': '1410', 'CS1':'0', 'CS2': '1325', 'CS3': '85', 'CS4': '0'},
                     {'strucnum':'000000000000008', 'EN': '12', 'EPN': 'None', 'TOTALQTY': '5922', 'CS1':'5626', 'CS2': '296', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000008', 'EN': '110', 'EPN': 'None', 'TOTALQTY': '5922', 'CS1':'0', 'CS2': '5922', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000008', 'EN': '204', 'EPN': 'None', 'TOTALQTY': '16', 'CS1':'0', 'CS2': '16', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000008', 'EN': '205', 'EPN': 'None', 'TOTALQTY': '12', 'CS1':'0', 'CS2': '12', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000008', 'EN': '234', 'EPN': 'None', 'TOTALQTY': '188', 'CS1':'0', 'CS2': '188', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000008', 'EN': '301', 'EPN': 'None', 'TOTALQTY': '94', 'CS1':'0', 'CS2': '94', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000008', 'EN': '333', 'EPN': 'None', 'TOTALQTY': '252', 'CS1':'0', 'CS2': '252', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000018', 'EN': '12', 'EPN': 'None', 'TOTALQTY': '924', 'CS1':'924', 'CS2': '0', 'CS3': '0', 'CS4': '0'}, 
                     {'strucnum':'000000000000018', 'EN': '38', 'EPN': 'None', 'TOTALQTY': '836', 'CS1':'836', 'CS2': '0', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000018', 'EN': '110', 'EPN': 'None', 'TOTALQTY': '176', 'CS1':'0', 'CS2': '109', 'CS3': '44', 'CS4': '23'}, 
                     {'strucnum':'000000000000018', 'EN': '204', 'EPN': 'None', 'TOTALQTY': '12', 'CS1':'12', 'CS2': '0', 'CS3': '0', 'CS4': '0'}, 
                     {'strucnum':'000000000000018', 'EN': '210', 'EPN': 'None', 'TOTALQTY': '63', 'CS1':'0', 'CS2': '63', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000018', 'EN': '234', 'EPN': 'None', 'TOTALQTY': '120', 'CS1':'120', 'CS2': '0', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000018', 'EN': '331', 'EPN': 'None', 'TOTALQTY': '88', 'CS1':'88', 'CS2': '0', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000019', 'EN': '12', 'EPN': 'None', 'TOTALQTY': '4092', 'CS1':'3846', 'CS2':'246', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000019', 'EN': '110', 'EPN': 'None', 'TOTALQTY': '528', 'CS1':'0', 'CS2':'528', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000019', 'EN': '204', 'EPN': 'None', 'TOTALQTY': '14', 'CS1':'0', 'CS2':'14', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000019', 'EN': '205', 'EPN': 'None', 'TOTALQTY': '14', 'CS1':'0', 'CS2':'14', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000019', 'EN': '234', 'EPN': 'None', 'TOTALQTY': '217', 'CS1':'0', 'CS2':'217', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000019', 'EN': '301', 'EPN': 'None', 'TOTALQTY': '155', 'CS1':'0', 'CS2':'155', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000019', 'EN': '331', 'EPN': 'None', 'TOTALQTY': '264', 'CS1':'0', 'CS2':'264', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000034', 'EN': '12', 'EPN': 'None', 'TOTALQTY': '264', 'CS1':'0', 'CS2': '264', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000034', 'EN': '110', 'EPN': 'None', 'TOTALQTY': '264', 'CS1':'0', 'CS2': '264', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000036', 'EN': '331', 'EPN': 'None', 'TOTALQTY': '264', 'CS1':'0', 'CS2': '264', 'CS3': '0', 'CS4': '0'},
                         {'strucnum':'000000000000039', 'EN': '16', 'EPN': 'None', 'TOTALQTY': '264', 'CS1':'0', 'CS2': '264', 'CS3': '0', 'CS4': '0'}])


df19 = pd.DataFrame([{'strucnum':'000000000000004', 'EN': '16', 'EPN': 'None', 'TOTALQTY': '21917', 'CS1':'21913', 'CS2': '0', 'CS3': '4', 'CS4': '0'},
                     {'strucnum':'000000000000004', 'EN': '110', 'EPN': 'None', 'TOTALQTY': '3278', 'CS1':'0', 'CS2':'3180', 'CS3':'8', 'CS4':'90'},
                     {'strucnum':'000000000000004', 'EN': '210', 'EPN': 'None', 'TOTALQTY': '216', 'CS1':'214', 'CS2':'0', 'CS3':'0', 'CS4':'2'},
                     {'strucnum':'000000000000004', 'EN': '225', 'EPN': 'None', 'TOTALQTY': '82', 'CS1':'0', 'CS2':'82', 'CS3':'0', 'CS4':'0'},
                     {'strucnum':'000000000000004', 'EN': '234', 'EPN': 'None', 'TOTALQTY': '775', 'CS1':'775', 'CS2':'0', 'CS3':'0', 'CS4':'0'},
                     {'strucnum':'000000000000004', 'EN': '331', 'EPN': 'None', 'TOTALQTY': '1414', 'CS1':'1349', 'CS2':'0', 'CS3':'0', 'CS4':'65'},
                     {'strucnum':'000000000000008', 'EN': '12', 'EPN': 'None', 'TOTALQTY': '5922', 'CS1':'0', 'CS2':'5922', 'CS3':'0', 'CS4':'0'},
                     {'strucnum':'000000000000008', 'EN': '110', 'EPN': 'None', 'TOTALQTY': '5922', 'CS1':'0', 'CS2':'5921', 'CS3':'1', 'CS4':'0'},
                     {'strucnum':'000000000000008', 'EN': '205', 'EPN': 'None', 'TOTALQTY': '12', 'CS1':'12', 'CS2':'0', 'CS3':'0', 'CS4':'0'},
                     {'strucnum':'000000000000008', 'EN': '226', 'EPN': 'None', 'TOTALQTY': '16', 'CS1':'16', 'CS2':'0', 'CS3':'0', 'CS4':'0'},
                     {'strucnum':'000000000000008', 'EN': '234', 'EPN': 'None', 'TOTALQTY': '188', 'CS1':'0', 'CS2':'185', 'CS3':'3', 'CS4':'0'},
                     {'strucnum':'000000000000008', 'EN': '301', 'EPN': 'None', 'TOTALQTY': '94', 'CS1':'94', 'CS2':'0', 'CS3':'0', 'CS4':'0'},
                     {'strucnum':'000000000000008', 'EN': '331', 'EPN': 'None', 'TOTALQTY': '252', 'CS1':'252', 'CS2':'0', 'CS3':'0', 'CS4':'0'},
                     {'strucnum':'000000000000009', 'EN': '38', 'EPN': 'None', 'TOTALQTY': '9960', 'CS1':'9960', 'CS2':'0', 'CS3':'0', 'CS4':'0'},
                     {'strucnum':'000000000000009', 'EN': '226', 'EPN': 'None', 'TOTALQTY': '28', 'CS1':'28', 'CS2':'0', 'CS3':'0', 'CS4':'0'}, 
                     {'strucnum':'000000000000009', 'EN': '234', 'EPN': 'None', 'TOTALQTY': '334', 'CS1':'334', 'CS2':'0', 'CS3':'0', 'CS4':'0'},
                     {'strucnum':'000000000000009', 'EN': '310', 'EPN': 'None', 'TOTALQTY': '4', 'CS1':'4', 'CS2':'0', 'CS3':'0', 'CS4':'0'}, 
                     {'strucnum':'000000000000009', 'EN': '331', 'EPN': 'None', 'TOTALQTY': '240', 'CS1':'0', 'CS2':'240', 'CS3':'0', 'CS4':'0'}, 
                     {'strucnum':'000000000000018', 'EN': '38', 'EPN': 'None', 'TOTALQTY': '1760', 'CS1':'1760', 'CS2':'0', 'CS3':'0', 'CS4':'0'},
                     {'strucnum':'000000000000018', 'EN': '110', 'EPN': 'None', 'TOTALQTY': '176', 'CS1':'81', 'CS2':'94', 'CS3':'1', 'CS4':'0'},
                     {'strucnum':'000000000000018', 'EN': '205', 'EPN': 'None', 'TOTALQTY': '6', 'CS1':'4', 'CS2':'2', 'CS3':'0', 'CS4':'0'},
                     {'strucnum':'000000000000018', 'EN': '226', 'EPN': 'None', 'TOTALQTY': '12', 'CS1':'12', 'CS2':'0', 'CS3':'0', 'CS4':'0'},
                     {'strucnum':'000000000000018', 'EN': '234', 'EPN': 'None', 'TOTALQTY': '121', 'CS1':'114', 'CS2':'6', 'CS3':'1', 'CS4':'0'},
                     {'strucnum':'000000000000018', 'EN': '331', 'EPN': 'None', 'TOTALQTY': '88', 'CS1':'88', 'CS2':'0', 'CS3':'0', 'CS4':'0'},
                     {'strucnum':'000000000000018', 'EN': '510', 'EPN': '38', 'TOTALQTY': '836', 'CS1':'836', 'CS2':'0', 'CS3':'0', 'CS4':'0'},
                     {'strucnum':'000000000000019', 'EN': '12', 'EPN': 'None', 'TOTALQTY': '4092', 'CS1':'4068', 'CS2':'24', 'CS3':'0', 'CS4':'0'},
                     {'strucnum':'000000000000019', 'EN': '110', 'EPN': 'None', 'TOTALQTY': '528', 'CS1':'322', 'CS2':'206', 'CS3':'0', 'CS4':'0'},
                     {'strucnum':'000000000000019', 'EN': '205', 'EPN': 'None', 'TOTALQTY': '14', 'CS1':'0', 'CS2':'14', 'CS3':'0', 'CS4':'0'},
                     {'strucnum':'000000000000019', 'EN': '226', 'EPN': 'None', 'TOTALQTY': '14', 'CS1':'0', 'CS2':'14', 'CS3':'0', 'CS4':'0'},
                     {'strucnum':'000000000000019', 'EN': '234', 'EPN': 'None', 'TOTALQTY': '217', 'CS1':'0', 'CS2':'217', 'CS3':'0', 'CS4':'0'},
                     {'strucnum':'000000000000019', 'EN': '301', 'EPN': 'None', 'TOTALQTY': '155', 'CS1':'155', 'CS2':'0', 'CS3':'0', 'CS4':'0'},
                     {'strucnum':'000000000000019', 'EN': '330', 'EPN': 'None', 'TOTALQTY': '264', 'CS1':'264', 'CS2':'0', 'CS3':'0', 'CS4':'0'},
                     {'strucnum':'000000000000019', 'EN': '331', 'EPN': 'None', 'TOTALQTY': '264', 'CS1':'264', 'CS2':'0', 'CS3':'0', 'CS4':'0'},
                     {'strucnum':'000000000000044', 'EN': '12', 'EPN': 'None', 'TOTALQTY': '264', 'CS1':'0', 'CS2': '264', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000049', 'EN': '110', 'EPN': 'None', 'TOTALQTY': '264', 'CS1':'0', 'CS2': '264', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000049', 'EN': '331', 'EPN': 'None', 'TOTALQTY': '264', 'CS1':'0', 'CS2': '264', 'CS3': '0', 'CS4': '0'},
                     {'strucnum':'000000000000061', 'EN': '16', 'EPN': 'None', 'TOTALQTY': '264', 'CS1':'0', 'CS2': '264', 'CS3': '0', 'CS4': '0'}])


b_17 = df17['strucnum'].to_numpy()

b_18 = df18['strucnum'].to_numpy()

b_19 = df19['strucnum'].to_numpy()

b_20 = df20['strucnum'].to_numpy()

b_21 = df21['strucnum'].to_numpy()


strucnum_in_all = list(set.intersection(*map(set, [b_17, b_18, b_19])))
strucnum_in_all


# Remove element numbers not present in all dfs

df17 = df17[np.isin(df17['strucnum'].to_numpy(), strucnum_in_all)]

df18 = df18[np.isin(df18['strucnum'].to_numpy(), strucnum_in_all)]

df19 = df19[np.isin(df19['strucnum'].to_numpy(), strucnum_in_all)]

df20 = df20[np.isin(df20['strucnum'].to_numpy(), strucnum_in_all)]

df21 = df21[np.isin(df21['strucnum'].to_numpy(), strucnum_in_all)]

df17_18_19 =  pd.concat([df17, df18, df19], axis=0)

df17_18_19[['CS1','CS2','CS3','CS4']] = df17_18_19[[float('CS1'),float('CS2'),float('CS3'),float('CS4')]].div(df17_18_19.TOTALQTY, axis=0)


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



class df_names:
    pass

element_df = df_names() #element_df will hold all the variables (which will also be variables in the form of dataframes) to be created associated with the different bridge elements or  ENs.  

elements = df17_18_19['EN'].unique()


for element in elements:
    
    setattr(element_df, f"{element}", df17_18_19[df17_18_19['EN']==element].reset_index(drop=True))
    
for element in elements: #very important to keep the two for loops be indented to the same spot! Second loop is not a nested loop!
        print(getattr(element_df, f"{element}"))
        
        
        
        

deck_rc = getattr(element_df, '12')

deck_pc = getattr(element_df, '13')

topFlg_pc = getattr(element_df, '15')

topFlg_rc= getattr(element_df, '16')

stDeck_og = getattr(element_df, '28')

stDeck_cfg = getattr(element_df, '29')

stDeck_corrOrtho = getattr(element_df, '30')

deck_timb = getattr(element_df, '31')

slab_rc = getattr(element_df, '38')

slab_pc = getattr(element_df, '39')

slab_timb = getattr(element_df, '54')

deck_other = getattr(element_df, '60')

slab_other = getattr(element_df, '65')

cwBg_steel = getattr(element_df, '102')

cwBg_pc = getattr(element_df, '103')

cwBg_rc = getattr(element_df, '105')

cwBg_other = getattr(element_df, '106')

oGb_steel = getattr(element_df, '107')

oGb_pc = getattr(element_df, '109')

oGb_rc = getattr(element_df, '110')

oGb_timb = getattr(element_df, '111')

oGb_other = getattr(element_df, '112')

stringer_steel = getattr(element_df, '113')

stringer_pc = getattr(element_df, '115')

stringer_rc = getattr(element_df, '116')

stringer_timb = getattr(element_df, '117')

stringer_other = getattr(element_df, '118')

truss_steel = getattr(element_df, '120')

truss_timb = getattr(element_df, '135')

truss_other = getattr(element_df, '136')

arch_steel = getattr(element_df, '141')

arch_other = getattr(element_df, '142')

arch_pc = getattr(element_df, '143')

arch_rc = getattr(element_df, '144')

arch_masonry = getattr(element_df, '145')

arch_timb = getattr(element_df, '146')

cbl_mSt = getattr(element_df, '147')

cbl_secSt = getattr(element_df, '148')

cbl_secOthr = getattr(element_df, '149')

flrB_steel = getattr(element_df, '152')

flrB_pc = getattr(element_df, '154')

flrB_rc = getattr(element_df, '155')

flrB_timb = getattr(element_df, '156')

flrB_other = getattr(element_df, '157')

spph = getattr(element_df, '161')

sgp = getattr(element_df, '162')

rrcf = getattr(element_df, '170')

miscSS = getattr(element_df, '171')

eqrcII = getattr(element_df, '180')

eqrcC1 = getattr(element_df, '181')

eqrc_Othr = getattr(element_df, '182')

col_st = getattr(element_df, '202')

col_othr = getattr(element_df, '203')

col_pc = getattr(element_df, '204')

col_rc = getattr(element_df, '205')

col_timb = getattr(element_df, '206')

twr_st = getattr(element_df, '207')

tres_timb = getattr(element_df, '208')

pw_rc = getattr(element_df, '210')

pw_othr = getattr(element_df, '211')

pw_timb = getattr(element_df, '212')

pw_mas = getattr(element_df, '213')

abmt_rc = getattr(element_df, '215')

abmt_timb = getattr(element_df, '216')

abmt_mas = getattr(element_df, '217')

abmt_othr = getattr(element_df, '218')

abmt_steel = getattr(element_df, '219')

pcf_rc = getattr(element_df, '220')

pile_st = getattr(element_df, '225')

pile_pc = getattr(element_df, '226')

pile_rc = getattr(element_df, '227')

pile_timb = getattr(element_df, '228')

pile_othr = getattr(element_df, '229')

pc_steel = getattr(element_df, '231')

pc_PrConc = getattr(element_df, '233')

pc_rc = getattr(element_df, '234')

pc_timb = getattr(element_df, '235')

pc_othr = getattr(element_df, '236')

culv_st = getattr(element_df, '240')

culv_rc = getattr(element_df, '241')

culv_timb = getattr(element_df, '242')

culv_othr = getattr(element_df, '243')

culv_mas = getattr(element_df, '244')

culv_pc = getattr(element_df, '245')

tunnel = getattr(element_df, '250')

pile_castSh = getattr(element_df, '251')

pile_castDr = getattr(element_df, '252')

cSh_stFH = getattr(element_df, '254')

cSh_stPH = getattr(element_df, '255')

slopeScP = getattr(element_df, '256')

joint_sse = getattr(element_df, '300')

joint_ps = getattr(element_df, '301')

joint_cs = getattr(element_df, '302')

joint_aws = getattr(element_df, '303')

joint_oe = getattr(element_df, '304')

joint_awo = getattr(element_df, '305')

joint_othr = getattr(element_df, '306')

joint_ap = getattr(element_df, '307')

joint_ssp = getattr(element_df, '308')

joint_sf = getattr(element_df, '309')

appSl_pc = getattr(element_df, '320')

appSl_rc = getattr(element_df, '321')

br_m = getattr(element_df, '330')

br_rc = getattr(element_df, '331')

br_timb = getattr(element_df, '332')

br_othr = getattr(element_df, '333')

br_mas = getattr(element_df, '334')

dws_ac = getattr(element_df, '510')

dws_cp = getattr(element_df, '511')

dws_ep = getattr(element_df, '512')

dws_timb = getattr(element_df, '513')

spc_p = getattr(element_df, '515')

spc_galv = getattr(element_df, '516')

spc_ws = getattr(element_df, '517')

rsps = getattr(element_df, '520')

cpc = getattr(element_df, '521')

deck_memb = getattr(element_df, '522')

