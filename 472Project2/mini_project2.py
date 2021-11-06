# based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python

import time
import sys
from enum import Enum

# global variables
global n, b, b_locs, s, d1, d2, t

MAX_GRID_SIZE = 10
MIN_GRID_SIZE = 3


class Letter(Enum):
    A = 0
    B = 1
    C = 2
    D = 3
    E = 4
    F = 5
    G = 6
    H = 7
    I = 8
    J = 9


class Game:
    MINIMAX = 0
    ALPHABETA = 1
    HUMAN = 2
    AI = 3

    def __init__(self, n, b, b_locs, s, d1, d2, t, recommend=True):
        # game parameters
        self.n = n  # size of the board
        self.b = b  # num of blocs
        self.b_locs = b_locs  # positions of the blocs
        self.s = s  # winning line-up length
        self.d1 = d1  # player 1 max depth
        self.d2 = d2  # player 2 max depth
        self.t = t  # max allowed time
        self.recommend = recommend
        self.current_state = []
        self.initialize_game()

    # 棋盘结构 the game board structure
    def initialize_game(self):

        for i in range(n):
            row = [];
            for j in range(n):
                # add bloc '*'
                for b_loc in self.b_locs:
                    if b_loc == (i, j):
                        row.append('*')
                else:
                    row.append('.')

            self.current_state.append(row)
        # Player X always plays first
        self.player_turn = 'X'

    # 画出来draw board
    def draw_board(self):
        print()
        # print column header
        print(' ', end=" ")
        for i in range(0, n):
            print(F'{Letter(i).name}', end=" ")

        print()
        # draw the board
        for x in range(0, n):
            for y in range(0, n):
                if y == 0:
                    # print row header
                    print(F'{x}', end="")
                    print(F'|', end="")
                # draw row content
                print(F'{self.current_state[x][y]}', end=" ")

            print()
        print()

    # check whether the input coordinate is valid or not
    def is_valid(self, px, py):
        if is_valid_positive_int(px) and is_valid_positive_int(py):
            if int(px) >= n or int(py) >= n:
                return False
            elif self.current_state[int(px)][int(py)] != '.':
                return False
            else:
                return True
        return False

    # check horizontal line win
    def horizontal(self):
        for i in range(0, n):
            # count how many tokens in a horizontal line
            count = 0
            for j in range(0, n - 1):
                if self.current_state[i][j] != '.' and self.current_state[i][j] == self.current_state[i][j + 1]:
                    win_token = self.current_state[i][j]
                    count += 1
                    if count == (s - 1):
                        return win_token
                # reset
                else:
                    count = 0
        return None

    # check vertical line win
    def vertical(self):
        for i in range(0, n):
            # count how many tokens in a vertical line
            count = 0
            for j in range(0, n - 1):
                if self.current_state[j][i] != '.' and self.current_state[j][i] == self.current_state[j + 1][i]:
                    win_token = self.current_state[j][i]
                    count += 1
                    if count == (s - 1):
                        return win_token
                # reset
                else:
                    count = 0
        return None

    # chekc main diagonal line win
    def main_diagonal(self):
        # loop over rows
        for i in range(0, n - s + 1):
            # loop over columns
            for j in range(0, n - s + 1):
                # protect out of bounds error
                alarm = j
                # count how many tokens in main diagonal line
                count = 0
                # loop over diagonals
                for index in range(0, n):
                    try:
                        # index out of bounds, break
                        if index + j + 1 > n:
                            break

                        if (self.current_state[index + j][i + index] != '.' and self.current_state[index + j][
                            i + index] == self.current_state[index + j + 1][i + index + 1]):
                            win_token = self.current_state[index + j][i + index]
                            count += 1

                            # token appeared s times in a row, win
                            if count == (s - 1):
                                return win_token
                        # reset
                        else:
                            count = 0
                    except:
                        # index out of bounds, break
                        break
                    alarm += 1

    # chekc second diagonal line win
    def second_diagonal(self):

        # loop over rows
        for i in range(0, (n - s + 1)):
            m = 0
            # loop over columns
            for j in range((n - 1), s - 2, -1):
                # keep track of how many times win_token appears in a vertical row
                count = 0

                # protect from out of bounds error
                alarm = m

                # loop over diagonals
                for index in range(0, (n)):
                    try:

                        # index out of bounds, break
                        if j - index - 1 < 0:
                            break

                        if (self.current_state[j - index][i + index] != '.' and self.current_state[j - index][
                            i + index] == self.current_state[j - index - 1][i + index + 1]):
                            win_token = self.current_state[j - index][i + index]
                            count += 1

                            # token appeared s times in a row, win
                            if count == (s - 1):
                                return win_token
                        # reset
                        else:
                            count = 0
                    except:
                        # index out of bounds, break
                        break
                    alarm += 1
                m += 1

    # check tie
    def tie(self):
        for i in range(0, n):
            for j in range(0, n):
                if self.current_state[i][j] == '.':
                    return None
        return '.'

    # whether the winner occurs or not
    def is_end(self):
        # Vertical win
        win_token = self.vertical()
        if win_token == 'X' or win_token == 'O':
            return win_token

        # Horizontal win
        win_token = self.horizontal()
        if win_token == 'X' or win_token == 'O':
            return win_token

        # Main diagonal win
        win_token = self.main_diagonal()
        if win_token == 'X' or win_token == 'O':
            return win_token

        # Second diagonal win
        win_token = self.second_diagonal()
        if win_token == 'X' or win_token == 'O':
            return win_token

        # tie, nobody win
        win_token = self.tie()
        if win_token == '.':
            return win_token

    # 判断谁胜利 who wins ?
    def check_end(self):
        self.result = self.is_end()
        # Printing the appropriate message if the game has ended
        if self.result != None:
            if self.result == 'X':
                print('The winner is X !!!')
            elif self.result == 'O':
                print('The winner is O !!!')
            elif self.result == '.':
                print("It's a tie !!!")
            self.initialize_game()
        return self.result

    # 提示该谁下棋，要求输入坐标 show the player and input coordinates
    def input_move(self):
        while True:
            print(F'Player {self.player_turn}, enter your move:')
            px = input('enter the x coordinate: ')
            py = input('enter the y coordinate: ')
            if self.is_valid(px, py) and is_valid_positive_int(px) and is_valid_positive_int(py):
                return (int(px), int(py))
            else:
                print('The (x,y) is not valid! Try again.')

    # 轮换玩家 change player
    def switch_player(self):
        if self.player_turn == 'X':
            self.player_turn = 'O'
        elif self.player_turn == 'O':
            self.player_turn = 'X'
        return self.player_turn

    # calculate possible Wins
    def calculatePossibleWins1(self, token):
        possible_win = 0
        # row count
        for i in range(0, n):
            temp_count = 0
            for j in range(0, n - 1):
                # check if current state is empty or successive token, count +1
                if ((self.current_state[i][j] == '.' or self.current_state[i][j] == token) and
                        (self.current_state[i][j + 1] == '.' or self.current_state[i][j + 1] == token)):
                    temp_count += 1
                    if temp_count == s - 1:
                        possible_win += 1
                # reset
                else:
                    temp_count = 0

        # column count
        for i in range(0, n):
            temp_count = 0
            for j in range(0, n - 1):
                # check if current state is empty or successive token, count +1
                if ((self.current_state[j][i] == '.' or self.current_state[j][i] == token) and
                        (self.current_state[j + 1][i] == '.' or self.current_state[j + 1][i] == token)):
                    temp_count += 1
                    if temp_count == s - 1:
                        possible_win += 1
                # reset
                else:
                    temp_count = 0

        # main diagonal count
        for i in range(0, (n - s + 1)):
            for j in range(0, (n - s + 1)):
                temp_count = 0
                l = j
                # loop over diagonals
                for k in range(0, n):
                    try:
                        # index out of bounds
                        if k + j + 1 > n:
                            break
                        # check if current state is empty or successive token, count +1
                        if ((self.current_state[j + k][i + k] == '.' or self.current_state[j + k][i + k] == token) and
                                (self.current_state[j + k + 1][i + k + 1] == '.' or self.current_state[j + k + 1][
                                    i + k + 1] == token)):
                            temp_count += 1
                            if temp_count == s - 1:
                                possible_win += 1
                        # reset
                        else:
                            temp_count = 0
                    except:
                        break
                    l += 1

        # second diagonal win
        for i in range(0, (n - s + 1)):
            m = 0
            # the loop start at n-1, stops n-2+1, decreasing by 1 with each iteration
            for j in range((n - 1), s - 2, -1):
                temp_count = 0
                # protect from out of bounds error
                l = m
                # loop over diagonals
                for k in range(0, n):
                    try:
                        # index out of bounds
                        if (j - k - 1 < 0):
                            break
                        # check if current state is empty or successive token, count +1
                        if ((self.current_state[i + k][j - k] == '.' or self.current_state[i + k][j - k] == token) and
                                (self.current_state[i + k + 1][j - k - 1] == '.' or self.current_state[i + k + 1][
                                    j - k - 1] == token)):
                            temp_count += 1
                            if temp_count == s - 1:
                                possible_win += 1
                        # reset
                        else:
                            temp_count = 0
                    except:
                        break
                    l += 1
                m += 1

        return possible_win

    # e1 heuristic function
    def heuristic1(self):
        value1 = self.calculatePossibleWins1('0')  # max
        value2 = self.calculatePossibleWins1('X')  # min
        value = value1 - value2
        return value

    def calculatePossibleWins2(self, symbol, another_symbol):
        value = 0
        return value

    # e2 heuristic function
    def heuristic2(self):
        value = self.calculatePossibleWins2('0', 'X')
        return value

    def checkHasEmpty(self):
        for i in range(0, n):
            for j in range(0, n):
                if self.current_state[i][j] == '.':
                    return True
        return False

    # minimax
    def minimax(self, depth, max=False):  # max is false => the player is min
        # Minimizing for 'X' and maximizing for 'O'
        # Possible values are:
        # -100 - win for 'X' loss for '0'
        # value  - a tie
        # 100  - loss for 'X' win for '0'
        # We're initially setting it to 2000 or -2000 as worse than the worst case:
        value = 2000
        if max:
            value = -2000

        start = time.time()

        if not self.checkHasEmpty() or depth == 0:
            value = self.heuristic1()

        x = None
        y = None
        result = self.is_end()
        if result == 'X':
            return (-100, x, y)
        elif result == 'O':
            return (100, x, y)
        elif result == '.':
            return (value, x, y)
        for i in range(0, n):
            for j in range(0, n):
                if self.current_state[i][j] == '.':
                    if max:  # if the player is max => '0'
                        interrupt = time.time() - start
                        if interrupt > t:
                            break
                        self.current_state[i][j] = 'O'
                        (v, _, _) = self.minimax(depth-1, max=False)
                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:  # if the player is min => 'X'
                        interrupt = time.time() - start
                        if interrupt > t:
                            break
                        self.current_state[i][j] = 'X'
                        (v, _, _) = self.minimax(depth-1, max=True)
                        if v < value:
                            value = v
                            x = i
                            y = j
                    self.current_state[i][j] = '.'
        return (value, x, y)

    def alphabeta(self, alpha=-2000, beta=2000, depth=100, max=False):
        # Minimizing for 'X' and maximizing for 'O'
        # Possible values are:
        # -100 - win for 'X'
        # value  - a tie
        # 100 - loss for 'X'
        # We're initially setting it to 2000 or -2000 as worse than the worst case:
        value = 2000
        if max:
            value = -2000
        start = time.time()
        if not self.checkHasEmpty():
            value = self.heuristic1()
        x = None
        y = None
        result = self.is_end()
        if result == 'X':
            return (-100, x, y)
        elif result == 'O':
            return (100, x, y)
        elif result == '.':
            return (value, x, y)
        for i in range(0, n):
            for j in range(0, n):
                if self.current_state[i][j] == '.':
                    if max:
                        interrupt = time.time() - start
                        if interrupt > t:
                            break
                        self.current_state[i][j] = 'O'
                        (v, _, _) = self.alphabeta(alpha, beta, depth-1, max=False)
                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:
                        interrupt = time.time() - start
                        if interrupt > t:
                            break
                        self.current_state[i][j] = 'X'
                        (v, _, _) = self.alphabeta(alpha, beta, depth-1, max=True)
                        if v < value:
                            value = v
                            x = i
                            y = j
                    self.current_state[i][j] = '.'
                    if max:  # max think alpha
                        if value >= beta:
                            return (value, x, y)
                        if value > alpha:
                            alpha = value
                    else:  # min think beta
                        if value <= alpha:
                            return (value, x, y)
                        if value < beta:
                            beta = value
        return (value, x, y)

    def play(self, algo=None, player_x=None, player_o=None):
        if algo == None:
            algo = self.ALPHABETA
        if player_x == None:
            player_x = self.HUMAN
        if player_o == None:
            player_o = self.HUMAN
        while True:
            self.draw_board()
            if self.check_end():
                return
            start = time.time()
            if algo == self.MINIMAX:
                if self.player_turn == 'X':
                    (_, x, y) = self.minimax(d1, max=False)
                else:
                    (_, x, y) = self.minimax(d2, max=True)
            else:  # algo == self.ALPHABETA
                if self.player_turn == 'X':
                    (m, x, y) = self.alphabeta(depth=d1, max=False)
                else:
                    (m, x, y) = self.alphabeta(depth=d2, max=True)
            end = time.time()
            if (self.player_turn == 'X' and player_x == self.HUMAN) or (
                    self.player_turn == 'O' and player_o == self.HUMAN):
                if self.recommend:
                    print(F'Evaluation time: {round(end - start, 7)}s')
                    print(F'Recommended move: x = {x}, y = {y}')
                (x, y) = self.input_move()
            if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI):
                print(F'Evaluation time: {round(end - start, 7)}s')
                print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')
            self.current_state[x][y] = self.player_turn
            self.switch_player()


