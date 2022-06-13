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

# {'strucnum' :'CS1'}
Bridges_17 = {'04' :'9', '08' :'14', '09' :'6', '16' :'21'}

# dfScatter_strucnum is the dataframe that is meant to order the chronology of the observations on the x-axis by strucnum increasing from lowest to highest strucnum on a yearly basis.  

# How do I get the ENs out of the strucnums common to each set and then stack them in successive years?  Do I even need to?


# df20_19 = pd.merge(df2020, df2019, suffixes=['_20', '_19'], on=['strucnum','EN']) # Keeping the observations that match by structure number (strucnum) and that have the same element numbers (EN) wuthin that strucnum.  


# It may be a better plan to check the regression of the CS4 condition as it is the one most likely to increase- as I'm noticing the CS1 may be lower in successive years than in others.












# 2017
""" 	FHWAED	STATE	strucnum	EN	EPN	TOTALQTY	CS1	CS2	CS3	CS4
0		45	000000000000004	12		21855	20544	1311	0	0
1		45	000000000000004	110		3270	0	2616	458 	196
2		45	000000000000004	202		84	0	67	17	0
3		45	000000000000004	210		171	0	125	46	0
4		45	000000000000004	234		695	0	500	195	0
5		45	000000000000004	331		1410	0	1325	85	0
8		45	000000000000008	12		5922	5626	296	0	0
9		45	000000000000008	110		5922	0	5922	0	0
10		45	000000000000008	204		16	0	16	0	0
11		45	000000000000008	205		12	0	12	0	0
12		45	000000000000008	234		188	0	188	0	0
13		45	000000000000008	301		94	0	94	0	0
14		45	000000000000008	333		252 0	252 0	0
16		45	000000000000018	12		924	 924 0 0	0
17		45	000000000000018	38		836	 836	0	0	0
18		45	000000000000018	110		176	 0	109 44 23
19		45	000000000000018	204		12	12	0	0	0
20		45	000000000000018	210		63	0	63	0	0
21		45	000000000000018	234		120	 120	0	0	0
22		45	000000000000018	331		88	88	0	0	0
25		45	000000000000019	12		4092	3846	246	0	0
26		45	000000000000019	110		528	 0	528 0	0
27		45	000000000000019	204		14	0	14	0	0
28		45	000000000000019	205		14	0	14	0	0
29		45	000000000000019	234		217 0	217	 0	0
30		45	000000000000019	301		155	 0	155 0	0
31		45	000000000000019	331		264	 0	264 0	0 """

	
# No EN associated 
# Can one be added to this format?
# TOTALQTY is per element
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

# 2018
""" 	FHWAED	STATE	strucnum	EN	EPN	TOTALQTY	CS1	CS2	CS3	CS4
0		45	000000000000004	12		21855	20544	1311	0	0
1		45	000000000000004	110		3270	0	2616	458 	196
2		45	000000000000004	202		84	0	67	17	0
3		45	000000000000004	210		171 	0	125 	46	0
4		45	000000000000004	234		695 	0	500	 195	0
5		45	000000000000004	331		1410	0	1325	85	0
8		45	000000000000008	12		5922	5626	296	0	0
9		45	000000000000008	110		5922	0	5922	0	0
10		45	000000000000008	204		16	0	16	0	0
11		45	000000000000008	205		12	0	12	0	0
12		45	000000000000008	234		188 	0	188 0	0
13		45	000000000000008	301		94	0	94	0	0
14		45	000000000000008	333		252 	0	252	 0	0
16		45	000000000000018	12		924	 924	0	0	0
17		45	000000000000018	38		836	 836	0	0	0
18		45	000000000000018	110		176	 0	109 44 23
19		45	000000000000018	204		12	12	0	0	0
20		45	000000000000018	210		63	0	63	0	0
21		45	000000000000018	234		120	120	0	0	0
22		45	000000000000018	331		88	88	0	0	0
25		45	000000000000019	12		4092	3846	246	0	0
26		45	000000000000019	110		528	0	528	0	0
27		45	000000000000019	204		14	0	14	0	0
28		45	000000000000019	205		14	0	14	0	0
29		45	000000000000019	234		217	0	217	0	0
30		45	000000000000019	301		155	0	155	0	0
31		45	000000000000019	331		264	0	264	0	0 """                   

