# 0 1 1 2 3 5 8 13 21

#f[n] = f[n-1] + f[n-2]


cache = {0:0,1:1}
def fib(num):
    retval = 0
    try:
        retval = cache[num]
    except:
        retval = fib(num-1) + fib(num-2)
        cache[num] = retval

    return retval


#print(fib(8))
print(fib(80))