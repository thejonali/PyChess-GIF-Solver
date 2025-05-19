# PyChess-GIF-Solver - chess_solver.py
# ------------------------------------
# ChessSolver: integrates ChessBoard, ChessEngine, and GIF creation.
#
# Author: thejonali (https://github.com/thejonali)
# License: Apache 2.0

from chess_engine import ChessEngine
from gif import create_gif_from_moves

class ChessSolver:
    """
    High-level solver that integrates ChessBoard, ChessEngine, and GIF creation.
    """
    def __init__(self, engine_path):
        self.engine = ChessEngine(engine_path)

    def solve_and_gif(self, chess_board, gif_out_path="chess_moves.gif"):
        """
        Solve the board and create a GIF of the best move sequence.

        Args:
            chess_board (ChessBoard): The board object.
            gif_out_path (str): Output path for the GIF.

        Returns:
            moves_text (str): Description of best moves or error.
        """
        moves, moves_text = self.engine.solve(chess_board)
        if moves:
            create_gif_from_moves(moves, chess_board.get_board_state(), out_path=gif_out_path)
        return moves_text
