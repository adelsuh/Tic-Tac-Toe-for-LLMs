#write to all_tictactoe.jsonl
#fine-tune on all possible games -> See if that leads to an "understanding"

import jsonlines
from collections import defaultdict
import copy

class GameState:
	def __init__(self, board, turn):
		self.board = board
		self.turn = turn

gameStates = [GameState([["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]], "O"),
	GameState([["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]], "X")]

def returnStrGameState(board):
	lines = [" | ".join(line)+"\n" for line in board]
	return "---------\n".join(lines)

def checkThreeVals(a, b, c):
	if a == b and b==c:
		return True, a
	else:
		return False, "-"

straights = [[(0,0), (0,1), (0,2)], [(1,0), (1,1), (1,2)], [(2,0), (2,1), (2,2)], #rows
	[(0,0), (1,0), (2,0)], [(0,1), (1,1), (2,1)], [(0,2), (1,2), (2,2)], #cols
	[(0,0), (1,1), (2,2)], [(0,2), (1,1), (2,0)]] #diagonals

def checkEndGameState(board): #returns True for endgame and winner "O"/"X"/Tie "-"
	for a,b,c in straights:
		same, winner = checkThreeVals(board[a[0]][a[1]], board[b[0]][b[1]], board[c[0]][c[1]])
		if same:
			return True, winner
	if all([square=="O" or square=="X" for row in board for square in row]):
		return True, "-"

	return False, "-"

def generateSuccessor(board, actor):
	successors = []
	actions = []
	for i in range(3):
		for j in range(3):
			if board[i][j] != "O" and board[i][j] != "X":
				successor = copy.deepcopy(board)
				successor[i][j] = actor
				successors.append(GameState(successor, "O" if actor=="X" else "X"))
				actions.append((i,j))
	return actions, successors

def actionToString(action):
	return str(action[0]*3+action[1]+1)

def gameStateToSystemMsg(board, actor, action, successor):
	msg = "The game board currently looks likes this.\n"
	msg += returnStrGameState(board)
	msg += "\nI place "+actor+" on square "+actionToString(action)+". Now the game board looks like this.\n"
	msg += returnStrGameState(successor)
	return msg

system = [{"role": "system", "content": "We are playing tic-tac-toe."}]

with jsonlines.open('all_tictactoe.jsonl', mode='w') as writer:
	while len(gameStates) > 0:
		gameState = gameStates.pop(0)
		#If beginning state, AI always starts

		actions, successors = generateSuccessor(gameState.board, gameState.turn)
		for action, successor in zip(actions, successors):
			firstmsg = gameStateToSystemMsg(gameState.board, gameState.turn, action, successor.board)
			isEnd, winner = checkEndGameState(successor.board)
			if isEnd:
				continue
			gameStates.append(successor)
			exchangeFirst = [{"role": "assistant", "content": firstmsg}]
			#print(firstmsg)

			actionsUser, successorsUser = generateSuccessor(successor.board, successor.turn)
			for actionUser, successorUser in zip(actionsUser, successorsUser):
				exchangeSecond = copy.deepcopy(exchangeFirst)
				#print(f'\nI place {successor.turn} on square {actionToString(actionUser)}.\n')
				exchangeSecond.append({"role": "user", "content": f'I place {successor.turn} on square {actionToString(actionUser)}.'})
				
				lastmsg = "The game board currently looks likes this.\n"
				lastmsg += returnStrGameState(successorUser.board)
				isEnd, winner = checkEndGameState(successorUser.board)
				if isEnd:
					endmsg = copy.deepcopy(lastmsg)
					endmsg += "\nThe game is over. "
					if winner == "-":
						endmsg += "It's a tie!"
					else:
						endmsg += winner + " wins the game!"
					#print(lastmsg)
					writer.write({"messages": system + exchangeSecond + 
						[{"role": "assistant", "content": endmsg}, {"role": "user", "content": "Okay!"}]})
					continue

				actionsLast, successorsLast = generateSuccessor(successorUser.board, successorUser.turn)
				for actionLast, successorLast in zip(actionsLast, successorsLast):
					endmsg = copy.deepcopy(lastmsg)
					endmsg += f'\nI place {successorUser.turn} on square {actionToString(actionLast)}. Now the game board looks like this.\n'
					endmsg += returnStrGameState(successorLast.board)
					isEnd, winner = checkEndGameState(successorLast.board)
					if isEnd:
						endmsg += "\nThe game is over. "
						if winner == "-":
							endmsg += "It's a tie!"
						else:
							endmsg += winner + " wins the game!"
					#print(lastmsg)
					writer.write({"messages": system + exchangeSecond + [{"role": "assistant", "content": endmsg}]})

