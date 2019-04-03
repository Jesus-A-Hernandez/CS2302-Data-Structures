"""
CS2303 - Data Structures
Jesus A. Hernandez - 80629917
Lab#5 - Natural Language Processing
Instructor - Dr. Olac Fuentes
TA - Anindita Nath & Maliheh Zargaran

Find how natural language processing applications such as Siri work. Using
Binary Search Trees and Hash Tables to see their different running times when
being constructed and searching for items in them.
Last Modified on April 2, 2019
"""
import numpy as np
import string
import timeit
import statistics

"""
BTS ---------------------------------------------------------------------------
"""
class BST(object):
    # Constructor
    def __init__(self, item, left=None, right=None):  
        self.item = item
        self.left = left 
        self.right = right      
        
def Insert(T,newItem, itemVal): # Edited to receive string value as a parameter
    if T == None:
        T =  BST(newItem)
    # Compare val of item to be inserted against current node string val
    elif wordVal(T.item[0]) > itemVal:
        T.left = Insert(T.left,newItem,itemVal)
    else:
        T.right = Insert(T.right,newItem,itemVal)
    return T

def Find(T,k,kVal): # Edited to receive string value as a parameter
    # Returns the address of k in BST, or None if k is not in the tree
    if T is None or T.item[0] == k:
        if T == None:
            print(k,"not found in BST")
        return T
    # Compare val of item to be inserted against current node string val
    if wordVal(T.item[0]) < kVal:
        return Find(T.right,k,kVal)
    return Find(T.left,k,kVal)

def InOrderD(T,space):
    # Prints items and structure of BST
    if T is not None:
        InOrderD(T.right,space+'   ')
        print(space,T.item[0])
        InOrderD(T.left,space+'   ')

def Height(T): # Obtain Tree height
    if T is None: 
        return 0 ;  
    else : 
        lDepth = Height(T.left) 
        rDepth = Height(T.right) 
        if (lDepth > rDepth): 
            return lDepth+1
        else: 
            return rDepth+1

def wordVal(s): # Obtain an integer value for a given string
    val = 0
    y = 0
    for char in s:
        val += ord(char)*26**y
        y += 1
    return val

def numNodes(T): # Find number of nodes in the Tree
    if T is not None:
        count = 1
        if T.left is not None:
            count += numNodes(T.left)
        if T.right is not None:
            count += numNodes(T.right)
    return count

"""
Hash-Table --------------------------------------------------------------------
"""
class HashTableC(object):
    # Builds a hash table of size 'size'
    # Item is a list of (initially empty) lists
    # Constructor
    def __init__(self,size):  
        self.item = []
        self.num_items = 0 # Added num 
        for i in range(size):
            self.item.append([])
        
def InsertC(H,k):
    # Inserts k in appropriate bucket (list) 
    # Does nothing if k is already in the table
    b = h(k[0],len(H.item))
    H.num_items += 1
    H.item[b].append(k)
   
def FindC(H,k):
    # Returns bucket (b) and index (i) 
    # If k is not in table, i == -1
    b = h(k,len(H.item))
    for i in range(len(H.item[b])):
        if H.item[b][i][0] == k:
            return b, i
    print(k,"not found in hash table")
    return b, -1

def h(s,n):
    r = 0
    for c in s:
        r = (r*26+ord(c))%n
    return r

def reHash(H): # Duplicate table size + 1 and insert all items in new table
    n = len(H.item)
    n = (n*2)+1
    newH = HashTableC(n)
    for i in range(len(H.item)):
        for j in range(len(H.item[i])):
            InsertC(newH,H.item[i][j])
    return newH

def findEmpty(H): # Find number of empty slots in the hash table
    count = 0
    for i in range(len(H.item)):
        if len(H.item[i]) == 0:
            count += 1
    return count

def stdevSample(H): # Obtain list of different hash table lists sizes
    L = []
    for i in range(len(H.item)):
        L.append(len(H.item[i]))
    return L

"""
File to BST -------------------------------------------------------------------
Read the text file line by line, convert the string line into a list of strings
separating each element when a space is found. Insert the word of the string
into an item list and also the numpy array. Insert the item list into the BST.
"""
def File2BST():
    file = open("glove.6B.50d.txt", encoding='utf-8')
    BSTree = None
    for line in file:
        item = []
        line = line.strip('\n')
        lineList = line.split(" ") # Convert string into a list
        if lineList[0][0] in string.ascii_lowercase:        
            item.append(lineList.pop(0)) # Append the word to the list
            lineList = list(map(float,lineList)) # Convert string array into float array
            item.append(np.array(lineList)) # Append the embedding of the word
            BSTree = Insert(BSTree,item,wordVal(item[0])) # Insert list into tree
    return BSTree

