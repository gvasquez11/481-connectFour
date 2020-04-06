import numpy as np
import pygame as c4
import sys
import math

BLUE = (0, 0, 255) 
RED = (255, 0, 0) 
YELLOW = (255, 255, 0) 
BLACK = (0,0,0)


COLUMNS = 7
ROWS = 6

def create_board():
		board = np.zeros((ROWS,COLUMNS))
		return board

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_valid_location(board, col):
	return board[ROWS-1][col] == 0

def get_next_open_row(board, col):
	#Goes from bottom of board upwards to find the first open slot
	for r in range(ROWS):
		if board[r][col]==0:
			return r

def print_board(board):
	print(np.flipud(board))

def check_horitontal(board, piece):
	#check all horizontal locations
	for c in range(COLUMNS-3):
		for r in range(ROWS):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

def check_vertical(board, piece):
	#check all vertical locations
	for c in range(COLUMNS):
		for r in range(ROWS-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

def check_up_diagonal(board, piece):
	#check all upward diagonal locations
	for c in range(COLUMNS-3):
		for r in range(ROWS-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

def check_down_diagonal(board, piece):
	#check all downward diagonal locations
	for c in range(COLUMNS-3):
		for r in range(3, ROWS):
			if board[r][c] == piece and board[r-1][c-1] == piece and board[r-2][c-2] == piece and board[r-3][c-3] == piece:
				return True


def winning_move(board, piece):
	if (check_horitontal(board, piece)):
		return True
	elif (check_vertical(board, piece)):
		return True
	elif (check_up_diagonal(board, piece)):
		return True
	elif (check_down_diagonal(board, piece)):
		return True
	else:
		return False

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
				
			
		
board = create_board()
game_over = False
turn = 0


#initializing connect4 board
c4.init()

SQUARE_SIZE = 100
RADIUS = int(SQUARE_SIZE/2 -5)

width = COLUMNS * SQUARE_SIZE
height = (ROWS+1) * SQUARE_SIZE
size = (width, height)
screen = c4.display.set_mode(size)
draw_board(board)
c4.display.update()

while not game_over:
	for event in c4.event.get():
		if event.type== c4.QUIT:
			sys.exit()

		if event.type == c4.MOUSEMOTION:
			c4.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
			posx = event.pos[0]
			if turn == 0:
				c4.draw.circle(screen, RED, (posx, int(SQUARE_SIZE/2)), RADIUS)
			else:
				c4.draw.circle(screen, YELLOW, (posx, int(SQUARE_SIZE/2)), RADIUS)
			c4.display.update()

		if event.type == c4.MOUSEBUTTONDOWN:
			posx = event.pos[0]
			col = int(math.floor(posx/SQUARE_SIZE))
			#Ask for player 1 input
			if turn==0:
				
				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, 1)
					if winning_move(board, 1):
						print("Player 1 wins")
						game_over = True
			
			#Ask for player 2 input
			else:
				

				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, 2)
					if winning_move(board, 2):
						print("Player 2 wins")
						game_over = True

			turn+=1
			turn = turn%2 
			
			draw_board(board)
			
print("Game Over")
