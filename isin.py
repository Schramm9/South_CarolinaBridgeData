# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 20:28:10 2022

@author: Chris
"""

import numpy as np

import pandas as pd

df = pd.DataFrame(
 [
  (73, 15, 55, 33, 'foo'),
  (63, 64, 11, 11, 'bar'),
  (56, 72, 57, 55, 'foo'),
 ],
 columns=['A', 'B', 'C', 'D', 'E'],
)




print(df)

#df.loc[df['B'].isin([64, 15])]

#filter_list = ['this','that','something else','another thing', ... ]
#new_df = df.loc[df['column'].isin(filter_list)]


#df17 = df.loc[df['B'].isin([64, 15])]

from collections import defaultdict
from copy import deepcopy
from operator import itemgetter



def srt(args):
    for ind, sub in enumerate(args, 1):
        sub.sort()
        yield ind, sub


list1 = ['one', 'three', 'four', 'six', 'seven', 'nine', 'zero']
list2 = ['two', 'four', 'five', 'six', 'eight', 'ten']
list3 = ['one', 'two', 'zero', 'three', 'seven']
list4 = ['four', 'five', 'six', 'eight', 'ten']
list5 = ['zero', 'one', 'three', 'four', 'seven', 'ten']
list6 = ['one', 'two']

l1l2 = len(set(list1).intersection(list2))


d = defaultdict(defaultdict)
orig = [list1, list2, list3, list4, list5, list6]

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