# No EN associated 
# Can one be added to this format?
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
                
# 2019
""" 	FHWAED	STATE	strucnum	EN	EPN	TOTALQTY	CS1	CS2	CS3	CS4
0		45	000000000000004	16		21917	21913	0	4	0
1		45	000000000000004	110		3278	0	3180	8	90
2		45	000000000000004	210		216 214	0	0	2
3		45	000000000000004	225		82	0	82	0	0
4		45	000000000000004	234		775	 775	0	0	0
5		45	000000000000004	331		1414	1349	0	0	65
6		45	000000000000008	12		5922	0	5922	0	0
7		45	000000000000008	110		5922	0	5921	1	0
8		45	000000000000008	205		12	12	0	0	0
9		45	000000000000008	226		16	16	0	0	0
10		45	000000000000008	234		188	 0	185 3	0
11		45	000000000000008	301		94	94	0	0	0
12		45	000000000000008	331		252	 252	0	0	0 # !!!
13		45	000000000000009	38		9960	9960	0	0	0
14		45	000000000000009	226		28	28	0	0	0
15		45	000000000000009	234		334 334	0	0	0
16		45	000000000000009	310		4	4	0	0	0
17		45	000000000000009	331		240	 0	240 0	0  # !!!
18		45	000000000000018	38		1760	1760	0	0	0
19		45	000000000000018	110		176 81 94 1	0
20		45	000000000000018	205		6	4	2	0	0
21		45	000000000000018	226		12	12	0	0	0
22		45	000000000000018	234		121 114	6	1	0
23		45	000000000000018	331		88	88	0	0	0
24		45	000000000000018	510	38	836	 836	0	0	0
25		45	000000000000019	12		4092	4068	24	0	0
26		45	000000000000019	110		528 322 206 0	0
27		45	000000000000019	205		14	0	14	0	0
28		45	000000000000019	226		14	0	14	0	0
29		45	000000000000019	234		217	0	217	0	0
30		45	000000000000019	301		155 155	0	0	0
31		45	000000000000019	330		264	 264	0	0	0
32		45	000000000000019	331		264	 264	0	0	0  """
# No EN associated 
# Can one be added to this format?

# !!! 

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
                   





# 2020
"""	FHWAED	STATE	strucnum	EN	EPN	TOTALQTY	CS1	CS2	CS3	CS4
0		45	000000000000004	12		21855	20544	1311	0	0
1		45	000000000000004	110		3270	0	2616	458	196
2		45	000000000000004	202		84	0	67	17	0
3		45	000000000000004	210		171	0	125	46	0
4		45	000000000000004	234		695	0	500	195	0
5		45	000000000000004	331		1410	0	1325	85	0
6		45	000000000000004	510	12	21855	21855	0	0	0
7		45	000000000000004	515	202	10753	10753	0	0	0
8		45	000000000000008	12		5922	5626	296	0	0
9		45	000000000000008	110		5922	0	5922	0	0
10		45	000000000000008	204		16	0	16	0	0
11		45	000000000000008	205		12	0	12	0	0
12		45	000000000000008	234		188	0	188	0	0
13		45	000000000000008	301		94	0	94	0	0
14		45	000000000000008	333		252	0	252	0	0
15		45	000000000000008	510	12	5922	5626	296	0	0
16		45	000000000000009	38		9960	9960	0	0	0
17		45	000000000000009	226		28	28	0	0	0
18		45	000000000000009	234		334	334	0	0	0
19		45	000000000000009	310		4	4	0	0	0
20		45	000000000000009	331		240	0	240	0	0
21		45	000000000000018	38		1769	1760	5	4	0
22		45	000000000000018	110		176	31	138	7	0
23		45	000000000000018	205		6	4	2	0	0
24		45	000000000000018	226		12	8	4	0	0
25		45	000000000000018	234		121	112	4	5	0
26		45	000000000000018	331		88	75	12	1	0
27		45	000000000000019	12		4092	3846	246	0	0
28		45	000000000000019	110		528	0	528	0	0
29		45	000000000000019	204		14	0	14	0	0
30		45	000000000000019	205		14	0	14	0	0
31		45	000000000000019	234		217	0	217	0	0
32		45	000000000000019	301		155	0	155	0	0
33		45	000000000000019	331		264	0	264	0	0
34		45	000000000000019	510	12	4092	3887	205	0	0 """


