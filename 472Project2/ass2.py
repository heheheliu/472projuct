# based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python

import time
import sys
from enum import Enum
import numpy as np

# global variables
global n, b, b_locs, s, d1, d2, t, a, p1e, p2e, player1, player2

# global time variables
global start, time_interrupt
# states count
data_run = []

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
    E1 = 4
    E2 = 5
    e1_win = 0
    e2_win = 0
    game_times = 0

    total_Evaluation_Time = 0
    total_moves = 0
    total_heuristic_eval_num = 0
    total_eval_depth = {}
    total_avg_eval_depth = 0

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

    # the game board structure
    def initialize_game(self):

        for i in range(n):
            row = []
            for j in range(n):
                # add bloc '*'

                if (i, j) in self.b_locs:
                    row.append('*')
                else:
                    row.append('.')

            self.current_state.append(row)
        # Player X always plays first
        self.player_turn = 'X'

    # draw board
    def draw_board(self, f=None):

        print()
        # print column header
        print(' ', file=f)
        for i in range(0, n):
            print(F'  {Letter(i).name}', end="")
            print(F'  {Letter(i).name}', end="", file=f)

        print()
        # draw the board
        for x in range(0, n):
            for y in range(0, n):
                if y == 0:
                    # print row header
                    print(F'\n{x}', end="")
                    print(F'|', end="")
                    print(F'\n{x}', end="", file=f)
                    print(F'|', end="", file=f)

                # draw row content
                print(self.current_state[x][y], end="  ")
                print(self.current_state[x][y], end="  ", file=f)

            print()
        print()

    # check whether the input coordinate is valid or not
    def is_valid(self, px, py):
        if is_valid_positive_int(px) and is_valid_positive_int(py):
            # if int(px) >= n or int(py) >= n:
            #     return False
            if self.current_state[int(px)][int(py)] != '.':
                return False
            else:
                print(f'this ({px} , {py}) coordinate is valid')
                return True
        return False

    # check p coordinate is a valid integer
    def is_valid_p(self, p):
        if is_valid_positive_int(p):
            if int(p) >= n:
                return False
            else:
                return True
        else:
            print(f"{p} is not valid number!")

    # check the input is valid Letter
    def is_valid_letter(self, px):
        if px.isalpha() and len(px) == 1:
            try:
                if self.is_valid_p(Letter[px.upper()].value):
                    return True
                else:
                    print(f'{px} is not a valid Letter!')
                    return False
            except KeyError:
                print(f'{px} is not valid letter')
        else:
            print(f'{px} must be a Letter!')
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

    def reset_data(self):
        global data_run
        data_run = []
        # initiating data_run list for statistics
        if d1 > d2:
            # instantiate_Data_run(d1)
            for i in range(0, d1 + 1):
                data_run.append(-88)
        else:
            # instantiate_Data_run(d2)
            for i in range(0, d2 + 1):
                data_run.append(-88)

    def output_stats(self):  # This will evaluate the data and output the statistics
        print(f"The total of {len(data_run)} states :")
        i = 0
        count = 0
        while True:
            for data in data_run:
                if data == i:
                    count = count + 1
            if (count == 0):
                break
            print(f"Depth {i} has {count} members")
            i = i + 1
            count = 0

    #  who wins ?
    def check_end(self,  f=None):
        self.result = self.is_end()
        # Printing the appropriate message if the game has ended
        if self.result is not None:
            if self.result == 'X':
                self.e1_win += 1
                print('The winner is X !!!')
                f.write('\nThe winner is X !!! \n')
            elif self.result == 'O':
                self.e2_win += 1
                print('The winner is O !!!')
                f.write('\nThe winner is O !!! \n')
            elif self.result == '.':
                self.e1_win += 1
                self.e2_win += 1
                print("It's a tie !!!")
                f.write("\nIt's a tie! \n")
            # print(f'the total number of {len(data_run)} states: ')
            # depth = 0
            # count = 0
            # while True:
            #     for index in data_run:
            #         if index == depth:
            #             count = count + 1
            #     if count == 0:
            #         break
            #     print(f'depth {depth} has {count} states. ')
            #     depth = depth + 1
            #     count = 0

            self.initialize_game()
        return self.result

    #  show the player and input coordinates
    def input_move(self):
        while True:
            print(F'Player {self.player_turn}, enter your move:')

            # check the px coordinate
            while True:
                px = input('enter the x coordinate: ')
                if self.is_valid_p(px):
                    break

            while True:
                # check py coordinate
                py_Letter = input('enter the y coordinate: ')
                if self.is_valid_letter(py_Letter):
                    py = str(Letter[py_Letter.upper()].value)
                    break
            # check (px,py) coordinate is valid
            if self.is_valid(px, py):
                return (int(px), int(py))
            else:
                print('The (x,y) is not valid! Try again.')

    # change player
    def switch_player(self):
        if self.player_turn == 'X':
            self.player_turn = 'O'
        elif self.player_turn == 'O':
            self.player_turn = 'X'
        return self.player_turn

    # calculate possible Wins
    def calculatePossibleWins1(self, symbol):
        possible_win = 0
        # row count
        for i in range(0, n):
            temp_count = 0
            for j in range(0, n - 1):
                # check if current state is empty or successive token, count +1
                if ((self.current_state[i][j] == '.' or self.current_state[i][j] == symbol) and
                        (self.current_state[i][j + 1] == '.' or self.current_state[i][j + 1] == symbol)):
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
                if ((self.current_state[j][i] == '.' or self.current_state[j][i] == symbol) and
                        (self.current_state[j + 1][i] == '.' or self.current_state[j + 1][i] == symbol)):
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
                        if ((self.current_state[j + k][i + k] == '.' or self.current_state[j + k][i + k] == symbol) and
                                (self.current_state[j + k + 1][i + k + 1] == '.' or self.current_state[j + k + 1][
                                    i + k + 1] == symbol)):
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
                        if ((self.current_state[i + k][j - k] == '.' or self.current_state[i + k][j - k] == symbol) and
                                (self.current_state[i + k + 1][j - k - 1] == '.' or self.current_state[i + k + 1][
                                    j - k - 1] == symbol)):
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
        result = self.is_end()
        # min win
        if result == 'X':
            return -5000000
        # max win
        elif result == 'O':
            return 5000000

        value1 = self.calculatePossibleWins1('0')  # max
        value2 = self.calculatePossibleWins1('X')  # min
        value = value1 - value2
        return value

    def calculatePossibleWins2(self, max_symbol, min_symbol):
        score = 0
        # diagonal calculate
        board = np.array(self.current_state)
        diags = [board[::-1, :].diagonal(i) for i in range(-board.shape[0] + 1, board.shape[1])]
        diags.extend(board.diagonal(i) for i in range(board.shape[1] - 1, -board.shape[0], -1))

        for arr in diags:
            if arr.size >= s:
                count_max = 0
                count_min = 0

                for k in arr:
                    if k == '0':
                        count_max = count_max + 1
                    if k == 'X':
                        count_min = count_min + 1
                score += self.calculate_score(count_max, count_min, score)
        # row calculate
        for i in range(0, n):
            count_max = 0
            count_min = 0
            for j in range(0, n):
                if self.current_state[i][j] == '0':
                    count_max += 1
                if self.current_state[i][j] == 'X':
                    count_min += 1
            score += self.calculate_score(count_max, count_min, score)

        # column calculate
        for i in range(0, n):
            count_max = 0
            count_min = 0
            for j in range(0, n):
                if self.current_state[j][i] == '0':
                    count_max += 1
                if self.current_state[j][i] == 'X':
                    count_min += 1
            score += self.calculate_score(count_max, count_min, score)

        return score

    def calculate_score(self, count_max, count_min, score):
        if count_max == 10:
            score = score + 100000
        elif count_min == 10:
            score = score - 100000
        elif count_max == 9:
            score = score + 50000
        elif count_min == 9:
            score = score - 50000
        elif count_max == 8:
            score = score + 20000
        elif count_min == 8:
            score = score - 20000
        elif count_max == 7:
            score = score + 6000
        elif count_min == 7:
            score = score - 6000
        elif count_max == 6:
            score = score + 1500
        elif count_min == 6:
            score = score - 1500
        elif count_max == 5:
            score = score + 400
        elif count_min == 5:
            score = score - 400
        elif count_max == 4:
            score = score + 100
        elif count_min == 4:
            score = score - 100
        elif count_max == 3:
            score = score + 25
        elif count_min == 3:
            score = score - 25
        elif count_max == 2:
            score = score + 5
        elif count_min == 2:
            score = score - 5
        elif count_max == 1:
            score = score + 1
        elif count_min == 1:
            score = score - 1
        return score

    # e2 heuristic function
    def heuristic2(self):
        result = self.is_end()
        # min win
        if result == 'X':
            return -5000000
        # max win
        elif result == 'O':
            return 5000000

        value = self.calculatePossibleWins2('0', 'X')
        return value

    # def checkHasEmpty(self):
    #     for i in range(0, n):
    #         for j in range(0, n):
    #             if self.current_state[i][j] == '.':
    #                 return True
    #     return False

    # minimax
    def minimax(self, depth=0, depth_max=0, max=False, e=E1):  # max is false = player is min
        # Minimizing for 'X' and maximizing for 'O'
        # Possible values are:
        # -100 - win for 'X' loss for '0'
        # value  - a tie
        # 100  - loss for 'X' win for '0'
        # We're initially setting it to 50000 or -50000 as worse than the worst case:

        value = 500000
        if max:
            value = -500000
        # if not self.checkHasEmpty():
        #     value = self.heuristic1()
        x = None
        y = None

        for i in range(0, n):
            for j in range(0, n):
                # find a empty cell, can put token
                if self.current_state[i][j] == '.':
                    if x is None:
                        x = i
                    if y is None:
                        y = j
                    # if not reach the depth max, can call recursive minimax function
                    if depth < depth_max:
                        if max:  # if the player is max => '0'
                            interrupt = time.time() - start
                            if interrupt > time_interrupt:
                                if e == self.E1:
                                    v = self.heuristic1()
                                else:
                                    v = self.heuristic2()
                                if v > value:
                                    value = v
                                    x = i
                                    y = j
                                return (value, x, y)

                            self.current_state[i][j] = 'O'
                            (v, _, _) = self.minimax(depth=depth + 1, depth_max=depth_max, max=False)
                            if v > value:
                                value = v
                                x = i
                                y = j
                        else:  # if the player is min => 'X'
                            interrupt = time.time() - start
                            if interrupt > time_interrupt:
                                if e == self.E1:
                                    v = self.heuristic1()
                                else:
                                    v = self.heuristic2()
                                if v < value:
                                    value = v
                                    x = i
                                    y = j
                                return (value, x, y)

                            self.current_state[i][j] = 'X'
                            (v, _, _) = self.minimax(depth=depth + 1, depth_max=depth_max, max=True)
                            if v < value:
                                value = v
                                x = i
                                y = j
                        self.current_state[i][j] = '.'
                    # if depth reach the max depth
                    else:
                        if max:
                            if e == self.E1:
                                v = self.heuristic1()
                            else:
                                v = self.heuristic2()
                            if v > value:
                                value = v
                                x = i
                                y = j
                        else:
                            if e == self.E1:
                                v = self.heuristic1()
                            else:
                                v = self.heuristic2()
                            if v < value:
                                value = v
                                x = i
                                y = j

                    # if x is None or y is None:
                    #     x = i
                    #     y = j

                    # store the states number at this depth
                    data_run.append(depth)

        return (value, x, y)

    def alphabeta(self, alpha=-2000, beta=2000, depth=0, depth_max=0, max=False, e=E1):
        # Minimizing for 'X' and maximizing for 'O'
        # Possible values are:
        # -100 - win for 'X'
        # value  - a tie
        # 100 - loss for 'X'
        # We're initially setting it to 50000 or -50000 as worse than the worst case:

        value = 500000
        if max:
            value = -500000

        # if not self.checkHasEmpty() or depth == 0:
        #     value = self.heuristic1()
        x = None
        y = None

        for i in range(0, n):
            for j in range(0, n):
                if self.current_state[i][j] == '.':
                    if x is None:
                        x = i
                    if y is None:
                        y = j
                    if depth < depth_max:
                        if max:
                            interrupt = time.time() - start
                            if interrupt > time_interrupt:
                                if e == self.E1:
                                    v = self.heuristic1()
                                else:
                                    v = self.heuristic2()
                                if v > value:
                                    value = v
                                    x = i
                                    y = j
                                return (value, x, y)
                            self.current_state[i][j] = 'O'
                            (v, _, _) = self.alphabeta(alpha, beta, depth=depth + 1, depth_max=depth_max, max=False)
                            if v > value:
                                value = v
                                x = i
                                y = j
                        else:
                            interrupt = time.time() - start
                            if interrupt > time_interrupt:
                                if e == self.E1:
                                    v = self.heuristic1()
                                else:
                                    v = self.heuristic2()
                                if v < value:
                                    value = v
                                    x = i
                                    y = j
                                return (value, x, y)
                            self.current_state[i][j] = 'X'
                            (v, _, _) = self.alphabeta(alpha, beta, depth=depth + 1, depth_max=depth_max, max=True)
                            if v < value:
                                value = v
                                x = i
                                y = j
                        self.current_state[i][j] = '.'
                    # reach the max depth
                    else:
                        if max:
                            if e == self.E1:
                                v = self.heuristic1()
                            else:
                                v = self.heuristic2()
                            if v > value:
                                value = v
                                x = i
                                y = j
                        else:
                            if e == self.E1:
                                v = self.heuristic1()
                            else:
                                v = self.heuristic2()
                            if v < value:
                                value = v
                                x = i
                                y = j
                    # if x is None or y is None:
                    #     x = i
                    #     y = j
                    if max:  # if parent alpha >= child beta, prune the child right branch
                        if value >= beta:
                            return (value, x, y)
                        if value > alpha:
                            alpha = value
                    else:  # # if parent beta <= child alpha , prune the child right branch
                        if value <= alpha:
                            return (value, x, y)
                        if value < beta:
                            beta = value

                    # store the states number at this depth
                    data_run.append(depth)

        return (value, x, y)

    def play(self, algo=None, player_x=None, player_o=None, p1e=E1, p2e=E2, f=None):
        self.game_times += 1
        global start, time_interrupt
        self.reset_data()

        if algo:
            algo = self.ALPHABETA
        else:
            algo = self.MINIMAX

        if player_x is None:
            player_x = self.HUMAN
        if player_o is None:
            player_o = self.HUMAN
        while True:
            print(' ', file=f)
            self.total_moves += 1
            print(f'(move  #{self.total_moves})')
            print(f'(move  #{self.total_moves})', file=f)
            self.draw_board(f=f)
            if self.check_end(f=f):
                return
            start = time.time()
            if algo == self.MINIMAX:
                # start = time.time()
                if self.player_turn == 'X':
                    (_, x, y) = self.minimax(depth_max=d1, max=False, e=p1e)
                else:
                    (_, x, y) = self.minimax(depth_max=d2, max=True, e=p2e)
            else:  # algo == self.ALPHABETA
                # start = time.time()
                if self.player_turn == 'X':
                    (m, x, y) = self.alphabeta(depth_max=d1, max=False, e=p1e)
                else:
                    (m, x, y) = self.alphabeta(depth_max=d2, max=True, e=p2e)
            end = time.time()
            self.total_Evaluation_Time += round(end - start, 7)
            if (self.player_turn == 'X' and player_x == self.HUMAN) or (
                    self.player_turn == 'O' and player_o == self.HUMAN):
                if self.recommend:
                    print(F'\n\ni Evaluation time: {round(end - start, 7)}s \n')
                    print(F'\n\ni Evaluation time: {round(end - start, 7)}s \n', file=f)
                    print(F'Recommended move: x = {x}, y = {Letter(y).name} \n')
                    print(F'Recommended move: x = {x}, y = {Letter(y).name} \n', file=f)

                (x, y) = self.input_move()
            if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI):
                print(F'\n\ni Evaluation time: {round(end - start, 7)}s \n')
                print(F'\n\ni Evaluation time: {round(end - start, 7)}s \n', file=f)
                print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {Letter(y).name} \n')
                print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {Letter(y).name} \n', file=f)
            # print(data_run)
            # print(len(data_run))

            count_arr = {}
            # print(count_arr)
            num = max(data_run)
            sum = 0
            ad = 0
            for i in range(num + 1):
                count = 0
                for j in data_run:
                    if j == i:
                        count += 1

                count_arr[i+1] = count
                if self.total_eval_depth.get(i+1) is None:
                    self.total_eval_depth[i+1] = count
                else:
                    self.total_eval_depth[i+1] = self.total_eval_depth[i+1] + count
                sum += count
                ad += (i+1) * count
            if sum != 0:
                ad = ad / sum
            else:
                ad = ad / 1
            self.total_heuristic_eval_num += sum
            # print(self.total_eval_depth)

            print(f"ii Heuaristic evaluation: {sum} \n")
            print(f"ii Heuaristic evaluation: {sum} \n", file=f)
            print(f"iii Evaluations by depth: {count_arr} \n")
            print(f"iii Evaluations by depth: {count_arr} \n", file=f)
            print(f"iv Average evaluation depth: {round(ad, 2)} \n")
            print(f"iv Average evaluation depth: {round(ad, 2)} \n", file=f)

            self.reset_data()

            self.current_state[x][y] = self.player_turn
            self.switch_player()


