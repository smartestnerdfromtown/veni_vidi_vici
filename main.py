import pygame
import chess
import sys
import random
import os
import pprint

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

# -------------------------
# Simple Engine (1-ply)
# -------------------------
def evaluate(b):
    score = 0
    for piece_type in piece_values:
        score += len(b.pieces(piece_type, chess.WHITE)) * piece_values[piece_type]
        score -= len(b.pieces(piece_type, chess.BLACK)) * piece_values[piece_type]
    return score

def engine_move():
    best_move = None
    best_score = -9999 if board.turn == chess.WHITE else 9999

    for move in board.legal_moves:
        print(list(board.legal_moves))
        random_move = random.choice(list(board.legal_moves))
        board.push(move)
        score = evaluate(board)
        board.pop()

        if board.turn == chess.WHITE:
            if score > best_score:
                best_score = score
                best_move = move
        else:
            if score < best_score:
                best_score = score
                best_move = move

    print(best_move)
    return best_move if best_move else random_move


# -------------------------
# Drawing
# -------------------------
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
        move = engine_move()
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
