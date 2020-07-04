#function that makes list of subsequence that in index i, only lst[0,...,i] is used
def inc_sub(l):
    n = len(l)
    subproblem_subseq = [[l[0]]]
    for i in range(1, n):
        max_subseq = [l[i]]
        for j in range(0,i):
            if l[j]<l[i] and len(max_subseq)<len(subproblem_subseq[j])+1:
                max_subseq = subproblem_subseq[j].copy()
                max_subseq.append(l[i])
        subproblem_subseq.append(max_subseq)
    return subproblem_subseq

def longest_inc_sub(l):
    n = len(l)
    subproblem_subseq = inc_sub(l)
    #find the longest subseq 
    max_index = 0
    for i in range(0, n):
        if len(subproblem_subseq[max_index])<len(subproblem_subseq[i]):
            max_index = i
    return len(subproblem_subseq[max_index]), subproblem_subseq[max_index]

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
    #subproblem[i][j]: l1[1..i], l2[1...j]엝서의 longest common_sub.
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
                cnt = lst_search(lst_slice(i,l1), l2[j])
                print(cnt, j)
                if (cnt == 0) or (j == 0):
                    subseq2 = [l2[j]]
                else:
                    subseq2 = subproblem[cnt-1][j-1].copy()
                    subseq2.append(l2[j])
            if len(subseq1)>len(subseq2):
                subproblem[i].append(subseq1)
            else:
                subproblem[i].append(subseq2)
    return len(subproblem[n1-1][n2-1]), subproblem[n1-1][n2-1]



#---------------Problem Info-------------------#
# You are asked to arrange a party for a company. 
#There are identity numbers for the members in the company such that if there are n members, 
#each gets assigned an integer 0 ~ n. Of course, the identity number of the president is 0.

# Every employee has a supervisor and, obviously, the president does not have any. 
#One cannot have two different direct supervisors, hence the relation yields a tree 
#rooted at 0 (the president). The HR team evaluated performance rates for every member of the company, 
#even for the president.

# You need to arrange a year-end party for the company, decide whom to be invited. 
#To make the party a bit fun, you should not invite both an employee and her or his direct supervisor. 
#Also, you want to make the sum of the performance rates of those who get invited to be maximized.

# Implement arrange_party function where

# n is the number of members in the company,
# supervising is the 2-dimensional array where supervising[i] is the array of the identity numbers 
#that i do supervise, and p_rate is the array of floating-point numbers such that p_rate[i] 
#is the performance rate of i.
#--------------------------------------#


def depth_of_tree(lst):# the depth[i] is the depth of persom i in the supervisor tree #base case: president is depth of 0
    # other's depth will be changed. so don't matter # also returns maximum depth
    depth = [0]*len(lst)
    cnt = 0
    Q= [0]
    while len(Q) != 0:
        for person in Q:
            depth[person] = cnt 
        cnt = cnt+1
        newQue = []
        for person in Q:
            newQue.extend(lst[person])
        Q = newQue 
    return depth , (cnt-1)

def lst_of_child(i, lst):
    return lst[i]

def lst_of_grand_child(i,lst):
    lst_of_grand_child = []
    for child in lst_of_child(i,lst):
        lst_of_grand_child.extend(lst_of_child(child, lst))
    return lst_of_grand_child

def sum_of_p(lst, p_rate):
    sum = 0
    for i in lst:
        sum = sum + p_rate[i]
    return sum 

def arrange_party(n, supervising, p_rate):
    invitation = [[]]*n # invitation[i] is the max performace number list of member invited of tree root of i.
    depth, maxdepth = depth_of_tree(supervising)

    for dep in range(maxdepth, -1, -1): # sub is maxdepth-1, maxdepth-2, ..., 0 
        for i in range(n): #searching for person who's depth is dep
            if(depth[i] == dep):
                if(dep == maxdepth):
                    invitation[i] = [i]
                    continue
                invitation1 = []
                for k in lst_of_child(i, supervising):
                    invitation1.extend(invitation[k])

                invitation2 = []
                for k in lst_of_grand_child(i, supervising):
                    invitation2.extend(invitation[k])
                invitation2.append(i)
                if sum_of_p(invitation1, p_rate)> sum_of_p(invitation2, p_rate):
                    invitation[i] = invitation1 
                else:
                    invitation[i] = invitation2 
    result_p = sum_of_p(invitation[0], p_rate)
    result_lst = invitation[0].copy()
    result_lst.sort()
    return result_p, result_lst

print(arrange_party(5, [[3], [2], [4], [1], []], [15.0, 11.1, 5.5, 4.5, 2.0]))


def find_pair(lst1, lst2):
    #find the same element, and pair it.and return it 
    l1 = lst1.copy()
    l2 = lst2.copy()
    n1 = len(lst1)
    n2 = len(lst2)
    pair = []
    for i in range(n1):
        for j in range(n2):
            if l1[i] == l2[j]:
                pair.append([i, j])
    return pair

def max_length_list(lst): #lst is list of list / return max length list in lst 
    max = lst[0]
    for i in range(len(lst)):
        if len(max)<len(lst[i]):
            max = lst[i]
    return max 

def longest_common_inc_sub(l1, l2): # k is 
    pair_list = find_pair(l1, l2)
    pair_num = len(pair_list)
    subproblem = []
    #subproblem[i]: i?? ???? ??? ??? ?? common_inc subsequence  
    if pair_list == []:
        return []
    def val_pair(x): # x ?? ?? ? 
        return l1[pair_list[x][0]]
    #basecase: subproblem[0] = l1[pair_list[0][0]]
    subproblem.append([l1[pair_list[0][0]]])
    # subproblem is [ [?? ?? ??? ?? subsequence] ]
    for i in range(1, pair_num):
        subseq_list = [[val_pair(i)]]
        for j in range(i):
            if val_pair(j)<val_pair(i) and pair_list[j][0] < pair_list[i][0] and pair_list[j][1]<pair_list[i][1]:
                subseq = subproblem[j].copy()
                subseq.append(val_pair(i))
                subseq_list.append(subseq)
        #return max length list in subseq_list 
        subproblem.append(max_length_list(subseq_list))
    result = max_length_list(subproblem)
    length = len(result)
    return length, result

print(longest_common_inc_sub([1,42,3,2,1,5], [2,5,1,6,42,3,2,5]))