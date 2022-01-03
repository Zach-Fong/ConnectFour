import numpy as np
import pygame
import sys
import math
import time
import random

SQUARESIZE = 100

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0 ,0)
YELLOW = (255, 255, 0)
ORANGE = (255, 127, 0)
RADIUS = int(SQUARESIZE/2 - 5)

ROW_COUNT = 6
COL_COUNT = 7

PLAYER_PIECE = 1
AI_PIECE = 2


def create_board():
    board = np.zeros((ROW_COUNT,COL_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid(board, col):
    return board[(ROW_COUNT-1, col)] == 0

def get_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def win_check(board, piece):
    for c in range(COL_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    for c in range(COL_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
    for c in range(COL_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def draw_check(board):
    draw = True
    for c in range (COL_COUNT):
        for r in range (ROW_COUNT):
            if board[r][c] == 0:
                draw = False
    if draw:
        print("DRAW")
        pygame.display.update()
        label = font.render("DRAW", 1, ORANGE)
        screen.blit(label, (230, 10))
        pygame.display.update()
        return True
    
    return False


def drop_animation(r, c, colour):
    for r in range(ROW_COUNT, row, -1):
        pygame.draw.circle(screen, colour, (int(c*SQUARESIZE + SQUARESIZE/2), height - int(r*SQUARESIZE + SQUARESIZE/2)), RADIUS)
        pygame.display.update()
        time.sleep(0.005)
        pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE + SQUARESIZE/2), height - int(r*SQUARESIZE + SQUARESIZE/2)), RADIUS)
        pygame.display.update()
        time.sleep(0.005)
            

def draw_board(board):
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE + SQUARESIZE/2), int(r*SQUARESIZE + SQUARESIZE/2 + SQUARESIZE)), RADIUS)
            
    for c in range (COL_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE + SQUARESIZE/2), height - int(r*SQUARESIZE + SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE + SQUARESIZE/2), height - int(r*SQUARESIZE + SQUARESIZE/2)), RADIUS)

def draw_circle():
    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
    pygame.display.update()
    xpos = event.pos[0]
    if (round % 2) == 0:
            pygame.draw.circle(screen, RED, (xpos, int(SQUARESIZE/2)), RADIUS)
            pygame.display.update()

def get_valid_locations(board):
    locations = []
    for c in range(COL_COUNT):
        if is_valid(board, c):
            locations.append(c)
    return locations

def window_value(window, piece):
    score = 0
    opponent = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opponent = AI_PIECE

    if window.count(piece) == 4:
        score += 500
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 30
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 10
    if window.count(opponent) == 3 and window.count(0) == 1:
        score -= 250
    return score

def score_pos(board, piece):

    score = 0
    
    #center
    center_array = [int(i) for i in list(board[:, COL_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 5

    #horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COL_COUNT-3):
            window = row_array[c:c+4]
            score += window_value(window, piece)

    #vertical
    for c in range(COL_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+4]
            score += window_value(window, piece)

    #upper diagonal
    for r in range(ROW_COUNT-3):
        for c in range(COL_COUNT-3):
            window = [board[r+i][c+i] for i in range(4)]
            score += window_value(window, piece)

    #lower diagonal
    for r in range(ROW_COUNT-3):
        for c in range(COL_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(4)]
            score += window_value(window, piece)
    return score

def pick_move(board, piece):

    highest_score = -100000 #so highest_score will not be 0 when all scores are negatives
    valid_locations = get_valid_locations(board)
    best_col = random.choice(valid_locations)

    for c in valid_locations:
        r = get_row(board, c)
        temp = board.copy()
        drop_piece(temp, r, c, piece)
        score = score_pos(temp, piece)
        print(score)
        if score > highest_score:
            highest_score = score
            best_col = c
    print(highest_score)
    print(best_col)
    return best_col

board = create_board()
round = random.randint(0, 1)

pygame.init()
width = COL_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)
screen = pygame.display.set_mode(size)
font = pygame.font.SysFont("monospace", 75)
game_over = False
draw_board(board)
pygame.display.update()
print_board(board)

while not game_over:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            draw_circle()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            pygame.display.update()
            if (round % 2) == 0:
                xpos = event.pos[0]
                col = int(math.floor(xpos/SQUARESIZE))
                if is_valid(board, col):
                    row = get_row(board, col)
                    drop_animation(row, col, RED)
                    drop_piece(board, row, col, PLAYER_PIECE)
                    pygame.display.update()
                    round += 1
                    if win_check(board, 1):
                        print("PLAYER 1 WINS")
                        pygame.display.update()
                        label = font.render("RED WINS", 1, RED)
                        screen.blit(label, (180, 10))
                        game_over = True
                        draw_board(board)
                        pygame.display.update()
                        pygame.time.wait(3000)
                    else:
                        game_over = draw_check(board)

                    print_board(board)
                    draw_board(board)
                    pygame.display.update()
                    print(game_over)
                        
    if (round % 2) == 1 and not game_over:
        col = pick_move(board, AI_PIECE)

        if is_valid(board, col):
            pygame.time.wait(500)
            row = get_row(board, col)
            drop_animation(row, col, YELLOW)
            drop_piece(board, row, col, AI_PIECE)
            pygame.display.update()
            round += 1
            if win_check(board, AI_PIECE):
                print("PLAYER 2 WINS")
                pygame.display.update()
                label = font.render("YELLOW WINS", 1, YELLOW)
                screen.blit(label, (110, 10))
                pygame.display.update()
                game_over = True
                draw_board(board)
                pygame.display.update()
                pygame.time.wait(3000)
            else:
                game_over = draw_check(board)

            print_board(board)
            draw_board(board)
            pygame.display.update()
            print(game_over)
                