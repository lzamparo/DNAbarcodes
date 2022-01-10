#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 16:49:58 2022

@author: weiqiyao
"""

#!/usr/bin/env python
# coding: utf-8

# In[21]:

from collections import defaultdict

import pandas as pd
import matplotlib.pyplot as plt

import os
import re
import Bio.SeqIO as SeqIO


THIS_MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
#print(THIS_MODULE_PATH)

###############################################################################
# Paths
###############################################################################

BC = re.compile(
    'T[ACTG]{2}T[ACTG]{3}A[ACTG]{2}T[ACTG]{3}A[ACTG]{2}A')
