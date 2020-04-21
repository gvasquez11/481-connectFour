import numpy as np
import pygame as c4
import sys
import math
import random

#colors on board
BLUE = (0, 0, 255) 
RED = (255, 0, 0) 
YELLOW = (255, 255, 0) 
BLACK = (0,0,0)

COLUMNS = 7
ROWS = 6

#dimensions for visualizing the board
#size of each cell within the visual grid
SQUARE_SIZE = 100
#size of each circle within the square
RADIUS = int(SQUARE_SIZE/2 -5)
#width of the board, determined by how many columns specified
width = COLUMNS * SQUARE_SIZE
#height of the board, deteremined by how many rows specified, +1 above board for placing pieces
height = (ROWS+1) * SQUARE_SIZE
#final size of board
size = (width, height)

#human players turn is represented by a 0, AI's turn is represented by a 1
HUMAN = 0
AI = 1

#values for the two dimensional array 
#if 0 is in the array cell, its empty 
#if 1, the human player has a piece there
#if 2, the AI player has a piece there
HUMAN_PIECE = 1
AI_PIECE = 2
EMPTY = 0

#when the algorithm scans the board, it scans in a window size of 4, checking 4 pieces in a row at a time
#could be horizontal, vertical, or diagonal
WINDOW_LENGTH = 4

#creates a two dimensional array that is ROWS x COLUMNS in size and returns that array
def create_board():
		board = np.zeros((ROWS,COLUMNS))
		return board

#passes in the board array and fills array[row][col] with either a human game piece or an AI game piece
def drop_piece(board, row, col, piece):
	board[row][col] = piece

#checks if the column in question is not totally full with game pieces
def is_valid_location(board, col):
	return board[ROWS-1][col] == 0

#Goes from bottom of column upwards to find the first 0 to show up which will be the first open slot and returns that row
def get_next_open_row(board, col):
	for r in range(ROWS):
		if board[r][col]==0:
			return r

#prints the two dimensional array board to the console and flips it to make the value ascend from 0 to ROWS-1
def print_board(board):
	print(np.flipud(board))

#checks the board for a win by checking all possible ways to win
def winning_move(board, piece):
	# Check horizontal locations for win
	for c in range(COLUMNS-3):
		for r in range(ROWS):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check vertical locations for win
	for c in range(COLUMNS):
		for r in range(ROWS-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positively sloped diagonals0-pp
	for c in range(COLUMNS-3):
		for r in range(ROWS-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMNS-3):
		for r in range(3, ROWS):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

def eval_window(window, piece):
	score = 0
	opp_piece = HUMAN_PIECE
	if piece == HUMAN_PIECE:
		opp_piece = AI_PIECE

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 2

	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 4

	return score

def score_pos(board, piece):
	score = 0

	## Score center column
	center_array = [int(i) for i in list(board[:, COLUMNS//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	## Score Horizontal
	for r in range(ROWS):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(COLUMNS-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += eval_window(window, piece)

	## Score Vertical
	for c in range(COLUMNS):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROWS-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += eval_window(window, piece)

	## Score posiive sloped diagonal
	for r in range(ROWS-3):
		for c in range(COLUMNS-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += eval_window(window, piece)

	for r in range(ROWS-3):
		for c in range(COLUMNS-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += eval_window(window, piece)

	return score

#returns true if the piece played will end the game
def is_terminal_node(board):
	return winning_move(board, HUMAN_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(board, AI_PIECE):
				return (None, 100000000000000)
			elif winning_move(board, HUMAN_PIECE):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, score_pos(board, AI_PIECE))
	if maximizingPlayer:
		value = float('-inf')
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			board_copy = board.copy()
			drop_piece(board_copy, row, col, AI_PIECE)
			new_score = minimax(board_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: # Minimizing player
		value = float('inf')
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			board_copy = board.copy()
			drop_piece(board_copy, row, col, HUMAN_PIECE)
			new_score = minimax(board_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value

def get_valid_locations(board):
	valid_locations = []
	for col in range(COLUMNS):
		if is_valid_location(board, col):
			valid_locations.append(col)
	return valid_locations

#draws the visual board
def draw_board(board):
	for c in range(COLUMNS):
		for r in range(ROWS):
			c4.draw.rect(screen, BLUE, (c*SQUARE_SIZE, r*SQUARE_SIZE+SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
			c4.draw.circle(screen, BLACK, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), int(r*SQUARE_SIZE+SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
			
	for c in range(COLUMNS):
		for r in range(ROWS):
			if board[r][c]==1:
				c4.draw.circle(screen, RED, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), height-int(r*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
			elif board[r][c]==2:
				c4.draw.circle(screen, YELLOW, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), height-int(r*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)		
			
	c4.display.update()
				
			
#initalize board as two dimensional array [ROWS, COLUMNS]
board = create_board()
#set game over to false, only exits while loop when a player gets a connect 4
game_over = False
##picks at random whether Human or AI goes first
turn = random.randint(HUMAN, AI)


#initializing connect4 visual board
c4.init()



screen = c4.display.set_mode(size)
draw_board(board)
c4.display.update()

myfont = c4.font.SysFont("monospace", 75)



while not game_over:
	for event in c4.event.get():
		if event.type== c4.QUIT:
			sys.exit()

		if event.type == c4.MOUSEMOTION:
			c4.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
			posx = event.pos[0]
			if turn == HUMAN:
				c4.draw.circle(screen, RED, (posx, int(SQUARE_SIZE/2)), RADIUS)
			c4.display.update()

		if event.type == c4.MOUSEBUTTONDOWN:
			c4.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
			if turn==HUMAN:
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARE_SIZE))
				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, HUMAN_PIECE)
					if winning_move(board, HUMAN_PIECE):
						label = myfont.render("Player 1 wins!!", 1, RED)
						screen.blit(label, (40,10))
						game_over = True

					turn+=1
					turn = turn%2 
					draw_board(board)
			
			#Ask for player 2 input
	if turn == AI and not game_over:
		col, minimax_score = minimax(board, 4, float('-inf'), float('inf'), True)

		if is_valid_location(board,col):
			row = get_next_open_row(board, col)
			drop_piece(board, row, col, AI_PIECE)
			if winning_move(board, AI_PIECE):
				label = myfont.render("Player 2 wins!!", 1, YELLOW)
				screen.blit(label, (40,10))
				game_over = True
			turn+=1
			turn = turn%2 
			draw_board(board)

	if game_over:
		c4.time.wait(3000)

			
			
print("Game Over")

