"""
CS2303 - Data Structures
Jesus A. Hernandez - 80629917
Lab#6 Disjointed Set Forests
Instructor - Dr. Olac Fuentes
TA - Anindita Nath & Maliheh Zargaran
Last Modified on April 15, 2019
"""
from scipy import interpolate 
import matplotlib.pyplot as plt
import numpy as np
import random
import time

"""
Disjoint Set Forest -----------------------------------------------------------
"""
def DisjointSetForest(size):
    return np.zeros(size,dtype=np.int)-1
    
        
def dsfToSetList(S):
    #Returns aa list containing the sets encoded in S
    sets = [ [] for i in range(len(S)) ]
    for i in range(len(S)):
        sets[find(S,i)].append(i)
    sets = [x for x in sets if x != []]
    return sets

def find(S,i):
    # Returns root of tree that i belongs to
    if S[i]<0:
        return i
    return find(S,S[i])

def find_c(S,i): #Find with path compression 
    if S[i]<0: 
        return i
    r = find_c(S,S[i]) 
    S[i] = r 
    return r
    
def union(S,i,j):
    # Joins i's tree and j's tree, if they are different
    ri = find(S,i) 
    rj = find(S,j)
    if ri!=rj:
        S[rj] = ri
 

def union_c(S,i,j):
    # Joins i's tree and j's tree, if they are different
    # Uses path compression
    ri = find_c(S,i) 
    rj = find_c(S,j)
    if ri!=rj:
        S[rj] = ri

         
def union_by_size(S,i,j):
    # if i is a root, S[i] = -number of elements in tree (set)
    # Makes root of smaller tree point to root of larger tree 
    # Uses path compression
    ri = find_c(S,i) 
    rj = find_c(S,j)
    if ri!=rj:
        if S[ri]>S[rj]: # j's tree is larger
            S[rj] += S[ri]
            S[ri] = rj
        else:
            S[ri] += S[rj]
            S[rj] = ri

        
def draw_dsf(S):
    scale = 30
    fig, ax = plt.subplots()
    for i in range(len(S)):
        if S[i]<0: # i is a root
            ax.plot([i*scale,i*scale],[0,scale],linewidth=1,color='k')
            ax.plot([i*scale-1,i*scale,i*scale+1],[scale-2,scale,scale-2],linewidth=1,color='k')
        else:
            x = np.linspace(i*scale,S[i]*scale)
            x0 = np.linspace(i*scale,S[i]*scale,num=5)
            diff = np.abs(S[i]-i)
            if diff == 1: #i and S[i] are neighbors; draw straight line
                y0 = [0,0,0,0,0]
            else:      #i and S[i] are not neighbors; draw arc
                y0 = [0,-6*diff,-8*diff,-6*diff,0]
            f = interpolate.interp1d(x0, y0, kind='cubic')
            y = f(x)
            ax.plot(x,y,linewidth=1,color='k')
            ax.plot([x0[2]+2*np.sign(i-S[i]),x0[2],x0[2]+2*np.sign(i-S[i])],[y0[2]-1,y0[2],y0[2]+1],linewidth=1,color='k')
        ax.text(i*scale,0, str(i), size=20,ha="center", va="center",
         bbox=dict(facecolor='w',boxstyle="circle"))
    ax.axis('off') 
    ax.set_aspect(1.0)

def num_of_sets(S): #return number of roots in dsf (-1s)
    num = 0
    for i in range(len(S)):
        if S[i] < 0:
            num += 1
    return num

"""
Maze Functions ----------------------------------------------------------------
"""
def draw_maze(walls,maze_rows,maze_cols,cell_nums=False):
    fig, ax = plt.subplots()
    for w in walls:
        if w[1]-w[0] ==1: # Vertical Wall position
            x0 = (w[1]%maze_cols)
            x1 = x0
            y0 = (w[1]//maze_cols)
            y1 = y0+1
        else: # Horizontal Wall postion
            x0 = (w[0]%maze_cols)
            x1 = x0+1
            y0 = (w[1]//maze_cols)
            y1 = y0  
        ax.plot([x0,x1],[y0,y1],linewidth=1,color='k')
    sx = maze_cols
    sy = maze_rows
    ax.plot([0,0,sx,sx,0],[0,sy,sy,0,0],linewidth=2,color='k')
    if cell_nums:
        for r in range(maze_rows):
            for c in range(maze_cols):
                cell = c + r*maze_cols   
                ax.text((c+.5),(r+.5), str(cell), size=10,
                        ha="center", va="center")
    ax.axis('off') 
    ax.set_aspect(1.0)

# Creates a list with all the walls in the maze
def wall_list(maze_rows, maze_cols):
    w =[]
    for r in range(maze_rows):
        for c in range(maze_cols):
            cell = c + r*maze_cols
            if c!=maze_cols-1: # If not last column
                w.append([cell,cell+1]) # wall between adjacent columns
            if r!=maze_rows-1: #if not last row
                w.append([cell,cell+maze_cols]) # wall between adjacent rows
    return w

def Maze_normal(r,c,S,W):
    while num_of_sets(S) > 1: 
        d = random.randint(0,len(W)-1) # Random index
        if find(S,W[d][0]) != find(S,W[d][1]): # Check if the roots are different
            union(S,W[d][0],W[d][1]) # Join the sets
            W.pop(d) # Delete wall

def Maze_C(r,c,S,W):
    while num_of_sets(S) > 1:
        d = random.randint(0,len(W)-1) # Random index
        if find_c(S,W[d][0]) != find_c(S,W[d][1]): # Use path compression
            union_by_size(S,W[d][0],W[d][1]) # Union by size
            W.pop(d)

"""
Main --------------------------------------------------------------------------
"""
plt.close("all")

c = int(input("Choose the number cells for the length and height of the maze:"))
W = wall_list(c,c)
S = DisjointSetForest(c * c)

choice = 0
print("1 for normal DSF or 2 for compressed DSF:")
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
    start = time.time()
    Maze_normal(c,c,S,W)
    end = time.time()
    print("Using standard union and no compression, time:",end - start)

if choice == 2:
    start = time.time()
    Maze_C(c,c,S,W)
    end = time.time()
    print("Using compression and union by size, time:",end - start)

print("\nDrawing maze...")
draw_maze(W,c,c) 