import math
import random
import sys

import numpy as np
import pygame as c4

BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0,0,0)


COLUMNS = 7
ROWS = 6

PLAYER = 0
AI = 1

EMPTY = 0
PLAY_DISK = 1
AI_DISK = 2

SCORE_WINDOW_LENGTH= 4


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
   print (np.flipud(board))

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
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
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

def evaluate_window(score_window, piece):

    score = 0
    ai_piece = PLAY_DISK

    if piece == PLAY_DISK:
        ai_piece = AI_DISK

    if score_window.count(piece) == 4:
        score += 100
    elif score_window.count(piece) == 3 and score_window.count(EMPTY) == 1:
        score+= 5
    elif score_window.count(piece) == 2 and score_window.count(EMPTY) == 2:
        score += 2

    if score_window.count(ai_piece) == 3 and score_window.count(EMPTY) == 1:
        score -= 4

    return score

def disk_Score(board, piece):
    score = 0

    centerArray = [int(i) for i in list(board[:, COLUMNS // 2])]
    centerCount = centerArray.count(piece)
    score += centerCount * 3

    # score horizontal
    for h in range(ROWS):
        row_array = [int(i) for i in list(board[h, :])]
        for v in range(COLUMNS-3):
            score_Window = row_array[v:v + SCORE_WINDOW_LENGTH]
            score += evaluate_window(score_Window, piece)

        # score vertical
    for v in range(COLUMNS):
        col_array = [int(i) for i in list(board[:, v])]
        for h in range(ROWS-3):
            score_Window = col_array[h:h + SCORE_WINDOW_LENGTH]
            score += evaluate_window(score_Window, piece)

        # score sloped diagonal
    for h in range(ROWS-3):
        for v in range(COLUMNS-3):
            score_Window = [board[h + i][v + i] for i in range(SCORE_WINDOW_LENGTH)]
            score += evaluate_window(score_Window, piece)

    for h in range(ROWS-3):
        for v in range(COLUMNS-3):
            score_Window = [board[h + 3 - i][v + i] for i in range(SCORE_WINDOW_LENGTH)]
            score += evaluate_window(score_Window, piece)

    return score


def is_last_move(board):
    return winning_move(board, PLAY_DISK) or winning_move(board, AI_DISK) or len(get_open_spots(board)) == 0

def minimax(board, depth, alpha, beta, maxPlay):
    # this section might not be necessary or will need to altered more
    openSpots = get_open_spots(board)
    last_Move = is_last_move(board)
    if depth == 0 or last_Move:
        if last_Move:
            if winning_move(board, AI_DISK):
                return (None, 999999999999)  # so it knows its the best move
            elif winning_move(board, PLAY_DISK):
                return (None, -999999999999)  # so it knows it lost
            else:
                return (None,0)
        else:
            return (None, disk_Score(board, AI_DISK))
    # start of min max for player
    if maxPlay:
        value = -math.inf
        column = random.choice(openSpots)
        for vert in openSpots:
            horiz = get_next_open_row(board, vert)
            state_copy = board.copy()
            drop_piece(state_copy, horiz, vert, AI_DISK)
            new_State = minimax(state_copy, depth-1, alpha, beta, False)[1]
            if new_State > value:
                value = new_State
                column = vert
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value


    else:  # minimize play
        value = math.inf
        column = random.choice(openSpots)
        for vert in openSpots:
            horiz = get_next_open_row(board, vert)
            state_copy = board.copy()
            drop_piece(state_copy, horiz, vert, PLAY_DISK)
            new_State = minimax(state_copy, depth-1, alpha, beta, True)[1]
            if new_State < value:
                value = new_State
                column = vert
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

def get_open_spots(board):
    open_Spots = []
    for c  in range(COLUMNS):
        if is_valid_location(board, c):
            open_Spots.append(c)
    return open_Spots

def best_Move(board, piece):
    valid_spot = get_open_spots(board)
    winning_score = -99999
    best_column = random.choice(valid_spot)
    for c in valid_spot:
        horiz = get_next_open_row(board, c)
        temp_board = board.copy()
        drop_piece(temp_board, horiz, c, piece)
        score = disk_Score(temp_board, piece)
        if score > winning_score:
            winning_score = score
            best_column = c

    return best_column


def draw_board(board):
    for c in range(COLUMNS):
        for r in range(ROWS):
            c4.draw.rect(screen, BLUE, (c*SQUARE_SIZE, r*SQUARE_SIZE+SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            c4.draw.circle(screen, BLACK, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), int(r*SQUARE_SIZE+SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)

    for c in range(COLUMNS):
        for r in range(ROWS):
            if board[r][c]==PLAY_DISK:
                c4.draw.circle(screen, RED, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), height-int(r*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
            elif board[r][c]==AI_DISK:
                c4.draw.circle(screen, YELLOW, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), height-int(r*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)

    c4.display.update()



board = create_board()
print_board(board)
game_over = False
#turn = 0


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
turn = random.randint(0, 1)
font = c4.font.Font(None, 48)
while not game_over:

        for event in c4.event.get():
            if event.type== c4.QUIT:
                sys.exit()

            if event.type == c4.MOUSEMOTION:
                c4.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
                posx = event.pos[0]
                if turn == 0:
                    c4.draw.circle(screen, RED, (posx, int(SQUARE_SIZE/2)), RADIUS)

            c4.display.update()

            if event.type == c4.MOUSEBUTTONDOWN:
                c4.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))

                #Ask for player 1 input
                if turn== 0:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARE_SIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, PLAY_DISK)
                        if winning_move(board, PLAY_DISK):
                            text = font.render("Player Wins",1,RED)
                            screen.blit(text, (60, 30))
                            game_over = True

                        turn += 1
                        turn = turn % 2
                        print_board(board)
                        draw_board(board)






        if turn == 1 and not game_over:

            col, ai_alg_Score = minimax(board, 5, -math.inf, math.inf, True)

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_DISK)

                if winning_move(board, AI_DISK):
                    text = font.render("A.I. Wins", 1, YELLOW)
                    screen.blit(text, (60, 30))
                    game_over = True

                print_board(board)
                draw_board(board)

                turn += 1
                turn = turn % 2


        if game_over:
            
            c4.time.wait(5000)
