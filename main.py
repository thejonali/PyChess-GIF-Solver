# PyChess-GIF-Solver
# ------------------
# An interactive GUI tool to set up chess positions, solve them using a UCI chess engine,
# and generate animated GIFs of the best move sequence. Designed for easy manual setup,
# engine integration, and future extensibility.
#
# Author: thejonali (https://github.com/thejonali)
# License: Apache 2.0

import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import chess
import chess.engine

ENGINE_PATH = "chessidle"  # Path to your UCI chess engine (e.g., "stockfish")

# List of chess piece names, including a blank for empty squares
chess_pieces = [
    "", "w_pawn", "w_knight", "w_bishop", "w_rook", "w_queen", "w_king",
    "b_pawn", "b_knight", "b_bishop", "b_rook", "b_queen", "b_king"
]

def load_piece_images():
    """Load and resize chess piece images for display on the board."""
    piece_images = {"": None}
    for piece in chess_pieces[1:]:
        img = Image.open(f"Images/{piece}.png")
        img = img.resize((60, 60), Image.LANCZOS)
        piece_images[piece] = ImageTk.PhotoImage(img)
    return piece_images

def clear_board():
    """Clear all pieces from the board and reset the display."""
    global board_pieces, board
    for row in range(8):
        for col in range(8):
            board_pieces[row][col] = ""
            board[row][col].config(image='', width=10, height=5)
            board[row][col].image = None

def load_chess_scenario_touch():
    """Create the chessboard grid and bind mouse events for piece placement."""
    global board
    for row in range(8):
        for col in range(8):
            square = tk.Label(
                board_frame,
                width=10,
                padx=0,
                pady=0,
                height=5,
                bg="white" if (row + col) % 2 == 0 else "gray"
            )
            square.grid(row=row, column=col)
            # Bind left click, right click, double right click, and hover events
            square.bind("<Button-1>", lambda e, r=row, c=col: on_square_click(e, r, c))
            square.bind("<Button-3>", lambda e, r=row, c=col: on_square_right_click(e, r, c))
            square.bind("<Double-Button-3>", lambda e, r=row, c=col: on_square_double_right_click(e, r, c))
            square.bind("<Enter>", lambda e, r=row, c=col: on_square_hover(e, r, c))
            board[row][col] = square

def on_square_click(event, row, col):
    """Cycle through all pieces for the clicked square."""
    global board_pieces, board, piece_images
    current_piece = board_pieces[row][col]
    next_piece_index = (chess_pieces.index(current_piece) + 1) % len(chess_pieces)
    next_piece = chess_pieces[next_piece_index]
    board_pieces[row][col] = next_piece
    if next_piece == "":
        board[row][col].config(image='', width=10, height=5)
    else:
        board[row][col].config(image=piece_images[next_piece], width=60, height=60)
    board[row][col].image = piece_images[next_piece]

def on_square_right_click(event, row, col):
    """Swap the color of the piece on the clicked square (white <-> black)."""
    global board_pieces, board, piece_images
    current_piece = board_pieces[row][col]
    if current_piece.startswith("w_"):
        new_piece = "b_" + current_piece[2:]
    elif current_piece.startswith("b_"):
        new_piece = "w_" + current_piece[2:]
    else:
        return
    board_pieces[row][col] = new_piece
    board[row][col].config(image=piece_images[new_piece], width=60, height=60)
    board[row][col].image = piece_images[new_piece]

def on_square_double_right_click(event, row, col):
    """Remove any piece from the clicked square."""
    global board_pieces, board
    board_pieces[row][col] = ""
    board[row][col].config(image='', width=10, height=5)
    board[row][col].image = None

def on_square_hover(event, row, col):
    """Bind keypresses to place a specific piece on the hovered square."""
    global board_pieces, board, piece_images, root
    def on_key_press(event):
        # Map keys to piece names
        piece_map = {
            "p": "w_pawn", "P": "b_pawn",
            "n": "w_knight", "N": "b_knight",
            "b": "w_bishop", "B": "b_bishop",
            "r": "w_rook", "R": "b_rook",
            "q": "w_queen", "Q": "b_queen",
            "k": "w_king", "K": "b_king"
        }
        piece = piece_map.get(event.char)
        if piece:
            board_pieces[row][col] = piece
            board[row][col].config(image=piece_images[piece], width=60, height=60)
            board[row][col].image = piece_images[piece]
    root.bind("<Key>", on_key_press)

def get_board_fen():
    """Convert the current board state to a FEN string."""
    piece_to_fen = {
        "w_pawn": "P", "w_knight": "N", "w_bishop": "B", "w_rook": "R", "w_queen": "Q", "w_king": "K",
        "b_pawn": "p", "b_knight": "n", "b_bishop": "b", "b_rook": "r", "b_queen": "q", "b_king": "k"
    }
    board_fen = ""
    for row in board_pieces:
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

