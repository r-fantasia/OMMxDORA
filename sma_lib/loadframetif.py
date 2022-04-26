# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 15:26:29 2021

@author: rfantasia
"""

import numpy as np 
from PIL import Image

def load_tif(fileptr,frnum):
    fileptr.seek(frnum)
    frame=np.array(fileptr)
    return frame