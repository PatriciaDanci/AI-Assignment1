# AI-Assignment1
Maze Solver using Pygame module for graphical user interactions

I implemented DFS, BFS, UCS, A Star and Dijkstra

I colored the grid in pastel colors, each color having a specific meaning:
Green - start
Orange - goal
Purple - Wall
Pink - Visited Cells
Blue - Final Path

Additionally, when encountering a wall that can't be passed (such as a wall that covers a whole column / line), I designed a new grid that shows a sad face as the algorithm can't finish and therefore the goal can't be reached. :) 

I have ran the program multiple times for many particular cases, and I couldn't find one that doesn't work. 

Each algorithm can be implemented on the grid by pressing a particular keypad:

D - DFS
B - BFS
U - UCS
A - A Star
K - Dijkstra

Additionally, after the path has been displayed, you can press 'G' (for Grid) to view the Cost of each cell, should the algorithm require it (UCS/ Dijsktra/ A Star) 
I also tried displaying the Cost Grid continuously for these 3 algorithms for a better visualization, but there were slow-downs or even program responding issues. 
In order to determine the Cost, I simple gave each cell a random number ranging from 1 to 10. 