# return non matches and then drop corresponding rows?


b_17 = df17['strucnum'].to_numpy()

print(b_17)

print(np.unique(b_17))





# below is from https://www.geeksforgeeks.org/python-get-unique-values-list/#:~:text=Using%20Python's%20import%20numpy%2C%20the,unique%20values%20from%20the%20list

def unique(list1):
    x = np.array(list1)
    print(np.unique(x))
    
    print("the unique values from 1st list is")
    unique(list1)
    
# Sets are unordered collections of unique elements meaning that any duplicates will be removed when the set is formed.  



strUnique_17 =  pd.value_counts(b_17)

b_18 = df18['strucnum'].to_numpy()

print(b_18)

# From a function's perspective: A parameter is the variable listed inside the parentheses in the function definition. An argument is the value(s) that are sent to the function when it is called.

# non_match_elements is the function, b_17 and b_18 are the parameters.
def non_match_elements(b_17, b_18):
    non_match = []
    for i in b_17:
        if i not in b_18:
            non_match.append(i)
    return non_match
       

#list_a = [2, 4, 6, 8, 10, 12]
#list_b = [2, 4, 6, 8]

non_match = non_match_elements(b_17, b_18)
print("No match elements: ", non_match)


strUnique_18 =  pd.value_counts(b_18)

b_19 = df19['strucnum'].to_numpy()

print(b_19)

strUnique_19 =  pd.value_counts(b_19)

# b_20 = df20['strucnum'].to_numpy()

# print(b_20)

# strUnique_20 =  pd.value_counts(b_20)

# strUnique_20.equals(strUnique_19)

# strUnique_19 is the largest set:
    
# set(strUnique_19).intersection(strUnique_20)

# b_19_20 = set(b_19).intersection(b_20)

# b_19_20 = sorted(b_19_20) #10151

# !!! start here

#List1 = b_17.tolist()
#List2 = b_18.tolist()
#List3 = b_19.tolist()

# maybe eliminate these variables in the main version, just put the three lists in the strucnum_in_all equation as they are already.

strucnum_in_all = list(set.intersection(*map(set, [b_17, b_18, b_19])))
strucnum_in_all
# [3, 4]


# Remove element numbers not present in all 3 dfs

df17 = df17[np.isin(df17['strucnum'].to_numpy(), strucnum_in_all)]

df18 = df18[np.isin(df18['strucnum'].to_numpy(), strucnum_in_all)]

df19 = df19[np.isin(df19['strucnum'].to_numpy(), strucnum_in_all)]


df17_18_19 =  pd.concat([df17, df18, df19], axis=0)





#var=pd.Series({'a':1, 'b':2})
#update both keys and variables
#var.a=3
#print(var.a,var['a'])


#from operator import itemgetter

#params = {'a': 1, 'b': 2}

#a, b = itemgetter('a', 'b')(params)


# elements variable below refers to the different bridge elements or EN
# pd.Series ???

#el_names refers to the dict of possible element names for a bridge as denoted in the National Bridge Inventory 

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
            '147': 'cbl_mst',
            '148': 'cbl_secst',
            '149': 'cbl_secothr',
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
        

# getattr(df17_18_19[elements], df_names()).values.tolist()