# get and validate parameters to initialize game's variables
def validate_Input():
    global n, b, b_locs, s, d1, d2, t
    # enter grid size
    while True:
        temp = input("Please enter grids size: ")
        if is_valid_positive_int(temp) and is_valid_bound(temp, min_bound=3, max_bound=10):
            n = int(temp)
            break
    # enter bloc number
    while True:
        temp = input("Please enter a number of blocs: ")
        if is_valid_positive_int(temp) and is_valid_bound(temp, min_bound=0, max_bound=(2 * n)):
            b = int(temp)
            b_locs = []
            # enter coordinates for each bloc
            for i in range(b):
                x_cord = 0
                y_cord = 0
                # enter coordinate
                while True:
                    valid = True
                    # get x coordinate
                    while True:
                        val_x = input("	Please enter x coordinate for bloc " + str(i + 1) + ": ")
                        if is_valid_positive_int(val_x) and is_valid_bound(val_x, max_bound=(n - 1)):
                            x_coordinate = int(val_x)
                            break

                    # get y coordinate
                    while True:
                        val_y = input("	Please enter y coordinate for bloc " + str(i + 1) + ": ")
                        if is_valid_positive_int(val_y) and is_valid_bound(val_y, max_bound=(n - 1)):
                            y_coordinate = int(val_y)
                            break
                    coordinate = (x_coordinate, y_coordinate)

                    # check the x,y coordinate already exists
                    for bloc in b_locs:
                        if bloc == coordinate:
                            valid = False
                            print(f'{coordinate} has already been in the board.')
                            break
                    if valid:
                        break
                b_locs.append(coordinate)
                print()

            break
    # enter winning line-up length
    while True:
        temp = input("Please enter winning line-up length: ")
        if is_valid_positive_int(temp) and is_valid_bound(temp, min_bound=3, max_bound=n):
            s = int(temp)
            break

    # enter max depth search for player 1
    while True:
        temp = input("Please enter max depth search for player 1 : ")
        if is_valid_positive_int(temp) and is_valid_bound(temp):
            d1 = int(temp)
            break
    # enter max depth search for player 2
    while True:
        temp = input("Please enter max depth search for player 2 : ")
        if is_valid_positive_int(temp) and is_valid_bound(temp):
            d2 = int(temp)
            break
    while True:
        temp = input("Please enter max allowed time : ")
        if is_valid_float(temp) and is_valid_bound(temp):
            t = int(temp)
            break

    # if all variables have been set
    return True