"""
File to Hash-Table ------------------------------------------------------------
Same as with File to BST but this method instead inserts the item list into a 
hash table.
"""
def File2H(H):
    file = open("glove.6B.50d.txt", encoding='utf-8')
    for line in file:
        item = []
        line = line.strip('\n')
        lineList = line.split(" ")
        if lineList[0][0] in string.ascii_lowercase:        
            item.append(lineList.pop(0))
            lineList = list(map(float,lineList))
            item.append(np.array(lineList))
            InsertC(H,item)
            if H.num_items >= len(H.item): # If load factor becomes 1 double table size
                H = reHash(H)
    return H

"""
Similarity Check BST ----------------------------------------------------------
Obtain words to be looked up in BST. Search each node and traverse the BST 
depending on the value of each string.
"""
def Similarity(T):
    file = open("test.txt") # Words to be looked up
    for line in file:
        line = line.strip('\n')
        words = line.split(" ")
        similarity = CheckT(T,words[0],words[1]) # Call check method
        if similarity != None: # Check to see if word was not found
            print("Similarity",words,"=",similarity)

def CheckT(T,s1,s2):
    s1Node = Find(T,s1,wordVal(s1)) # Obtain node of frist word
    s2Node = Find(T,s2,wordVal(s2)) # Obtain node of second word
    if s1Node == None or s2Node == None: # Word was not found return None
        return
    product = np.dot(s1Node.item[1],s2Node.item[1])
    magnitude = np.linalg.norm(s1Node.item[1])*np.linalg.norm(s2Node.item[1])
    return round(product/(magnitude),4) # Return similarity rounded up

"""
Similarity Check Table --------------------------------------------------------
Obtain words to be looked up in hash table. Traverse the hash table depenging
on the value of each string.
"""
def SimilarityC(H):
    file = open("test.txt") # Words to be looked up
    for line in file:
        line = line.strip('\n')
        words = line.split(" ")
        similarity = CheckC(H,words[0],words[1])
        if similarity != None: # Check to see if word was not found
            print("Similarity",words,"=",similarity)

def CheckC(H,s1,s2):
    b1,p1 = FindC(H,s1) # Obtain bucket and position of first word
    b2,p2 = FindC(H,s2) # Obtain bucket and position of second word
    if p1 == -1 or p2 == -1: # Word was not found return None
        return
    s1Array = H.item[b1][p1][1] # Numpy array of first word
    s2Array = H.item[b2][p2][1] # Numpy array of second word
    product = np.dot(s1Array,s2Array)
    magnitude = np.linalg.norm(s1Array)*np.linalg.norm(s2Array)
    return round((product/magnitude),4)

"""
Main --------------------------------------------------------------------------
"""
print("Choose table implementation")
print("Type 1 for binary search tree or 2 for hash table with chaining",end='')
choice = 0
while 1: # Continue until 1 or 2 is input
    try:
        choice = int(input("Choice: "))
        if choice == 1 or choice == 2: 
            break
        else:
            print("Choose 1 or 2")
    except:
        print("Choose 1 or 2")

if choice == 1:
    print("\nBuilding BST")
    start_time = timeit.default_timer()
    BSTree = File2BST()
    end_time = timeit.default_timer()
    print("\nBST stats:")
    print("Number of nodes:",numNodes(BSTree))
    print("Height:",Height(BSTree))
    print("Running time for BST construction:",round((end_time - start_time),4))
    print("\nWord similarities found:")
    start_time = timeit.default_timer()
    Similarity(BSTree)
    end_time = timeit.default_timer()
    print("\nRunning time for BST query processing:",round((end_time - start_time),4))
    
if choice == 2:
    initialSize = 3
    H = HashTableC(initialSize)
    print("\nBuilding hash table with chaining")
    start_time = timeit.default_timer()
    H = File2H(H)
    end_time = timeit.default_timer()
    print("\nHash table stats:")
    print("Initial table size:",initialSize)
    print("Final table size:",len(H.item))
    print("Load factor:",round((H.num_items/len(H.item)),4))
    empty = findEmpty(H)
    print("Percentage of empty lists:",round(((empty*100)/len(H.item)),4))
    sample = stdevSample(H)
    print("Standard deviation of the lengths of the lists:",round(statistics.stdev(sample),4))
    print("Time to build hash table:", end_time - start_time)
    print("\nWord similarities found:")
    start_time = timeit.default_timer()
    SimilarityC(H)
    end_time = timeit.default_timer()
    print("\nRunning time for hash table query processing:",round((end_time - start_time),4))