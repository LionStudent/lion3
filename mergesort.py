import random

def mergesort(array, start, end):
    if (end - start) > 1:
        half = (end - start) // 2
        left = mergesort(array, start, start+half)
        right = mergesort(array, start+half, end)
        return merge(left, right)
    else:
        return array[start:end]

def merge(left, right):
    retval = []
    idxLt = 0
    idxRt = 0
    i = 0
    while (idxLt < len(left) and idxRt < len(right)):
        if left[idxLt] < right[idxRt]:
            retval.append(left[idxLt])
            idxLt+=1
        else:
            retval.append(right[idxRt])
            idxRt+=1
        i += 1
    return retval + left[idxLt:] + right[idxRt:]

l = [random.randrange(100) for x in range(25)]
#s = l[:]
print(l)
s = mergesort(l, 0, len(l))
print(s)