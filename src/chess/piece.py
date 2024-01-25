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
        self.has_moved = 0

    def is_valid_move(self, new_pos, board) -> bool:
        """
        Checks if the move to the new position is valid for the piece on the given chessboard.

        Args:
            new_pos (tuple): The position to which the piece is being moved.
            board (Board): The chessboard on which the piece is placed.

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        #if self.pos in self.get_all_moves(board):
        #    return True
        # TODO: Test the get_all_moves then switch is_valid_move to use this logic

    def get_all_moves(self, board) -> list:
        """
        Returns a list of all possible moves for the piece on the given chessboard.

        Args:
            board (Board): The chessboard on which the piece is placed.

        Returns:
            list: A list of all possible moves for the piece on the given chessboard.
        """
        moves = []


# Child classes
class Pawn(Piece):
    def __init__(self, color, pos) -> None:
        super().__init__(color, pos)
        self.id = "P" if color == 1 else "p"

    def is_valid_move(self, new_pos, board) -> bool:
        row, col = self.pos
        new_row, new_col = new_pos
        # NOTE: self.color is -1 or +1, so it is used to determine direction

        # General Movement
        if self.has_moved == 0 and abs(new_row - row) in [2, 5]:
            # If first move, can move 2 spaces
            if new_row == (row + (2 * self.color)) and col == new_col:
                 # If no pieces in the way
                if (board[row + (1 * self.color)][col] == None and board[new_row][new_col] == None):
                    return True
                
        # If not first move, can only move 1 space
        if new_row == row + (1 * self.color) and new_col == col:
            if board[new_row][new_col] == None:  # If no pieces in the way
                if new_row in [0,7]:
                    return Queen(self.color, new_pos)
                return True
                
        # Capture
        if new_row == row + (1 * self.color) and (new_col == col + 1 or new_col == col - 1):
            # If the piece at the desired location is not
            desired_location = board[new_row][new_col]
            if desired_location is not None:
                if (desired_location.id.islower() and self.id.isupper()) or \
                    (desired_location.id.isupper() and self.id.lower()):
                    if new_row in [0,7]:
                        return Queen(self.color, new_pos)
                    return True
        # TODO: En Passant
        return False
    
    def get_all_moves(self, board) -> list:
        moves = []
        row, col = self.pos
        step = -1 if self.color == 1 else 1

        # Forward movement
        if board[row+step][col] is None:
            moves.append((row+step, col))
            # If first move, can move 2 spaces
            if not self.has_moved and board[(row+2)*step][col] is None:
                moves.append((row + 2 * step, col))

        # Capturing
        for lateral in [-1, 1]:
            if 0 <= (col+lateral) < 8:
                capture_row, capture_col = (row+step, col+lateral)
                # If there is a piece to capture
                if board[capture_row][capture_col] is not None:
                    if board[capture_row][capture_col].color != self.color:
                        moves.append((capture_row, capture_col))
        return moves

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
    
    def get_all_moves(self, board) -> list:
        row, col = self.pos
        moves = []
        potential_moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for direction in potential_moves:
            for i in range(1, 8):
                potent_row, potent_col = direction[0], direction[1]
                end_row = row + potent_row * i
                end_col = col + potent_col * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_pos = board[end_row][end_col]
                    if end_pos is None or end_pos.color != self.color: # If the square is empty
                        moves.append((end_row, end_col))
                        break
                    else: break
                else: break
        return moves
    
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
            return True
        return False
    
    def get_all_moves(self, board) -> list:
        row, col = self.pos
        moves = []
        potential_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        for direction in potential_moves:
            potent_row, potent_col = direction[0], direction[1]
            end_row = row + potent_row
            end_col = col + potent_col
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_pos = board[end_row][end_col]
                if end_pos is None or end_pos.color != self.color:
                    moves.append((end_row, end_col))
        return moves

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
        
    def get_all_moves(self, board) -> list:
        row, col = self.pos
        moves = []
        potential_moves = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for direction in potential_moves:
            potent_row, potent_col = direction[0], direction[1]
            for i in range(1, 8):
                end_row = row + potent_row * i
                end_col = col + potent_col * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_pos = board[end_row][end_col]
                    if end_pos is None or end_pos.color != self.color:
                        moves.append((end_row, end_col))
                        break
                    else: break
                else: break
        return moves

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
    
    def get_all_moves(self, board) -> list:
        # Queen moves are a combination of Rook and Bishop moves
        return Rook.get_all_moves(self, board) + Bishop.get_all_moves(self, board)


class King(Piece):
    def __init__(self, color, pos) -> None:
        super().__init__(color, pos)
        self.id = "K" if color == 1 else "k"
        self.moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

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
        if row_diff <= 1 and col_diff <= 1 and (row_diff + col_diff > 0):
            destination_piece = board[new_row][new_col]
            if destination_piece is not None:
                if destination_piece.id.lower() == "k" or \
                    (destination_piece.id.isupper() and self.id.isupper()) or \
                        (destination_piece.id.islower() and self.id.islower()):
                    return False
            return True
                
        # Castling
        elif row_diff == 0 and col_diff == 2 and self.pos == (row, 3):
            return 'castle' # Return 'castle' to indicate that the move is valid logically and is a castle move
        return False
    
    def get_all_moves(self, board) -> list:
        row, col = self.pos
        moves = []
        potential_moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for direction in potential_moves:
            potent_row, potent_col = direction[0], direction[1]
            end_row = row + potent_row
            end_col = col + potent_col

            # Check if the move is within the board
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_pos = board[end_row][end_col]
                if end_pos is None or end_pos.color != self.color:
                    if not board.is_in_check([end_pos, self.color]):
                        moves.append((end_row, end_col))

        # Castling
        for direction in range[-2, 2]:
            if board.can_king_castle((row, col+direction), self):
                moves.append((row, col+direction))
        return moves