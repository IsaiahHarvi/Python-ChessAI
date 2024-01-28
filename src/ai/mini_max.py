import numpy as np
from ..chess.piece import Knight, Bishop, Rook, Queen, King, Pawn

def minimax(board_obj, board, depth, alpha, beta, simulating_player=bool):
    if board_obj.is_checkmate():
        return -1000 if simulating_player else 1000
    
    elif depth == 0:
        return evaluate(board)

    if simulating_player:
        max_eval = -np.inf
        for move in set(board_obj.get_moves(color=0)): # Black
            print('PLAYER MOVE', move)
            c_board = board_obj.simulate_move(move)
            #board_obj.print_board(c_board)
            eval = minimax(board_obj, c_board, depth-1, alpha, beta, simulating_player=False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)

            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = np.inf
        for move in set(board_obj.get_moves(color=1)): # White
            print('AI MOVE', move, 'COLOR: ')
            c_board = board_obj.simulate_move(move)
            #board_obj.print_board(c_board)
            eval = minimax(board_obj, c_board, depth-1, alpha, beta, simulating_player=True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)

            if beta <= alpha:
                break
        return min_eval
    
def evaluate(board):
    value = { # Value of each piece
        Pawn: 1,
        Knight: 3,
        Bishop: 3,
        Rook: 5,
        Queen: 9,
        King: 100
    }

    white_score, black_score = 0, 0
    
    for row in board:
        for piece in row:
            if piece:
                if piece.color:
                    white_score += value[type(piece)]
                else:
                    black_score += value[type(piece)]
    
    return white_score - black_score # White is positive, black is negative