# get and validate parameters to initialize game's variables
def validate_Input():
    global n, b, b_locs, s, d1, d2, t, a, p1e, p2e, player1, player2, time_interrupt
    # enter grid size
    while True:
        temp = input("Please enter board size: ")
        if is_valid_positive_int(temp) and is_valid_bound(temp, min_bound=MIN_GRID_SIZE, max_bound=MAX_GRID_SIZE):
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
                x_coordinate = 0
                y_coordinate = 0
                # enter coordinate
                while True:
                    valid = True
                    # get x coordinate
                    while True:
                        val_x = input("	Please enter X coordinate for bloc " + str(i + 1) + ": ")
                        if is_valid_positive_int(val_x) and is_valid_bound(val_x, max_bound=(n - 1)):
                            x_coordinate = int(val_x)
                            break

                    # get y coordinate
                    while True:
                        val_y = input("	Please enter Y coordinate for bloc " + str(i + 1) + ": ")
                        if is_valid_letter(val_y.upper()) and is_valid_positive_int(
                                str(Letter[val_y.upper()].value)) and is_valid_bound(
                            str(Letter[val_y.upper()].value), max_bound=(n - 1)):
                            y_coordinate = Letter[val_y.upper()].value
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
    # enter max allowed time to interrupt
    while True:
        temp = input("Please enter max allowed time : ")
        if is_valid_float(temp) and is_valid_bound(temp):
            t = int(temp)
            time_interrupt = t * 99 / 100
            break
    while True:
        temp = int(input("Please enter the choice between minimax (0) or alphabeta (1): "))
        if temp == 0:
            a = False
            break
        elif temp == 1:
            a = True
            break
        else:
            print("Your input must be either 0 for minimax or 1 for alphabeta! Please try again.")

    while True:
        temp = int(input("Should player 1 be human controlled? Enter 1 for yes, 0 for no: "))
        if temp == 1:
            player1 = Game.HUMAN
            break
        elif temp == 0:
            player1 = Game.AI
            break
        else:
            print("Your input must be either 0 for no or 1 for yes! Please try again.")
    while True:
        temp = int(input("Should player 2 be human controlled? Enter 1 for yes, 0 for no: "))
        if temp == 1:
            player2 = Game.HUMAN
            break
        elif temp == 0:
            player2 = Game.AI
            break
        else:
            print("Your input must be either 0 for no or 1 for yes! Please try again.")

    while True:
        temp = int(input("Choose the heuristic function for player 1. Enter 1 for e1 or 0 for e2: "))
        if temp == 1:
            p1e = Game.E1
            break
        elif temp == 0:
            p1e = Game.E2
            break
        else:
            print("Your input must be either 0 for e2 or 1 for p1e! Please try again.")
    while True:
        temp = int(input("Choose the heuristic function for player 2. Enter 1 for e1 or 0 for e2: "))
        if temp == 1:
            p2e = Game.E1
            break
        elif temp == 0:
            p2e = Game.E2
            break
        else:
            print("Your input must be either 0 for e2 or 1 for p2e! Please try again.")
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


