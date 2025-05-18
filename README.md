# PyChess-GIF-Solver

A simple graphical tool to set up chess positions, solve them using a UCI chess engine, and generate animated GIFs of the best move sequence.

## Features

- Interactive chessboard for manual piece placement.
- Keyboard shortcuts for quick piece selection.
- Solve the current position using a UCI chess engine (e.g., Stockfish or ChessIdle).
- Generates a GIF showing the best move sequence.
- Clear/reset the board easily.

## Requirements

- Python 3.7+
- [Pillow](https://pypi.org/project/Pillow/)
- [python-chess](https://pypi.org/project/python-chess/)
- [tkinter](https://wiki.python.org/moin/TkInter) (usually included with Python)

Install dependencies:
```
pip install -r requirements.txt
```

### Chess Engine

This project is preconfigured to use [ChessIdle](https://github.com/alvinypeng/chessidle) as the default UCI chess engine.  
If you want to use another engine (like [Stockfish](https://stockfishchess.org/download/)), change the `ENGINE_PATH` variable in `main.py` to the path or command for your engine.

## Usage

1. Place chess piece images in the `Images/` directory, named as:
   - `w_pawn.png`, `w_knight.png`, `w_bishop.png`, `w_rook.png`, `w_queen.png`, `w_king.png`
   - `b_pawn.png`, `b_knight.png`, `b_bishop.png`, `b_rook.png`, `b_queen.png`, `b_king.png`
2. Make sure your chess engine (e.g., ChessIdle or Stockfish) is installed and update the `ENGINE_PATH` variable in `main.py` if needed.
3. Run the application:
   ```
   python main.py
   ```
4. Use the GUI to set up your position:
   - Left-click a square to cycle through pieces.
   - Right-click to swap piece color.
   - Double right-click to clear a square.
   - Hover and press a shortcut key to place a specific piece.
5. Click "Solve" to compute the best move sequence and generate a GIF (`chess_moves.gif`).

## Keyboard Shortcuts

Hover over a square and press:

- `p`: White Pawn
- `P`: Black Pawn
- `n`: White Knight
- `N`: Black Knight
- `b`: White Bishop
- `B`: Black Bishop
- `r`: White Rook
- `R`: Black Rook
- `q`: White Queen
- `Q`: Black Queen
- `k`: White King
- `K`: Black King

---

**Author:** [thejonali](https://github.com/thejonali)

**License:** Apache 2.0
