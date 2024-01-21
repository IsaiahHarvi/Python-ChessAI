import os
import numpy as np
from piece import Piece, Pawn, Rook, Knight, Bishop, Queen, King


class Board:
    """
    Represents a chess board.

    Attributes:
        board (list): The 2D list representing the chess board.
        board_df (None): Placeholder for a DataFrame representation of the board.

    Methods:
        __init__(): Initializes the Board object.
        create_start_board(): Creates the starting configuration of the chess board.
        print_board(): Prints the current state of the chess board.
        move_piece(current_pos, new_pos): Moves a chess piece from the current position to the new position.
        get_piece_from(pos): Retrieves the chess piece at the specified position.
        set_piece_at(pos, old_pos, piece): Sets a chess piece at the specified position and updates its old position.
    """

    def __init__(self) -> None:
        """
        Initializes the Board object.
        """
        self.board = None
        self.create_start_board()
        self.white_king = self.get_piece_from((0, 4))
        self.black_king = self.get_piece_from((7, 4))
        self.white_pieces = None
        self.black_pieces = None
        self.white_threats = None
        self.black_threats = None
        self.kings = [self.black_king, self.white_king]

    def create_start_board(self):
        """
        Creates the starting configuration of the chess board.
        """
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
        np.array(self.board)

        # Update piece lists
        self.white_pieces = row7.copy().extend(row6)
        self.black_pieces = row1.copy().extend(row0)


    def print_board(self):
        """
        Prints the current state of the chess board.
        """
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

    def move_piece(self, current_pos, new_pos, turn_color):
        """
        Moves a chess piece from the current position to the new position.

        Args:
            current_pos (str): The current position of the piece in algebraic notation (e.g., "a2").
            new_pos (str): The new position to move the piece to in algebraic notation (e.g., "a4").
        """
        current_pos = (int(current_pos[1]) - 1, ord(current_pos[0]) - 97)
        new_pos = (int(new_pos[1]) - 1, ord(new_pos[0]) - 97)

        # White can't move black and vice versa
        piece = self.get_piece_from(current_pos)
        if piece and (not ((piece.color == 1 and turn_color == 1) or (piece.color == -1 and turn_color == 0))):
            print("Invalid move: Not your piece!")
            return False

        # Show the retrieved piece
        print(retrieved_string := f"Retrieved '{piece.__class__.__name__}' from {current_pos}")
        print(f"{'─' * len(retrieved_string)}")

        # Check if piece can move to new position
        if piece != None and piece.is_valid_move(new_pos, self.board):
            self.set_piece_at(new_pos, current_pos, piece)
            return True

        else:
            print(f"Invalid move: {current_pos} -> {new_pos}", end="\n\n")
            return False
            # TODO: Add error handling

    def get_piece_from(self, pos):
        """
        Retrieves the chess piece at the specified position.

        Args:
            pos (tuple): The position of the piece as a tuple of row and column indices.

        Returns:
            object: The chess piece at the specified position.
        """
        row, col = pos
        return self.board[row][col]

    def set_piece_at(self, pos, old_pos, piece):
        """
        Sets a chess piece at the specified position and updates its old position.

        Args:
            pos (tuple): The position to set the piece at as a tuple of row and column indices.
            old_pos (tuple): The old position of the piece as a tuple of row and column indices.
            piece (object): The chess piece object to set at the specified position.
        """
        row, col = pos
        self.board[row][col] = piece

        # Remove piece from old position
        old_row, old_col = old_pos
        self.board[old_row][old_col] = None

        # Update piece position
        piece.pos = pos

    # TODO: Optimize
    def is_in_check(self, color=None) -> tuple:
        """
        Determines if the current player's king is in check.

        Returns:
            A tuple containing a boolean value indicating if the king is in check,
            and the color of the king that is in check.
        """
        is_check, checked_color, self.white_threats, self.black_threats = False, None, [], []
        check_kings = self.kings if not color else [self.kings[color]]

        for king in check_kings:
            for row in self.board:
                for piece in row:
                    if piece and piece.color != king.color:
                        if piece.is_valid_move(king.pos, self.board):
                            is_check = True
                            checked_color = king.color
                            self.white_threats.append(piece) if king.color else self.black_threats.append(piece)
        return is_check, checked_color
                    
    def is_checkmate(self, color):
        """
        Determines if the specified color is in checkmate.

        Parameters:
        - color (str): The color of the player to check for checkmate.

        Returns:
        - bool: True if the specified color is in checkmate, False otherwise.
        """
        # Check if King can move out of check
        king = self.kings[color]

        if self.can_king_escape(king):
            return False

        if self.can_block_king(king) or self.can_eliminate_threat(king):
            return False
        
        return True

    def can_king_escape(self, king):
        """
        Checks if the king can escape from check.

        Args:
            king (King): The king piece.

        Returns:
            bool: True if the king can escape from check, False otherwise.
        """
        for move in king.moves:
            new_pos = (king.pos[0] + move[0], king.pos[1] + move[1])
            new_row, new_col = new_pos
            if (0 <= new_row < 8 and 0 <= new_col < 8):
                if king.is_valid_move(new_pos, self.board):
                    # Temp move
                    original_piece = self.get_piece_from(new_pos)
                    self.board[king.pos[0]][king.pos[1]], self.board[new_pos[0]][new_pos[1]] = None, king
                    if not self.is_in_check():
                        # Restore pieces
                        self.board[king.pos[0]][king.pos[1]], self.board[new_pos[0]][new_pos[1]] = king, original_piece
                        return False
                    # Restore pieces
                    self.board[king.pos[0]][king.pos[1]], self.board[new_pos[0]][new_pos[1]] = king, original_piece
        return True
        
    def can_block_king(self, king):
        """
        Checks if any piece can block the check on the king.

        Args:
            king (Piece): The king piece.

        Returns:
            bool: True if a piece can block the check, False otherwise.
        """
        # Check if any piece can block the check
        threat_pieces = [self.black_threats, self.white_threats][king.color]
        for threat in threat_pieces:
            if isinstance(threat, (Bishop, Rook, Queen)):
                blocking_tiles = []
                k_row, k_col = king.pos
                t_row, t_col = threat.pos
                row_step = 1 if t_row > k_row else -1 if t_row < k_row else 0
                col_step = 1 if t_col > k_col else -1 if t_col < k_col else 0

                current_row, current_col = k_row + row_step, k_col + col_step
                while(current_row, current_col) != threat.pos:
                    blocking_tiles.append((current_row, current_col)) # Append a tuple of possible pos to block at
                    current_row += row_step
                    current_col += col_step
                
                for new_pos in blocking_tiles:
                    # Check if any piece can move to this square to block the check
                    for piece in [self.black_pieces, self.white_pieces][king.color]:
                        if piece.is_valid_move(new_pos, self.board):
                            return True
        return False
                
    def can_eliminate_threat(self, king):
        """
        Checks if the given king can eliminate any threats on the board.

        Args:
            king (King): The king to check for threat elimination.

        Returns:
            bool: True if the king can eliminate a threat, False otherwise.
        """
        threat_pieces = [self.black_threats, self.white_threats][king.color]

        for threat in threat_pieces:
            for row in self.board:
                for piece in row:
                    if piece and (piece.color == king.color) and (not isinstance(piece, King)):
                        if piece.is_valid_move(threat.pos, self.board):
                            return True
        return False
