# IGM utility functions
# 
# author: Nan Hua
from __future__ import division, print_function

import os


def MakeRealPath(path):
    if not os.path.exists(path):
        os.makedirs(path)
    
    return os.path.realpath(os.path.abspath(path))