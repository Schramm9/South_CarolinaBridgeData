# -*- coding: utf-8 -*-
"""
Created on Tue May 17 18:23:55 2022

@author: Chris
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dfCAN = pd.read_csv('Canadian_climate_history.csv')

dfCAN = dfCAN[['LOCAL_DATE', 'MEAN_TEMPERATURE_TORONTO']]

dfCAN['LOCAL_DATE'] = pd.to_datetime(dfCAN['LOCAL_DATE'])

dfCAN['YEAR'] = dfCAN['LOCAL_DATE'].dt.year