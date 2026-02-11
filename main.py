import pygame
import chess
import sys
import random
import os
import pprint

from pst import *

pygame.init()

FONT = pygame.font.SysFont("arial", 18)
SIZE = 640
SQ = SIZE // 8
screen = pygame.display.set_mode((SIZE, SIZE))
pygame.display.set_caption("Play vs Engine")

board = chess.Board()

LIGHT = (240, 217, 181)
DARK = (181, 136, 99)
HIGHLIGHT = (100, 200, 100)

selected = None

piece_values = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0
}

# -------------------------
# Simple Engine (1-ply)
# -------------------------
def evaluate(board: chess.Board):
    if board.is_checkmate:
        return -999 if board.turn else 999
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        piece_name = piece.piece_type
        print(piece_name)
        if piece:
            value = piece_values[piece_name]

            # Getting Positional Bonus
            index = (
                square if piece.color == chess.WHITE
                       else 63 - square 
            )

            pst = 0
            if piece.piece_type == chess.PAWN:
                pst = PAWN_TABLE[index]
            elif piece.piece_type == chess.KNIGHT:
                pst = KNIGHT_TABLE[index]
            elif piece.piece_type == chess.BISHOP:
                pst = BISHOP_TABLE[index]
            elif piece.piece_type == chess.ROOK:
                pst = ROOK_TABLE[index]
            elif piece.piece_type == chess.QUEEN:
                pst = QUEEN_TABLE[index]
            elif piece.piece_type == chess.KING:
                pst = KING_TABLE[index]


            if piece.color == chess.WHITE:
                score += value + pst
            else:
                score -= value + pst

    return score

def minimax(depth, alpha, beta, maximizing):
    print("MINIMAX FUNCTION IS BEING CALLED")
    if depth == 0 or board.is_game_over():
        print("NOW DEPTH IS 0. CALL EVALUATE")
        return evaluate(board)

    if maximizing:
        max_eval = -999999
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(depth-1, alpha, beta, False)
            board.pop()

            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break

        return max_eval
    else:
        min_eval = 999999
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(depth-1, alpha, beta, True)
            board.pop()

            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break

        return min_eval

def engine_move(depth=3):
    best_move = None
    best_value = -9999 if board.turn == chess.WHITE else 9999

    for move in board.legal_moves:
        board.push(move)
        value = minimax(depth-1, -999999, 999999, board.turn == chess.WHITE)
        board.pop()

        if board.turn == chess.WHITE:
            if value > best_value:
                best_value = value
                best_move = move
        else:
            if value < best_value:
                best_value = value
                best_move = move

    return best_move


# -------------------------
# Drawing
# -------------------------
def load_images(square_size):
    images = {}

    colors = ["white", "black"]
    names = ["pawn", "rook", "knight", "bishop", "queen", "king"]

    for color in colors:
        for name in names:
            filename = f"{color}-{name}.png"
            path = os.path.join("pieces", filename)

            image = pygame.image.load(path).convert_alpha()
            image = pygame.transform.smoothscale(image, (square_size, square_size))

            if name == "knight":
                key = color[0] + "n"  # wp, wr, etc.
            else:
                key = color[0] + name[0]
            
            print(f"{color} {name} -----> {key}")

            images[key] = image

    return images

IMAGES = load_images(SQ)
pprint.pprint(IMAGES)

def draw_coordinates():
    files = "abcdefgh"
    ranks = "12345678"

    for i in range(8):
        # Letters (bottom)
        file_text = FONT.render(files[i], True, (0, 0, 0))
        screen.blit(file_text, (i * SQ + 5, SIZE - 20))

        # Numbers (left side)
        rank_text = FONT.render(ranks[7 - i], True, (0, 0, 0))
        screen.blit(rank_text, (5, i * SQ + 5))

def draw():
    for r in range(8):
        for c in range(8):
            color = LIGHT if (r+c)%2==0 else DARK
            pygame.draw.rect(screen, color, (c*SQ, r*SQ, SQ, SQ))

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            r = 7 - chess.square_rank(square)
            c = chess.square_file(square)

            color = "w" if piece.color == chess.WHITE else "b"
            piece_name = piece.piece_type

            name_map = {
                chess.PAWN: "p",
                chess.ROOK: "r",
                chess.KNIGHT: "n",
                chess.BISHOP: "b",
                chess.QUEEN: "q",
                chess.KING: "k"
            }

            key = color + name_map[piece_name]
            screen.blit(IMAGES[key], (c*SQ, r*SQ))
    
    draw_coordinates()


def mouse_to_square(pos):
    x,y = pos
    col = x // SQ
    row = y // SQ
    return chess.square(col, 7-row)


# -------------------------
# Game Loop
# -------------------------
while True:
    draw()
    pygame.display.flip()

    if board.is_game_over():
        print("Game over:", board.result())
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit()

    # Engine plays black
    if board.turn == chess.BLACK:
        move = engine_move(depth=5)
        board.push(move)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and board.turn == chess.WHITE:
            square = mouse_to_square(pygame.mouse.get_pos())

            if selected is None:
                if board.piece_at(square) and board.piece_at(square).color == chess.WHITE:
                    selected = square
            else:
                move = chess.Move(selected, square)
                if move in board.legal_moves:
                    board.push(move)
                selected = None
