from abc import ABC, abstractmethod

class AIPlayer(ABC):
    """Abstract base class for AI Player"""

    def __init__(self,rng):
        """Store a random.Random instance for move"""
        self._rng = rng

    @abstractmethod
    def choose_move(self, board, mark):
        """Return a (row, col) move for mark without changing the board"""
        raise NotImplementedError

class EasyAI(AIPlayer):
    """EasyAI that picks a random empty cell"""

    def __init__(self,rng):
        """Create an EasyAI using the random.Random instance."""
        super().__init__(rng)

    def choose_move(self, board, mark):
        """Return a random empty cell as (row, col)"""
        return self._rng.choice(board.empty_cells())

class HardAI(AIPlayer):
    """HardAI that uses minimax for optimal play on a 3x3 board"""

    def __init__(self,rng):
        """Create a HardAI using the random.Random instance"""
        super().__init__(rng)
    
    def _minmax_algorithm(self, board, ai_move, is_maximizing_output):
        """Return a score for the position: 1 win, -1 loss, 0 draw"""
        opponent_mark = "O" if ai_move == "X" else "X"
        if board.has_won(ai_move):
            return 1
        if board.has_won(opponent_mark):
            return -1
        if board.is_full():
            return 0
        
        if is_maximizing_output:
            ans = -2
            for row, col in board.empty_cells():
                board.place_mark(row, col, ai_move)
                score = self._minmax_algorithm(board, ai_move, False)
                board.remove_mark(row, col)
                if score > ans:
                    ans = score
            return ans

        ans = 2
        for row, col in board.empty_cells():
            board.place_mark(row, col, opponent_mark)
            score = self._minmax_algorithm(board, ai_move, True)
            board.remove_mark(row, col)
            if score < ans:
                ans = score
        return ans

    def choose_move(self, board, mark):
        """Return an optimal (row, col) move, ties broken with rng"""
        ans = None
        best_moves = []
        for row, col in board.empty_cells():
            board.place_mark(row, col, mark)
            score = self._minmax_algorithm(board, mark, is_maximizing_output=False)
            board.remove_mark(row, col)

            if ans is None or score > ans:
                ans = score
                best_moves = [(row, col)]
            elif score == ans:
                best_moves.append((row, col))
        return self._rng.choice(best_moves)