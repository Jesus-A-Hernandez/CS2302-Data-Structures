$ git commit --amend --date "Sun, 28 Apr 2019 11:20:05"
"""
CS2303 - Data Structures
Jesus A. Hernandez - 80629917
Lab#7 - Graphs
Instructor - Dr. Olac Fuentes
TA - Anindita Nath & Maliheh Zargaran
Last Modified on May 02, 2019
"""
import matplotlib.pyplot as plt
import numpy as np
import random
import time

"""
Disjoint Set Forest -----------------------------------------------------------
"""
def DisjointSetForest(size):
    return np.zeros(size,dtype=np.int)-1

def find(S,i):
    # Returns root of tree that i belongs to
    if S[i]<0:
        return i
    return find(S,S[i])
    
def union(S,i,j):
    # Joins i's tree and j's tree, if they are different
    ri = find(S,i) 
    rj = find(S,j)
    if ri!=rj:
        S[rj] = ri

"""
Maze Functions ----------------------------------------------------------------
"""
def draw_maze_path(walls,path,maze_rows,maze_cols,cell_nums=False):
    fig, ax = plt.subplots()
    for p in path:
        if p[1]-p[0] != 1: 
            # Vertical Path
            px0 = (p[1]%maze_cols)+.5
            px1 = px0
            py0 = (p[1]//maze_cols)-.5
            py1 = py0+1
        else: 
            # Horizontal Path
            px0 = (p[0]%maze_cols)+.5
            px1 = px0+1
            py0 = (p[1]//maze_cols)+.5
            py1 = py0
        ax.plot([px0,px1],[py0,py1],linewidth=1,color='r')
    for w in walls:
        if w[1]-w[0] == 1: # Vertical Wall position
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
    ax.axis('on') 
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

# Creates an edje list 
def Maze_User(m,S,W):
    edge_list = []
    counter = 0
    path = False
    while counter < m:
        d = random.randint(0,len(W)-1) # Random index
        if find(S,W[d][0]) != find(S,W[d][1]): # Check if the roots are different
            union(S,W[d][0],W[d][1]) # Join the sets
            edge_list.append(W.pop(d)) # Delete wall
            counter += 1
            if counter >= len(S)-1:
                path = True
        elif path: # Once there is a path start removing any wall
            union(S,W[d][0],W[d][1]) # Join the sets
            edge_list.append(W.pop(d)) # Delete wall
            counter += 1
    return edge_list

"""
Convert Edge List to Adj List -------------------------------------------------
Adj list will be used in methods for traversing the graph.
"""
def edge_list_to_adj_list(G,size):
    adj_list = [[] for i in range(size)]
    for i in range(len(G)):
        adj_list[G[i][0]].append(G[i][1])
        adj_list[G[i][1]].append(G[i][0])
    return adj_list 

"""
Find Path using Breadth-First Search ------------------------------------------
Use a Queue to find a path to the last cell. Return the prev array generated.
"""
def findPathBFS(adj):
    prev = np.zeros(len(adj), dtype=np.int)-1 # Initialize prev array
    visited = [False]*len(adj) # No vertex has been visited
    Q = []
    
    Q.append(adj[0][0]) # Insert the first element of the graph to the queue 
    visited[adj[0][0]] = True # Mark the vertex as visited
    
    while Q:
        if prev[len(adj)-1] >= 0: # Since the wanted vertex has been reached end
            break
        n = Q.pop(0)
        for j in adj[n]:
            if visited[j] == False: # Add to the queue if vertex hasn't been visited
                visited[j] = True
                prev[j] = n
                Q.append(j)
    prev[0] = -1 # Mark the starting vertex as -1 since no vertex points to this
    return prev

"""
Find Path using Depth First Search --------------------------------------------
Use a stack to find the path to the last cell. Some adjustments compared to 
the queue had to be made.
"""
def findPathDepth(adj):
    prev = np.zeros(len(adj), dtype=np.int)-1
    visited = [False]*len(adj)
    S = []
    
    S.append(adj[0][0])
    visited[adj[0][0]] = True
    visited[0] = True 
    prev[adj[0][0]] = 0
    
    while True:
        if prev[len(adj)-1] >= 0: # Since the wanted vertex has been reached end
            break
        n = S.pop()
        for j in adj[n]:
            if visited[j] == False:
                visited[j] = True
                prev[j] = n
                S.append(j)
        if S == []:
            S.append(adj[0][1])
    return prev
        
"""
Find Path using Recursive DFS -------------------------------------------------
"""        
def recursiveDFS(adj,origin,visited,prev):
    visited[origin] = True
    for i in adj[origin]:
        if visited[i] == False:
            prev[i] = origin
            recursiveDFS(adj, i, visited, prev)
    return prev
    

"""
Prev Array to Edje List -------------------------------------------------------
To draw the path in the maze we first need to convert the prev array into an
edje list.
"""
def prev_edje(prev):
    E = []
    i = len(prev)-1 # Start at the end
    while True: # Continue until reaching the start point
        if prev[i] == 0 or prev[i] < 0: # Base case, exit when reached
            E.append([0,i])
            break
        elif i < prev[i]: # Edjes must be in the order of (small,big)
            E.append([i,prev[i]])
        else:    
            E.append([prev[i],i])
        i = prev[i]
    return E # Return edje list
        
    
"""
Main --------------------------------------------------------------------------
"""
plt.close("all")

c = int(input("Choose the number of columns for the maze: "))
r = int(input("Choose the number of rows for the maze: "))
W = wall_list(r,c)
S = DisjointSetForest(c*r)

m = int(input("Choose number of walls to remove: "))

void = False
if (c*r)-1 == m:
    print("\nThere is a unique path from source to destination.")
elif (c*r) > m:
    print("\nA path from source to destination is not guaranteed to exist.")
    void = True
else:
    print("\nThere is at least one path from source to destination.")

selection = 0
if void:
    print("There is no path since maze has no solution.")
else:
    selection = int(input("Choose traversal method (1.BFS, 2.Depth First Search, 3. Recursive Depth Search): "))

edge_list = Maze_User(m,S,W) # Obtain edje list from randomly created maze

adj_list = edge_list_to_adj_list(edge_list,c*r) # Obtain adj list from edje list

if selection == 1:
    start = time.time()
    prev = findPathBFS(adj_list) # Function ends when goal has been reached to shorten time
    end = time.time()
    print("time to obtain prev array: ",end-start)
    print("prev array: ",prev) # Array won't be completed sometimes due to above
    path = (prev_edje(prev))
    print("edje list of path: ",path)
    print("drawing maze...")
    draw_maze_path(W,path,r,c)

if selection == 2:
    start = time.time()
    prev = findPathDepth(adj_list) # Function ends when goal has been reached to shorten time
    end = time.time()
    print("time to obtain prev array: ",end-start)
    print("prev array: ",prev) # Array won't be completed sometimes due to above
    path = (prev_edje(prev))
    print("edje list of path: ",path)
    print("drawing maze...")
    draw_maze_path(W,path,r,c)

if selection == 3:
    visited = [False]*len(adj_list)
    p = np.zeros(len(adj_list),dtype=int)-1
    start = time.time()
    prev = recursiveDFS(adj_list,0,visited,p)
    end = time.time()
    print("time to obtain prev array: ",end-start)
    print("prev array: ",prev)
    path = (prev_edje(prev))
    print("edje list of path: ",path)
    print("drawing maze...")
    draw_maze_path(W,path,r,c)