# check whether the it is positive integer or not
def is_valid_positive_int(it):
    try:
        if int(it) >= 0:
            return True
        print('please enter a positive int')
        print()
        return False
    except:
        # can not cast to integer
        print('Invalid input!')
        return False


# check if f is a float and non-negative
def is_valid_float(f):
    try:
        if float(f) >= 0:
            return True
        print("Float must be positive.")
        return False
    except:
        print("Invalid input.")
        # could not cast into float, invalid input
        return False


# check if value is within bounds
def is_valid_bound(k, min_bound=0, max_bound=sys.maxsize):
    if min_bound <= int(k) <= max_bound:
        return True
    print(f'Value must be within bounds {min_bound} - {max_bound}.')
    return False


def main():
    global n, b, b_locs, s, d1, d2, t
    # user input
    valid = validate_Input()
    print(f' n={n}, b={b}, s={s}, d1={d1}, d2={d2}, t={t}')
    print(f' blocs: {b_locs}')

    if valid:
        g = Game(n, b, b_locs, s, d1, d2, t, recommend=True)
        g.draw_board()
        # g.play(algo=Game.MINIMAX, player_x=Game.AI, player_o=Game.AI)
        # g.play(algo=Game.MINIMAX, player_x=Game.HUMAN, player_o=Game.HUMAN)
        g.play(algo=Game.MINIMAX, player_x=Game.AI, player_o=Game.HUMAN)
        # g.play(algo=Game.ALPHABETA, player_x=Game.AI, player_o=Game.AI)
        # g.play(algo=Game.ALPHABETA, player_x=Game.AI, player_o=Game.HUMAN)
        # g.play(algo=Game.ALPHABETA, player_x=Game.HUMAN, player_o=Game.HUMAN)


if __name__ == "__main__":
    main()
