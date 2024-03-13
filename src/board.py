from const import *
from square import Square
from piece import *
from move import Move


class Board:
    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]

        self._create()
        self._create()

        self._add_pieces('white')
        self._add_pieces('black')

    def calc_moves(self, piece, row, col):
        # Calculate all the possible (valid) moves of an specific piece pn a specific position

        def pawn_moves():
            # steps
            steps = 1 if piece.moved else 2
            # vertical moves
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for move_row in range(start, end, piece.dir):
                if Square.in_range(move_row):
                    if self.squares[move_row][col].isempty():
                        # create initial and final move squares
                        initial = Square(move_row, col)
                        final = Square(move_row, col)
                        # create a new move
                        move = Move(initial, final)
                        piece.add_move(move)
                    # blocked
                    else:
                        break
                # not in range
                else:
                    break

            # diagonal moves
            possible_move_row = row + piece.dir
            possible_move_cols = [col-1, col+1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        # create initial and final move squares
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)

                        # create a new move
                        move = Move(initial, final)
                        # append new move
                        piece.add_move(move)

        def knight_moves():
            # 8 possible moves
            possible_moves = [
                (row-2, col + 1),
                (row-2, col - 1),
                (row-1, col + 2),
                (row-1, col - 2),
                (row+1, col + 2),
                (row+1, col - 2),
                (row+2, col + 1),
                (row+2, col - 1),
            ]
            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color):
                        # create squares of the new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)

                        # create new move
                        move = Move(initial, final)

                        # append valid move
                        piece.add_move(move)

        def straightline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        # create squares of the possible new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)

                        # empty
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            piece.add_move(move)

                        # has enemy piece
                        if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            piece.add_move(move)
                            break

                        # has teeam piece
                        if self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break

                    # not in range
                    else:
                        break
                    # incremanting incrs
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr

        def king_moves():
            adjs = [
                (row-1, col+0),  # up
                (row-1, col+1),  # up-right
                (row+0, col+1),  # right
                (row+1, col+1),  # down-right
                (row+1, col+0),  # down
                (row+1, col-1),  # down-left
                (row+0, col-1),  # left
                (row-1, col-1),  # up-left
            ]

            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        # create squares of the new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
                        piece.add_move(move)

        if isinstance(piece, Pawn):  # piece is a pawn
            pawn_moves()
        elif isinstance(piece, Knight):  # piece is a knight
            knight_moves()

        elif isinstance(piece, Bishop):  # piece is a bishop
            straightline_moves([
                (-1, 1),  # up-right
                (-1, -1),  # up_left
                (1, 1),  # down-right
                (1, -1)  # down-left
            ])
        elif isinstance(piece, Rook):  # piece is a rook
            straightline_moves([
                (-1, 0),  # up
                (1, 0),  # down
                (0, -1),  # left
                (0, 1)  # right
            ])
        elif isinstance(piece, Queen):  # piece is a queen
            straightline_moves([
                (-1, 1),  # up-right
                (-1, -1),  # up_left
                (1, 1),  # down-right
                (1, -1),  # down-left
                (-1, 0),  # up
                (1, 0),  # down
                (0, -1),  # left
                (0, 1),  # right
            ])

        elif isinstance(piece, King):  # piece is a king
            king_moves()

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)
        # pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))
        self.squares[5][0] = Square(5, 0, Pawn(color))
        self.squares[4][3] = Square(5, 0, Pawn(color))

        # knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 1, Knight(color))

        # bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 2, Bishop(color))
        self.squares[4][5] = Square(4, 2, Bishop(color))

        # rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # king
        self.squares[row_other][4] = Square(row_other, 4, King(color))
        self.squares[3][4] = Square(row_other, 4, King(color))
