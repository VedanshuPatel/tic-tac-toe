from board import Board
from enum import Enum
from typing import Optional


class GameState(Enum):
    """Possible outcomes while a game is running or finished."""
    IN_PROGRESS = "IN_PROGRESS"
    WON = "WON"
    DRAW = "DRAW"


class Game:
    """A Tic-Tac-Toe game."""
    def __init__(self, player1, player2):
        """Start a new game. player1 moves first use X then O."""
        self.board = Board()
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.state = GameState.IN_PROGRESS
        self.winner: Optional[str] = None

    def get_current_player(self) -> str:
        """Return the mark whose turn it is X or O)."""
        return self.current_player

    def get_game_state(self) -> GameState:
        """Return whether the game is in progress, won, or a draw."""
        return self.state

    def get_winner(self) -> Optional[str]:
        """Return the winning mark, or None if there is no winner yet."""
        return self.winner

    def get_board(self) -> Board:
        """Return the Board used by this game."""
        return self.board

    def make_move(self, player, row:int, column: int) -> bool:
        """Place player's mark at row, column.
        Returns True if the move was applied. Returns False if the game is
        over, it is not that player's turn, or the cell is taken/off-board.
        An invalid move does not change the current player.
        """
        if self.state is not GameState.IN_PROGRESS:
            return False
        if player is not self.current_player:
            return False

        if not self.board.place_mark(row, column, player):
            return False

        if self.board.has_won(player):
            self.state = GameState.WON
            self.winner = player
        elif self.board.is_full():
            self.state = GameState.DRAW
        else:
            self.current_player = self.player2 if self.current_player is self.player1 else self.player1
        return True

if __name__ == "__main__":
    game = Game("X", "O")
    print("Start:", game.get_current_player(), game.get_game_state())
    print(game.get_board())
    print("X plays 2 3:", game.make_move("X", 1, 2))
    print("Current:", game.get_current_player())
    print(game.get_board())
    print("O tries taken cell:", game.make_move("O", 1, 2))
    print("Still O's turn:", game.get_current_player())
    print("O plays 1 1:", game.make_move("O", 0, 0))
    print("X plays 3 1:", game.make_move("X", 2, 0))
    print("O plays 2 2:", game.make_move("O", 1, 1))
    print("X plays 1 3:", game.make_move("X", 0, 2))
    print("State:", game.get_game_state(), "Winner:", game.get_winner())
    print(game.get_board())