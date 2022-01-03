import numpy as np
import pygame
import sys
import math
import time

SQUARESIZE = 100

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0 ,0)
YELLOW = (255, 255, 0)
ORANGE = (255, 127, 0)
RADIUS = int(SQUARESIZE/2 - 5)

ROW_COUNT = 6
COL_COUNT = 7

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
        draw_board(board)
        pygame.display.update()
        pygame.time.wait(3000)
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
    else:
        pygame.draw.circle(screen, YELLOW, (xpos, int(SQUARESIZE/2)), RADIUS)
        pygame.display.update()



board = create_board()
round = 0

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
                    drop_piece(board, row, col, 1)
                    pygame.display.update()
                    round += 1
                    if win_check(board, 1):
                        print("PLAYER 1 WINS")
                        pygame.display.update()
                        label = font.render("RED WINS", 1, RED)
                        screen.blit(label, (180, 10))
                        draw_board(board)
                        pygame.display.update()
                        pygame.time.wait(3000)
                        game_over = True
                    else:
                        game_over = draw_check(board)
            else:
                xpos = event.pos[0]
                col = int(math.floor(xpos/SQUARESIZE))

                if is_valid(board, col):
                    row = get_row(board, col)
                    drop_animation(row, col, YELLOW)
                    drop_piece(board, row, col, 2)
                    pygame.display.update()
                    round += 1
                    if win_check(board, 2):
                        print("PLAYER 2 WINS")
                        pygame.display.update()
                        label = font.render("YELLOW WINS", 1, YELLOW)
                        screen.blit(label, (110, 10))
                        draw_board(board)
                        pygame.display.update()
                        pygame.time.wait(3000)
                        game_over = True
                    else:
                        game_over = draw_check(board)
            print_board(board)
            draw_board(board)
            pygame.display.update()