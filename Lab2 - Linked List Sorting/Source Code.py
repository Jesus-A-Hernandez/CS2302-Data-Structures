"""
CS2303 - Data Structures
Jesus A. Hernandez - 80629917
Lab#2 List Sorting
Instructor - Dr. Olac Fuentes
TA - Anindita Nath & Maliheh Zargaran

Sort Linked Lists using different methods to better understand their
functioning, such as use of pointers and pass by references.
Last Modified on February 24, 2019
"""
import random
"""
Node Functions----------------------------------------------------------------
"""
class Node(object):
    # Constructor
    def __init__(self, item, next=None):  
        self.item = item
        self.next = next 
        
def PrintNodes(N):
    if N != None:
        print(N.item, end=' ')
        PrintNodes(N.next)
        
def PrintNodesReverse(N):
    if N != None:
        PrintNodesReverse(N.next)
        print(N.item, end=' ')

"""        
List Functions----------------------------------------------------------------
"""
class List(object):   
    # Constructor
    def __init__(self): 
        self.head = None
        self.tail = None
        
def IsEmpty(L):  
    return L.head == None     
        
def Append(L,x): 
    # Inserts x at end of list L
    if IsEmpty(L):
        L.head = Node(x)
        L.tail = L.head
    else:
        L.tail.next = Node(x)
        L.tail = L.tail.next
        
def Print(L):
    # Prints list L's items in order using a loop
    temp = L.head
    while temp is not None:
        print(temp.item, end=' ')
        temp = temp.next
    print()  # New line 

def PrintRec(L):
    # Prints list L's items in order using recursion
    PrintNodes(L.head)
    print() 
    
def Remove(L,x):
    # Removes x from list L
    # It does nothing if x is not in L
    if L.head == None:
        return
    if L.head.item == x:
        if L.head == L.tail: # x is the only element in list
            L.head = None
            L.tail = None
        else:
            L.head = L.head.next
    else:
         # Find x
         temp = L.head
         while temp.next != None and temp.next.item != x:
             temp = temp.next
         if temp.next != None: # x was found
             if temp.next == L.tail: # x is the last node
                 L.tail = temp
                 L.tail.next = None
             else:
                 temp.next = temp.next.next
         
def PrintReverse(L):
    # Prints list L's items in reverse order
    PrintNodesReverse(L.head)
    print()     

"""
Bubble Sort------------------------------------------------------------------
Keep swaping objects until there is no swap,
meaning the list is already sorted
"""
def bubbleSort(L):
    if L.head == None or L.head == L.tail:
        return
    else:
        swaps = True
        while swaps == True:
            swaps = False
            temp = L.head
            while temp.next != None:
                if temp.item > temp.next.item:
                    token = temp.item
                    temp.item = temp.next.item
                    temp.next.item = token
                    swaps = True
                temp = temp.next

"""
Merge Sort------------------------------------------------------------------
Break the list in the half and continue breaking each new list until we have
a single noded list, then unite this lists in their correct position
"""
def mergeSort(L): #Split the lists and unite them
    if L.head == None or L.head.next == None:
        return L.head
    else:
        left, right = partition(L)
    
    return mergeLists(mergeSort(left), mergeSort(right))
    
def partition(L): #Split the lists
    left = List()
    right = List()
    
    if L.head == None or L.head.next == None:
        left = L
        right = None
        return left, right
    else:
        slow = L.head
        fast = L.head.next
        while fast != None:
            fast = fast.next
            if fast != None:
                fast = fast.next
                slow = slow.next
        
        left = L
        right.head = slow.next
        slow.next = None
        
        return left, right
        
def mergeLists(left, right): #Unite the lists
    temp = List()
    
    if left == None:
        return right
    elif right == None:
        return left
    
    if left.item <= right.item:
        temp = left
        temp.next = mergeLists(left.next, right)
    else:
        temp = right
        temp.next = mergeLists(left,right.next)
    
    return temp

"""
Quick Sort------------------------------------------------------------------- 
Obtain a pivot point for the list then split the list based on this pivot
point, repeat the same for each new list and then list will be sorted
"""
def quickSort(head):
    #Base Case
    if head == None or head.next == None:
        return head
    
    #Chose first element as pivot and move all elements smaller than the 
    #pivot at the end of LL.
    partitionPoint = split(head)
    
    #The elements to the left of pivot were all large , so they go
    #in right partition
    rightPartition = partitionPoint.next
    
    #The elements to the right of pivot were all smaller than pivot 
    #after partioned
    leftPartition = head
    partitionPoint.next = None
    
    #Edge cases
    if rightPartition == None:
        rightPartition = head
        leftPartition = head.next
        head.next = None
    
    leftPartition = quickSort(leftPartition)
    rightPartition = quickSort(rightPartition)
    
    #Now Recursively Sort
    iterator = rightPartition
    while iterator.next != None:
        iterator = iterator.next
    iterator.next = leftPartition
    
    temp = rightPartition
    while temp.next != None:
        if temp.item <= temp.next.item:
            temp = temp.next
        else:
            quickSort(rightPartition)

    return rightPartition

def split(head):
    if head.next.next == None:
        if head.next.item > head.item:
            return head.next
        else:
            return head
    else:
        i = head.next
        pivot = head
        lastSwap = Node(1)
        if pivot.next.item >= pivot.item:
            lastSwap = pivot.next
        else:
            lastSwap = pivot
            
        while i != None and i.next != None:
            if i.next.item >= pivot.item:
                if i.next == lastSwap.next:
                    lastSwap = lastSwap.next
                else:
                    temp = lastSwap.next
                    lastSwap.next = i.next
                    i.next = i.next.next
                    lastSwap = lastSwap.next
                    lastSwap.next = temp
            
            i = i.next
        
        return lastSwap

"""
Main -------------------------------------------------------------------------
"""
#User Interface
while True:
    try:
        n = int(input('Enter the length of random number list (0-8): '))
        if n > 8 or n < 0:
            print("--Length must be between 0 and 8")
            continue
        else:
            break
    except:
        print("--Length must be a number")
        continue
    break

#Create the List following user constrains
L = List()
for i in range(n):
    Append(L, random.randint(1,101))
print("List: ", end='')
Print(L)

#User Interface
print("\n1. Bubble Sort \n2. Merge Sort \n3. Quick Sort")
n = int(input("Method to use: "))
if n == 1:
    bubbleSort(L)
if n == 2:
    mergeSort(L)
if n == 3:
    L.head = quickSort(L.head)
print("Sorted List: ", end='')
Print(L)