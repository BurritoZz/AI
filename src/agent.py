from gameobjects import GameObject
from move import Move
from move import Direction
import heapq
import math
from board import Board


class Agent:
    def get_move(self, board: Board, score, turns_alive,
                 turns_to_starve, direction):
        """This function behaves as the 'brain' of the snake. You only need to
        change the code in this function for the project. Every turn the agent
        needs to return a move. This move will be executed by the snake. If
        this functions fails to return a valid return (see return), the snake
        will die (as this confuses its tiny brain that much that it will
        explode). The starting direction of the snake will be North.

        :param board: A two dimensional array representing the current state of
        the board. The upper left most coordinate is equal to (0,0) and each
        coordinate (x,y) can be accessed by executing board[x][y]. At each
        coordinate a GameObject is present. This can be either GameObject.EMPTY
        (meaning there is nothing at the given coordinate), GameObject.FOOD
        (meaning there is food at the given coordinate), GameObject.WALL
        (meaning there is a wall at the given coordinate. TIP: do not run into
        them), GameObject.SNAKE_HEAD (meaning the head of the snake is located
        there) and GameObject.SNAKE_BODY (meaning there is a body part of the
        snake there. TIP: also, do not run into these). The snake will also die
        when it tries to escape the board (moving out of the boundaries of the
        array)

        :param score: The current score as an integer. Whenever the snake eats,
        the score will be increased by one. When the snake tragically dies
        (i.e. by running its head into a wall) the score will be reset. In
        ohter words, the score describes the score of the current (alive) worm.

        :param turns_alive: The number of turns (as integer) the current snake
        is alive.

        :param turns_to_starve: The number of turns left alive (as integer) if
        the snake does not eat. If this number reaches 1 and there is not eaten
        the next turn, the snake dies. If the value is equal to -1, then the
        option is not enabled and the snake can not starve.

        :param direction: The direction the snake is currently facing. This can
        be either Direction.NORTH, Direction.SOUTH, Direction.WEST,
        Direction.EAST. For instance, when the snake is facing east and a move
        straight is returned, the snake wil move one cell to the right.

        :return: The move of the snake. This can be either Move.LEFT (meaning
        going left), Move.STRAIGHT (meaning going straight ahead) and
        Move.RIGHT (meaning going right). The moves are made from the viewpoint
        of the snake. This means the snake keeps track of the direction it is
        facing (North, South, West and East). Move.LEFT and Move.RIGHT changes
        the direction of the snake. In example, if the snake is facing north
        and the move left is made, the snake will go one block to the left and
        change its direction to west.
        """
        aStar = AStar(board)
        aStar.init_grid()
        nextDirection = aStar.process()
        if direction == Direction.NORTH:
            if nextDirection == Direction.WEST:
                return Move.LEFT
            elif nextDirection == Direction.EAST:
                return Move.RIGHT
            elif nextDirection == Direction.SOUTH:
                return Move.LEFT
        elif direction == Direction.EAST:
            if nextDirection == Direction.NORTH:
                return Move.LEFT
            elif nextDirection == Direction.SOUTH:
                return Move.RIGHT
            elif nextDirection == Direction.WEST:
                return Move.LEFT
        elif direction == Direction.SOUTH:
            if nextDirection == Direction.EAST:
                return Move.LEFT
            elif nextDirection == Direction.WEST:
                return Move.RIGHT
            elif nextDirection == Direction.NORTH:
                return Move.LEFT
        elif direction == Direction.WEST:
            if nextDirection == Direction.SOUTH:
                return Move.LEFT
            elif nextDirection == Direction.NORTH:
                return Move.RIGHT
            elif nextDirection == Direction.EAST:
                return Move.LEFT
        return Move.STRAIGHT

    def on_die(self):
        """This function will be called whenever the snake dies. After its dead
        the snake will be reincarnated into a new snake and its life will start
        over. This means that the next time the get_move function is called,
        it will be called for a fresh snake. Use this function to clean up
        variables specific to the life of a single snake or to host a funeral.
        """
        pass


class Cell(object):
    def __init__(self, x, y, reachable):
        self.reachable = reachable
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f


class AStar(object):
    def __init__(self, board: Board):
        self.opened = []
        heapq.heapify(self.opened)
        self.closed = set()
        self.cells = []
        self.grid_height = 25
        self.grid_width = 25
        self.board = board
        self.ends = []
        self.end = None
        self.distance = math.inf

    def init_grid(self):
        self.start = None
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if self.board[x][y] == GameObject.WALL \
                        or self.board[x][y] == GameObject.SNAKE_BODY:
                    reachable = False
                else:
                    reachable = True
                self.cells.append(Cell(x, y, reachable))
                if self.board[x][y] == GameObject.SNAKE_HEAD:
                    self.start = self.get_cell(x, y)
                if self.board[x][y] == GameObject.FOOD:
                    self.ends.append(self.get_cell(x, y))

    def find_nearest(self):
        for cell in self.ends:
            new_distance = abs(cell.x - self.start.x) + abs(cell.y - self.start.y)
            if new_distance < self.distance:
                self.end = cell
                self.distance = new_distance


    def get_heuristic(self, cell):
        return 10 * (abs(cell.x - self.end.x) + abs(cell.y - self.end.y))

    def get_cell(self, x, y):
        return self.cells[x * self.grid_height + y]

    def get_adjacent_cells(self, cell):
        cells = []
        if cell.x < self.grid_width-1:
            cells.append(self.get_cell(cell.x+1, cell.y))
        if cell.y > 0:
            cells.append(self.get_cell(cell.x, cell.y-1))
        if cell.x > 0:
            cells.append(self.get_cell(cell.x-1, cell.y))
        if cell.y < self.grid_height-1:
            cells.append(self.get_cell(cell.x, cell.y+1))
        return cells

    def display_path(self):
        cell = self.end
        while cell.parent is not self.start:
            cell = cell.parent
        if cell.x > self.start.x:
            return Direction.EAST
        if cell.x < self.start.x:
            return Direction.WEST
        if cell.y > self.start.y:
            return Direction.SOUTH
        if cell.y < self.start.y:
            return Direction.NORTH

    def update_cell(self, adj, cell):
        adj.g = cell.g + 10
        adj.h = self.get_heuristic(adj)
        adj.parent = cell
        adj.f = adj.h + adj.g

    def process(self):
        self.find_nearest()
        # add starting cell to open heap queue
        heapq.heappush(self.opened, self.start)
        while len(self.opened):
            # pop cell from heap queue
            cell = heapq.heappop(self.opened)
            # add cell to closed list so we don't process it twice
            self.closed.add(cell)
            # if ending cell, display found path
            if cell is self.end:
                return self.display_path()
                break
            # get adjacent cells for cell
            adj_cells = self.get_adjacent_cells(cell)
            for adj_cell in adj_cells:
                if adj_cell.reachable and adj_cell not in self.closed:
                    if (adj_cell.f, adj_cell) in self.opened:
                        # if adj cell in open list, check if current path is
                        # better than the one previously found for this adj
                        # cell
                        if adj_cell.g > cell.g + 10:
                            self.update_cell(adj_cell, cell)
                    else:
                        self.update_cell(adj_cell, cell)
                        # add adj cell to open list
                        heapq.heappush(self.opened, adj_cell)
