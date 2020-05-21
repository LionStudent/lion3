import random
import math

l = [random.randrange(100) for x in range(10)]
print(l)

def merge(a,b, level):
    print("Log: %s%s" % ("* "*level, (a,b)))
    m = []
    ai = 0
    bi = 0 
    while ai < len(a) and bi < len(b):
        if a[ai] < b[bi]:
            m.append(a[ai])
            ai+=1
        else:
            m.append(b[bi])
            bi+=1
    m = m + a[ai:] + b[bi:]
    return m

def mergesort(l, level, levelMax):
    # (4) monitor
    # (5) good!, print("Log: %s%s" % ("* "*level, l))
    # (3) block infinate recursion
    assert level <= levelMax, "%s <= %s" % (level, levelMax)
    level+=1

    # (2) based case based on input
    length = len(l)
    if length < 2:
        return l

    # (1) high level recursion
    sIdx = 0
    eIdx = length

    halfLen = length // 2
    halfIdx = sIdx+halfLen
    lt = l[sIdx:halfIdx]
    rt = l[halfIdx:eIdx]

    lt = mergesort(lt, level, levelMax)
    rt = mergesort(rt, level, levelMax)

    return merge(lt, rt, level)

# (3) block infinate recursion
levelMax = math.ceil(math.log(len(l), 2))

s = mergesort(l, 0, levelMax)
print(s)