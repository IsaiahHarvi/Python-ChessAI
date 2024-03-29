import copy
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
        self.white_pieces, self.white_threats = None, None
        self.black_pieces, self.black_threats = None, None
        self.board = self.create_start_board()
        self.piece_count = 32 # Count of the number of pieces on the board--used to determine when to update the piece lists
        self.update_piece_lists()
        self.kings = [self.get_piece_from((7, 3)), self.get_piece_from((0, 3))]

    def create_start_board(self):
        """
        Creates the starting configuration of the chess board.
        """

        # Main pieces
        row0, row7 = [], []
        for index, color in enumerate([-1, 1]):
            for col, piece_object in enumerate([[Rook, Knight, Bishop, King, Queen, Bishop, Knight, Rook], [Rook, Knight, Bishop, King, Queen, Bishop, Knight, Rook]][index]):
                piece = piece_object(color=color, pos=(0 if color == 1 else 7, col))
                row0.append(piece) if color == 1 else row7.append(piece)

        # Pawns
        row1, row6 = [], []
        for col in range(8):
            row1.append([Pawn, Pawn, Pawn, Pawn, Pawn, Pawn, Pawn, Pawn][col](1, pos=(1, col)))
            row6.append([Pawn, Pawn, Pawn, Pawn, Pawn, Pawn, Pawn, Pawn][col](-1, pos=(6, col)))

        board = [
                row0, 
                row1, 
                [None for _ in range(8)], 
                [None for _ in range(8)], 
                [None for _ in range(8)], 
                [None for _ in range(8)], 
                row6, 
                row7
            ]
        board = np.array(board)
        return board

    def update_piece_lists(self):
        """
        Updates the lists of pieces with what is currently on the board.
        """
        self.white_pieces, self.white_threats = [], []
        self.black_pieces, self.black_threats = [], []
        self.kings = []

        for row in self.board:
            for piece in row:
                if isinstance(piece, King):
                    self.kings.insert(piece.color, piece)
                elif piece:
                    if piece.color == 1:
                        self.white_pieces.append(piece)
                    else:
                        self.black_pieces.append(piece)

    def print_board(self, copy_board=None):
        """
        Prints the current state of the chess board.
        """
        board = copy_board if copy_board is not None else self.board
        row_label = [1, 2, 3, 4, 5, 6, 7, 8]
        sum_pieces = 0
        print("    a  b  c  d  e  f  g  h")
        for index, i in enumerate(board):
            print(row_label[index], end = "  ")
            for jndex, piece in enumerate(i):
                sum_pieces += 1 if piece else 0
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
        print("    a  b  c  d  e  f  g  h")

        self.update_piece_lists() if sum_pieces < self.piece_count else None 
        self.piece_count = sum_pieces

    def move_piece(self, current_pos, new_pos, player_checked=False):
        """
        Moves a chess piece from the current position to the new position.

        Args:
            current_pos (str): The current position of the piece in algebraic notation (e.g., "a2").
            new_pos (str): The new position to move the piece to in algebraic notation (e.g., "a4").
        """
        current_pos = (int(current_pos[1]) - 1, ord(current_pos[0]) - 97)
        new_pos = (int(new_pos[1]) - 1, ord(new_pos[0]) - 97)
        piece = self.get_piece_from(current_pos)

        # Show the retrieved piece
        print(retrieved_string := f"Retrieved '{piece.__class__.__name__}' from {current_pos}")
        print(f"{'─' * len(retrieved_string)}")

        if piece:
            moved = piece.is_valid_move(new_pos, self.board)

        # If the player is currently in check, they can only escape check
        if (piece and moved) and player_checked:
            # Temp move the piece
            original_piece = self.get_piece_from(new_pos)
            self.board[current_pos[0]][current_pos[1]], self.board[new_pos[0]][new_pos[1]] = None, piece # Move the piece

            if self.is_in_check([new_pos, piece.color]): # If the king is still in check
                print("Invalid move: You're in check!", end="\n\n")
                self.board[current_pos[0]][current_pos[1]], self.board[new_pos[0]][new_pos[1]] = piece, original_piece # Restore pieces
                return False
            
            else: # If the king is no longer in check
                self.board[current_pos[0]][current_pos[1]], self.board[new_pos[0]][new_pos[1]] = piece, original_piece # Restore pieces
                self.set_piece_at(new_pos, current_pos, piece)
                return True
        
        # If the player is not in check
        if (piece and moved) and not player_checked:
            if isinstance(piece, King): # If the piece is a king
                if self.is_in_check([new_pos, piece.color]): # They can't move into check
                    print("Invalid move: Can't move into check!", end="\n\n")
                    return False

                elif moved == 'castle': # If the piece is a king and the king moved laterally 2 spaces
                    if self.can_king_castle(new_pos, piece): # If the king can castle
                        self.castle_king(new_pos, piece) # Castle the king
                        return True
                    print(f"Invalid Castle: {current_pos} -> {new_pos}", end="\n\n")
                    return False
    
                else: # Regular move
                    self.set_piece_at(new_pos, current_pos, piece)
                    return True
                    
            elif isinstance(moved, Queen): # If the result of moving the piece is a queen, it was a pawn promotion
                self.set_piece_at(new_pos, current_pos, moved)
                return True
            
            # Regular move
            else:
                self.set_piece_at(new_pos, current_pos, piece)
                return True
        else:
            print(f"Invalid move: {current_pos} -> {new_pos}", end="\n\n")
            return False

    def get_piece_from(self, pos, copy_board=None):
        """
        Retrieves the chess piece at the specified position.

        Args:
            pos (tuple): The position of the piece as a tuple of row and column indices.

        Returns:
            object: The chess piece at the specified position.
        """
        board = copy_board if copy_board is not None else self.board
        row, col = pos
        return board[row][col]

    def set_piece_at(self, pos, old_pos, piece, copy_board=None):
        """
        Sets a chess piece at the specified position and updates its old position.

        Args:
            pos (tuple): The position to set the piece at as a tuple of row and column indices.
            old_pos (tuple): The old position of the piece as a tuple of row and column indices.
            piece (object): The chess piece object to set at the specified position.
        """
        board = copy_board if copy_board is not None else self.board
        row, col = pos
        board[row][col] = piece

        # Remove piece from old position
        old_row, old_col = old_pos
        board[old_row][old_col] = None

        # Update piece position
        piece.pos = pos
        piece.has_moved = True
    
    def get_moves(self, color=int) -> list:
        """
        Gets the valid moves for all pieces of a specific color on the board.

        Args:
            color (int): The color of the pieces to get the valid moves for.
        """
        if color == 1:
            pieces = self.white_pieces
        elif color == 0:
            pieces = self.black_pieces

        valid_moves = []
        for piece in pieces:
            for valid_move in piece.get_all_moves(self.board):
                if valid_move:
                    if type(piece) == Pawn: print(valid_move)
                    valid_moves.append(valid_move)

        return valid_moves


    # TODO: Optimize 
    def is_in_check(self, at_location=None) -> tuple or bool:
        """
        Determines if there is a king, or any king, in check on the Board.

        Args:
            at_location (list): For checking if a king will be in check at a specific location.
                                [pos, color]
                                Defaults to none

        Returns:
            A tuple containing a boolean value indicating if the king is in check,
            and the color of the king that is in check.

            If at_location is specified, returns a boolean value indicating if the king will be in check.
        """
        is_check, checked_color, self.white_threats, self.black_threats = False, None, [], []
        if len(self.kings) != 2: raise Exception("Missing King.")

        if not at_location:
            for king in self.kings:
                for row in self.board:
                    for piece in row:
                        if piece and piece.color != king.color:
                            if piece.is_valid_move(king.pos, self.board):
                                is_check = True
                                checked_color = king.color
                                self.white_threats.append(piece) if king.color else self.black_threats.append(piece)
            return is_check, checked_color
        
        else: # Allows to check is a king WILL be in check at a specific location
            for row in self.board:
                for piece in row:
                    if (piece and piece.color != at_location[1]):
                        if piece.is_valid_move(at_location[0], self.board):
                            return True
            return False
                    
    def is_checkmate(self, color=False):
        """
        Determines if the specified color is in checkmate.

        Parameters:
        - color (int): The color of the player to check for checkmate.

        Returns:
        - bool: True if the specified color is in checkmate, False otherwise.
        """
        # Check if King can move out of check

        for king in self.kings if not color else [self.kings[color]]:
            if self.can_king_escape(king):
                return False

            if self.can_block_king(king) or self.can_eliminate_threat(king):
                return False
        
        return Exception("Checkmate!") # TODO: Actually end the game

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
                    if not self.is_in_check()[0]: # TODO: Test with the at_location parameter--passing in new_pos
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
    
    def can_king_castle(self, new_pos, king, copy_board=None) -> bool:
        """
        Checks if the king can castle to the given position on the given board.

        Args:
            new_pos (tuple): The position to which the king is being castled.
            king (King): The king piece to castle.

        Returns:
            bool: True if the king can castle to the given position, False otherwise.
        """
        board = copy_board if copy_board is not None else self.board
        row, col = king.pos
        new_row, new_col = new_pos

        if king.has_moved or self.get_piece_from(new_pos).has_moved:
            return False
        
        # Check if the king is in check
        if self.is_in_check([king.pos, king.color]):
            print("Can't castle while in check!")
            return False

        step = 1 if new_col > col else -1
        rook_col = 7 if step == 1 else 0

        # Check if the king is castling with a rook
        rook = self.get_piece_from((row, rook_col))
        if not rook or not isinstance(rook, Rook):
            print("Can't castle without a rook!")
            return False

        # Check if there are any pieces between the king and the rook
        # and check if the king is moving into check
        for c in range(col+step, new_col-step, step):
            if board[row][c] is not None or (self.is_in_check([(row, c), king.color])):
                print("Can't castle through pieces or check!")
                return False
        
        # Check if the king's new destination is in check
        if self.is_in_check([(row, new_col), king.color]):
            print("Can't castle into check!")
            return False
        
        return True
    
    def castle_king(self, new_pos, king, copy_board=None) -> None:
        """
        Castles the king to the given position on the given board.

        Args:
            new_pos (tuple): The position to which the king is being castled.
            copy_board (Board): The chessboard on which the king is placed.
        """
        board = copy_board if copy_board is not None else self.board
        row, col = king.pos
        _, new_col = new_pos

        step = 1 if new_col > col else -1
        rook_col = 7 if step == 1 else 0
        move_rook_col = col + step

        rook = self.get_piece_from((row, rook_col))

        self.set_piece_at(new_pos, king.pos, king, board)
        self.set_piece_at((row, move_rook_col), (row, rook_col), rook, board)

    def simulate_move(self, move) -> np.ndarray:
        """
        Simulates a move on the board.

        Args:
            move (tuple): The move to simulate.
        """
        c_board = copy.deepcopy(self.board)
        current_pos, new_pos = move
        piece = self.get_piece_from(current_pos, c_board)

        if piece and (moved := piece.is_valid_move(new_pos, c_board)):
            if isinstance(piece, King) and moved == 'castle':
                if self.can_king_castle(new_pos, piece, c_board):
                    self.castle_king(new_pos, piece, c_board)
                    return c_board  # Return the copied board with the move applied
                return c_board  # Return the copied board without the move if castling is invalid
            elif isinstance(moved, Queen):  # Pawn promotion
                self.set_piece_at(new_pos, current_pos, moved, c_board)
                return c_board
            else:  # Regular move
                self.set_piece_at(new_pos, current_pos, piece, c_board)
                return c_board
        else:
            return c_board  # Return the copied board without the move if the move is invalid
