"""
CS2303 - Data Structures
Jesus A. Hernandez - 80629917
Lab#1 Recursive Shapes
Instructor - Dr. Olac Fuentes
TA - Anindita Nath & Maliheh Zargaran

Draw shapes using recursion in order to better understand recursive methods and use of libraries such as pyplot
or numpy.
Last Modified on February 08, 2019
"""

import numpy as np
import matplotlib.pyplot as plt
import math

def draw_squares(ax,d,v,w):
    if d>0:
        percentage = [w*.25,w*.75] #the percentage means the rate of change of the vertices placement in x and y coordinates
        
        br = np.copy(v) #bottom right vertices array
        br[0][0] = br[0][0]+percentage[1] #the rate of change is +75% for x
        br[0][1] = br[0][1]-percentage[0] #the rate of change is -25% for y
        br[1][0] = br[1][0]+percentage[1]
        br[1][1] = br[1][1]-percentage[1]
        br[2][0] = br[2][0]+percentage[0]
        br[2][1] = br[2][1]-percentage[1]
        br[3][0] = br[3][0]+percentage[0]
        br[3][1] = br[3][1]-percentage[0]
        br[4][0] = br[4][0]+percentage[1]
        br[4][1] = br[4][1]-percentage[0]       

        ur = np.copy(v) #upper right vertices array
        ur[0] = ur[0]+percentage[1] #the rate of change is +75% for both x & y
        ur[1][0] = ur[1][0]+percentage[1]
        ur[1][1] = ur[1][1]+percentage[0]
        ur[2] = ur[2]+percentage[0] #the rate of change is +25% for both x & y
        ur[3][0] = ur[3][0]+percentage[0]
        ur[3][1] = ur[3][1]+percentage[1]
        ur[4] = ur[4]+percentage[1]
    
        bl = np.copy(v) #bottom left vertices array
        bl[0] = bl[0]-percentage[0]
        bl[1][0] = bl[1][0]-percentage[0]
        bl[1][1] = bl[1][1]-percentage[1]
        bl[2] = bl[2]-percentage[1]
        bl[3][0] = bl[3][0]-percentage[1]
        bl[3][1] = bl[3][1]-percentage[0]
        bl[4] = bl[4]-percentage[0]
    
        ul = np.copy(v) #upper left vertices array
        ul[0][0] = ul[0][0]-percentage[0]
        ul[0][1] = ul[0][1]+percentage[1]
        ul[1][0] = ul[1][0]-percentage[0]
        ul[1][1] = ul[1][1]+percentage[0]
        ul[2][0] = ul[2][0]-percentage[1]
        ul[2][1] = ul[2][1]+percentage[0]
        ul[3][0] = ul[3][0]-percentage[1]
        ul[3][1] = ul[3][1]+percentage[1]
        ul[4][0] = ul[4][0]-percentage[0]
        ul[4][1] = ul[4][1]+percentage[1]
        
        ax.plot(v[:,0],v[:,1],color='k')
        draw_squares(ax,d-1,bl,w/2) #create bottom left squares
        draw_squares(ax,d-1,ul,w/2) #create upper left squares
        draw_squares(ax,d-1,ur,w/2) #create upper right squares
        draw_squares(ax,d-1,br,w/2) #create bottom right squares

def draw_trees(ax,d,v,w): #will create a new vertice array and plot the last ones 
    if d>0:
        ls = np.copy(v)*0 #left side vertices array
        ls[0][0] = v[0][0]-w[1]
        ls[0][1] = v[0][1]-w[0]
        ls[1] = v[0]
        ls[2][0] = v[0][0]+w[1]
        ls[2][1] = v[0][1]-w[0]
        
        rs = np.copy(v)*0 #right side vertices array
        rs[0][0] = v[2][0]-w[1]
        rs[0][1] = v[2][1]-w[0]
        rs[1] = v[2]
        rs[2][0] = v[2][0]+w[1]
        rs[2][1] = v[2][1]-w[0]
        
        ax.plot(v[:,0],v[:,1],color='k') #plot the arrays
        draw_trees(ax,d-1,ls,[w[0],w[1]/2]) #check if a left side needs to be added
        draw_trees(ax,d-1,rs,[w[0],w[1]/2]) #check if a right side needs to be added

