# pathfinding-visualiser

A program which visualises the execution of various search algorithms, given a start and end point (as well as some optional barriers). Developed using Pygames. Currently supports the A* search algorithm and allows the addition of walls.

*Existing Commands:*
+*Left Mouse Button:* Adds a custom tile on the clicked position; first 2 clicks will allocate the start and end point respectively (cannot be the same tile) and subsequent clicks allocate wall tiles.
+*Right Mouse Button:* Removes the current tile at this position, if any.
+*C:* Clear the entire board.
+*Space:* Execute the search algorithm.

*Future Additions:*
+More search algorithms (BFS, DFS etc.)
+More custom tile types (weighted tiles etc.)
