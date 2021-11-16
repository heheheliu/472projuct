# 472projuct
fall 2021 472 mini project team
Liu He, Zhihong Qian, Ni Zeng
# Game of Line ’em Up

Implement an adversarial search for the game of Line ’em up for values of ** n**, **s** and**b** given as input.


## Implement Game
a skeleton code which implements a standard tic-tac-toe game (i.e. with n=3, b=0 and s=3) is available to start: then we implement the fllowing:


### 1.using mini-max function and alpha-beta function
### 2.develop 2 heuristics e1 and e2 
e1 be a very simple but fast heuristic, and e2 be more sophisticated and complex to compute.
### 3.Game Parameters: 
(a) the size of the board – n – an integer in [3..10]
(b) the number of blocs – b – an integer in [0..2n]
(c) the positions of the blocs – b board coordinates
(d) the winning line-up size – s – an integer in [3..n]
(e) the maximum depth of the adversarial search for player 1 and for player 2 – 2 integers d1 and d2 (f) the maximum allowed time (in seconds) for your program to return a move – t
(g) a Boolean to force the use of either minimax (FALSE) or alphabeta (TRUE) – a (h) the play modes: 
H-H, H-AI, AI-H and AI-AI.



## The Output

Generated 2 types of output ﬁles: game traces and a scoreboard with statistics of multiple games. 

### Game Trace Files

1.	The parameters of the game: the values of n, b, s, t
2.	The position of the blocs
3.	The parameters of each player: the values human or AI, and in the case of an AI, the corresponding values of the depth of the search (d1 or d2), the corresponding values of the alphabeta vs minimax of the search (a1 or a2, or both) and which heuristic was used (e1 or e2).
4.	A display of the initial conﬁguration of the board.
5.
(a) the move taken (eg. B 4)
(b) the new conﬁguration of the board
and statistics:
i.	The evaluation time of the heuristic (in seconds)
ii.	The number of states evaluated by the heuristic function
iii.	The number of states evaluated at each depth (consider the root to be at depth 0)
The number of states evaluated at each depth. 
iv.	The average depth (AD) of the heuristic evaluation in the tree
v.	The average recursion depth (ARD) at the current state
6.	Then, at the end of the game, display:
(a) the winner
(b) for each heuristic, the following statistics:
i.	The average evaluation time of the heuristic for each state evaluated (in seconds)
ii.	The number of states evaluated by the heuristic function during the entire game
iii. The average of the per-move average depth of the heuristic evaluation in the tree – i.e. the average of statistic 4(c)iii above for all moves
iv.	The total number of states evaluated at each depth during the entire game
v.	The average of the per-move average recursion depth 
vi.	The total number of moves in the game

### Scoreboard File
Display the following information:
1.	The parameters of the game (the values of n, b, l, t)
2.	The parameters of each player: their max search depth (d1 and d2)), their alphabeta or minimax (a1 and a1) and their heuristic
3.	The number of games played (the value of 2×r)
4.	The number and percentage of wins for heuristic e1 and for heuristic e2
5.	All the information displayed at the end of a game , but averaged over 2×s games
## Programming Environment
Use Python 3.7. Using the PyPy1 runtime
GitHub to develop your project
