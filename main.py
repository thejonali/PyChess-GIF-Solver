# PyChess-GIF-Solver
# ------------------
# An interactive GUI tool to set up chess positions, solve them using a UCI chess engine,
# and generate animated GIFs of the best move sequence. Designed for easy manual setup,
# engine integration, and future extensibility.
#
# Author: thejonali (https://github.com/thejonali)
# License: Apache 2.0

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton, QGridLayout,
    QVBoxLayout, QHBoxLayout, QFrame
)
from PyQt5.QtGui import QPixmap, QImage, QMovie
from PyQt5.QtCore import Qt
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtGui import QPainter
from PIL import Image, ImageDraw
from chess_board import ChessBoard
from chess_piece import ChessPiece
from chess_solver import ChessSolver
import os

ENGINE_PATH = "chessidle"  # Path to your UCI chess engine (e.g., "stockfish")

# List of chess piece names, including a blank for empty squares
chess_pieces = [
    "", "w_pawn", "w_knight", "w_bishop", "w_rook", "w_queen", "w_king",
    "b_pawn", "b_knight", "b_bishop", "b_rook", "b_queen", "b_king"
]

def load_piece_images():
    """
    Load and resize chess piece images for display on the board.

    Returns:
        dict: Mapping from piece name to QPixmap.
    """
    piece_images = {"": None}
    for piece in chess_pieces[1:]:
        img = Image.open(f"Images/{piece}.png")
        img = img.resize((44, 44), Image.LANCZOS)  # Slightly smaller than 60x60 for padding
        data = img.convert("RGBA").tobytes("raw", "RGBA")
        qimg = QImage(data, img.width, img.height, QImage.Format_RGBA8888)
        piece_images[piece] = QPixmap.fromImage(qimg)
    return piece_images

def get_default_icon_pixmap():
    """
    Return a blank light gray square as a QPixmap.

    Returns:
        QPixmap: Default placeholder icon.
    """
    size = 120
    image = QPixmap(size, size)
    image.fill(Qt.lightGray)
    return image

