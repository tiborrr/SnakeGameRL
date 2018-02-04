from gameobjects import GameObject
from move import Move
from heapq import *
from pypaths import astar

import numpy as np

class Agent:
    def get_move(self, board, score, turns_alive, turns_to_starve, direction):


        """
        An implementation of the a star algorithm
        """
        def heuristic(a, b):
            return abs(b[0] - a[0]) + abs(b[1] - a[1])

        def aStar(array, start, goal):

            neighbors = [(0, 1), (-1, 0), (1, 0), (0, -1)]

            close_set = set()
            came_from = {}
            gscore = {start: 0}
            fscore = {start: heuristic(start, goal)}
            oheap = []

            heappush(oheap, (fscore[start], start))

            while oheap:

                current = heappop(oheap)[1]

                if current == goal:
                    data = []
                    while current in came_from:
                        data.append(current)
                        current = came_from[current]
                    return data

                close_set.add(current)
                for i, j in neighbors:
                    neighbor = current[0] + i, current[1] + j
                    tentative_g_score = gscore[current] + heuristic(current, neighbor)
                    if 0 <= neighbor[0] < array.shape[0]:
                        if 0 <= neighbor[1] < array.shape[1]:
                            if array[neighbor[0]][neighbor[1]] == GameObject.WALL:
                                continue
                            if array[neighbor[0]][neighbor[1]] == GameObject.SNAKE_BODY:
                                continue
                        else:
                            # array bound y walls
                            continue
                    else:
                        # array bound x walls
                        continue

                    if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                        continue

                    if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                        came_from[neighbor] = current
                        gscore[neighbor] = tentative_g_score
                        fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                        heappush(oheap, (fscore[neighbor], neighbor))

            return False

        """This function behaves as the 'brain' of the snake. You only need to change the code in this function for
        the project. Every turn the agent needs to return a move. This move will be executed by the snake. If this
        functions fails to return a valid return (see return), the snake will die (as this confuses its tiny brain
        that much that it will explode). The starting direction of the snake will be North.

        :param board: A two dimensional array representing the current state of the board. The upper left most
        coordinate is equal to (0,0) and each coordinate (x,y) can be accessed by executing board[x][y]. At each
        coordinate a GameObject is present. This can be either GameObject.EMPTY (meaning there is nothing at the
        given coordinate), GameObject.FOOD (meaning there is food at the given coordinate), GameObject.WALL (meaning
        there is a wall at the given coordinate. TIP: do not run into them), GameObject.SNAKE_HEAD (meaning the head
        of the snake is located there) and GameObject.SNAKE_BODY (meaning there is a body part of the snake there.
        TIP: also, do not run into these). The snake will also die when it tries to escape the board (moving out of
        the boundaries of the array)

        :param score: The current score as an integer. Whenever the snake eats, the score will be increased by one.
        When the snake tragically dies (i.e. by running its head into a wall) the score will be reset. In ohter
        words, the score describes the score of the current (alive) worm.

        :param turns_alive: The number of turns (as integer) the current snake is alive.

        :param turns_to_starve: The number of turns left alive (as integer) if the snake does not eat. If this number
        reaches 1 and there is not eaten the next turn, the snake dies. If the value is equal to -1, then the option
        is not enabled and the snake can not starve.

        :param direction: The direction the snake is currently facing. This can be either Direction.NORTH,
        Direction.SOUTH, Direction.WEST, Direction.EAST. For instance, when the snake is facing east and a move
        straight is returned, the snake wil move one cell to the right.

        :return: The move of the snake. This can be either Move.LEFT (meaning going left), Move.STRAIGHT (meaning
        going straight ahead) and Move.RIGHT (meaning going right). The moves are made from the viewpoint of the
        snake. This means the snake keeps track of the direction it is facing (North, South, West and East).
        Move.LEFT and Move.RIGHT changes the direction of the snake. In example, if the snake is facing north and the
        move left is made, the snake will go one block to the left and change its direction to west.
        """
        # Init variables
        foodLocation = []
        food = []
        wallLocation = []
        headLocation = (0,0)
        closestPath = []

        tempScore = score

        # Find the foods
        for x in range(0, len(board)):
            for y in range(0, len(board[0])):
                if board[x][y] == GameObject.FOOD:
                  foodLocation.append((x,y))

        # Find the walls
        for x in range(0, len(board)):
            for y in range(0, len(board[0])):
                if board[x][y] == GameObject.WALL:
                  wallLocation.append((x,y))

        # Find the snake head
        for x in range(0, len(board)):
            for y in range(0, len(board[0])):
                if board[x][y] == GameObject.SNAKE_HEAD:
                    headLocation = (x, y)

        # create instance of pathfinder & find the path to all the foods
        finder = astar.pathfinder()

        # Create an array from the received board (which is a list)
        boardArray = np.asarray(board)

        # Find the paths to the foods
        path1 = finder(headLocation, foodLocation[0])
        path2 = finder(headLocation, foodLocation[1])
        path3 = finder(headLocation, foodLocation[2])

        # Choose the food with the lowest manhatten distance
        if path1[0] < path2[0] and path1[0] < path3[0]:
            food = foodLocation[0]
        elif path2[0] < path1[0] and path2[0] < path3[0]:
            food = foodLocation[1]
        else:
            food = foodLocation[2]

        # Build a path to the closest food
        closestPath = aStar(boardArray, headLocation, food)


        if not closestPath:
            closestPath = aStar(boardArray, headLocation, foodLocation[0])

        if not closestPath:
            closestPath = aStar(boardArray, headLocation, foodLocation[1])

        if not closestPath:
            closestPath = aStar(boardArray, headLocation, foodLocation[2])

        if not closestPath:
            if headLocation[1] - 1 > 0:
                northObject = board[headLocation[0]][headLocation[1] - 1]
            else:
                northObject = GameObject.WALL
            if headLocation[0] - 1 > 0:
                westObject = board[headLocation[0] - 1][headLocation[1]]
            else:
                westObject = GameObject.WALL
            if headLocation[0] + 1 < len(board[0]):
                eastObject = board[headLocation[0] + 1][headLocation[1]]
            else:
                eastObject = GameObject.WALL
            if headLocation[1] + 1 < len(board[1]):
                southObject = board[headLocation[0]][headLocation[1] + 1]
            else:
                southObject = GameObject.WALL
            if direction == direction.NORTH:
                # check if out of bound and wall in north direction
                if headLocation[1] - 1 < 0 or (northObject != GameObject.EMPTY and northObject != GameObject.FOOD):
                    # check if out of bound and wall in west direction
                        if headLocation[0] - 1 < 0 or (westObject != GameObject.EMPTY and westObject != GameObject.FOOD):
                            return Move.RIGHT
                        else:
                            return Move.LEFT
                else:
                    if westObject == GameObject.EMPTY:
                        return Move.LEFT
                    if eastObject == GameObject.EMPTY:
                        return Move.RIGHT
                    else:
                        return Move.STRAIGHT
            if direction == direction.SOUTH:
                # check if out of bound and wall in south direction
                if headLocation[1] + 1 > len(board[1]) or (southObject != GameObject.EMPTY and southObject != GameObject.FOOD):
                    # check if out of bound and wall in west direction
                    if headLocation[0] - 1 < 0 or (eastObject != GameObject.EMPTY and eastObject != GameObject.FOOD):
                        return Move.RIGHT
                    else:
                        return Move.LEFT
                else:
                    if westObject == GameObject.EMPTY:
                        return Move.RIGHT
                    if eastObject == GameObject.EMPTY:
                        return Move.LEFT
                    else:
                        return Move.STRAIGHT
            if direction == direction.WEST:
                # check if out of bound and wall in west direction
                if headLocation[0] - 1 < 0 or (westObject != GameObject.EMPTY and westObject != GameObject.FOOD):
                    # check if out of bound and wall in north direction
                    if headLocation[1] - 1 < 0 or (northObject != GameObject.EMPTY and northObject != GameObject.FOOD):
                        return Move.LEFT
                    else:
                        return Move.RIGHT
                else:
                    if northObject == GameObject.EMPTY:
                        return Move.RIGHT
                    if southObject == GameObject.EMPTY:
                        return Move.LEFT
                    else:
                        return Move.STRAIGHT
            if direction == direction.EAST:
                # check if out of bound and wall in east direction
                if headLocation[0] + 1 > len(board) or (eastObject != GameObject.EMPTY and eastObject != GameObject.FOOD):
                    # check if out of bound and wall in south direction
                    if headLocation[1] - 1 < 0 or (northObject != GameObject.EMPTY and northObject != GameObject.FOOD):
                        return Move.RIGHT
                    else:
                        return Move.LEFT
                else:
                    if northObject == GameObject.EMPTY:
                        return Move.LEFT
                    if southObject == GameObject.EMPTY:
                        return Move.RIGHT
                    else:
                        return Move.STRAIGHT

        # Reverse the array
        closestPath.reverse()


        # print("Direction: " , direction)
        # print("Path: " ,closestPath)
        # print("Head: " , headLocation)
        # print("Food: " , foodLocation)
        #



        if direction == direction.NORTH and headLocation[0] < closestPath[0][0]:
            return Move.RIGHT
        if direction == direction.NORTH and headLocation[0] > closestPath[0][0]:
            return Move.LEFT
        if direction == direction.NORTH and headLocation[0] == closestPath[0][0]:
            if headLocation[1] > closestPath[0][1]:
                return Move.STRAIGHT
            return Move.LEFT


        if direction == direction.SOUTH and headLocation[0] < closestPath[0][0]:
            return Move.LEFT
        if direction == direction.SOUTH and headLocation[0] > closestPath[0][0]:
            return Move.RIGHT
        if direction == direction.SOUTH and headLocation[0] == closestPath[0][0]:
            if headLocation[1] < closestPath[0][1]:
                return Move.STRAIGHT
            return Move.LEFT


        if direction == direction.EAST and headLocation[0] < closestPath[0][0]:
            return Move.STRAIGHT
        if direction == direction.EAST and headLocation[0] > closestPath[0][0]:
            return Move.LEFT
        if direction == direction.EAST and headLocation[0] == closestPath[0][0]:
            if headLocation[1] > closestPath[0][1]:
                return Move.LEFT
            return Move.RIGHT


        if direction == direction.WEST and headLocation[0] < closestPath[0][0]:
            return Move.LEFT
        if direction == direction.WEST and headLocation[0] > closestPath[0][0]:
            return Move.STRAIGHT
        if direction == direction.WEST and headLocation[0] == closestPath[0][0]:
            if headLocation[1] > closestPath[0][1]:
                return Move.RIGHT
            return Move.LEFT

        # If else fails, do this:
        return Move.STRAIGHT

    def on_die(self):
        """This function will be called whenever the snake dies. After its dead the snake will be reincarnated into a
        new snake and its life will start over. This means that the next time the get_move function is called,
        it will be called for a fresh snake. Use this function to clean up variables specific to the life of a single
        snake or to host a funeral.
        """
        self.path = []
        self.foodLocation = []
        self.wallLocation = []
        self.headLocation = (0, 0)

        pass

    """ 
    Find the locations of the food in the game 

    Returns: an array of tuples (coordinates)
    """