# check the input is valid Letter
def is_valid_letter(px):
    if px.isalpha() and len(px) == 1:
        try:
            if is_valid_positive_int(Letter[px.upper()].value):
                return True
            else:
                return False
        except KeyError:
            print(f'{px} is not valid letter')
    else:
        print(f'The input must be a Letter!')
        return False


def final_summary(f_score, g, a):

    print(f'n={g.n} b={g.b} s={g.s} t={g.t}', file=f_score)

    print(f'Player 1: d={g.d1} a={a}', file=f_score)
    print(f'Player 2: d={g.d2} a={a}', file=f_score)

    print(f'{g.game_times} game(s)', file=f_score)

    print("Total wins for heuristic e1: {} ({}%) (regular)".format(g.e1_win, g.e1_win * 100 / (g.e1_win + g.e2_win)),
          file=f_score)
    print("Total wins for heuristic e2: {} ({}%) (defensive)".format(g.e2_win, g.e2_win * 100 / (g.e1_win + g.e2_win)),
          file=f_score)
    print("i:   Average evaluation time: {}".format(g.total_Evaluation_Time / g.game_times), file=f_score)
    print("ii   Total heuristic evaluations: {}".format(g.total_heuristic_eval_num), file=f_score)
    print("iii   Evaluations by depth: {}".format(g.total_eval_depth), file=f_score)
    n = 0
    t = 0
    for i in g.total_eval_depth.keys():
        t += i * g.total_eval_depth.get(i)
        n += g.total_eval_depth.get(i)
    ad = t / n
    print("iv   Average evaluation depth: {}".format(ad/g.game_times), file=f_score)
    print("vi:  Average Total moves: {}".format(g.total_moves/g.game_times), file=f_score)




