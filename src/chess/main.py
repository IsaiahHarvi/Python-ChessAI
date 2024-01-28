import numpy as np
from ..chess.board import Board
from ..ai.mini_max import minimax
from ..chess.utils import valid_move_input

def chess():
    """
    This function initializes the chess board, prompts the players for moves,
    and updates the board accordingly until the game is finished or interrupted.

    NOTE: Moves are given in the format: 'a2 a4' (from a2 to a4)
    """

    input("\nMoves are given in the format: 'a2 a4' (from a2 to a4)\nPress enter to continue...")
    global board
    board = Board()
    board.print_board()
    turn_color = 0 # Black
    AI_color = 1 # White
    player_checked = False

    try:
        print("\n\n")
        while True:
            if turn_color == AI_color:
                best_evaluation = -np.inf
                best_move = None

                for move in board.get_moves(color=AI_color):
                    c_board = board.simulate_move(move)
                    evaluation = minimax(board_obj = board, board=c_board, depth=4, alpha=-np.inf, beta=np.inf, simulating_player=False)
                    if evaluation > best_evaluation:
                        best_evaluation = evaluation
                        best_move = move
                
                piece = board.get_piece_from(best_move[0])
                print(retrieved_string := f"\n\nAI Retrieved '{piece.__class__.__name__}' from {best_move[0]}")
                print(f"{'─' * len(retrieved_string)}")
                board.set_piece_at(pos=best_move[1], old_pos=best_move[0], piece=piece)
                
                checked, color = board.is_in_check()
                if checked:
                    print(f"Check! {['Black', 'White'][not color]} is in check!")
                    player_checked = True

                board.print_board()
                turn_color = 0 # Switch turns to white

            else:
                position = valid_move_input(f"\n{['Black', 'White'][turn_color]}'s move: ").split()

                # If the move was valid, switch turns
                if board.move_piece(position[0], position[1], player_checked) == 1:
                    checked, color = board.is_in_check()
                    if checked and board.is_checkmate(color): # If the king is in checkmate
                        input(f"Checkmate! {['Black', 'White'][not color]} wins!")
                        break # End the game

                    elif checked == 1: # If the king is in check, but not checkmate 
                        print(f"Check! {['Black', 'White'][not color]} is in check!")

                    board.print_board()
                    turn_color = 1 # Switch turns to black
                    
    except KeyboardInterrupt:
        print("\nGoodbye!")


if __name__ == "__main__":
    chess()
