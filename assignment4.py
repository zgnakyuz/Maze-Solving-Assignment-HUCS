# Özgün Akyüz, 3.01.2020
# Maze Solver
import sys

maze, healthMaze = open(sys.argv[1], encoding="utf-8-sig"), open(sys.argv[2], encoding="utf-8-sig")
maze, healthMaze = [line.upper().strip() for line in maze], [line.upper().strip() for line in healthMaze]
health_time = int(sys.argv[3])
board, startingPoint, finalPoint, paths = list(), list(), list(), list()


def board_creator(maze):  # Creates a 2D Array to use points as if they have a coordinate
    board.clear(), startingPoint.clear(), finalPoint.clear(), paths.clear()  # Clears lists for every new board creating
    for x, line in enumerate(maze):
        list_line = []
        for y, letter in enumerate(line):
            list_line.append(letter)
            if letter == "S":
                startingPoint.extend([x, y])
            elif letter == "F":
                finalPoint.extend([x, y])
        board.append(list_line)
    return len(board), len(board[0])


xLength, yLength = board_creator(maze)


def maze_solver(x, y, health=xLength * yLength):  # Health is the length of the area for non-health-containing mazes
    if board[x][y] == "S":
        paths.append([x, y])
        board[x][y] = 1
    if board[x][y] == "F":
        paths.append([x, y])
        return 1

    if board[x][y] == "H":
        board[x][y] = 1
        paths.append([x, y])
        if maze_solver(x, y, health_time) == 0:
            paths.remove([x, y])
            board[x][y] = "P"
            return 0
    if health == 0 or board[x][y] == "W":
        return 0
    if board[x][y] == "P":
        board[x][y] = 1
        paths.append([x, y])
        if maze_solver(x, y, health - 1) == 0:
            paths.remove([x, y])
            board[x][y] = "P"
            return 0

    if board[x][y] == 1 and [x, y] != paths[-1]:  # To prevent checking the passed way
        if paths[-1] == finalPoint:  # It shows that we reached the final point
            return 1
        return 0

    # Checking the position's left, downward, upward, right side respectively,
    # if the point has not any paths around itself, it will return 0 and make it "P" again (line 50), instead of 1
    if ((y > 0 and maze_solver(x, y - 1, health)) or (x + 1 < xLength and maze_solver(x + 1, y, health))
            or (x > 0 and maze_solver(x - 1, y, health)) or (y + 1 < yLength and maze_solver(x, y + 1, health))):
        return 1
    return 0


def writing_phase(board, mode, new_line=True):
    board = [[x if x == 1 or x == "F" else 0 for x in i] for i in board]  # Converting all points (except 1 and F) to 0
    board[startingPoint[0]][startingPoint[1]] = "S"  # Rewriting the "S"

    with open(sys.argv[4], mode) as outputF:  # Writing output to the .txt
        for line in board:
            outputF.write(", ".join(map(str, line)) + "\n")
        if new_line:
            outputF.write("\n")


maze_solver(startingPoint[0], startingPoint[1])

writing_phase(board, "w")

# Maze with health - starting phase
xLength, yLength = board_creator(healthMaze)  # Creating new board and finding its edge lengths

maze_solver(startingPoint[0], startingPoint[1], health_time)

writing_phase(board, "a", False)