deck_rc = getattr(element_df, '12')


# !!! Probably need to delete the two rows below. 05/08/2022 Start with the coding above first!
for element_df(el_names):
    print(element_df(value))




# need to start figuring out how to resample the date for time periods


# for element in elements: #very important to keep the two for loops indented to the the same spot! Second loop is not a nested loop!
#        print(getattr(element_df, f"{element}"))

def filter_el_names(element_df, callback):
    newDict = dict()
# Iterate over all the items in dictionary
for (key, value) in element_df.values():
# Check if item satisfies the given condition then add to new dict
    if callback((value)):
        newDict[key] = value
return newDict





getattr(element_df, '12')

#for key, value in el_names.keys():

    #value = element_df.values()



#i can be the items of the el_names dictionary above

for item in element_df:
    print(item)
    print(type(item))

for key, value in el_names.items():
    
    print(key, '->', value)

    
    el_names.values() = getattr(element_df.keys())



#for element in elements:
#  element = pd.DataFrame() # fruit will not be anymore Apple or Orange
#  element5 = df[df['Fruit']==fruit].reset_index(drop=True) 




d={} #empty dictionary
for x in range(1,10): #for looping 
        d["string{0}".format(x)]="Variable1"
        
my_variables = {}
i = 0
for j in range(5):
    i += 1
    my_variables["w" + str(i)] = function(i)
    
print (my_variables["w1"])

currency_dict={'USD':'Dollar',
             'EUR':'Euro',
             'GBP':'Pound',
              'INR':'Rupee'}

df=pd.DataFrame({'abbr':list(currency_dict.keys()),
                 'curr':list(currency_dict.values())})

# elno means element number as used in the elements dictionary above, also serves as the key in the 
# vardf means the dataframe to be created that will have a variable name 

df_elements = pd.DataFrame({'elno':list(elements.keys()), 'vardf':list(elements.values())})

df_elements.elno[df_elements.vardf==]


# look at using the elements dict above as a dataframe of its own and then iterate over that df somehow...

for el_name in elements:
    elements[el_name] = df17_18_19[df17_18_19['EN'] == '']



#deck_rc = df17_18_19.loc[df17_18_19['EN'] == '12']

#deck_rc.plot(x='TOTALQTY', y='')

deck_rc = df17_18_19[df17_18_19['EN'] == '12']

# Next either concatente or pull the different 

# concatenating df17, df18 and df19 along rows
dftot = pd.concat([df17, df18, df19], axis=0)



dftot = dftot.astype({"strucnum": 'int32', "EN": 'int32', 'EPN': 'int32', "TOTALQTY": 'int32', "CS1": 'int32', "CS2": 'int32', "CS3": 'int32', "CS4": 'int32'})

dfDeckSlab = dftot.loc[(dftot['EN'] >= 12) & (dftot['EN'] <= 65), ['strucnum', 'CS1', 'CS2', 'CS3', 'CS4']]



df20_19_18_17['STATE_20'] = pd.to_numeric(df20_19_18_17['STATE_20'],errors='coerce')
df20_19_18_17 = df20_19_18_17.replace(np.nan, 0, regex=True)
df20_19_18_17['STATE_20'] = df20_19_18_17['STATE_20'].astype(int)




dfDeckSlab = vertical_concat.loc[(vertical_concat['EN'] >= 12) & (vertical_concat['EN'] <= 65), ['strucnum', 'CS1', 'CS2', 'CS3', 'CS4']]







# No EN associated 
# Can one be added to this format?
df20 = pd.DataFrame([{'strucnum':'04','CS1':'40','Period':'03-31-2020'},
                   {'strucnum':'08','CS1':'24','Period':'06-30-2020'},
                   {'strucnum':'09','CS1':'53','Period':'09-30-2020'},
                   {'strucnum':'11','CS1':'48','Period':'12-31-2020'}])

datatypePeriod = df17.dtypes

df17.plot('Period', 'CS1')


