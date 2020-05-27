banned = [
(2,1),
(6,1),
(4,2),
(0,3),
(2,3),
(5,3),
(2,4),
(3,5),
(4,5),
(6,5),
(1,6),
(5,6),
]
for r in range(-1,8):
    for c in range(-1,8):
        if r in [-1,7] or c in [-1,7]:
            banned.append((c,r))

# 7x7 table
graph = {}
for r in range(7):
    for c in range(7):
        top = (r-1, c)
        bottom = (r+1, c)
        left = (r, c-1)
        right = (r, c+1)
        node = []
        for n in [top,bottom,left,right]:
            if n not in banned:
                node.append(n)
        graph[(r,c)] = node
        
visitted = {}

cache ={(6,6):0, (5,6):1, (6,5):1}
def paths(start, level):
    visitted[start] = True
    print("%s %s" % ("* "*level, start))
    #visitted[start] = True
    #assert level < 21, str(cache)

    level +=1
    retval = 0
    try:
        retval = cache[start]
    except:
        for n in graph[start]:
            if n not in visitted:
                retval += 1
                retval += paths(n, level)
    return retval 

#banned.sort()
#print(graph[(0,0)])
level = 1
print(paths((0,0), level))



'''

        if blocked[r][c]:
            pass
        else:
            node[r][c]
        
            board.append(0)
            '''