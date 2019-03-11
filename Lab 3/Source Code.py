"""
CS2303 - Data Structures
Jesus A. Hernandez - 80629917
Lab#3 Binary Search Trees
Instructor - Dr. Olac Fuentes
TA - Anindita Nath & Maliheh Zargaran

See different methods for creating trees and how they work.
Last Modified on March 11, 2019
"""
import math
import queue
import random
import numpy as np
import matplotlib.pyplot as plt
 
class BST(object):
    # Constructor
    def __init__(self, item, left=None, right=None):  
        self.item = item
        self.left = left 
        self.right = right      
        
def Insert(T,newItem):
    if T == None:
        T =  BST(newItem)
    elif T.item > newItem:
        T.left = Insert(T.left,newItem)
    else:
        T.right = Insert(T.right,newItem)
    return T

def Delete(T,del_item):
    if T is not None:
        if del_item < T.item:
            T.left = Delete(T.left,del_item)
        elif del_item > T.item:
            T.right = Delete(T.right,del_item)
        else:  # del_item == T.item
            if T.left is None and T.right is None: # T is a leaf, just remove it
                T = None
            elif T.left is None: # T has one child, replace it by existing child
                T = T.right
            elif T.right is None:
                T = T.left    
            else: # T has two chldren. Replace T by its successor, delete successor
                m = Smallest(T.right)
                T.item = m.item
                T.right = Delete(T.right,m.item)
    return T
         
def InOrder(T):
    # Prints items in BST in ascending order
    if T is not None:
        InOrder(T.left)
        print(T.item,end = ' ')
        InOrder(T.right)
  
def InOrderD(T,space):
    # Prints items and structure of BST
    if T is not None:
        InOrderD(T.right,space+'   ')
        print(space,T.item)
        InOrderD(T.left,space+'   ')
  
def SmallestL(T):
    # Returns smallest item in BST. Returns None if T is None
    if T is None:
        return None
    while T.left is not None:
        T = T.left
    return T   
 
def Smallest(T):
    # Returns smallest item in BST. Error if T is None
    if T.left is None:
        return T
    else:
        return Smallest(T.left)

def Largest(T):
    if T.right is None:
        return T
    else:
        return Largest(T.right)   

def Find(T,k):
    # Returns the address of k in BST, or None if k is not in the tree
    if T is None or T.item == k:
        return T
    if T.item<k:
        return Find(T.right,k)
    return Find(T.left,k)
    
def FindAndPrint(T,k):
    f = Find(T,k)
    if f is not None:
        print(f.item,'found')
    else:
        print(k,'not found')

"""
Draw BST ---------------------------------------------------------------------
The method will first draw a circle if the current node isn't null, then put
the item of the node in the middle of the circle and check if the node has 
a left and right child. A left line will be ploted if there is a left child
and the same repeats for a right child.
"""
def circle(center,rad):
    n = int(4*rad*math.pi)
    t = np.linspace(0,6.3,n)
    x = center[0]+rad*np.sin(t)
    y = center[1]+rad*np.cos(t)
    return x,y

def DrawTree(T,ax_tree,vL,vR,center,rad,chg):
    if T == None:
        return
    
    newCenterL = vL[1] #New center for left child
    newCenterR = vR[1] #New center for right child
    
    x,y = circle(center,rad)
    ax_tree.plot(x,y,'k') #plot a circle in our current center
    ax_tree.fill(x,y,'k') #fill the circle in a black color
    #Output the current node item at the center of the circle in a white font
    ax_tree.text(center[0],center[1],T.item,color='w',
                 horizontalalignment='center',verticalalignment='center',
                 fontsize=10)
    
    if T.left != None: #check for left child and draw a line if it exists
        ax_tree.plot(vL[:,0],vL[:,1],color='k')
    if T.right != None: #check for right child and draw a line if it exists
        ax_tree.plot(vR[:,0],vR[:,1],color='k')
    
    #New vertices arrrays for left and right lines
    leftVL = np.copy(vL)*0
    leftVL[0] = vL[1]
    leftVL[1][0] = vL[1][0]-chg[1] #rate of change for x
    leftVL[1][1] = vL[1][1]-chg[0] #rate of change for y
    
    leftVR = np.copy(vL)*0
    leftVR[0] = vL[1]
    leftVR[1][0] = vL[1][0]+chg[1]
    leftVR[1][1] = vL[1][1]-chg[0]
    
    rightVL = np.copy(vR)*0
    rightVL[0] = vR[1]
    rightVL[1][0] = vR[1][0]-chg[1]
    rightVL[1][1] = vR[1][1]-chg[0]
    
    rightVR = np.copy(vR)*0
    rightVR[0] = vR[1]
    rightVR[1][0] = vR[1][0]+chg[1]
    rightVR[1][1] = vR[1][1]-chg[0]
    
    DrawTree(T.left,ax_tree,leftVL,leftVR,newCenterL,rad,[chg[0],chg[1]*.75])
    DrawTree(T.right,ax_tree,rightVL,rightVR,newCenterR,rad,[chg[0],chg[1]*.75])
    
