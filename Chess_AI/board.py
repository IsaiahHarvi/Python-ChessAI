import numpy as np
import pandas as pd


class Board:
    def __init__(self) -> None:
        self.board = None
        self.board_df = None

        # Create board, update board_df
        self.create_start_board()

    def create_start_board(self):
        self.board = np.array(
            [
                ["r", "n", "b", "q", "k", "b", "n", "r"],
                ["p", "p", "p", "p", "p", "p", "p", "p"],
                [" ", " ", " ", " ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " ", " ", " ", " "],
                ["P", "P", "P", "P", "P", "P", "P", "P"],
                ["R", "N", "B", "Q", "K", "B", "N", "R"],
            ]
        )
        self.update_board_df()

    def update_board_df(self):
        self.board_df = pd.DataFrame(
            self.board,
            columns=["a", "b", "c", "d", "e", "f", "g", "h"],
            index=["8", "7", "6", "5", "4", "3", "2", "1"],
        )

    def print_board(self, pretty=True):
        print(self.board_df) if pretty else (self.board)

    def move_piece(self, current_pos, new_pos):
        piece = self.get_piece_from(current_pos)

        if piece and piece.is_valid_move(new_pos, self.board):
            piece.move(new_pos, self.board)
            self.set_piece_at(new_pos, current_pos, piece)

        else:
            print("Invalid move")
            # TODO: Add error handling

    def get_piece_from(self, pos):
        x, y = pos
        return self.board[x][y]

    def set_piece_at(self, pos, old_pos, piece):
        x, y = pos
        self.board[x][y] = piece

        # Remove piece from old position
        o_x, o_y = old_pos
        self.board[o_x][o_y] = " "
