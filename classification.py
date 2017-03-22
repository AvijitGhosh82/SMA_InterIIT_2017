#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 16:07:49 2017

@author: Avijit
"""

import graphlab
from graphlab import SFrame

import pandas

model_csv = pandas.read_csv('article_dataframe.csv', sep='\t', encoding='utf-8')

del model_csv['Unnamed: 0']
del model_csv['Unnamed: 0.1']


sf = SFrame(data=model_csv)
