import random, math
from operator import add, mul, sub, div

codecA = {}
codecB = {}
chars = ((mul, '*'), (div, '/'), (add, '+'), (sub, '-'))

def formBit(num, place):
    form = '0' + str(place) + 'b'
    return format(num, form)

for i in range(1, 10):
    index = formBit(i, 4) 
    codecA[index] = i

for i, j in zip(range(10, 14), chars):
    index = formBit(i, 4)
    codecB[str(index)] = j

def generate(popNum, popList, solved, numOfBits):
    item = int(random.getrandbits(numOfBits))
    if popNum <= 0:
        return popList
    elif (item not in popList) and (item not in solved):
        popList.append(item)
        generate(popNum - 1, popList, solved, numOfBits)
    else:
        generate(popNum, popList, solved, numOfBits)

def calculate(byte, numOfBits):
    split = [byte[i: i + 4] for i in range(0, numOfBits, 4)]
    stack = []
    for i in split:
        if i in codecA:
            stack.append(int(i, 2))
        elif i in codecB and len(stack) >= 2:
            try:
                a, b = float(stack.pop()), float(stack.pop())
                stack.append(codecB[i][0](b, a))
            except:
                return -(9 ** 4)
        else:
            return -(9 ** 4)
    if len(stack) > 1:
        return -(9 ** 4)
    return stack[0]

def fitness(solution, targetNum):
    l = 0
    try:
        l = 1.0 / abs(targetNum - solution)
    except ZeroDivisionError:
        l = None
    return l

def cross(numA, numB, popList, numOfBits):
    chance = 1.0 / numOfBits
    isFound = False
    sent = 0
    while not isFound:
        if random.random() <= chance:
            index = int(sent % numOfBits)
            break
        sent += 1
    a, b = popList[numA], popList[numB]
    headA, headB = (a >> index) << index, (b >> index) << index
    bodyA, bodyB = headA ^ a, headB ^ b
    popList[numA], popList[numB] = headA | bodyB, headB | bodyA
    
def mutate(index, popList, numOfBits, mutRate):
    mut = 0
    for i in xrange(numOfBits):
        if random.random() <= mutRate:
            mut += 2 ** i
    popList[index] ^= mut

def fitCheck(target, total, i, pop, numOfBits, solutions, afterMut):
    fit = fitness(total, target)
    if fit == None:
        solutions.append((pop[i], afterMut))
        generate(1, pop, solutions, numOfBits)
        pop[i] = pop[-1]
        del pop[-1]
        print 'M'
        

def mutChance(mutRate, numOfBits):
    out = []
    for i in xrange(numOfBits):
        n = random.random()
        if n < mutRate:
            out.append(i)

def end(solutionList, codecA, codecB, numOfBits):
    last = []
    for i in solutionList:
        out = ''
        byte = formBit(i[0], numOfBits)
        split = [byte[j: j + 4] for j in range(0, numOfBits, 4)]
        for j in split:
            if j in codecA:
                out += str(codecA[j])
            elif j in codecB:
                out += codecB[j][1]
        final = (out, calculate(byte, numOfBits), byte)
        last.append(final)
        print final, i[1]
    return last

def endA(solutionList, codecA, codecB, numOfBits):
    for i in solutionList:
        byte = formBit(i, numOfBits)
        print byte, calculate(byte, numOfBits)
        
def main(popNum = 100, nums = 4, target = 24,\
         numOfSolution = 25, crossRate = .1, mutRate = .01\
         ):
    try:
        step = 0
        pop = []
        solutions = []
        numOfBits = 4 * (2 * nums - 1)
        generate(popNum, pop, solutions, numOfBits)
        while len(solutions) < numOfSolution:
            breed = []
            for i in xrange(len(pop)):
                step += 1
                byte = formBit(pop[i], numOfBits)
                total = calculate(byte, numOfBits)
                fitCheck(target, total, i, pop, numOfBits, solutions, False)
                mutate(i, pop, numOfBits, mutRate)
                byte = formBit(pop[i], numOfBits)
                total = calculate(byte, numOfBits)
                #something about indexes...
                fitCheck(target, total, i, pop, numOfBits, solutions, step)
                total = fitness(target, total)
                breedSelect = random.random()
                if breedSelect <= total:
                    breed.append(i)
            if len(breed) > 1 and len(breed) % 2 == 1:
                del breed[-1]
            elif len(breed) <= 1:
                continue
            random.shuffle(breed)
            breedA = breed[::2]
            breedB = breed[1::2]
            for k, l in zip(breedA, breedB):
                cross(k, l, pop, crossRate)
            
        end(solutions, codecA, codecB, numOfBits)
        return step
    except KeyboardInterrupt:
        end(solutions, codecA, codecB, numOfBits)
main()
""" Process:
    Fitness check
        if solution valid
            add to 'good' list
            generate new entry
    mutation check
    fitness check
    cross check
"""
