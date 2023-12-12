#write to optimal_tictactoe.jsonl
#optimal on the side of the AI, random on the side of the user

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
	result = ""
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

def get(arr, tup):
	return arr[tup[0]][tup[1]]

def getNearWin(board, actor):
	nearWins = []
	for a, b, c in straights:
		if get(board,a)==actor and get(board,b)==actor and get(board,c).isnumeric():
			nearWins.append(c)
		if get(board,a)==actor and get(board,c)==actor and get(board,b).isnumeric():
			nearWins.append(b)
		if get(board,b)==actor and get(board,c)==actor and get(board,a).isnumeric():
			nearWins.append(a)
	return nearWins

def generateOptimalSuccessor(board, actor, mode="quiet"):
	opponent = "O" if actor=="X" else "X"

	#Win
	nearWins = getNearWin(board, actor)
	if len(nearWins)>0:
		successors = []
		for nearWin in nearWins:
			successor = copy.deepcopy(board)
			successor[nearWin[0]][nearWin[1]] = actor
			successors.append(GameState(successor, opponent))
		if mode=="verbose":
			return nearWins, successors, "Win"
		return nearWins, successors

	#Block
	nearLosses = getNearWin(board, opponent)
	if len(nearLosses)>0:
		successors = []
		for nearLoss in nearLosses:
			successor = copy.deepcopy(board)
			successor[nearLoss[0]][nearLoss[1]] = actor
			successors.append(GameState(successor, opponent))
		if mode=="verbose":
			return nearLosses, successors, "Block"
		return nearLosses, successors

	#Fork
	actions = []
	successors = []
	for i in range(3):
		for j in range(3):
			if board[i][j].isnumeric():
				successor = copy.deepcopy(board)
				successor[i][j] = actor
				nearWins = getNearWin(successor, actor)
				if len(nearWins)>1:
					actions.append((i,j))
					successors.append(GameState(successor, opponent))
	if len(actions)>0:
		if mode=="verbose":
			return actions, successors, "Fork"
		return actions, successors

	#ForkBlock
	blocks = []
	betterBlocks = []
	makeTwo = []
	forkPossible = False
	for a in range(3):
		for b in range(3):
			if board[a][b].isnumeric():
				successor = copy.deepcopy(board)
				successor[a][b] = actor
				nearWinNum = len(getNearWin(successor, actor))
				if nearWinNum > 0:
					makeTwo.append((a,b))
				results = []
				for c in range(3):
					for d in range(3):
						if successor[c][d].isnumeric():
							successor[c][d] = opponent
							results.append(len(getNearWin(successor, opponent)))
							successor[c][d] = str(3*c+d+1)
				if all(result<2 for result in results):
					blocks.append((a,b))
					if nearWinNum > 0:
						betterBlocks.append((a,b))
				else:
					forkPossible = True
	if forkPossible:
		if len(blocks)>0:
			if len(betterBlocks)>0:
				for block in betterBlocks:
					successor = copy.deepcopy(board)
					successor[block[0]][block[1]] = actor
					successors.append(GameState(successor, opponent))
				if mode=="verbose":
					return betterBlocks, successors, "ForkBlock betterBlocks"
				return betterBlocks, successors
			for block in blocks:
				successor = copy.deepcopy(board)
				successor[block[0]][block[1]] = actor
				successors.append(GameState(successor, opponent))
			if mode=="verbose":
				return blocks, successors, "ForkBlock blocks"
			return blocks, successors
		if len(makeTwo)>0:
			for action in makeTwo:
				successor = copy.deepcopy(board)
				successor[action[0]][action[1]] = actor
				successors.append(GameState(successor, opponent))
			if mode=="verbose":
				return makeTwo, successors, "ForkBlock makeTwo"
			return makeTwo, successors

	#Center
	if board[1][1].isnumeric():
		successor = copy.deepcopy(board)
		successor[1][1] = actor
		if mode=="verbose":
			return [(1,1)], [GameState(successor, opponent)], "Center"
		return [(1,1)], [GameState(successor, opponent)]

	#Opposite corner
	if board[0][0] == opponent and board[2][2].isnumeric():
		actions.append((2,2))
		successor = copy.deepcopy(board)
		successor[2][2] = actor
		successors.append(GameState(successor, opponent))
	if board[2][0] == opponent and board[0][2].isnumeric():
		actions.append((0,2))
		successor = copy.deepcopy(board)
		successor[0][2] = actor
		successors.append(GameState(successor, opponent))
	if board[2][2] == opponent and board[0][0].isnumeric():
		actions.append((0,0))
		successor = copy.deepcopy(board)
		successor[0][0] = actor
		successors.append(GameState(successor, opponent))
	if board[0][2] == opponent and board[2][0].isnumeric():
		actions.append((2,0))
		successor = copy.deepcopy(board)
		successor[2][0] = actor
		successors.append(GameState(successor, opponent))
	if len(actions)>0:
		if mode=="verbose":
			return actions, successors, "Opposite corner"
		return actions, successors

	#Empty corner
	if board[0][0].isnumeric():
		actions.append((0,0))
		successor = copy.deepcopy(board)
		successor[0][0] = actor
		successors.append(GameState(successor, opponent))
	if board[2][0].isnumeric():
		actions.append((2,0))
		successor = copy.deepcopy(board)
		successor[2][0] = actor
		successors.append(GameState(successor, opponent))
	if board[0][2].isnumeric():
		actions.append((0,2))
		successor = copy.deepcopy(board)
		successor[0][2] = actor
		successors.append(GameState(successor, opponent))
	if board[2][2].isnumeric():
		actions.append((2,2))
		successor = copy.deepcopy(board)
		successor[2][2] = actor
		successors.append(GameState(successor, opponent))
	if len(actions)>0:
		if mode=="verbose":
			return actions, successors, "Empty corner"
		return actions, successors

	#Empty side
	if board[0][1].isnumeric():
		actions.append((0,1))
		successor = copy.deepcopy(board)
		successor[0][1] = actor
		successors.append(GameState(successor, opponent))
	if board[1][0].isnumeric():
		actions.append((1,0))
		successor = copy.deepcopy(board)
		successor[1][0] = actor
		successors.append(GameState(successor, opponent))
	if board[1][2].isnumeric():
		actions.append((1,2))
		successor = copy.deepcopy(board)
		successor[1][2] = actor
		successors.append(GameState(successor, opponent))
	if board[2][1].isnumeric():
		actions.append((2,1))
		successor = copy.deepcopy(board)
		successor[2][1] = actor
		successors.append(GameState(successor, opponent))
	if len(actions)>0:
		if mode=="verbose":
			return actions, successors, "Empty side"
		return actions, successors

