# Parent Piece Class
# ♚♛♜♝♞♟︎
# ♔♕♖♗♘♙

class Piece:
    """
    Represents a chess piece.  Is a parent class for the child classes..
    Pawn, Rook, Knight, Bishop, Queen, and King.

    Attributes:
        color (int): The color of the piece (1, white or -1, black).
        pos (tuple): The current position of the piece on the 2d board np array

    Methods:
        is_valid_move(new_pos, board) -> bool:
            Checks if the move to the new position is valid for the piece on the given chessboard.
    """

    def __init__(self, color, pos) -> None:
        self.color = color
        self.pos = pos

    def is_valid_move(self, new_pos, board) -> bool:
        """
        Checks if the move to the new position is valid for the piece on the given chessboard.

        Args:
            new_pos (tuple): The position to which the piece is being moved.
            board (Board): The chessboard on which the piece is placed.

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        pass

# Child classes
class Pawn(Piece):
    def __init__(self, color, pos) -> None:
        super().__init__(color, pos)
        self.first_move = True
        self.id = "P" if color == 1 else "p"

    def is_valid_move(self, new_pos, board) -> bool:
        row, col = self.pos
        new_row, new_col = new_pos
        # NOTE: self.color is -1 or +1, so it is used to determine direction
        
        # General Movement
        if self.first_move and abs(new_row - row) in [2, 5]:
            # If first move, can move 2 spaces
            if new_row == (row + (2 * self.color)) and col == new_col:
                 # If no pieces in the way
                if (board[row + (1 * self.color)][col] == None and board[new_row][new_col] == None):
                    self.first_move = False
                    return True
                
        # If not first move, can only move 1 space
        if new_row == row + (1 * self.color) and new_col == col:
            if board[new_row][new_col] == None:  # If no pieces in the way
                return True
                
        # Capture
        if new_row == row + (1 * self.color) and (new_col == col + 1 or new_col == col - 1):
            # If the piece at the desired location is not
            desired_location = board[new_row][new_col]
            if desired_location is not None:
                if (desired_location.id.islower() and self.id.isupper()) or \
                    (desired_location.id.isupper() and self.id.lower()):
                    return True
        # TODO: En Passant
        
        # Promotion TODO: Implement promotion

        return False

    def promote(self, board):
        raise NotImplementedError

class Rook(Piece):
    def __init__(self, color, pos) -> None:
        super().__init__(color, pos)
        self.id = "R" if color == 1 else "r"
    
    def is_valid_move(self, new_pos, board) -> bool:
        row, col = self.pos
        new_row, new_col = new_pos

        # Check board boundaries
        if not (0 <= new_row < 8 and 0 <= new_col < 8):
            return False

        # Check horizontal
        if row == new_row and col != new_col:
            step = 1 if new_col > col else -1
            for c in range(col + step, new_col, step):
                if board[row][c]: # If there is a piece in the way
                    return False

        # Check vertical
        elif row != new_row and col == new_col:
            step = 1 if new_row > row else -1
            for r in range(row + step, new_row, step):
                if board[r][col]: # If there is a piece in the way
                    return False
        else:  # If not purely horizontal or vertical move
            return False

        # Check content of destination
        destination_piece = board[new_row][new_col]
        if destination_piece is not None:
            if (destination_piece.id.isupper() and self.id.isupper()) or \
               (destination_piece.id.islower() and self.id.islower()):
                return False
        return True
    
class Knight(Piece):
    def __init__(self, color, pos) -> None:
        super().__init__(color, pos)
        self.id = "N" if color == 1 else "n"
    
    def is_valid_move(self, new_pos, board) -> bool:
        row, col = self.pos
        new_row, new_col = new_pos

        # Check board boundaries
        if not (0 <= new_row < 8 and 0 <= new_col < 8):
            return False

        # Calculate the row/col differences
        row_diff = abs(new_row - row)
        col_diff = abs(new_col - col)

        # Check L-shape (2, 1) or (1, 2)
        if (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2):
            destination_piece = board[new_row][new_col]
            if destination_piece is not None:
                if (destination_piece.id.isupper() and self.id.islower()) or \
                   (destination_piece.id.islower() and self.id.isupper()):
                    return True
        return False

class Bishop(Piece):
    def __init__(self, color, pos) -> None:
        super().__init__(color, pos)
        self.id = "B" if color == 1 else "b"
    
    def is_valid_move(self, new_pos, board) -> bool:
        row, col = self.pos
        new_row, new_col = new_pos

        # Check board boundaries
        if not (0 <= new_row < 8 and 0 <= new_col < 8):
            return False

        # Check if the move is diagonal
        if abs(new_row - row) != abs(new_col - col):
            return False

        # Check if there are no pieces between the current pos and the new pos
        row_step = 1 if new_row > row else -1
        col_step = 1 if new_col > col else -1
        current_row, current_col = row + row_step, col + col_step

        while current_row != new_row and current_col != new_col:
            if board[current_row][current_col] is not None:
                return False
            current_row += row_step
            current_col += col_step

        # Check if the destination square is either empty or contains an opponent's piece
        destination_piece = board[new_row][new_col]
        if destination_piece is not None:
            if (destination_piece.id.isupper() and self.id.isupper()) or \
               (destination_piece.id.islower() and self.id.islower()):
                return False
        return True

class Queen(Piece):
    def __init__(self, color, pos) -> None:
        super().__init__(color, pos)
        self.id = "Q" if color == 1 else "q"

    def is_valid_move(self, new_pos, board) -> bool:
        row, col = self.pos
        new_row, new_col = new_pos

        # Check board bounds
        if not (0 <= new_row < 8 and 0 <= new_col < 8):
            return False

        # Determine if the move is along a row, column, or diagonal
        if row == new_row:  # Horizontal move
            step = 1 if new_col > col else -1
            for c in range(col + step, new_col, step):
                if board[row][c] is not None: # If there is a piece in the way
                    return False

        elif col == new_col:  # Vertical move
            step = 1 if new_row > row else -1
            for r in range(row + step, new_row, step):
                if board[r][col] is not None:
                    return False

        elif abs(new_row - row) == abs(new_col - col):  # Diagonal move
            row_step = 1 if new_row > row else -1
            col_step = 1 if new_col > col else -1
            current_row, current_col = row + row_step, col + col_step
            while current_row != new_row and current_col != new_col:
                if board[current_row][current_col] is not None:
                    return False
                current_row += row_step
                current_col += col_step
        else: # If not purely horizontal, vertical, or diagonal
            return False

        # Check the destination contents
        destination_piece = board[new_row][new_col]
        if destination_piece is not None and \
            ((destination_piece.id.isupper() == self.id.isupper()) or \
              (destination_piece.id.islower() == self.id.islower())):
            return False
        return True

class King(Piece):
    def __init__(self, color, pos) -> None:
        super().__init__(color, pos)
        self.id = "K" if color == 1 else "k"

    def is_valid_move(self, new_pos, board) -> bool:
        row, col = self.pos
        new_row, new_col = new_pos

        # Check board boundaries
        if not (0 <= new_row < 8 and 0 <= new_col < 8):
            return False

        # Calculate the row/col differences
        row_diff = abs(new_row - row)
        col_diff = abs(new_col - col)

        # One square any direction
        # TODO: Check if moving into check
        if row_diff <= 1 and col_diff <= 1 and (row_diff + col_diff > 0):
            destination_piece = board[new_row][new_col]
            if destination_piece is not None:
                if destination_piece.id.lower() == "k" or \
                    (destination_piece.id.isupper() and self.id.isupper()) or \
                        (destination_piece.id.islower() and self.id.islower()):
                    return False
            return True
        return False
            
            