# PyChess-GIF-Solver - chess_board.py
# -----------------------------------
# ChessBoard widget: manages the 8x8 grid of ChessPiece objects and board state.
#
# Author: thejonali (https://github.com/thejonali)
# License: Apache 2.0

from PyQt5.QtWidgets import QFrame, QGridLayout
from PyQt5.QtCore import Qt
from chess_piece import ChessPiece

class ChessBoard(QFrame):
    """
    ChessBoard widget: manages the 8x8 grid of ChessPiece objects and board state.
    """
    def __init__(self, piece_images, parent=None):
        super().__init__(parent)
        self.setFixedSize(480, 480)
        self.grid = QGridLayout()
        self.grid.setSpacing(0)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.grid)
        self.piece_images = piece_images
        self.board_pieces = [["" for _ in range(8)] for _ in range(8)]
        self.squares = [[None for _ in range(8)] for _ in range(8)]
        self._init_board()

    def _init_board(self):
        for row in range(8):
            for col in range(8):
                color = "#ffffff" if (row + col) % 2 == 0 else "#808080"
                piece = ChessPiece("", parent=self)
                piece.setStyleSheet(f"background-color: {color};")
                self.squares[row][col] = piece
                self.grid.addWidget(piece, row, col)

    def set_piece(self, row, col, piece_type):
        self.board_pieces[row][col] = piece_type
        pixmap = self.piece_images.get(piece_type)
        self.squares[row][col].set_piece(piece_type, pixmap)

    def clear_piece(self, row, col):
        self.board_pieces[row][col] = ""
        self.squares[row][col].clear_piece()

    def clear_board(self):
        for row in range(8):
            for col in range(8):
                self.clear_piece(row, col)

    def get_board_state(self):
        return [row[:] for row in self.board_pieces]

    def get_fen(self):
        piece_to_fen = {
            "w_pawn": "P", "w_knight": "N", "w_bishop": "B", "w_rook": "R", "w_queen": "Q", "w_king": "K",
            "b_pawn": "p", "b_knight": "n", "b_bishop": "b", "b_rook": "r", "b_queen": "q", "b_king": "k"
        }
        board_fen = ""
        for row in self.board_pieces:
            empty_count = 0
            for piece in row:
                if piece == "":
                    empty_count += 1
                else:
                    if empty_count > 0:
                        board_fen += str(empty_count)
                        empty_count = 0
                    board_fen += piece_to_fen[piece]
            if empty_count > 0:
                board_fen += str(empty_count)
            board_fen += "/"
        board_fen = board_fen[:-1] + " w - - 0 1"
        return board_fen