#minimax - O is maximizer, X is minimizer
'''def generateOptimalSuccessor(board, actor):
	def getValue(board, actor):
		isEnd, winner = checkEndGameState(board)
		if isEnd:
			if winner == "O":
				return 1
			if winner == "-":
				return 0.1
			else:
				return -1

		actions, successors = generateSuccessor(board, actor)
		values = [0.9*getValue(successor.board, successor.turn) for successor in successors]
		if actor == "O":
			return max(values)
		else:
			return min(values)

	bestActions = []
	bestSuccessors = []
	bestVal = float('-inf') if actor=="O" else float('inf')
	actions = [(i,j) for i in range(3) for j in range(3) if board[i][j].isnumeric()]
	for action in actions:
		successor = copy.deepcopy(board)
		successor[action[0]][action[1]] = actor
		newVal = getValue(successor, "O" if actor=="X" else "X")
		if bestVal == newVal:
			bestActions.append(action)
			bestSuccessors.append(GameState(successor, "O" if actor=="X" else "X"))
		if actor == "O" and bestVal < newVal:
			bestActions = [action]
			bestSuccessors = [GameState(successor, "O" if actor=="X" else "X")]
			bestVal = newVal
		if actor == "X" and bestVal > newVal:
			bestActions = [action]
			bestSuccessors = [GameState(successor, "O" if actor=="X" else "X")]
			bestVal = newVal

	return bestActions, bestSuccessors'''

def actionToString(action):
	return str(action[0]*3+action[1]+1)

def gameStateToSystemMsg(board, actor, action, successor):
	msg = "The game board currently looks likes this.\n"
	msg += returnStrGameState(board)
	msg += "\nI place "+actor+" on square "+actionToString(action)+". Now the game board looks like this.\n"
	msg += returnStrGameState(successor)
	return msg

system = [{"role": "system", "content": "We are playing tic-tac-toe."}]

with jsonlines.open('optimal_tictactoe.jsonl', mode='w') as writer:
	while len(gameStates) > 0:
		gameState = gameStates.pop(0)
		#If beginning state, AI always starts

		actions, successors = generateOptimalSuccessor(gameState.board, gameState.turn)
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
					#print(endmsg)
					writer.write({"messages": system + exchangeSecond + 
						[{"role": "assistant", "content": endmsg}, {"role": "user", "content": "Okay!"}]})
					continue

				actionsLast, successorsLast = generateOptimalSuccessor(successorUser.board, successorUser.turn)
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
					#print(endmsg)
					writer.write({"messages": system + exchangeSecond + [{"role": "assistant", "content": endmsg}]})