dfScatter_strucnum['Period'] = pd.to_datetime(dfScatter_strucnum['Period'])

dfScatter_strucnum = dfScatter_strucnum.astype({"strucnum": 'int32', "CS1": 'int32'})

dfScatter_strucnum.sort_values(by=['strucnum'])



# dfScatter_CSX is the dataframe that is meant to order the chronology of the observations on the x-axis by condition state (CSX, meaning the value of the condition state i.e. CS1, CS2 etc.) increasing from lowest to highest condition state value.  
dfScatter_CSX = pd.DataFrame([{'strucnum':'04','CS1':'14','Period':'03-31-2017'},
                   {'strucnum':'08','CS1':'9','Period':'06-30-2017'},
                   {'strucnum':'09','CS1':'21','Period':'09-30-2017'},
                   {'strucnum':'11','CS1':'44','Period':'12-31-2017'}])

dfScatter_strucnum.plot('Period', 'CS1')

plt.scatter(dfScatter_strucnum.Period, dfScatter_strucnum.strucnum.CS1)



#!!! 

# delete below:
    
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

# print("Non-match elements: ", non_match1)

#!!!

list_func = lambda x, y: list((set(x)- set(y))) + list((set(y)- set(x)))


intersection_17_18 = set(b_17).intersection(b_18)

intersection_18_17 = set(b_18).intersection(b_17)

intersection_17_18 == intersection_18_17 # returns true

intersection_17_19 = set(b_17).intersection(b_19)

intersection_19_17 = set(b_19).intersection(b_17)

intersection_17_19 == intersection_19_17 # returns true


# var = some_function()

# Checking whether List 1 value present in List2 and List 3
for l1 in List1:  
    if l1 in List2: 
        List2.remove(l1)  
        if l1 in List3: 
            List3.remove(l1)  
            print(l1," ",l1," ",l1)  
        else:  
            print(l1," ",l1," ","NA")  
    else:
        if l1 in List3:   
            List3.remove(l1)
            print(l1," ","NA"," ",l1)
        else:
            print(l1," ","NA"," ","NA")

# Checking whether List 2 value present in List3
for l2 in List2:
    if l2 in List3:
        List3.remove(l2)
        print("NA"," ",l2," ",l2)
    else:
        print("NA"," ",l2," ","NA")

# Checking for values present only in List 3

for l3 in List3:
    print("NA","NA",l3)


# Reset of what I'm trying to do: Get the strucnum common across all 4 years of data- 
# then select all the rows in all 4 years that correspond to the common strucnum
# make individual dataframes out of each year consisting of only the set of strucnum common across all 4 years
# concatenate the 4 years one after the next (i.e. 2017 on top of 2018 on top of 2019 on top of 2020)
# once that concatenation is done select rows from the concatenated dataframe on the key of EN (element number)
# Split all those EN with their corresponding CS1 - CS4 into individual dataframes
# Convert the CS numbers into "rates" of change in CS (condition state, i.e. CS 2018 - CS 2017, so I may have only 3 graphs)
# Use the individual dataframes of each element (EN) to make graphs
# Review the graphs for possible trends in the data, and can the data look like it fits your hypothesis ()
# Adjust the arrangement of the strucnum in time (i.e. come up with the order in time to make each observation occur as may help to make the graphs and data fit the predictions
# 

# Sets are what needs conversion

# len() returns the size of the first dimension, so arrays are no. of columns x no. of rows

a_1d = np.arange(3)
print(a_1d)
# [0 1 2]
print(a_1d.ndim)
print(type(a_1d.ndim))


a_2d = np.arange(12).reshape((3, 4))
print(a_2d)
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]]
print(a_2d.ndim)


a_3d = np.arange(24).reshape((2, 3, 4))
print(a_3d)
print(a_3d.ndim)

# [[[ 0  1  2  3]
#   [ 4  5  6  7]
#   [ 8  9 10 11]]
# 
#  [[12 13 14 15]
#   [16 17 18 19]
#   [20 21 22 23]]]