# @Author: Edmund Lam <edl>
# @Date:   15:30:36, 12-Aug-2018
# @Filename: utils.py
# @Last modified by:   edl
# @Last modified time: 23:32:25, 10-Oct-2019


import itertools
from random import shuffle
from collections import OrderedDict

def group(lst, n):
  return list(zip(*[itertools.islice(lst, i, None, n) for i in range(n)]))

def chunkify(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

def isint(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def list2int(l):
    #convert all intable strings in list to int
    return list(map(lambda x:int(x) if isint(x) else x, l))
