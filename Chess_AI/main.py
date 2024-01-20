from board import Board
from utils import valid_move_input

if __name__ == "__main__":
    input("\nMoves are given in the format: 'a2 a4' (from a2 to a4)\nPress enter to continue...")

    board = Board()
    board.print_board()
    turn_color = 1

    try:
        print("\n\n")
        while True:
            move = valid_move_input(f"\n{['Black', 'White'][turn_color]}'s move: ").split()

            board.move_piece(move[0], move[1])
            board.print_board()

            turn_color = not turn_color


    except KeyboardInterrupt:
        print("\nGoodbye!")