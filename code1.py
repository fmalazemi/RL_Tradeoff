def line(row, rowMax, col, colMax, N): 

    l = [] 

    for i in range(row, rowMax+1): 

        for j in range(col, colMax+1): 

            node = i*N + j 

            l.append(node) 

    return l 

 

def generateSingleLoop(r1, c1, r2, c2, N): 

    l = [] 

    l = l + line(r1, r1, c1, c2, N) 

    l = l + line(r1, r2, c2, c2, N)[1:] 

 

    r = line(r1, r2, c1, c1, N) 

    r = r + line(r2, r2, c1+1, c2, N) 

    r = r[1:len(r)-1] 

    l = l + r[::-1] 

    return l 

 

def generateLoops_reversedRotate(N, r1, c1, r2, c2, withoutD): 

    if r2-r1 == 1: 

        l1 = generateSingleLoop(r1, c1, r2, c2, N) 

        l2 = generateSingleLoop(r1, c1, r2, c2, N) 

        return [l1, l2[::-1]] 

    L = [] 

 

    L.append(generateSingleLoop(r1, c1, r2, c2, N)) 

    for i in range(r1+1, r2): 

        L.append(generateSingleLoop(r1, c1, i, c2, N)[::-1]) 

    for i in range(r1+1, r2): 

        L.append(generateSingleLoop(i, c1, r2, c2, N)[::-1]) 

 

    if r1 != 0 and withoutD: 

        return L 

    for i in range(c1, c2): 

        L.append(generateSingleLoop(r1, i, r2, i+1, N)[::-1]) 

    return L 

 

def generateLoops(N, r1, c1, r2, c2, withoutD): 

    if r2-r1 == 1: 

        l1 = generateSingleLoop(r1, c1, r2, c2, N) 

        l2 = generateSingleLoop(r1, c1, r2, c2, N) 

        return [l1, l2[::-1]] 

    L = [] 

 

    tmp = generateSingleLoop(r1, c1, r2, c2, N) 

    L.append(tmp[::-1]) 

    for i in range(c1+1, c2): 

        L.append(generateSingleLoop(r1, c1, r2, i, N)) 

    for i in range(c1+1, c2): 

        L.append(generateSingleLoop(r1, i, r2, c2, N)) 

 

    if withoutD and r1 != 0: 

        return L 

    for i in range(r1, r2): 

        L.append(generateSingleLoop(i, c1, i+1, c2, N)) 

    return L 

 

def calcHopCount(N, loopSet): 

    D = [[ N*N*N for x in range(N*N)] for x in range(N*N)] 

    for l in loopSet:  

        for i in range(len(l)): 

            d = 0 

            for j in range(len(l)): 

                j = (i+j)%len(l) 

                D[l[i]][l[j]] = min(d, D[l[i]][l[j]]) 

                d += 1 

 

    s = 0.0 

    for i in D: 

        s += sum(i) 

 

    for i in D: 

        for j in i: 

            if j == N*N*N: 

                print("\nERROR: Not Complete interconnection.") 

                assert False  

    return s/(N**4-N**2) 

 

def calcNumLinks(L): 

    s = 0 

    for i in L: 

        s += len(i) 

    return s 

 

def calcOverlappingCap(L, N): 

    D = [[ 0 for x in range(N*N)] for x in range(N*N)] 

    max_overlapping = 0 

 

    for loop in L: 

        for j in range(len(loop)): 

            k = (j+1)%len(loop) 

            D[loop[j]][loop[k]] += 1 

            D[loop[k]][loop[j]] += 1 

            max_overlapping = max(max_overlapping, D[loop[j]][loop[k]]) 

    return max_overlapping 

 

def calcNumLoopInNode(L, N): 

    D = [0 for x in  range(N*N)] 

    max_intersection = 0 

    for loop in L: 

        for i in loop: 

            D[i] += 1 

            max_intersection = max(max_intersection, D[i]) 

    return max_intersection 

 

def printLinkCounts(L, N): 

    print("id - N  E  S  W") 

    print("---------------") 

    D = [[ 0 for x in range(4)] for x in range(N*N)] 

    for loop in L: 

        for i in range(len(loop)): 

            j = (i+1)%len(loop) 

            D[loop[i]][linkDirection(loop[i], loop[j], N)] += 1 

            D[loop[j]][linkDirection(loop[j], loop[i], N)] += 1 

 

    for i in range(N*N): 

        print(i, "|", D[i], sum(D[i])/2.0) 

 

def linkDirection(i, j, N): 

    if i-j == 1: 

        return 3 # W 

    elif i-j == -1: 

        return 1 # E 

    elif i-j == N: 

        return 0 # N 

    elif i-j == -N: 

        return 2 # S 

    else: 

        assert False and "WRONG" 

 

    return -1 

 

N = 4

r1 = 0 

c1 = 0 

r2 = N-1 

c2 = N-1 

 

L = [] 

f = False 

withoutD = True 

while r1 < r2 and c1 < c2: 

    if f: 

        l = generateLoops_reversedRotate(N, r1, c1, r2, c2, withoutD) 

    else: 

        l = generateLoops(N, r1, c1, r2, c2, withoutD) 

    f = not f 

    L = L + l 

    r1 += 1 

    c1 += 1 

    r2 -= 1 

    c2 -= 1 

 

for r1 in range(0, N-1): 

    for c1 in range(0, N-1): 

        temp = generateSingleLoop(r1, c1, r1+1, c1+1, N) 

 

print(N, "X", N) 

print("Total number of Loops =", len(L)) 

print("Average Hop Count =", calcHopCount(N, L)) 

print("Total number of Links =", calcNumLinks(L)) 

print("Overlapping-Cap =", calcOverlappingCap(L, N)) 

print("Maximum loops in a Node =", calcNumLoopInNode(L, N)) 
for i in L:
    print(i)
print(len(L))    
    
    
    
    
    