def main():
    global n, b, b_locs, s, d1, d2, t, a, p1e, p2e, player1, player2, e1_win, e2_win
    # user input
    valid = validate_Input()
    file_name = 'gameTrace-{}{}{}{}.txt'.format(n, b, s, t)
    f = open(file_name, "w+")
    score_board = 'scoreboard.txt'
    f_score = open(score_board, 'w+')
    print(f' n={n}, b={b}, s={s}, d1={d1}, d2={d2}, t={t}\n')
    print(f' n={n}, b={b}, s={s}, d1={d1}, d2={d2}, t={t}\n', file=f)
    print(f' blocs: {b_locs}\n')
    print(f' blocs: {b_locs}\n', file=f)
    print('Player 1: AI d={} a={} {}(regular)'.format(d1, a, 'e1' if p1e == 4 else 'e2'))
    print('Player 1: AI d={} a={} {}(regular)'.format(d1, a, 'e1' if p1e == 4 else 'e2'), file=f)
    print('Player 2: AI d={} a={} {}(defensive)'.format(d2, a, 'e1' if p2e == 4 else 'e2'))
    print('Player 2: AI d={} a={} {}(defensive)'.format(d2, a, 'e1' if p2e == 4 else 'e2'), file=f)

    if valid:
        if a:
            algo = Game.ALPHABETA
        else:
            algo = Game.MINIMAX
        g = Game(n, b, b_locs, s, d1, d2, t, recommend=True)
        g.draw_board(f=f)
        g.play(algo=algo, player_x=player1, player_o=player2, p1e=p1e, p2e=p2e, f=f)
        g.play(algo=algo, player_x=player1, player_o=player2, p1e=p1e, p2e=p2e, f=f)
        g.play(algo=algo, player_x=player1, player_o=player2, p1e=p1e, p2e=p2e, f=f)
        g.play(algo=algo, player_x=player1, player_o=player2, p1e=p1e, p2e=p2e, f=f)
        g.play(algo=algo, player_x=player1, player_o=player2, p1e=p1e, p2e=p2e, f=f)
        g.play(algo=algo, player_x=player1, player_o=player2, p1e=p1e, p2e=p2e, f=f)
        g.play(algo=algo, player_x=player1, player_o=player2, p1e=p1e, p2e=p2e, f=f)
        g.play(algo=algo, player_x=player1, player_o=player2, p1e=p1e, p2e=p2e, f=f)
        g.play(algo=algo, player_x=player1, player_o=player2, p1e=p1e, p2e=p2e, f=f)
        g.play(algo=algo, player_x=player1, player_o=player2, p1e=p1e, p2e=p2e, f=f)
        # g.play(algo=Game.MINIMAX, player_x=Game.HUMAN, player_o=Game.HUMAN)
        # g.play(algo=Game.MINIMAX, player_x=Game.AI, player_o=Game.HUMAN)
        # g.play(algo=Game.ALPHABETA, player_x=Game.AI, player_o=Game.AI)
        # g.play(algo=Game.ALPHABETA, player_x=Game.AI, player_o=Game.HUMAN)
        # g.play(algo=Game.ALPHABETA, player_x=Game.HUMAN, player_o=Game.HUMAN)
        print("6(b)i   Average evaluation time: {}".format(g.total_Evaluation_Time / g.total_moves))
        print("6(b)ii   Total heuristic evaluations: {}".format(g.total_heuristic_eval_num))
        print("6(b)iii   Evaluations by depth: {}".format(g.total_eval_depth))
        n = 0
        t = 0
        for i in g.total_eval_depth.keys():
            t += i * g.total_eval_depth.get(i)
            n += g.total_eval_depth.get(i)
        ad = t / n
        print("6(b)iv   Average evaluation depth: {}".format(ad))
        print("6(b)vi  Total moves: {}".format(g.total_moves))

        print("6(b)i   Average evaluation time: {}".format(g.total_Evaluation_Time / g.total_moves), file=f)
        print("6(b)ii   Total heuristic evaluations: {}".format(g.total_heuristic_eval_num), file=f)
        print("6(b)iii   Evaluations by depth: {}".format(g.total_eval_depth), file=f)
        print("6(b)iv   Average evaluation depth: {}".format(ad), file=f)
        print("6(b)vi  Total moves: {}".format(g.total_moves), file=f)

        final_summary(f_score=f_score, g=g, a=a)




if __name__ == "__main__":
    main()
