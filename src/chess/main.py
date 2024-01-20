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
            move = valid_move_input(f"\n{['Black', 'White'][turn_color]}'s move: ").split()

            # If the move was valid, switch turns
            if board.move_piece(move[0], move[1]) == 1:
                board.print_board()
                turn_color = not turn_color


    except KeyboardInterrupt:
        print("\nGoodbye!")


if __name__ == "__main__":
    chess()
