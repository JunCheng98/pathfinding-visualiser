# pathfinding-visualiser

A program which visualises the execution of various search algorithms, given a start and end point (as well as some optional barriers). Developed using Pygames. Currently supports the A* search algorithm, DFS, BFS as well as Dijkstra, and allows the addition of walls and weighted tiles.

**Existing Commands:**
+ **Left Mouse Button:** Adds a custom tile on the clicked position; first 2 clicks will allocate the start and end point respectively (cannot be the same tile) and subsequent clicks allocate wall tiles.
+ **Right Mouse Button:** Removes the current tile at this position, if any.
+ **c:** Clear and remake the entire board with all tiles at 0 cost.
+ **r:** Makes all tiles on the board weighted with a randomised cost between 0 to 99 inclusive. (start tile is always 0)
+ **a:** Execute A* Search algorithm.
+ **b:** Execute Breadth-First Search algorithm.
+ **d:** Execute Depth-First Search algorithm.
+ **j:** Execute Dijkstra Search algorithm.

**Future Additions:**
+ More search algorithms
+ More custom tile types
