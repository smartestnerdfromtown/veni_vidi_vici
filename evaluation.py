import chess
from pst import *

piece_values = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0
}

def evaluate(board: chess.Board):
    score = 0

    if board.is_checkmate():
        return -999 if board.turn else 999
    if board.is_stalemate() or board.is_insufficient_material():
        return 0
    if board.can_claim_threefold_repetition():
        return 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_name = piece.piece_type
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

            # Mobility Bonus
            mobility = len(list(board.legal_moves))
            mobility_bonus = + 0.02 * mobility

            # Repetition Penalty
            repetition_penaly = 0
            if len(board.move_stack) >= 4:
                if board.move_stack[-1] == board.move_stack[-3]:
                    repetition_penaly = -0.3

            if piece.color == chess.WHITE:
                score += value + pst + mobility_bonus + repetition_penaly
            else:
                score -= value + pst + 0.02 * mobility_bonus + abs(repetition_penaly)

    return score