def circle(center,rad):
    n = int(4*rad*math.pi)
    t = np.linspace(0,6.3,n)
    x = center[0]+rad*np.sin(t)
    y = center[1]+rad*np.cos(t)
    return x,y
        
def draw_circles(ax,n,center,radius):
    if n>0:
        r_chg = [radius/3,(2*radius/3)] #this will reduce the radius by a factor of 3 and also the amount of change needed for x & y
        
        x,y = circle(center,radius) #only used to draw the original biggest circle
        ax.plot(x,y,color='k')
        
        x,y = circle(center,r_chg[0]) #create plots for a circle 3 times smaller in the same x & y position
        ax.plot(x,y,color='k')
        
        x,y = circle([center[0]+r_chg[1],center[1]],r_chg[0]) #create a circle 3 times smaller as the original and move it to the right
        ax.plot(x,y,color='k')
        
        x,y = circle([center[0]-r_chg[1],center[1]],r_chg[0]) #same as before but move to the left
        ax.plot(x,y,color='k')

        x,y = circle([center[0],center[1]+r_chg[1]],r_chg[0]) #move upwards
        ax.plot(x,y,color='k')
        
        x,y = circle([center[0],center[1]-r_chg[1]],r_chg[0]) #move downwards
        ax.plot(x,y,color='k')
        
        draw_circles(ax,n-1,center,r_chg[0]) #check for middle circles
        draw_circles(ax,n-1,[center[0]+r_chg[1],center[1]],r_chg[0]) #check right circles
        draw_circles(ax,n-1,[center[0]-r_chg[1],center[1]],r_chg[0]) #left
        draw_circles(ax,n-1,[center[0],center[1]-r_chg[1]],r_chg[0]) #downwards
        draw_circles(ax,n-1,[center[0],center[1]+r_chg[1]],r_chg[0]) #upwards

def draw_circles2(ax,n,center,radius,w):
    if n>0:
        x,y = circle(center,radius)
        ax.plot(x,y,color='k')
        draw_circles2(ax,n-1,[center[0]*w,center[1]],radius*w,w) #constant change across of radius and center for every circle

plt.close("all")
orig_size = 400 #starting values for each figure

#starting vertices for square figure
vertices_square = np.array([[0,0],[0,orig_size],[orig_size,orig_size],[orig_size,0],[0,0]])
fig_square, ax_square = plt.subplots()

#create subplots for the circle in problem 2
fig_circle2, ax_circle2 = plt.subplots()

#starting vertices for tree figure
vertices_tree = np.array([[-orig_size,-orig_size],[0,0],[orig_size,-orig_size]])
fig_tree, ax_tree = plt.subplots()

#create subplots for the circle in problem 4
fig_circle, ax_circle = plt.subplots()


while True: #catch exception when user tries anything but a number, continue until a number is used
    try:
        depth = int(input('Choose depth level for figures 1, 3 & 4: '))
        depth2 = int(input('Choose depth level for figure 2: '))
        rate = float(input('Choose rate of change for figure 2: '))
    except:
        print('Depth level must be any number bigger or equal to 1')
        continue
    break
draw_squares(ax_square,depth,vertices_square,orig_size)
draw_circles2(ax_circle2,depth2,[100,0],100,rate)
draw_trees(ax_tree,depth,vertices_tree,[orig_size,orig_size/2])
draw_circles(ax_circle,depth,[orig_size,0],orig_size)
ax_square.set_aspect(1.0)
ax_tree.set_aspect(1.0)
ax_circle.set_aspect(1.0)
ax_circle2.set_aspect(1.0)
ax_square.axis('off')
ax_tree.axis('off')
ax_circle.axis('off')
ax_circle2.axis('off')