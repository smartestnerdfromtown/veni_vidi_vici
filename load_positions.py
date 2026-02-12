import chess
import chess.pgn
from pathlib import Path

def load_positions_with_result(pgn_path: Path):
    positions = []
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
                labels.append(game_value)
                board.push(move)

            print(f"Processed {game_count} games.")

    return positions, labels

load_positions_with_result(pgn_path="games/Modern.pgn")
