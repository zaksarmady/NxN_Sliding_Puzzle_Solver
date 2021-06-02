import argparse
import timeit
from collections import deque


#GameState Class **************************************************************
class GameState:

    def __init__(self, state, parent, move, depth, cost, key):

        self.state = state

        self.parent = parent

        self.move = move

        self.depth = depth

        self.cost = cost

        self.key = key

        if self.state:
            self.map = ''.join(str(e) for e in self.state)

    def __eq__(self, other):
        return self.map == other.map

    def __lt__(self, other):
        return self.map < other.map
    
    
#Global Variables *************************************************************
goal_state = list()
initial_state = list()

goal_node = GameState

board_len = 0
board_side = 0

nodes_expanded = 0
max_search_depth = 0
max_frontier_size = 0

moves = list()
costs = set()


#BFS **************************************************************************
def bfs(start_state):

    global max_frontier_size, goal_node, max_search_depth

    visited, queue = set(), deque([GameState(start_state, None, None, 0, 0, 0)])

    while queue:

        node = queue.popleft()

        visited.add(node.map)

        if node.state == goal_state:
            goal_node = node
            return queue

        neighbors = expand(node)

        for neighbor in neighbors:
            if neighbor.map not in visited:
                queue.append(neighbor)
                visited.add(neighbor.map)

                if neighbor.depth > max_search_depth:
                    max_search_depth += 1

        if len(queue) > max_frontier_size:
            max_frontier_size = len(queue)


#DFS **************************************************************************
def dfs(start_state):

    global max_frontier_size, goal_node, max_search_depth

    visited, stack = set(), list([GameState(start_state, None, None, 0, 0, 0)])

    while stack:

        node = stack.pop() #this makes it dfs, pop is LIFO

        visited.add(node.map)

        if node.state == goal_state:
            goal_node = node
            return stack

        neighbors = expand(node)

        for neighbor in neighbors:
            if neighbor.map not in visited:
                stack.append(neighbor) #append acts as a "push" as it would be in a stack
                visited.add(neighbor.map)

                if neighbor.depth > max_search_depth:
                    max_search_depth += 1

        if len(stack) > max_frontier_size:
            max_frontier_size = len(stack)


#Iterative Deepening A Star Search ********************************************
def ida(start_state):

    global costs

    threshold = h(start_state)

    while 1:
        response = ida_rec(start_state, threshold)

        if type(response) is list:
            return response

        else:
            threshold = response

        costs = set()

    
def ida_rec(start_state, threshold):
    global max_frontier_size, goal_node, max_search_depth, costs

    visited, stack = set(), list([GameState(start_state, None, None, 0, 0, threshold)])

    while stack:

        node = stack.pop()

        visited.add(node.map)

        if node.state == goal_state:
            goal_node = node
            return stack

        if node.key > threshold:
            costs.add(node.key)

        else:
            neighbors = expand(node)

            for neighbor in neighbors:
                if neighbor.map not in visited:

                    neighbor.key = neighbor.cost + h(neighbor.state)
                    stack.append(neighbor)
                    visited.add(neighbor.map)

                    if neighbor.depth > max_search_depth:
                        max_search_depth += 1

            if len(stack) > max_frontier_size:
                max_frontier_size = len(stack)

    return min(costs)


#This function expands nodes to give sub-nodes*********************************
def expand(node):

    global nodes_expanded
    nodes_expanded += 1

    neighbors = list()

    neighbors.append(GameState(move(node.state, 1), node, 1, node.depth + 1, node.cost + 1, 0))
    neighbors.append(GameState(move(node.state, 2), node, 2, node.depth + 1, node.cost + 1, 0))
    neighbors.append(GameState(move(node.state, 3), node, 3, node.depth + 1, node.cost + 1, 0))
    neighbors.append(GameState(move(node.state, 4), node, 4, node.depth + 1, node.cost + 1, 0))

    nodes = [neighbor for neighbor in neighbors if neighbor.state]

    return nodes


#How program takes steps ******************************************************
def move(state, position):

    new_state = state[:]

    index = new_state.index(0)

    if position == 1:  # Up

        if index not in range(0, board_side):

            temp = new_state[index - board_side]
            new_state[index - board_side] = new_state[index]
            new_state[index] = temp

            return new_state
        else:
            return None

    if position == 2:  # Down

        if index not in range(board_len - board_side, board_len):

            temp = new_state[index + board_side]
            new_state[index + board_side] = new_state[index]
            new_state[index] = temp

            return new_state
        else:
            return None

    if position == 3:  # Left

        if index not in range(0, board_len, board_side):

            temp = new_state[index - 1]
            new_state[index - 1] = new_state[index]
            new_state[index] = temp

            return new_state
        else:
            return None

    if position == 4:  # Right

        if index not in range(board_side - 1, board_len, board_side):

            temp = new_state[index + 1]
            new_state[index + 1] = new_state[index]
            new_state[index] = temp

            return new_state
        else:
            return None


#Heuristic ********************************************************************
def h(state):

    return sum(abs(b % board_side - g % board_side) + abs(b//board_side - g//board_side)
               for b, g in ((state.index(i), goal_state.index(i)) for i in range(1, board_len)))


def backtrace():

    current_node = goal_node

    while initial_state != current_node.state:

        if current_node.move == 1:
            movement = 'Up'
        elif current_node.move == 2:
            movement = 'Down'
        elif current_node.move == 3:
            movement = 'Left'
        else:
            movement = 'Right'

        moves.insert(0, movement)
        current_node = current_node.parent

    return moves


#Generate Output Document******************************************************
def export(frontier, time):

    global moves

    moves = backtrace()

    file = open('output.txt', 'w')
    file.write("path_to_goal: " + str(moves))
    file.write("\ncost_of_path: " + str(len(moves)))
    file.write("\nnodes_expanded: " + str(nodes_expanded))
    file.write("\nfringe_size: " + str(len(frontier)))
    file.write("\nmax_fringe_size: " + str(max_frontier_size))
    file.write("\nsearch_depth: " + str(goal_node.depth))
    file.write("\nmax_search_depth: " + str(max_search_depth))
    file.write("\nrunning_time: " + format(time, '.8f'))
    file.close()


#Assign values from .txt file**************************************************
def assign(puzzle):

    global board_len, board_side

    data = puzzle

    for element in data[1]:
        initial_state.append(int(element))
        
    for element in data[2]:
        goal_state.append(int(element))


    board_len = int(puzzle[0][0][0]) * int(puzzle[0][0][2])

    board_side = int(board_len ** 0.5)


#MAIN *************************************************************************
def main():
    
    with open("data.txt") as textFile:
        puzzle = [line.split() for line in textFile]
        
    parser = argparse.ArgumentParser()
    parser.add_argument('algorithm')
    args = parser.parse_args()

    assign(puzzle)
    
    textFile.close()

    function = function_map[args.algorithm]

    start = timeit.default_timer()

    frontier = function(initial_state)

    stop = timeit.default_timer()

    export(frontier, stop-start)


function_map = {
    'bfs': bfs,
    'dfs': dfs,
    'ida': ida
}

if __name__ == '__main__':
    main()
