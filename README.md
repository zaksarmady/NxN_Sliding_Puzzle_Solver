## NxN_Sliding_Puzzle_Solver
Tree-based search algorithms in software to search for solutions of the NxM-Puzzle problem using both informed and uninformed search methods
 	
## Features
* Depth First Search (dfs)
* Breath First Search (bfs)
* Iterative Deepening A* search (ida)
The program will run and output into a file in the same directory. This output file will be named ‘output.txt’.


## Bugs	
* DFS can take a large number of moves to find a solution. Unsure if this is the nature of DFS or if this is a bug. 


## Missing Features
* A Star search not supported. Solver can only solve NxN puzzles. At this time it cannot solve NxM puzzles. 

## Setup
* 'data.txt' file contains the initial set up for the nxn puzzle. First line indicates the size of puzzle, second line indicates intital puzzle state, last line indicates goal puzzle state.
For example:

```
3x3
5 3 6 1 7 8 4 2 0
1 2 3 4 5 6 7 8 0
``` 	
The program is run through a command line interface. Below is an example of how to run it:
``` <filename> <Search Type> ``` 

For example: ``` puzzler.py dfs ```

The output file displays the:
* Path to goal
* The cost it takes to get to that path
* The number of nudes expanded to reach that path
* How deep the search went
* Running time

