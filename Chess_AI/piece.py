# Parent Piece Class

# ♚♛♜♝♞♟︎
# ♔♕♖♗♘♙

class Piece:
    def __init__(self, color, pos) -> None:
        self.color = color
        self.pos = pos

    # Functions for child classes to implement
    def is_valid_move(self, new_pos, board) -> bool:
        pass

    def move(self, new_pos, board) -> None:
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
                if (board[row + (1 * self.color)][col] == None and board[new_row][new_col] == None):  # If no pieces in the way
                    self.first_move = False
                    return True
        else:
            # If not first move, can only move 1 space
            if new_row == row + (1 * self.color) and new_col == col:
                if board[new_row][new_col] == None:  # If no pieces in the way
                    return True
        # Capture
        if new_row == row + (1 * self.color) and new_col == col + (1 * self.color):
            if (desired_location := board[new_row][new_col].islower() and self.color):  # If black target and white pawn
                return True
            
            elif (desired_location.isupper() and self.color == -1):  # If white target and black pawn
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

class Knight(Piece):
    def __init__(self, color, pos) -> None:
        super().__init__(color, pos)
        self.id = "N" if color == 1 else "n"

class Bishop(Piece):
    def __init__(self, color, pos) -> None:
        super().__init__(color, pos)
        self.id = "B" if color == 1 else "b"

class Queen(Piece):
    def __init__(self, color, pos) -> None:
        super().__init__(color, pos)
        self.id = "Q" if color == 1 else "q"

class King(Piece):
    def __init__(self, color, pos) -> None:
        super().__init__(color, pos)
        self.id = "K" if color == 1 else "k"
