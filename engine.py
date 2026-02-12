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
            nn_score, eval_score, value = self.minimax(
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

        print(nn_score, eval_score, value)
        return best_move    


    def minimax(self, depth, board, alpha, beta, maximizing):
        if depth == 0 or board.is_game_over():
            nn_score = 1000 * evaluate_nn(board, model)
            eval_score = evaluate(board)
            total = nn_score + eval_score

            return nn_score, eval_score, total 

        if maximizing:
            best_total = -999999
            best_nn = 0
            best_eval = 0

            for move in board.legal_moves:
                board.push(move)
                nn_score, eval_score, total = self.minimax(
                    depth-1, board, alpha, beta, False
                )
                board.pop()

                if total > best_total:
                    best_total = total
                    best_nn = nn_score
                    best_eval = eval_score

                alpha = max(alpha, total)
                if beta <= alpha:
                    break

            return best_nn, best_eval, best_total
        

        else:
            best_total = 999999
            best_nn = 0
            best_eval = 0   

            for move in board.legal_moves:
                board.push(move)
                nn_score, eval_score, total = self.minimax(
                    depth-1, board, alpha, beta, True
                )
                board.pop()

                if total < best_total:
                    best_total = total
                    best_nn = nn_score
                    best_eval = eval_score

                beta = min(beta, total)
                if beta <= alpha:
                    break

            return best_nn, best_eval, best_total
