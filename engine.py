import chess
import torch

from evaluation import evaluate, evaluate_nn
from neural_network import EvalNet


DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

model = EvalNet()
model.load_state_dict(torch.load("chess_eval_model.pt", map_location=DEVICE))
model.to(DEVICE)

class Engine:
    def __init__(self, depth):
        self.depth = depth

    def search(self, board):
        best_move = None
        best_value = -9999 if board.turn == chess.WHITE else 9999

        for move in board.legal_moves:
            board.push(move)
            value = self.minimax(
                depth=self.depth-1, 
                board=board,
                alpha=-999999, 
                beta=999999, 
                maximizing=board.turn == chess.WHITE
            )
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


    def minimax(self, depth, board, alpha, beta, maximizing):
        if depth == 0 or board.is_game_over():
            return evaluate(board) + evaluate_nn(board, model)

        if maximizing:
            max_eval = -999999
            for move in board.legal_moves:
                board.push(move)
                eval = self.minimax(depth-1, board, alpha, beta, False)
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
                eval = self.minimax(depth-1, board, alpha, beta, True)
                board.pop()

                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