def clear_board():
    """
    Clear all pieces from the board and reset the display.
    Also resets the GIF display and disables the pause/play button.
    """
    global chess_board_widget, gif_label, pause_play_button
    chess_board_widget.clear_board()
    # Reset gif label to default icon
    if gif_label is not None:
        gif_label.setPixmap(get_default_icon_pixmap().scaled(480, 480, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        gif_label.setMovie(None)
    # Set pause/play button to "Play" and disable it
    if pause_play_button is not None:
        pause_play_button.setText("Play")
        pause_play_button.setEnabled(False)

def on_square_click(row, col):
    """
    Cycle through all pieces for the clicked square.
    """
    global chess_board_widget, piece_images
    current_piece = chess_board_widget.board_pieces[row][col]
    next_piece_index = (chess_pieces.index(current_piece) + 1) % len(chess_pieces)
    next_piece = chess_pieces[next_piece_index]
    chess_board_widget.set_piece(row, col, next_piece)

def on_square_right_click(row, col):
    """
    Swap the color of the piece on the clicked square (white <-> black).
    """
    global chess_board_widget
    current_piece = chess_board_widget.board_pieces[row][col]
    if current_piece.startswith("w_"):
        new_piece = "b_" + current_piece[2:]
    elif current_piece.startswith("b_"):
        new_piece = "w_" + current_piece[2:]
    else:
        return
    chess_board_widget.set_piece(row, col, new_piece)

def on_square_double_right_click(row, col):
    """
    Remove any piece from the clicked square.
    """
    global chess_board_widget
    chess_board_widget.clear_piece(row, col)

def on_square_hover(row, col):
    """
    Bind keypresses to place a specific piece on the hovered square.
    """
    global chess_board_widget, piece_images, main_window
    def on_key_press(event):
        piece_map = {
            "p": "w_pawn", "P": "b_pawn",
            "n": "w_knight", "N": "b_knight",
            "b": "w_bishop", "B": "b_bishop",
            "r": "w_rook", "R": "b_rook",
            "q": "w_queen", "Q": "b_queen",
            "k": "w_king", "K": "b_king"
        }
        piece = piece_map.get(event.text())
        if piece:
            chess_board_widget.set_piece(row, col, piece)
    main_window.keyPressEvent = on_key_press

def solve_chess_scenario():
    """
    Solve the current chess scenario using the chess engine and display the best moves.
    """
    global moves_label, chess_board_widget, gif_label, pause_play_button, gif_movie, gif_paused, solver
    moves_text = solver.solve_and_gif(chess_board_widget)
    moves_label.setText(moves_text)
    # Display the gif in the gif_label and enable pause/play button
    if gif_label is not None:
        from PyQt5.QtGui import QMovie
        gif_movie = QMovie("chess_moves.gif")
        gif_label.setMovie(gif_movie)
        gif_movie.start()
        gif_paused = False
        if pause_play_button is not None:
            pause_play_button.setEnabled(True)
            pause_play_button.setText("Pause")

def toggle_gif_pause_play():
    """
    Pause or play the gif animation, toggling the button text accordingly.
    """
    global gif_movie, gif_paused, pause_play_button
    if gif_movie is not None:
        if gif_paused:
            gif_movie.start()
            gif_paused = False
            pause_play_button.setText("Pause")
        else:
            gif_movie.setPaused(True)
            gif_paused = True
            pause_play_button.setText("Play")

class ChessMainWindow(QMainWindow):
    """
    Main application window for the Chess AI Solver / GIF tool.
    Handles all GUI layout and widget initialization.
    """
    def __init__(self):
        super().__init__()
        global chess_board_widget, piece_images, moves_label, main_window, gif_label, gif_movie, pause_play_button, gif_paused, solver
        main_window = self
        gif_movie = None
        gif_paused = False
        self.setWindowTitle("Chess AI Solver / GIF")
        piece_images = load_piece_images()
        solver = ChessSolver(ENGINE_PATH)
        central = QWidget()
        self.setCentralWidget(central)
        main_vbox = QVBoxLayout()
        central.setLayout(main_vbox)

        # Piece images row
        pieces_frame = QHBoxLayout()
        for piece in chess_pieces[1:]:
            lbl = QLabel()
            lbl.setPixmap(piece_images[piece])
            lbl.setFixedSize(60, 60)
            pieces_frame.addWidget(lbl)
        main_vbox.addLayout(pieces_frame)

        # Shortcut info
        shortcut_text = (
            "Shortcut keys for placing pieces (hover over a square and press key):\n"
            "p: White Pawn, P: Black Pawn, n: White Knight, N: Black Knight, "
            "b: White Bishop, B: Black Bishop, r: White Rook, R: Black Rook, "
            "q: White Queen, Q: Black Queen, k: White King, K: Black King"
        )
        shortcut_label = QLabel(shortcut_text)
        shortcut_label.setStyleSheet("color: gray; font-size: 10pt;")
        main_vbox.addWidget(shortcut_label)

        # --- Board and GIF side by side ---
        board_and_gif_hbox = QHBoxLayout()

        # --- Left: Board ---
        left_vbox = QVBoxLayout()
        chess_board_widget = ChessBoard(piece_images)
        # Attach event handlers to each square
        for row in range(8):
            for col in range(8):
                square = chess_board_widget.squares[row][col]
                square.mousePressEvent = lambda e, r=row, c=col: (
                    on_square_click(r, c) if e.button() == Qt.LeftButton else
                    on_square_right_click(r, c) if e.button() == Qt.RightButton else None
                )
                square.mouseDoubleClickEvent = lambda e, r=row, c=col: (
                    on_square_double_right_click(r, c) if e.button() == Qt.RightButton else None
                )
                square.enterEvent = lambda e, r=row, c=col: on_square_hover(r, c)
        left_vbox.addWidget(chess_board_widget, alignment=Qt.AlignLeft)

        # --- Buttons (Solve, Clear, Pause/Play) ---
        button_frame = QHBoxLayout()
        solve_button = QPushButton("Solve")
        solve_button.clicked.connect(solve_chess_scenario)
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(clear_board)
        pause_play_button = QPushButton("Pause")
        pause_play_button.setEnabled(False)
        pause_play_button.clicked.connect(toggle_gif_pause_play)
        button_frame.addWidget(solve_button)
        button_frame.addWidget(clear_button)
        button_frame.addWidget(pause_play_button)
        left_vbox.addLayout(button_frame)

        # Moves label
        moves_label = QLabel("")
        left_vbox.addWidget(moves_label)

        # --- Right: GIF/placeholder ---
        gif_label = QLabel()
        gif_label.setFixedSize(480, 480)
        gif_label.setAlignment(Qt.AlignCenter)
        gif_label.setPixmap(get_default_icon_pixmap().scaled(480, 480, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        # Add board and gif to the same row
        board_and_gif_hbox.addLayout(left_vbox)
        board_and_gif_hbox.addSpacing(30)
        board_and_gif_hbox.addWidget(gif_label, alignment=Qt.AlignRight | Qt.AlignTop)
        board_and_gif_hbox.addStretch(1)
        main_vbox.addLayout(board_and_gif_hbox)

def main():
    """
    Entry point for the application.
    Initializes and runs the QApplication event loop.
    """
    import sys
    app = QApplication(sys.argv)
    window = ChessMainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
