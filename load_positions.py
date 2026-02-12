import chess
import chess.pgn
from pathlib import Path
import torch

# NOTE: Those numbers are just for representing pieces. 
#       They are not aimed to present their values or something like that.
piece_map = {
    chess.PAWN: 0,
    chess.KNIGHT: 1,
    chess.BISHOP: 2,
    chess.ROOK: 3,
    chess.QUEEN: 4,
    chess.KING: 5,
}

def board_to_tensor(board):
    tensor = torch.zeros(12, 8, 8)
    for square, piece in board.piece_map().items():
        row = 7 - chess.square_rank(square)
        col = chess.square_file(square)
        offset = 0 if piece.color == chess.WHITE else 6
        tensor[piece_map[piece.piece_type] + offset][row][col] = 1
    return tensor

def load_positions_with_result(pgn_path: Path, games: int):
    positions = []
    positions_tensor = []
    labels = []

    with open(pgn_path, mode="r", encoding="utf-8") as pgn_file:
        game_count = 0
        while True:
            game = chess.pgn.read_game(pgn_file)
            if game is None:
                break
            game_count += 1

            result = game.headers.get("Result", "1/2-1/2")
            print("White:", game.headers.get("White"))
            print("Black:", game.headers.get("Black"))
            print("Result:", result)
            
            if result == "1-0":
                game_value = 1.0
            elif result == "0-1":
                game_value = -1.0
            else:
                game_value = 0.0

            board = game.board()

            for move in game.mainline_moves():
                positions.append(board.copy())
                positions_tensor.append(board_to_tensor(board))
                labels.append(game_value)
                board.push(move)

            print(f"Processed {game_count} games.")

            if game_count == games:
                break

    X = torch.stack(positions)
    y = torch.tensor(labels).unsqueeze(1)

    return (X, y, positions, labels)

load_positions_with_result(pgn_path="games/Modern.pgn")
