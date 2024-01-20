import os
import numpy as np
import pandas as pd
from piece import Piece, Pawn, Rook, Knight, Bishop, Queen, King


class Board:
    def __init__(self) -> None:
        self.board = None
        self.board_df = None

        # Create board, update board_df
        self.create_start_board()

    def create_start_board(self):
        pieces = [Pawn, Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        
        # Main pieces
        row0, row7 = [], []
        for color in [-1, 1]:
            for col, piece_object in enumerate(pieces[1:]):
                piece = piece_object(color=color, pos=(0 if color == 1 else 7, col))
                row0.append(piece) if color == 1 else row7.append(piece)

        # Pawns
        row1, row6 = [], []
        for col in range(8):
            row1.append(pieces[0](1, pos=(1, col)))
            row6.append(pieces[0](-1, pos=(6, col)))

        self.board = [
                row0, 
                row1, 
                [None for _ in range(8)], 
                [None for _ in range(8)], 
                [None for _ in range(8)], 
                [None for _ in range(8)], 
                row6, 
                row7
            ]

    def print_board(self):
        row_label = [1, 2, 3, 4, 5, 6, 7, 8]

        print("    a  b  c  d  e  f  g  h")
        for index, i in enumerate(self.board):
            print(row_label[index], end = "  ")
            for jndex, piece in enumerate(i):
                # Print Colors
                if (index + jndex) % 2 == 0:
                    print("\033[48;5;208m", end="")
                else:
                    print("\033[48;5;166m", end="")

                # Print piece
                if piece is None:
                    print("  ", end=" ")
                elif piece.id.isupper(): # - black
                    print("\033[97m" + " " + piece.id, end=" ")
                else: # piece.id.islower() - white
                    print("\033[30m" + " " + piece.id, end=" ")

                # Reset color
                print("\033[0m", end="")
            print("\033[0m")

    def move_piece(self, current_pos, new_pos):
        current_pos = (int(current_pos[1]) - 1, ord(current_pos[0]) - 97)
        new_pos = (int(new_pos[1]) - 1, ord(new_pos[0]) - 97)

        piece = self.get_piece_from(current_pos)
        print(f"Retrieved '{piece.__class__.__name__}' from {current_pos}")

        if piece != None and piece.is_valid_move(new_pos, self.board):
            self.set_piece_at(new_pos, current_pos, piece)

        else:
            print(f"Invalid move: {current_pos} -> {new_pos}", end="\n\n")
            # TODO: Add error handling

    def get_piece_from(self, pos):
        row, col = pos
        return self.board[row][col]

    def set_piece_at(self, pos, old_pos, piece):
        row, col = pos
        self.board[row][col] = piece

        # Remove piece from old position
        old_row, old_col = old_pos
        self.board[old_row][old_col] = None
