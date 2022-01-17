# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 12:35:42 2022

@author: Chris
"""

import pandas as pd

d1 = pd.DataFrame(dict(A=.1, B=.2, C=.3), [2, 3])
d2 = pd.DataFrame(dict(B=.4, C=.5, D=.6), [1, 2])
d3 = pd.DataFrame(dict(A=.7, B=.8, D=.9), [1, 3])