# PyChess-GIF-Solver - chess_piece.py
# -----------------------------------
# ChessPiece widget: represents a chess piece on the board.
#
# Author: thejonali (https://github.com/thejonali)
# License: Apache 2.0

from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class ChessPiece(QLabel):
    """
    Represents a chess piece on the board.
    Handles display and piece type.
    """
    def __init__(self, piece_type: str, pixmap=None, parent=None):
        super().__init__(parent)
        self.piece_type = piece_type  # e.g. "w_pawn", "b_queen", ""
        self.setFixedSize(60, 60)
        self.setAlignment(Qt.AlignCenter)
        if pixmap:
            self.setPixmap(pixmap)
        else:
            self.clear_piece()

    def set_piece(self, piece_type: str, pixmap=None):
        self.piece_type = piece_type
        if pixmap:
            self.setPixmap(pixmap)
        else:
            self.clear_piece()

    def clear_piece(self):
        self.piece_type = ""
        self.setPixmap(QPixmap())  # Use an empty QPixmap instead of None
