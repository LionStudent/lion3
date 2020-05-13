import random

def swap(A, i1, i2):
    #print("i1: %s" % i1) 
    tmp = A[i1]
    A[i1] = A[i2]
    A[i2] = tmp

def partition(A, start, end):
    retval = start # gotcha!
    randomIdx = end # gotcha!

    for i in range(start, end):
        if i == randomIdx: continue # skip last index
        if A[i] < A[randomIdx]:
            swap(A, retval, i)
            retval += 1
    swap(A, retval, randomIdx)   
    #print(retval)     
    return retval

def quicksort(A, start, end):

    if end <= start:
        return
    index = partition(A, start, end)
    quicksort(A, start, index-1)
    quicksort(A, index+1, end)

l = [random.randrange(100) for x in range(10)]
s = l[:]
print(l)
quicksort(s, 0, len(s)-1)
print(s)