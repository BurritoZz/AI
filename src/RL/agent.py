from gameobjects import GameObject
from move import Move, Direction
from board import Board


class Agent:

    def __init__(self):
        """" Constructor of the Agent, can be used to set up variables """

    def get_move(self, board, score, turns_alive, turns_to_starve, direction, head_position, body_parts):
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

        :param head_position: (x,y) of the head of the snake. The following should always hold: board[head_position[
        0]][head_position[1]] == GameObject.SNAKE_HEAD.

        :param body_parts: the array of the locations of the body parts of the snake. The last element of this array
        represents the tail and the first element represents the body part directly following the head of the snake.

        :return: The move of the snake. This can be either Move.LEFT (meaning going left), Move.STRAIGHT (meaning
        going straight ahead) and Move.RIGHT (meaning going right). The moves are made from the viewpoint of the
        snake. This means the snake keeps track of the direction it is facing (North, South, West and East).
        Move.LEFT and Move.RIGHT changes the direction of the snake. In example, if the snake is facing north and the
        move left is made, the snake will go one block to the left and change its direction to west.

        Function: give the food a reward of 1 and let the move cost -.04.
        """
       # print(head_position[0])
        rl = RL(board, direction, head_position)
        return rl.rightway()

    def should_redraw_board(self):
        """
        This function indicates whether the board should be redrawn. Not drawing to the board increases the number of
        games that can be played in a given time. This is especially useful if you want to train you agent. The
        function is called before the get_move function.

        :return: True if the board should be redrawn, False if the board should not be redrawn.
        """
        return True

    def should_grow_on_food_collision(self):
        """
        This function indicates whether the snake should grow when colliding with a food object. This function is
        called whenever the snake collides with a food block.

        :return: True if the snake should grow, False if the snake should not grow
        """
        return True

    def on_die(self, head_position, board, score, body_parts):
        """This function will be called whenever the snake dies. After its dead the snake will be reincarnated into a
        new snake and its life will start over. This means that the next time the get_move function is called,
        it will be called for a fresh snake. Use this function to clean up variables specific to the life of a single
        snake or to host a funeral.

        :param head_position: (x, y) position of the head at the moment of dying.

        :param board: two dimensional array representing the board of the game at the moment of dying. The board
        given does not include information about the snake, only the food position(s) and wall(s) are listed.

        :param score: score at the moment of dying.

        :param body_parts: the array of the locations of the body parts of the snake. The last element of this array
        represents the tail and the first element represents the body part directly following the head of the snake.
        When the snake runs in its own body the following holds: head_position in body_parts.
        """
class Cell(object):
    def __init__(self, x, y, reachable, reward):
        self.reachable = reachable
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0
        self.reward = reward

    def __lt__(self, other):
        return self.f < other.f

class RL(object):
    def __init__(self, board, direction, head_position):
        self.board = board
        self.direction = direction
        self.head_position = head_position
        self.cells = []
        self.init_rewards()
        for i in range(10):
            self.rewards()

    def init_rewards(self):
        for x in range(5):
            for y in range(5):
                if self.board[x][y] == GameObject.WALL:
                    self.cells.append(Cell(x, y, False, None))
                elif self.board[x][y] == GameObject.FOOD:
                    self.cells.append(Cell(x, y, True, 1))
                else:
                    self.cells.append(Cell(x, y, True, 0))

    def rewards(self):
        self.newcells = []
        otherreward = []
        samereward = 0
        same = 0
        highestreward = 0
        reward = 0

        for x in range(5):
            for y in range(5):
                if self.board[x][y] == GameObject.WALL:
                    self.newcells.append(Cell(x, y, False, None))
                elif self.board[x][y] == GameObject.FOOD:
                    self.newcells.append(Cell(x, y, True, 1))
                else:
                    adjacent = self.get_adjacent_cells(Cell(x, y, None, None))
                    length = len(adjacent)

                    for i in range(0, length):
                        if adjacent[i].reward == highestreward:
                            same = same + 1
                            samereward = samereward + (1 / length) * adjacent[i].reward
                            otherreward.append(adjacent[i].reward)
                        elif adjacent[i].reward > highestreward:
                            otherreward.append(highestreward)
                            highestreward = adjacent[i].reward
                        else:
                            otherreward.append(adjacent[i].reward)

                    if same == (length - 1):
                        reward = -0.04 + samereward
                    else:
                        for j in range(len(otherreward)):
                            reward = reward + (0.2 / (length - 1)) * otherreward[j]
                        reward = -0.04 + 0.8 * highestreward + reward

                    self.newcells.append(Cell(x, y, True, reward))
                    reward = 0
                    otherreward = []
                    samereward = 0
                    same = 0
                    highestreward = 0

        self.cells = self.newcells


    def get_adjacent_cells(self, cell):
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

    def walkable(self, x, y):
        cell = self.get_cell(x, y)
        if cell is not None:
            return cell.reachable
        else:
            return False

    def get_cell(self, x, y):
        if -1 < x < 5 and -1 < y < 5:
            return self.cells[x * 5 + y]
        else:
            return None

    def rightway(self):
        returns = Move.STRAIGHT

        right_x, right_y = self.direction.get_new_direction(Move.RIGHT).get_xy_manipulation()
        right_x = right_x + self.head_position[0]
        right_y = right_y + self.head_position[1]
        straight_x, straight_y = self.direction.get_new_direction(Move.STRAIGHT).get_xy_manipulation()
        straight_x = straight_x + self.head_position[0]
        straight_y = straight_y + self.head_position[1]
        left_x, left_y = self.direction.get_new_direction(Move.LEFT).get_xy_manipulation()
        left_x = left_x + self.head_position[0]
        left_y = left_y + self.head_position[1]

        rightcell = self.get_cell(right_x, right_y)
        straightcell = self.get_cell(straight_x, straight_y)
        leftcell = self.get_cell(left_x, left_y)

        allcells = []
        allcells.append(straightcell)
        allcells.append(leftcell)
        allcells.append(rightcell)

        heighestcell = -1
        heighestreward = -100

        for i in range(0, 3):
            if allcells[i] is not None:
                if allcells[i].reward is not None:
                    if allcells[i].reward > heighestreward:
                        heighestcell = i
                        heighestreward = allcells[i].reward

        if heighestcell == 0:
            returns = Move.STRAIGHT
        elif heighestcell == 1:
            returns = Move.LEFT
        elif heighestcell == 2:
            returns = Move.RIGHT

        return returns

    def test(self):
        self.cells = []
        for y in range(5):
            self.cells.append(Cell(y, 0, True, 500))
            self.cells.append(Cell(y, 1, True, 400))
            self.cells.append(Cell(y, 2, True, 300))
            self.cells.append(Cell(y, 3, True, 200))
            self.cells.append(Cell(y, 4, True, 100))