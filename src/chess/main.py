from board import Board
from utils import valid_move_input

def chess():
    """
    This function initializes the chess board, prompts the players for moves,
    and updates the board accordingly until the game is finished or interrupted.

    NOTE: Moves are given in the format: 'a2 a4' (from a2 to a4)
    """

    input("\nMoves are given in the format: 'a2 a4' (from a2 to a4)\nPress enter to continue...")

    board = Board()
    board.print_board()
    turn_color = 1

    try:
        print("\n\n")
        while True:
            position = valid_move_input(f"\n{['Black', 'White'][turn_color]}'s move: ").split()

            # If the move was valid, switch turns
            if board.move_piece(position[0], position[1], turn_color) == 1:
                checked, color = board.is_in_check()
                if checked and board.is_checkmate(color): # If the king is in checkmate
                    input(f"Checkmate! {['Black', 'White'][not color]} wins!")
                    break

                elif checked: # If the king is in check, but not checkmate 
                    print(f"Check! {['Black', 'White'][not color]} is in check!")

                board.print_board()
                turn_color = not turn_color
                
    except KeyboardInterrupt:
        print("\nGoodbye!")


if __name__ == "__main__":
    chess()
