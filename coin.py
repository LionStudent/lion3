#5:05p

amount = 5
choice = [1,2,5]

ways = 0

level = 1
maxLevel = amount // min(choice) 

def findways(amountLeft, choice, level):
    global ways
    assert level <= maxLevel, "%s %s" % (maxLevel, level)
    print("%s %s %s" % ("* "*level, amountLeft, choice))
    level +=1

    newChoice = choice[:]
    c = newChoice.pop()
    for i in range(1+amountLeft // c):
        newAmountLeft = amountLeft-i*c
        if newAmountLeft == 0:
            ways += 1
        elif newAmountLeft<0 or len(newChoice) == 0:
            pass
        else:
            findways(amountLeft-i*c, newChoice, level)

findways(amount, choice, level)
print(ways)

