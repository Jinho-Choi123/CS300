def lst_search(lst, ele): # assume lst contains ele.
    for i in range(len(lst)-1, -1, -1):
        if lst[i] == ele:
            return i 
            
def lst_slice(end_index, lst): #return lst[0...end_index]
    n = len(lst)
    if n-1 == end_index:
        return lst 
    else:
        return lst[:(end_index+1)]

def longest_common_sub(l1, l2):
    
    n1 = len(l1)
    n2 = len(l2)
    #subproblem[i][j]: l1[1..i], l2[1...j]에서의 longest common_sub.
    subproblem = [[]]
    
    #if one of l is empty, return []
    if n1==0 or n2 == 0:
        return 0, []
    
    
    #base case: subproblem [0][0]
    if l1[0] == l2[0]:
        subproblem[0].append([l1[0]])
    else:
        subproblem[0].append([])
    
    #recurrence relation:
        #subproblem[i][j] (when i>=0  and j>=0 where i!=0 and j!=0)
            #if j == 0 and lst2[0] in lst1[0...i] then [lst2[0]] else []
            #= subproblem[i][j-1] if j >1
            #= if lst2[j] in lst1[0...i] then let index of element in lst1 be cnt 
                # if cnt == 0 or j==0 then [lst2[j]]
                #else then subproblem[cnt-1][j-1]
            #= 
    for i in range(n1):
    
        if i!=0:
            subproblem.append([])
            
            
        for j in range(n2):
            if i==0 and j==0:
                continue
                
            if j==0 and l2[0] in lst_slice(i,l1):
                subseq1 = [l2[0]]
            elif j==0:
                subseq1 = []
            else:
                subseq1 = subproblem[i][j-1].copy()
            
            subseq2 = []
            if l2[j] in lst_slice(i, l1):
                cnt = lst_search(l1, l2[j])
                if cnt == 0 or j == 0:
                    subseq2 = [l2[j]]
                else:
                    subseq2 = subproblem[cnt-1][j-1].copy()
                    subseq2.append(l2[j])
            if len(subseq1)>len(subseq2):
                subproblem[i].append(subseq1)
            else:
                subproblem[i].append(subseq2)
    return len(subproblem[n1-1][n2-1]), subproblem[n1-1][n2-1]

print(longest_common_sub([4,1,2,3,4], [4,3,2,5]))