"""
Iterative Search -------------------------------------------------------------
If the item is bigger than the root then check the left child else check the
right one. If at the end of the while loop the current node is null then the
item isn't in the list.
"""
def Search(T,k):
    if T is None:
        return None
    temp = T
    while temp != None:
        if temp.item == k:
            break
        if temp.item > k:
            temp = temp.left
        else:
            temp = temp.right
    if temp == None:
        print("Item not found in list.")
        return
    print("Item found in list.")
    return temp

"""
Sorted List to BST -----------------------------------------------------------
Divide the list by the middle, the middle point becomes the root of the tree.
Continue dividing each newly partitioned list in the same way.
"""
def listToBST(L):
    if not L:
        return None
    mid = int((len(L))/2)
    root = BST(L[mid])
    root.left = listToBST(L[:mid])
    root.right = listToBST(L[mid+1:])
    return root
    
"""
BST to List ------------------------------------------------------------------
Obtain the root node and add it to the list, repeat the same for the left and
right nodes
"""
def createList(T):
    if T == None:
        return []
    return createList(T.left) + [T.item] + createList(T.right)

"""
Print by Depth ---------------------------------------------------------------
Used a queue to perform a Breadth-first traversal, while the queue isn't empty
continue obtaining the different nodes for the Tree.
"""
def PrintD(T):
    q = queue.Queue()
    q.put(T)
    depth = 0
    while not q.empty():
        counter = q.qsize()
        print("\nKeys at depth ",depth,": ",end='')
        while counter > 0: #when the counter reaches 0 means a new depth
            n = q.get()
            print(n.item,end=' ')
            if n.left:
                q.put(n.left) #if there is a left node add it to the queue
            if n.right:
                q.put(n.right) #if there is a right node at it to the queue
            counter -= 1
        depth += 1
    print("\n")
      
"""
Test -------------------------------------------------------------------------
"""
center = [0,0]
fig_tree, ax_tree = plt.subplots()
fig_tree2, ax_tree2 = plt.subplots()
vL = np.array([[0,0],[-100,-100]])
vR = np.array([[0,0],[100,-100]])

#Generate a Tree from a randomly generated List
T = None
A = random.sample(range(1, 101), 8)
for i in A:
    T = Insert(T,i)
print("----Randomly generated list: \n",A)

#Iterative search apllied
s = int(input("----Choose value to find iteratively: "))
Search(T,s)

print("\n----Each depth keys: ",end='')
PrintD(T)

#Convert Binary Search Tree to List
print("----Returned sorted list from randomly created tree: \n", createList(T))

#Convert list to Binary Search Tree
input_string = input("----Enter sorted list, separating elements by a space: ")
L = input_string.split(" ")
L = list(map(int,L))
T2 = listToBST(L)

#Tree drawn from previous list, parameters are: Binary Tree, 
#axes for tree number 1, vertices for the left and right line, coordinates for
#center point, radius and the rate of change for the x and y axis for each
#new center
DrawTree(T2,ax_tree,vL,vR,center,20,[100,100/2])

#Tree drawn from randomly generated list
DrawTree(T,ax_tree2,vL,vR,center,20,[100,100/2])

ax_tree.set_aspect(1.0)
ax_tree2.set_aspect(1.0)
ax_tree.axis('off')
ax_tree2.axis('off')
plt.show()