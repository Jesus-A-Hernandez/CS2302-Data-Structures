"""
CS2303 - Data Structures
Jesus A. Hernandez - 80629917
Lab#4 B-Trees
Instructor - Dr. Olac Fuentes
TA - Anindita Nath & Maliheh Zargaran

Solve a variety of problems involving B-Trees to better understand their
functioning.
Last Modified on March 24, 2019
"""
import math

class BTree(object):
    # Constructor
    def __init__(self,item=[],child=[],isLeaf=True,max_items=5):  
        self.item = item
        self.child = child 
        self.isLeaf = isLeaf
        if max_items <3: #max_items must be odd and greater or equal to 3
            max_items = 3
        if max_items%2 == 0: #max_items must be odd and greater or equal to 3
            max_items +=1
        self.max_items = max_items

def FindChild(T,k):
    # Determines value of c, such that k must be in subtree T.child[c], if k is in the BTree    
    for i in range(len(T.item)):
        if k < T.item[i]:
            return i
    return len(T.item)
             
def InsertInternal(T,i):
    # T cannot be Full
    if T.isLeaf:
        InsertLeaf(T,i)
    else:
        k = FindChild(T,i)   
        if IsFull(T.child[k]):
            m, l, r = Split(T.child[k])
            T.item.insert(k,m) 
            T.child[k] = l
            T.child.insert(k+1,r) 
            k = FindChild(T,i)  
        InsertInternal(T.child[k],i)   
            
def Split(T):
    #print('Splitting')
    #PrintNode(T)
    mid = T.max_items//2
    if T.isLeaf:
        leftChild = BTree(T.item[:mid]) 
        rightChild = BTree(T.item[mid+1:]) 
    else:
        leftChild = BTree(T.item[:mid],T.child[:mid+1],T.isLeaf) 
        rightChild = BTree(T.item[mid+1:],T.child[mid+1:],T.isLeaf) 
    return T.item[mid], leftChild,  rightChild   
      
def InsertLeaf(T,i):
    T.item.append(i)  
    T.item.sort()

def IsFull(T):
    return len(T.item) >= T.max_items

def Insert(T,i):
    if not IsFull(T):
        InsertInternal(T,i)
    else:
        m, l, r = Split(T)
        T.item =[m]
        T.child = [l,r]
        T.isLeaf = False
        k = FindChild(T,i)  
        InsertInternal(T.child[k],i)   
        
def Search(T,k):
    # Returns node where k is, or None if k is not in the tree
    if k in T.item:
        return T
    if T.isLeaf:
        return None
    return Search(T.child[FindChild(T,k)],k)
                  
def Print(T):
    # Prints items in tree in ascending order
    if T.isLeaf:
        for t in T.item:
            print(t,end=' ')
    else:
        for i in range(len(T.item)):
            Print(T.child[i])
            print(T.item[i],end=' ')
        Print(T.child[len(T.item)])    
 
def PrintD(T,space):
    # Prints items and structure of B-tree
    if T.isLeaf:
        for i in range(len(T.item)-1,-1,-1):
            print(space,T.item[i])
    else:
        PrintD(T.child[len(T.item)],space+'   ')  
        for i in range(len(T.item)-1,-1,-1):
            print(space,T.item[i])
            PrintD(T.child[i],space+'   ')
    
def SearchAndPrint(T,k):
    node = Search(T,k)
    if node is None:
        print(k,'not found')
    else:
        print(k,'found',end=' ')
        print('node contents:',node.item)

"""
Height ------------------------------------------------------------------------
Keep adding 1 after each recursive call until reaching a leaf node. All leaf
nodes of a B-Tree have the same height allowing us to just iterate over one
child.
"""
def height(T):
    if T.isLeaf:
        return 0
    return 1 + height(T.child[0])

"""
B-Tree to List ----------------------------------------------------------------
The same train of tought for a BST, the head is the center of the sorted list
and we just need to obtain the left side list and right side list. The childs 
at 0 are all smaller than the item at 0, then childs at 1 are smaller than 
the item at 1. Following this logic we just need to apply this rule when 
appending items to the sorted list and finally return this previous list
and append the child that is bigger than the last item.
"""
def Tree2List(T):
    if T.isLeaf:
        return T.item
    a = []
    for i in range(len(T.item)):
        a = a + (Tree2List(T.child[i])) 
        a.append(T.item[i]) #since the item is an integer we need to append it
    return a + Tree2List(T.child[-1])

"""
Return Minimum at Depth -------------------------------------------------------
Keep iterating in the child with the smallest items until d equals 0 and 
return the item at 0, if this check fails and the current node is a leaf then 
depth parameter was bigger than the tree's depth, return -1.
"""
def MinAtDepth(T,d):
    if d == 0:
        return T.item[0]
    if T.isLeaf:
        print("Chosen depth surpasses the tree's depth.")
        return -1
    return MinAtDepth(T.child[0], d-1) #T.child[0] carries the smallest items

