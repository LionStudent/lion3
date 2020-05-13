import random

l = [random.randrange(100) for x in range(10)]
s = l[:]

def partition(A, start, end):
    retval = -1
    return retval

def quicksort(A, start, end):
    index = partition(A, start, end)
    quicksort(A, start, index-1)
    quicksort(A, index+1, end)