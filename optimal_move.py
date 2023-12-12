from optimal_tictactoe import *

while True:
	board = input("Board: ")
	board = [[board[0], board[1], board[2]],
	[board[3], board[4], board[5]],
	[board[6], board[7], board[8]]]
	actor = input("Actor: ")
	actions, successors = generateOptimalSuccessor(board, actor)
	print(actions)
