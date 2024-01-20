# Parent Piece Class
class Piece:
    def __init__(self, color, id, pos) -> None:
        if color == 1:  # White
            self.id = id.upper()
        elif color == -1:  # Black
            self.id = id.lower()

        self.color = color
        self.pos = pos

    # Functions for child classes to implement
    def is_valid_move(self, new_pos, board) -> bool:
        pass

    def move(self, new_pos, board) -> None:
        if self.is_valid_move(new_pos, board):
            self.pos = new_pos


# Child classes
class Pawn(Piece):
    def __init__(self, color, pos) -> None:
        super().__init__(color, "p", pos)
        self.first_move = True

    def is_valid_move(self, new_pos, board) -> bool:
        x, y = self.pos
        new_x, new_y = new_pos

        # NOTE: self.color is -1 or +1, so it is used to determine direction

        # General Movement
        if self.first_move:
            # If first move, can move 2 spaces
            if new_x == x + (2 * self.color) and new_y == y:
                if (board[x + (1 * self.color)][y] == " " and board[new_x][new_y] == " "):  # If no pieces in the way
                    self.first_move = False
                    return True
        else:
            # If not first move, can only move 1 space
            if new_x == x + (1 * self.color) and new_y == y:
                if board[new_x][new_y] == " ":  # If no pieces in the way
                    return True

        # Capture
        if new_x == x + (1 * self.color) and (new_y == y + 1 or new_y == y - 1):
            if (desired_location := board[new_x][new_y].islower() and self.color):  # If black target and white pawn
                return True

            elif (
                desired_location.isupper() and self.color == -1
            ):  # If white target and black pawn
                return True

        return False

    def move(self, new_pos, board) -> None:
        super().move(new_pos, board)
        x, _ = self.pos

        if (x == 0 or x == 7):  # TODO: (NOTE) Is there ever a case where a pawn could be pushed backwards?
            self.promote(board)

    def promote(self, board):
        raise NotImplementedError


class Rook(Piece):
    def __init__(self, color, pos) -> None:
        super().__init__(color, "r", pos)


class Knight(Piece):
    def __init__(self, color, pos) -> None:
        super().__init__(color, "k", pos)


class Bishop(Piece):
    def __init__(self, color, pos) -> None:
        super().__init__(color, "b", pos)


class Queen(Piece):
    def __init__(self, color, pos) -> None:
        super().__init__(color, "q", pos)


class King(Piece):
    def __init__(self, color, pos) -> None:
        super().__init__(color, "k", pos)
