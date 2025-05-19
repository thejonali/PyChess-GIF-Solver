# PyChess-GIF-Solver - gif.py
# ---------------------------
# GIF creation utility for chess move sequences.
#
# Author: thejonali (https://github.com/thejonali)
# License: Apache 2.0

from PIL import Image, ImageDraw

def create_gif_from_moves(moves, start_position, piece_images_path="Images", out_path="chess_moves.gif"):
    """
    Create a GIF showing the sequence of best moves from the current position.

    Args:
        moves (list): List of chess.Move objects.
        start_position (list): 2D list representing the board state.
        piece_images_path (str): Path to piece images.
        out_path (str): Output GIF file path.
    """
    frames = []
    board_state = [row[:] for row in start_position]  # Deep copy

    def draw_board_state(board_state):
        frame = Image.new('RGB', (480, 480), (255, 255, 255))
        draw = ImageDraw.Draw(frame)
        for row in range(8):
            for col in range(8):
                color = (255, 255, 255) if (row + col) % 2 == 0 else (128, 128, 128)
                draw.rectangle([col * 60, row * 60, (col + 1) * 60, (row + 1) * 60], fill=color)
                piece = board_state[row][col]
                if piece:
                    # Match the board's piece size (44x44)
                    piece_img = Image.open(f"{piece_images_path}/{piece}.png").resize((44, 44), Image.LANCZOS)
                    # Center the piece in the 60x60 square
                    offset_x = col * 60 + (60 - 44) // 2
                    offset_y = row * 60 + (60 - 44) // 2
                    frame.paste(piece_img, (offset_x, offset_y), piece_img)
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
    frames[0].save(out_path, save_all=True, append_images=frames[1:], duration=500, loop=0)
