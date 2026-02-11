import chess
import pygame
import os

class ChessGUI:
    def __init__(self, board):
        self.board = board
        self.selected = None
        
        self.SIZE = 640
        self.SQ = self.SIZE // 8
        
        self.screen = pygame.display.set_mode((self.SIZE, self.SIZE))
        pygame.display.set_caption("Play vs Engine")

        self.FONT = pygame.font.SysFont("arial", 18)

        self.LIGHT = (240, 217, 181)
        self.DARK = (181, 136, 99)

        self.images = self.load_images(self.SQ)

    def load_images(self, square_size):
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
                images[key] = image
        return images

    def draw(self):
        # DRAW BOARD
        for r in range(8):
            for c in range(8):
                color = self.LIGHT if (r+c)%2==0 else self.DARK
                pygame.draw.rect(self.screen, color, 
                                (c*self.SQ, r*self.SQ, self.SQ, self.SQ))

        # DRAW PIECES
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
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
                self.screen.blit(self.images[key], 
                                (c*self.SQ, r*self.SQ))
        
        self.draw_coordinates()

    def handle_click(self, pos):
        square = self.mouse_to_square(pos)

        if self.selected is None:
            piece = self.board.piece_at(square)
            if piece and piece.color == self.board.turn:
                self.selected = square
        else:
            move = chess.Move(self.selected, square)

            if move in self.board.legal_moves:
                self.board.push(move)

            self.selected = None

    def mouse_to_square(self, pos):
        x, y = pos
        col = x // self.SQ
        row = y // self.SQ
        return chess.square(col, 7-row)
    
    def draw_coordinates(self):
        files = "abcdefgh"
        ranks = "12345678"

        for i in range(8):
            # Letters (bottom)
            file_text = self.FONT.render(files[i], True, (0, 0, 0))
            self.screen.blit(file_text, 
                            (i * self.SQ + 5, self.SIZE - 20))

            # Numbers (left side)
            rank_text = self.FONT.render(ranks[7 - i], True, (0, 0, 0))
            self.screen.blit(rank_text, 
                            (5, i * self.SQ + 5))