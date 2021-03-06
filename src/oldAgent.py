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
        self.ends.remove(cell)

    def get_heuristic(self, cell):
        return 10 * (abs(cell.x - self.end.x) + abs(cell.y - self.end.y))

    def get_cell(self, x, y):
        return self.cells[x * self.grid_height + y]

    def coorToDir(self, cell, target):
        if cell.x - target.x == 1:
            return Direction.WEST
        elif cell.x - target.x == -1:
            return Direction.EAST
        elif cell.y - target.y == -1:
            return Direction.SOUTH
        else:
            return Direction.NORTH

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

    def get_open_adjacent_cells(self, cell):
        x = cell.x
        y = cell.y
        N = y - 1
        S = y + 1
        E = x + 1
        W = x - 1
        openN = N > -1 and self.get_cell(x, N).reachable
        openS = S < self.grid_height and self.get_cell(x, S).reachable
        openE = E < self.grid_width and self.get_cell(E, y).reachable
        openW = W > -1 and self.get_cell(W, y).reachable
        result = []
        if openN:
            result.append({'x': x, 'y': N})
        if openE:
            result.append({'x': E, 'y': y})
        if openS:
            result.append({'x': x, 'y': S})
        if openW:
            result.append({'x': W, 'y': y})
        return result

    def get_all_adjacent_cells(self, cell):
        x = cell.x
        y = cell.y
        N = y - 1
        S = y + 1
        E = x + 1
        W = x - 1
        openN = N > -1 and self.get_cell(x, N).reachable
        openS = S < self.grid_height and self.get_cell(x, S).reachable
        openE = E < self.grid_width and self.get_cell(E, y).reachable
        openW = W > -1 and self.get_cell(W, y).reachable
        result = []
        if openN:
            result.append({'x': x, 'y': N, 'on': openN,
                           'z': self.get_consecutive_adjacent_cells(self.get_cell(x, N),
                                                         Direction.NORTH)})
        else:
            result.append({'x': x, 'y': N, 'on': openN, 'z': None})
        if openE:
            result.append({'x': E, 'y': y, 'on': openE,
                           'z': self.get_consecutive_adjacent_cells(self.get_cell(E, y),
                                                         Direction.EAST)})
        else:
            result.append({'x': E, 'y': y, 'on': openE, 'z': None})
        if openS:
            result.append({'x': x, 'y': S, 'on': openS,
                           'z': self.get_consecutive_adjacent_cells(self.get_cell(x, S),
                                                         Direction.SOUTH)})
        else:
            result.append({'x': x, 'y': S, 'on': openS, 'z': None})
        if openW:
            result.append({'x': W, 'y': y, 'on': openW,
                           'z': self.get_consecutive_adjacent_cells(self.get_cell(W, y),
                                                         Direction.WEST)})
        else:
            result.append({'x': W, 'y': y, 'on': openW, 'z': None})
        return result

    def get_consecutive_adjacent_cells(self, cell, direction: Direction):
        counter = 0
        currCell = cell
        if direction == Direction.NORTH:
            while currCell.reachable:
                counter += 1
                if currCell.y > 0:
                    currCell = self.get_cell(currCell.x, currCell.y - 1)
                else:
                    break
        elif direction == Direction.SOUTH:
            while currCell.reachable:
                counter += 1
                if currCell.y < self.grid_height - 1:
                    currCell = self.get_cell(currCell.x, currCell.y + 1)
                else:
                    break
        elif direction == Direction.EAST:
            while currCell.reachable:
                counter += 1
                if currCell.x < self.grid_width - 1:
                    currCell = self.get_cell(currCell.x + 1, currCell.y)
                else:
                    break
        elif direction == Direction.SOUTH:
            while currCell.reachable:
                counter += 1
                if currCell.x > 0:
                    currCell = self.get_cell(currCell.x - 1, currCell.y)
                else:
                    break
        return counter

    def check_chute(self, cell, direction: Direction):
        currCell = cell
        if direction == Direction.NORTH:
            while self.grid_height - 1 > currCell.y > -1\
                  and self.grid_width - 1 > currCell.x > -1\
                  and not self.get_cell(currCell.x - 1, currCell.y).reachable\
                  and not self.get_cell(currCell.x + 1, currCell.y).reachable:
                if not self.get_cell(currCell.x, currCell.y - 1).reachable:
                    return True
                else:
                    currCell = self.get_cell(currCell.x, currCell.y - 1)
        if direction == Direction.SOUTH:
            while self.grid_height - 1 > currCell.y > -1\
                  and self.grid_width - 1 > currCell.x > -1\
                  and not self.get_cell(currCell.x - 1, currCell.y).reachable\
                  and not self.get_cell(currCell.x + 1, currCell.y).reachable:
                if not self.get_cell(currCell.x, currCell.y + 1).reachable:
                    return True
                else:
                    currCell = self.get_cell(currCell.x, currCell.y + 1)
        if direction == Direction.EAST:
            while self.grid_height - 1 > currCell.y > -1\
                  and self.grid_width - 1 > currCell.x > -1\
                  and not self.get_cell(currCell.x, currCell.y - 1).reachable\
                  and not self.get_cell(currCell.x, currCell.y + 1).reachable:
                if not self.get_cell(currCell.x + 1, currCell.y).reachable:
                    return True
                else:
                    currCell = self.get_cell(currCell.x + 1, currCell.y)
        if direction == Direction.WEST:
            while self.grid_height - 1 > currCell.y > -1\
                  and self.grid_width - 1 > currCell.x > -1\
                  and not self.get_cell(currCell.x, currCell.y - 1).reachable\
                  and not self.get_cell(currCell.x, currCell.y + 1).reachable:
                if not self.get_cell(currCell.x - 1, currCell.y).reachable:
                    return True
                else:
                    currCell = self.get_cell(currCell.x - 1, currCell.y)
        return False

    def safe_move(self):
        ns = self.get_all_adjacent_cells(self.start)
        if not ns[0].get('on') and ns[1].get('on') and ns[3].get('on'):
            if ns[3].get('z') > ns[1].get('z') and not\
               self.check_chute(self.get_cell(ns[3].get('x'), ns[3].get('y')),
                                Direction.WEST):
                return Direction.WEST
            else:
                return Direction.EAST
        elif ns[0].get('on') and ns[2].get('on') and not\
                ns[1].get('on') and not ns[3].get('on'):
            if ns[2].get('z') > ns[0].get('z') and not\
               self.check_chute(self.get_cell(ns[2].get('x'), ns[2].get('y')),
                                Direction.SOUTH):
                return Direction.SOUTH
            else:
                return Direction.NORTH
        else:
            ns = self.get_all_adjacent_cells(self.start)
            if ns[0].get('on') and not self.check_chute(
                    self.get_cell(ns[0].get('x'), ns[0].get('y')),
                    Direction.NORTH):
                return Direction.NORTH
            if ns[1].get('on') and not self.check_chute(
                    self.get_cell(ns[1].get('x'), ns[1].get('y')),
                    Direction.EAST):
                return Direction.EAST
            if ns[2].get('on') and not self.check_chute(
                    self.get_cell(ns[2].get('x'), ns[2].get('y')),
                    Direction.SOUTH):
                return Direction.SOUTH
            if ns[3].get('on') and not self.check_chute(
                    self.get_cell(ns[3].get('x'), ns[3].get('y')),
                    Direction.WEST):
                return Direction.WEST
            else:
                ns = self.get_open_adjacent_cells(self.start)
                if len(ns) > 0:
                    return self.coorToDir(self.start, self.get_cell(ns[0].get('x'), ns[0].get('y')))
        print("Nothing found")

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
        self.opened = []
        self.find_nearest()
        # add starting cell to open heap queue
        heapq.heappush(self.opened, self.start)
        while len(self.opened) > 0:
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
                    if adj_cell in self.opened:
                        # if adj cell in open list, check if current path is
                        # better than the one previously found for this adj
                        # cell
                        if adj_cell.g > cell.g + 10:
                            self.update_cell(adj_cell, cell)
                    else:
                        self.update_cell(adj_cell, cell)
                        # add adj cell to open list
                        heapq.heappush(self.opened, adj_cell)
        if len(self.ends) > 0:
            return self.process()
        else:
            return self.safe_move()
        """cell = self.start
        if cell.x < self.grid_width - 1 \
                and (self.board[cell.x + 1][cell.y] == GameObject.EMPTY or
                     self.board[cell.x + 1][cell.y] == GameObject.FOOD):
            return Direction.EAST
        if cell.y < self.grid_height - 1 \
                and (self.board[cell.x][cell.y + 1] == GameObject.EMPTY or
                     self.board[cell.x][cell.y + 1] == GameObject.FOOD):
            return Direction.SOUTH
        if cell.x > 0 \
                and (self.board[cell.x - 1][cell.y] == GameObject.EMPTY or
                     self.board[cell.x - 1][cell.y] == GameObject.FOOD):
            return Direction.WEST
        if cell.y > 0 \
                and (self.board[cell.x][cell.y - 1] == GameObject.EMPTY or
                     self.board[cell.x][cell.y - 1] == GameObject.FOOD):
            return Direction.NORTH"""
