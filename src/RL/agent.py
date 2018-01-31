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
        rl = RL(board, direction, head_position)

        return rl.rewards()

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
        
class RL(object):
    def __init__(self, board, direction, head_position):
        self.board = board
        self.direction = direction
        self.head_position = head_position
        self.tuple = dict()
        self.oldtuple = dict()
        self.init_rewards()
        self.rewards()

    def init_rewards(self):
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                z = 1 if self.board[y][x] is GameObject.FOOD else 0
                self.tuple[(x, y)] = z

        self.oldtuple = self.tuple

        print(self.tuple)

#LOOPT FOUT OP MUUR EN DIE 0.8*
    def rewards(self):
        for j in range(len(self.board)):
            for i in range(len(self.board[j])):
                if self.board[i][j] == GameObject.FOOD:
                    self.tuple[(i, j)] = 1
                elif self.board[i][j] == GameObject.WALL:
                    self.tuple[(i, j)] = None
                else:
                    right_x, right_y = self.direction.get_new_direction(Move.RIGHT).get_xy_manipulation()
                    straight_x, straight_y = self.direction.get_new_direction(Move.STRAIGHT).get_xy_manipulation()
                    left_x, left_y = self.direction.get_new_direction(Move.LEFT).get_xy_manipulation()

                    manright_x = right_x + i
                    manright_y = right_y + j
                    if(manright_y < 0 or manright_y > len(self.board) or manright_x < 0 or manright_x > (len(self.board[j]) - 1)):
                        self.oldtuple[(manright_x, manright_y)] = 0
                    manstraight_x = straight_x + i
                    manstraight_y = straight_y + j
                    if (manstraight_y < 0 or manstraight_y > len(self.board) or manstraight_x < 0 or manstraight_x > (len(self.board[j]) - 1)):
                        self.oldtuple[(manstraight_x, manstraight_y)] = 0
                    manleft_x = left_x + i
                    manleft_y = left_y + j
                    if (manleft_y < 0 or manleft_y > len(self.board) or manleft_x < 0 or manleft_x > (len(self.board[j]) - 1)):
                        self.oldtuple[(manleft_x, manleft_y)] = 0

                    if (self.oldtuple[(manright_x, manright_y)] > self.oldtuple[(manstraight_x, manstraight_y)] and self.oldtuple[(manright_x, manright_y)] > self.oldtuple[(manleft_x,manleft_y)]):
                        self.tuple[(i, j)] = -0.04 + 0.8 * self.oldtuple[(manright_x, manright_y)] + 0.1 * self.oldtuple[(manstraight_x, manstraight_y)] + 0.1 * self.oldtuple[(manleft_x, manleft_y)]
                        print(self.tuple[(i, j)])
                        print((i,j))
                        print(self.oldtuple[(manright_x, manright_y)])
                        print(self.oldtuple[(manstraight_x, manstraight_y)])
                        print(self.oldtuple[(manleft_x, manleft_y)])

                    elif (self.oldtuple[(manright_x, manright_y)] < self.oldtuple[(manstraight_x, manstraight_y)] and self.oldtuple[(manstraight_x, manstraight_y)] > self.oldtuple[(manleft_x,manleft_y)]):
                        self.tuple[(i, j)] = -0.04 + 0.8 * self.oldtuple[(manstraight_x, manstraight_y)] + 0.1 * self.oldtuple[(manright_x, manright_y)] + 0.1 * self.oldtuple[(manleft_x, manleft_y)]

                    elif (self.oldtuple[(manleft_x, manleft_y)] > self.oldtuple[(manstraight_x, manstraight_y)] and self.oldtuple[(manright_x, manright_y)] < self.oldtuple[(manleft_x,manleft_y)]):
                        self.tuple[(i, j)] = -0.04 + 0.8 * self.oldtuple[(manleft_x, manleft_y)] + 0.1 * self.oldtuple[(manright_x, manright_y)] + 0.1 * self.oldtuple[(manstraight_x, manstraight_y)]

                    else:
                        self.tuple[(i, j)] = -0.04 + self.oldtuple[(i, j)]
        print(self.tuple)


    def returnTuple(self):
        return self.tuple

    def rightway(self):
        chance = random.randint(0, 10)

        right_x, right_y = self.direction.get_new_direction(Move.RIGHT).get_xy_manipulation()
        straight_x, straight_y = self.direction.get_new_direction(Move.STRAIGHT).get_xy_manipulation()
        left_x, left_y = self.direction.get_new_direction(Move.LEFT).get_xy_manipulation()

        manright_x = right_x + head_position[0]
        manright_y = right_y + head_position[1]
        if (manright_y < 0 or manright_y > len(self.board) or manright_x < 0 or manright_x > (len(self.board[j]) - 1)):
            self.tuple[(manright_x, manright_y)] = 0
        manstraight_x = straight_x + head_position[0]
        manstraight_y = straight_y + head_position[1]
        if (manstraight_y < 0 or manstraight_y > len(self.board) or manstraight_x < 0 or manstraight_x > (
                len(self.board[j]) - 1)):
            self.tuple[(manstraight_x, manstraight_y)] = 0
        manleft_x = left_x + head_position[0]
        manleft_y = left_y + head_position[1]
        if (manleft_y < 0 or manleft_y > len(self.board) or manleft_x < 0 or manleft_x > (len(self.board[j]) - 1)):
            self.tuple[(manleft_x, manleft_y)] = 0


        if (self.tuple[(manright_x, manright_y)] >= self.tuple[(manstraight_x, manstraight_y)] and self.tuple[
            (manright_x, manright_y)] >= self.tuple[(manleft_x, manleft_y)]):
            if (chance != 9 and chance != 10):
                return Move.RIGHT
            elif (chance == 9):
                return Move.STRAIGHT
            elif (chance == 10):
                return Move.LEFT


        elif (self.tuple[(manright_x, manright_y)] <= self.tuple[(manstraight_x, manstraight_y)] and self.tuple[
            (manstraight_x, manstraight_y)] >= self.tuple[(manleft_x, manleft_y)]):
            if (chance != 9 and chance != 10):
                return Move.STRAIGHT
            elif (chance == 9):
                return Move.LEFT
            elif (chance == 10):
                return Move.RIGHT

        elif (self.tuple[(manleft_x, manleft_y)] >= self.tuple[(manstraight_x, manstraight_y)] and self.tuple[
            (manright_x, manright_y)] <= self.tuple[(manleft_x, manleft_y)]):
            if (chance != 9 and chance != 10):
                return Move.LEFT
            elif (chance == 9):
                return Move.STRAIGHT
            elif (chance == 10):
                return Move.RIGHT
