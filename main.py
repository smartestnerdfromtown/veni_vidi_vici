import pygame
import chess
from gui import ChessGUI
from engine import Engine

pygame.init()

board = chess.Board()
engine = Engine(depth=3)
gui = ChessGUI(board)

while True:
    gui.draw()
    pygame.display.flip()

    if board.is_game_over():
        print("Game over:", board.result())
        pygame.time.wait(3000)
        pygame.quit()
        break

    # Engine Move
    if board.turn == chess.BLACK:
        move = engine.search(board)
        board.push(move)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            gui.handle_click(pygame.mouse.get_pos())