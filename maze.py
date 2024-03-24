import random

# Initialize maze and variables
maze = [['_' for _ in range(6)] for _ in range(6)]
mazeSave = [['_' for _ in range(6)] for _ in range(6)]
visited = []  # List to store visited nodes (not used in provided code)
sRow = int  # Variable to store the starting row (not used in provided code)
sColumn = int  # Variable to store the starting column (not used in provided code)
eRow = int  # Variable to store the ending row (not used in provided code)
eColumn = int  # Variable to store the ending column (not used in provided code)
maze_size = 6  # Size of the maze
timeCount = 0  # Variable to track time spent during algorithms

# Function to generate a random maze
def generateMaze():
    global maze, mazeSave
    # Generate start and end nodes
    barriers = []
    start_node = random.randint(0, 5), (random.randint(0, 1))
    end_node = random.randint(0, 5), (random.randint(4, 5))
    # Generate barriers
    i = 0
    while i < 4:
        barrier = (random.randint(0, 5), random.randint(0, 5))
        if barrier != start_node and barrier != end_node:
            barriers.append(barrier)
            i = i + 1
    # Place start, end, and barriers in the maze
    maze[start_node[0]][start_node[1]] = 'S'
    maze[end_node[0]][end_node[1]] = 'E'
    for i in range(len(barriers)):
        maze[barriers[i][0]][barriers[i][1]] = "B"
    # Copy maze for future use
    mazeSave = [row[:] for row in maze]
    # Print the generated maze
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            print(maze[i][j], end='     ')
        print("")
        print("")
    return maze, mazeSave

# Function to get the starting node coordinates
def getStartNode():
    global sColumn, sRow
    # Find and return the starting node coordinates
    for i in range(len(maze)):
        for j in range(maze_size):
            if maze[i][j] == "S":
                sRow = i
                sColumn = j
    return sRow, sColumn

# Function to get the goal node coordinates
def getGoalNode():
    global eRow, eColumn
    # Find and return the goal node coordinates
    for i in range(len(maze)):
        for j in range(maze_size):
            if maze[i][j] == "E":
                eRow = i
                eColumn = j
    return eRow, eColumn

# Depth-First Search (DFS) algorithm
def dfs(sRow, sColumn):
    global timeCount
    # Check if starting position is valid
    if sRow < 0 or sRow >= maze_size or sColumn < 0 or sColumn >= maze_size or maze[sRow][sColumn] == 'B' or maze[sRow][sColumn] == 'V':
        return False
    # Check if goal node is reached
    if maze[sRow][sColumn] == 'E':
        print("Visited:", (sRow, sColumn))
        print("Total time", timeCount)
        return True  # Goal node found
    if maze[sRow][sColumn] == 'S':
        print("Visited:", (sRow, sColumn))
    else:
        maze[sRow][sColumn] = 'V'  # Mark visited
        print("Visited:", (sRow, sColumn))
        timeCount += 1  # Increment timeCount when a cell is visited
    # Check in all directions (up left, left, left down, up, down, right up, right, right down)
    directions = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    for i, j in directions:
        if dfs(sRow + i, sColumn + j):
            return True
    return False

# Heuristic function to estimate the cost from a given point to the goal
def heuristic(row, col, eRow, eColumn):
    return abs(eRow - row) + abs(eColumn - col)

# A* Algorithm
def aStar(sRow, sColumn, eRow, eColumn):
    global timeCount
    timeCount = 0
    open_set = create_priority_queue()
    put(open_set, (sRow, sColumn, None, None), 0)  # Initial state with no parent
    closed_set = set()
    while not is_empty(open_set):
        current, current_cost = get(open_set)
        row, col, _, parent = current  # Unpack the current state
        if (row, col) == (eRow, eColumn):
            reconstruct_path(parent)
            return True  # Goal node found
        if (row, col) in closed_set:
            continue
        closed_set.add((row, col))
        visited.append((row, col))
        directions = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        for i, j in directions:
            new_row, new_col = row + i, col + j
            # Check if the new position is within the maze boundaries and not a barrier
            if 0 <= new_row < maze_size and 0 <= new_col < maze_size and maze[new_row][new_col] != 'B' and (
                    new_row, new_col) not in closed_set:
                new_cost = current_cost + 1
                total_cost = new_cost + heuristic(new_row, new_col, eRow, eColumn)
                put(open_set, (new_row, new_col, new_cost, current), total_cost)
        timeCount += 1
    return False, timeCount

# Function to print the path from 'S' to 'E'
def print_path():
    global path_nodes
    print("The path from 'S' to 'E' is:")
    print(f"({sRow}, {sColumn})")
    for node in path_nodes:
        print(node)
    print(f"({eRow}, {eColumn})")

# Function to reconstruct and mark the path from the goal to the start
def reconstruct_path(parent):
    global path_nodes
    path_nodes = []  # Clear the path_nodes list
    while parent:
        row, col, _, parent = parent
        if maze[row][col] != 'S':
            maze[row][col] = 'V'  # Mark visited
            path_nodes.append((row, col))  # Store path nodes
    path_nodes.reverse()  # Reverse the path to print it in order

# Function to create an empty priority queue
def create_priority_queue():
    return []

# Function to check if the priority queue is empty
def is_empty(priority_queue):
    return len(priority_queue) == 0

# Function to get and remove the item with the lowest priority from the priority queue
def get(priority_queue):
    if not is_empty(priority_queue):
        index = 0
        for i in range(1, len(priority_queue)):
            if priority_queue[i][1] < priority_queue[index][1]:
                index = i
        return priority_queue.pop(index)

# Function to put an item with its priority into the priority queue
def put(priority_queue, item, priority):
    priority_queue.append((item, priority))

# Function to start the maze-solving process
def start():
    print()
    print("\t\t\tWelcome to maze solver\t\t\t")
    print("this is the maze that randomly generates")
    print()
    generateMaze()
    print("Select Options in below")
    print("1. Solve this maze using DFS Algorithm")
    print("2. Solve this maze using A* Algorithm")
    print("3. Exit")

# Main loop for user input
start()
while True:
    decision = int(input("Enter your option: "))
    if decision == 1:
        maze = [row[:] for row in mazeSave]
        getStartNode()
        goal_found = dfs(sRow, sColumn)
        if goal_found:
            print("Goal node found!")
            print("The sorted maze using DFS Algorithm is: ")
            print()
            for i in range(len(maze)):
                for j in range(len(maze[i])):
                    print(maze[i][j], end='     ')
                print("")
                print("")
            print("Total time spent in minutes: ", timeCount, " mins")
            maze = [row[:] for row in mazeSave]
            timeCount = 0
        else:
            print("Goal node not reachable.")
    elif decision == 2:
        getGoalNode()
        getStartNode()
        goal_found = aStar(sRow, sColumn, eRow, eColumn)
        if goal_found:
            print("Goal node found!")
            print("The solved maze using aStar Algorithm is: ")
            print()
            print_path()
            for i in range(len(maze)):
                for j in range(len(maze[i])):
                    print(maze[i][j], end='     ')
                print("")
                print("")
            print()
            print("Total time spent in minutes: ", timeCount, " mins")
            maze = [row[:] for row in mazeSave]
        else:
            print("Goal node not reachable.")
    elif decision == 3:
        exit()  # Exit the program