def solve_chess_scenario():
    """Solve the current chess scenario using the chess engine and display the best moves."""
    global moves_label, board_pieces
    board_fen = get_board_fen()
    try:
        board_obj = chess.Board(board_fen)
    except ValueError as e:
        moves_label.config(text=f"Invalid FEN: {e}")
        return

    engine = chess.engine.SimpleEngine.popen_uci(ENGINE_PATH)
    info = engine.analyse(board_obj, chess.engine.Limit(time=5.0))
    best_moves = info["pv"]
    moves_text = "Best moves: " + " ".join(move.uci() for move in best_moves)
    moves_label.config(text=moves_text)
    engine.quit()
    create_gif_from_moves(best_moves, board_pieces)

def create_gif_from_moves(moves, start_position):
    """Create a GIF showing the sequence of best moves from the current position."""
    frames = []
    board_state = [row[:] for row in start_position]  # Copy the starting position

    def draw_board_state(board_state):
        """Draw the current board state as an image."""
        frame = Image.new('RGB', (480, 480), (255, 255, 255))
        draw = ImageDraw.Draw(frame)
        for row in range(8):
            for col in range(8):
                color = (255, 255, 255) if (row + col) % 2 == 0 else (128, 128, 128)
                draw.rectangle([col * 60, row * 60, (col + 1) * 60, (row + 1) * 60], fill=color)
                piece = board_state[row][col]
                if piece:
                    piece_img = Image.open(f"Images/{piece}.png").resize((60, 60), Image.LANCZOS)
                    frame.paste(piece_img, (col * 60, row * 60), piece_img)
        return frame

    frames.append(draw_board_state(board_state))
    for move in moves:
        move_str = move.uci()
        from_square = (ord(move_str[0]) - ord('a'), 8 - int(move_str[1]))
        to_square = (ord(move_str[2]) - ord('a'), 8 - int(move_str[3]))
        piece = board_state[from_square[1]][from_square[0]]
        board_state[from_square[1]][from_square[0]] = ""
        board_state[to_square[1]][to_square[0]] = piece
        frame = draw_board_state(board_state)
        frames.append(frame)
    frames[0].save('chess_moves.gif', save_all=True, append_images=frames[1:], duration=500, loop=0)

def setup_gui():
    """Set up the main GUI layout and widgets."""
    global root, board_frame, board, board_pieces, piece_images, moves_label
    root = tk.Tk()
    root.title("Chess AI Solver / GIF")
    piece_images = load_piece_images()

    # Display all chess piece images at the top
    pieces_frame = tk.Frame(root)
    pieces_frame.grid(row=0, column=0, columnspan=3, pady=20)
    for i, piece in enumerate(chess_pieces[1:]):
        piece_label = tk.Label(pieces_frame, image=piece_images[piece])
        piece_label.grid(row=0, column=i, padx=5)

    # Add shortcut keys info just below the images of the chess pieces, above the chessboard
    shortcut_text = (
        "Shortcut keys for placing pieces (hover over a square and press key):\n"
        "p: White Pawn, P: Black Pawn, n: White Knight, N: Black Knight, "
        "b: White Bishop, B: Black Bishop, r: White Rook, R: Black Rook, "
        "q: White Queen, Q: Black Queen, k: White King, K: Black King"
    )
    shortcut_label = tk.Label(root, text=shortcut_text, fg="gray", font=("Arial", 9))
    shortcut_label.grid(row=1, column=0, columnspan=3, pady=(0, 10))

    # Chessboard frame
    board_frame = tk.Frame(root)
    board_frame.grid(row=2, column=0, columnspan=3, pady=20)
    board = [[None for _ in range(8)] for _ in range(8)]
    board_pieces = [["" for _ in range(8)] for _ in range(8)]
    load_chess_scenario_touch()

    # Buttons for clearing and solving
    button_frame = tk.Frame(root)
    button_frame.grid(row=4, column=0, columnspan=3, pady=20)
    clear_button = tk.Button(button_frame, text="Clear", command=clear_board)
    clear_button.grid(row=0, column=0, padx=10)
    solve_button = tk.Button(button_frame, text="Solve", command=solve_chess_scenario)
    solve_button.grid(row=0, column=1, padx=10)

    # Label to display best moves
    moves_label = tk.Label(root, text="")
    moves_label.grid(row=3, column=0, columnspan=3)

def main():
    """Start the GUI application."""
    setup_gui()
    root.mainloop()

if __name__ == "__main__":
    main()
