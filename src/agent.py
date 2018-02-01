from gameobjects import GameObject
from move import Move
from move import Direction
import heapq
import math
from board import Board
import time

class Agent:
    def __init__(self, board_width, board_height):
        self.board_width = board_width
        self.board_height = board_height
        self.times = []

    def update_time(self, t):
        self.times.append(t)
        if len(self.times) == 30:
            print("measuring done")
            total = 0
            for t in self.times:
                total += t
            print("mean is: " + str(total / 30))

    def get_move(self, board: Board, score, turns_alive, turns_to_starve, direction):
        aStar = AStar(board, direction, self.board_width, self.board_height)
        aStar.init_grid()
        start = time.time()
        result = aStar.process()
        end = time.time()
        t = end - start
        print(t)
        self.update_time(t)
        return result

    def on_die(self):
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

    def __str__(self):
        return "x: " + str(self.x) + " y: " + str(self.y)

class AStar(object):
    def __init__(self, board: Board, currDir: Direction, board_width, board_height):
        self.opened = []
        heapq.heapify(self.opened)
        self.closed = set()
        self.cells = []
        self.grid_height = board_width
        self.grid_width = board_height
        self.board = board
        self.currDir = currDir
        self.ends = []
        self.end = None
        self.distance = math.inf
        self.start = None

    def init_grid(self):
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
        if -1 < x < self.grid_width and -1 < y < self.grid_height:
            return self.cells[x * self.grid_height + y]
        else:
            return None

    def coor_to_dir(self, cell, target):
        if cell.y - target.y > 0:
            ##print("cell x:" + str(cell.x) + " cell y: " + str(cell.y))
            ##print("target x:" + str(target.x) + "target y:" + str(target.y))
            return Direction.NORTH
        elif cell.x - target.x < 0:
            ##print("cell x:" + str(cell.x) + " cell y: " + str(cell.y))
            ##print("target x:" + str(target.x) + "target y:" + str(target.y))
            return Direction.EAST
        elif cell.y - target.y < 0:
            ##print("cell x:" + str(cell.x) + " cell y: " + str(cell.y))
            ##print("target x:" + str(target.x) + "target y:" + str(target.y))
            return Direction.SOUTH
        else:
            ##print("cell x:" + str(cell.x) + " cell y: " + str(cell.y))
            ##print("target x:" + str(target.x) + "target y:" + str(target.y))
            return Direction.WEST

    def dir_to_move(self, targetDir):
        if self.currDir == Direction.WEST:
            if targetDir == Direction.NORTH:
                return Move.RIGHT
            elif targetDir == Direction.SOUTH:
                return Move.LEFT
            elif targetDir == Direction.EAST:
                #print("going back!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                return Move.LEFT
        elif self.currDir == Direction.NORTH:
            if targetDir == Direction.WEST:
                return Move.LEFT
            elif targetDir == Direction.EAST:
                return Move.RIGHT
            elif targetDir == Direction.SOUTH:
                #print("going back!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                return Move.LEFT
        elif self.currDir == Direction.EAST:
            if targetDir == Direction.NORTH:
                return Move.LEFT
            elif targetDir == Direction.SOUTH:
                return Move.RIGHT
            elif targetDir == Direction.WEST:
                #print("going back!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                return Move.LEFT
        else:
            if targetDir == Direction.WEST:
                return Move.RIGHT
            elif targetDir == Direction.EAST:
                return Move.LEFT
            elif targetDir == Direction.NORTH:
                #print("going back!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                return Move.LEFT
        return Move.STRAIGHT

    def get_adjacent_cells(self, cell):
        cells = []
        if cell.x < self.grid_width - 1:
            cells.append(self.get_cell(cell.x + 1, cell.y))
        if cell.y > 0:
            cells.append(self.get_cell(cell.x, cell.y - 1))
        if cell.x > 0:
            cells.append(self.get_cell(cell.x - 1, cell.y))
        if cell.y < self.grid_height - 1:
            cells.append(self.get_cell(cell.x, cell.y + 1))
        return cells

    def get_open_neighbors(self, cell):
        x = cell.x
        y = cell.y
        N = y - 1
        S = y + 1
        E = x + 1
        W = x - 1
        openN = self.walkable(x, N)
        openS = self.walkable(x, S)
        openE = self.walkable(E, y)
        openW = self.walkable(W, y)
        result = []
        if openN:
            result.append(self.get_cell(x, N))
        if openS:
            result.append(self.get_cell(x, S))
        if openE:
            result.append(self.get_cell(E, y))
        if openW:
            result.append(self.get_cell(W, y))
        return result

    def get_all_neighbors(self, cell):
        x = cell.x
        y = cell.y
        N = y - 1
        S = y + 1
        E = x + 1
        W = x - 1
        openN = self.walkable(x, N)
        openS = self.walkable(x, S)
        openE = self.walkable(E, y)
        openW = self.walkable(W, y)
        if openN:
            NCell = self.get_cell(x, N)
        else:
            NCell = None
        if openS:
            SCell = self.get_cell(x, S)
        else:
            SCell = None
        if openE:
            ECell = self.get_cell(E, y)
        else:
            ECell = None
        if openW:
            WCell = self.get_cell(W, y)
        else:
            WCell = None
        result = []
        result.append({'cell': NCell, 'open': openN, 'z': self.get_consecutive(NCell, Direction.NORTH)})
        result.append({'cell': ECell, 'open': openE, 'z': self.get_consecutive(ECell, Direction.EAST)})
        result.append({'cell': SCell, 'open': openS, 'z': self.get_consecutive(SCell, Direction.SOUTH)})
        result.append({'cell': WCell, 'open': openW, 'z': self.get_consecutive(WCell, Direction.WEST)})
        return result

    def get_consecutive(self, cell, direction: Direction):
        counter = 0
        currCell = cell
        if currCell is None:
            return 0
        if direction == Direction.NORTH:
            while currCell is not None and currCell.reachable:
                counter += 1
                currCell = self.get_cell(currCell.x, currCell.y - 1)
        elif direction == Direction.SOUTH:
            while currCell is not None and currCell.reachable:
                counter += 1
                currCell = self.get_cell(currCell.x, currCell.y + 1)
        elif direction == Direction.EAST:
            while currCell is not None and currCell.reachable:
                counter += 1
                currCell = self.get_cell(currCell.x + 1, currCell.y)
        elif direction == Direction.WEST:
            while currCell is not None and currCell.reachable:
                counter += 1
                currCell = self.get_cell(currCell.x - 1, currCell.y)
        return counter

    def walkable(self, x, y):
        cell = self.get_cell(x, y)
        if cell is not None:
            return cell.reachable
        else:
            return False

    def check_chute(self, cell, direction: Direction):
        currCell = cell
        if direction == Direction.NORTH:
            while self.grid_height > currCell.y > -1 and self.grid_width > currCell.x > -1\
                  and not self.walkable(currCell.x - 1, currCell.y) and not self.walkable(currCell.x + 1, currCell.y):
                if not self.walkable(currCell.x, currCell.y - 1):
                    return True
                else:
                    currCell = self.get_cell(currCell.x, currCell.y - 1)
        elif direction == Direction.SOUTH:
            while self.grid_height > currCell.y > -1 and self.grid_width > currCell.x > -1\
                  and not self.walkable(currCell.x - 1, currCell.y) and not self.walkable(currCell.x + 1, currCell.y):
                if not self.walkable(currCell.x, currCell.y + 1):
                    return True
                else:
                    currCell = self.get_cell(currCell.x, currCell.y + 1)
        elif direction == Direction.EAST:
            while self.grid_height > currCell.y > -1 and self.grid_width > currCell.x > -1\
                  and not self.walkable(currCell.x, currCell.y - 1) and not self.walkable(currCell.x, currCell.y + 1):
                if not self.walkable(currCell.x + 1, currCell.y):
                    return True
                else:
                    currCell = self.get_cell(currCell.x + 1, currCell.y)
        elif direction == Direction.WEST:
            while self.grid_height > currCell.y > -1 and self.grid_width > currCell.x > -1\
                  and not self.walkable(currCell.x, currCell.y - 1) and not self.walkable(currCell.x, currCell.y + 1):
                if not self.walkable(currCell.x - 1, currCell.y):
                    return True
                else:
                    currCell = self.get_cell(currCell.x - 1, currCell.y)
        return False

    def move_safe(self):
        #print("safe move")
        ns = self.get_all_neighbors(self.start)
        if not ns[0].get('open') and not ns[2].get('open') and ns[1].get('open') and ns[3].get('open'):
            if ns[3].get('z') > ns[1].get('z') and not self.check_chute(ns[3].get('cell'), Direction.WEST):
                return self.dir_to_move(Direction.WEST)
            else:
                return self.dir_to_move(Direction.EAST)
        elif ns[0].get('open') and ns[2].get('open') and not ns[1].get('open') and not ns[3].get('open'):
            if ns[2].get('z') > ns[0].get('z') and not self.check_chute(ns[2].get('cell'), Direction.SOUTH):
                return self.dir_to_move(Direction.SOUTH)
            else:
                return self.dir_to_move(Direction.NORTH)
        else:
            #print(ns)
            sortedList = sorted(ns, key=lambda k: k['z'], reverse=True)
            #print(sortedList)
            if sortedList[0].get('open') and not self.check_chute(sortedList[0].get('cell'), self.coor_to_dir(self.start, sortedList[0].get('cell'))):
                return self.dir_to_move(self.coor_to_dir(self.start, sortedList[0].get('cell')))
            elif sortedList[1].get('open') and not self.check_chute(sortedList[1].get('cell'), self.coor_to_dir(self.start, sortedList[1].get('cell'))):
                return self.dir_to_move(self.coor_to_dir(self.start, sortedList[1].get('cell')))
            elif sortedList[2].get('open') and not self.check_chute(sortedList[2].get('cell'), self.coor_to_dir(self.start, sortedList[2].get('cell'))):
                return self.dir_to_move(self.coor_to_dir(self.start, sortedList[2].get('cell')))
            elif sortedList[3].get('open') and not self.check_chute(sortedList[3].get('cell'), self.coor_to_dir(self.start, sortedList[3].get('cell'))):
                return self.dir_to_move(self.coor_to_dir(self.start, sortedList[3].get('cell')))
            #if ns[0].get('open') and not self.check_chute(ns[0].get('cell'), Direction.NORTH):
            #    return self.dir_to_move(Direction.NORTH)
            #elif ns[1].get('open') and not self.check_chute(ns[1].get('cell'), Direction.EAST):
            #    return self.dir_to_move(Direction.EAST)
            #elif ns[2].get('open') and not self.check_chute(ns[2].get('cell'), Direction.SOUTH):
            #    return self.dir_to_move(Direction.SOUTH)
            #elif ns[3].get('open') and not self.check_chute(ns[3].get('cell'), Direction.WEST):
            #    return self.dir_to_move(Direction.WEST)
            else:
                ns = self.get_open_neighbors(self.start)
                if len(ns) > 0:
                    return self.dir_to_move(self.coor_to_dir(self.start, ns[0]))

    def next_move(self):
        #print("path")
        cell = self.end
        while cell.parent is not self.start:
            #print(cell)
            cell = cell.parent
        #print(cell)
        #print(cell.parent)
        return self.dir_to_move(self.coor_to_dir(self.start, cell))

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
            # if ending cell, return next move
            if cell is self.end:
                return self.next_move()
            # get adjacent cells for cell
            adj_cells = self.get_open_neighbors(cell)
            #adj_cells = self.get_adjacent_cells(cell)
            for adj_cell in adj_cells:
                if adj_cell not in self.closed:
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
            for cell in self.cells:
                cell.g = 0
                cell.h = 0
                cell.f = 0
                cell.parent = None
            return self.process()
        else:
            ##print("could not find path to food")
            return self.move_safe()
