# @Author: Edmund Lam <edl>
# @Date:   15:30:36, 12-Aug-2018
# @Filename: utils.py
# @Last modified by:   edl
# @Last modified time: 20:15:05, 11-Oct-2019


import itertools
from random import shuffle
from collections import OrderedDict

colours = {
'red':0xd32323,
'purple':0x9542f4
}

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

#from https://stackoverflow.com/questions/35517051/split-a-list-of-numbers-into-n-chunks-such-that-the-chunks-have-close-to-equal
#partitions list into k chunks such that the sum of each chunk is as close as possible
def partition_list(a, k):
    if k <= 1: return [a]
    if k >= len(a): return [[x] for x in a]
    partition_between = [round((i+1)*len(a)/k) for i in range(k-1)]
    average_height = float(sum(a))/k
    best_score = None
    best_partitions = None
    count = 0

    while True:
        starts = [0]+partition_between
        ends = partition_between+[len(a)]
        partitions = [a[starts[i]:ends[i]] for i in range(k)]
        heights = list(map(sum, partitions))

        abs_height_diffs = list(map(lambda x: abs(average_height - x), heights))
        worst_partition_index = abs_height_diffs.index(max(abs_height_diffs))
        worst_height_diff = average_height - heights[worst_partition_index]

        if best_score is None or abs(worst_height_diff) < best_score:
            best_score = abs(worst_height_diff)
            best_partitions = partitions
            no_improvements_count = 0
        else:
            no_improvements_count += 1

        if worst_height_diff == 0 or no_improvements_count > 5 or count > 100:
            return best_partitions
        count += 1

        move = -1 if worst_height_diff < 0 else 1
        bound_to_move = 0 if worst_partition_index == 0\
                        else k-2 if worst_partition_index == k-1\
                        else worst_partition_index-1 if (worst_height_diff < 0) ^ (heights[worst_partition_index-1] > heights[worst_partition_index+1])\
                        else worst_partition_index
        direction = -1 if bound_to_move < worst_partition_index else 1
        partition_between[bound_to_move] += move * direction