"""
Return Maximum at Depth -------------------------------------------------------
Keep iterating in the child with the largest items until d equals 0 and 
return the item at -1, if this check fails and the current node is a leaf then 
depth parameter was bigger than the tree's depth, return -1.
"""
def MaxAtDepth(T,d):
    if d == 0:
        return T.item[-1]
    if T.isLeaf:
        print("Chosen depth surpasses the tree's depth.")
        return -1
    return MaxAtDepth(T.child[-1],d-1) #T.child[-1] carries the largest items

"""
Return Nodes at Depth ---------------------------------------------------------
Use a variable to store everytime d is 0 meaning we reached a node at a 
wanted depth. If this check fails and the current node is a leaf then this
means the depth parameter was bigger than the tree's depth, return infinite.
"""
def NodesAtDepth(T,d):
    counter = 0
    if d == 0:
        return 1 #Node at a wanted depth found
    if T.isLeaf:
        return math.inf
    for i in range(len(T.child)):
        counter += NodesAtDepth(T.child[i],d-1) #iterate over each child
    return counter

"""
Print Items at Depth ----------------------------------------------------------
If d is 0 then print the items in the current node, is this check fails and
the current node is a leaf then the depth parameter was bigger than the
tree's depth, return.
"""
def ItemsAtDepth(T,d):
    if d == 0: #Node found print items in it
        for i in range(len(T.item)):
            print(T.item[i],end=' ')
    if T.isLeaf:
        return
    for i in range(len(T.child)):
        ItemsAtDepth(T.child[i],d-1) #iterate over each child

"""
Full Nodes --------------------------------------------------------------------
If the length of the current node item list's equal to the max number of items
possible in a node then add 1 the counter variable. If this check fails and 
it is a leaf node means the leaf node wasn't full, return 0. When the for
loop ends return the counter variable.
"""
def FullNodes(T):
    counter = 0
    if len(T.item) == T.max_items:
        counter += 1 #don't return to check current node childs.
    if T.isLeaf:
        return counter
    for i in range(len(T.child)):
        counter += FullNodes(T.child[i])
    return counter

"""
Full Leafs --------------------------------------------------------------------
Same as the method before but this time check if it is a leaf and then check
if it is full or not. 
"""
def FullLeafs(T):
    counter = 0
    if T.isLeaf:
        if len(T.item) == T.max_items:    
            return 1
        else:
            return 0
    for i in range(len(T.child)):
        counter += FullLeafs(T.child[i])
    return counter

"""
Depth of Key ------------------------------------------------------------------
Check if the key item is bigger or smaller than the items in the current node
and enter the node in which the key could be located. Each time we enter a node
add 1 to the depth variable. If the key is in the current checked node then
return the depth variable. Lastly, check if the item is in the current leaf 
node, if it isn't then return -1
"""
def KeyDepth(T,k):
    depth = 0
    while T.isLeaf != True:
        if k in T.item:
            return depth
        if k > T.item[-1]:
            T = T.child[-1]
        elif k < T.item[0]: #kept getting an error when doing this inside loop
            T = T.child[0]
        else:
            for i in range(len(T.item)):
                if k < T.item[i]:
                    T = T.child[i]
        depth += 1
    if k in T.item:
        return depth
    print("Item not found.")
    return -1
"""
Main --------------------------------------------------------------------------
"""
L = [30, 50, 10, 20, 60, 70, 100, 40, 90, 80, 110, 120, 11, 1, 3, 4, 5, 105, 
     115, 200, 2, 45, 6, 7, 8, 12, 13, 14, 15, 21, 22, 23]
T = BTree()    
for i in L:
    Insert(T,i)
print("----Generated List:\n",L)

print("\n----Generated Tree:")
PrintD(T,'')

print("\n----Tree to Sorted List:\n",Tree2List(T))

depthMin = int(input("----Choose depth to find the smallest item: "))
print("Smallest item at depth",depthMin,":",MinAtDepth(T,depthMin))

depthMax = int(input("----Choose depth to find the largest item: "))
print("Largest item at depth",depthMax,":",MaxAtDepth(T,depthMax))

depthNodes = int(input("----Choose depth to find the number of nodes: "))
if NodesAtDepth(T,depthNodes) == math.inf:
    print("Chosen depth surpasses the tree's depth")
print("Nodes at depth",depthNodes,":",NodesAtDepth(T,depthNodes))

depthItems = int(input("----Choose depth to print the items found: "))
print("Items at depth",depthItems,": ",end='')
ItemsAtDepth(T,depthItems)

print("\n\n----Full nodes found:",FullNodes(T))

print("\n----Full leafs found:",FullLeafs(T))

key = int(input("----Choose key to find at a certain depth: "))
print("Key",key,"found at depth:",KeyDepth(T,key))