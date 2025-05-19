# PyChess-GIF-Solver - chess_engine.py
# ------------------------------------
# ChessEngine: wrapper for UCI chess engine operations.
#
# Author: thejonali (https://github.com/thejonali)
# License: Apache 2.0

import chess
import chess.engine

class ChessEngine:
    """
    Wrapper for UCI chess engine operations.
    """
    def __init__(self, engine_path):
        self.engine_path = engine_path

    def solve(self, chess_board, time_limit=10.0):
        """
        Solve the position from a ChessBoard object.
        Args:
            chess_board (ChessBoard): The board object.
            time_limit (float): Time in seconds for engine analysis.
        Returns:
            (list[chess.Move], str): List of best moves and info string.
        """
        fen = chess_board.get_fen()
        try:
            board_obj = chess.Board(fen)
        except ValueError as e:
            return [], f"Invalid FEN: {e}"

        engine = chess.engine.SimpleEngine.popen_uci(self.engine_path)
        info = engine.analyse(board_obj, chess.engine.Limit(time=time_limit))
        best_moves = info["pv"]
        engine.quit()
        moves_text = "Best moves: " + " ".join(move.uci() for move in best_moves)
        return best_moves, moves_text
