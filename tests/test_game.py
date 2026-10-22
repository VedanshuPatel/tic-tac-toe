import pytest
from board import EMPTY
from game import Game, GameState

@pytest.fixture
def game():
    """A fresh two-player game: X then O."""
    return Game("X", "O")

def test_no_more_moves_after_player_wins(game):
    game.make_move("X", 1, 0)
    game.make_move("O", 0, 0)
    game.make_move("X", 1, 1)
    game.make_move("O", 0, 1)
    game.make_move("X", 1, 2)

    result = game.make_move("O", 2, 2)
    assert game.get_winner() == "X"
    assert result is False
    assert game.get_game_state() is GameState.WON

def test_taken_cell_is_rejected_and_player_turn_does_not_change(game):
    game.make_move("X", 1, 2)
    result = game.make_move("O", 1, 2)

    assert game.get_current_player() == "O"
    assert result is False
    assert game.get_board().cell(1, 2) == "X"

def test_winning_move_does_not_switch_player(game):
    game.make_move("X", 1, 0)
    game.make_move("O", 0, 0)
    game.make_move("X", 1, 1)
    game.make_move("O", 0, 1)
    game.make_move("X", 1, 2)

    assert game.get_current_player() == "X"

def test_wrong_player_cannot_play(game):
    result = game.make_move("O", 2, 2)

    assert game.get_board().cell(2, 2) == EMPTY
    assert result is False
    assert game.get_current_player() == "X"

def test_game_starts_with_x_and_in_progress(game):
    assert game.get_current_player() == "X"
    assert len(game.get_board().empty_cells()) == 9
    assert game.get_winner() is None
    assert game.get_game_state() is GameState.IN_PROGRESS

def test_full_board_with_no_winner_is_a_draw(game):
    for row, col in [(0, 1), (0, 0), (1, 0),(0, 2), (1, 1), (1, 2),(2, 0), (2, 1), (2, 2)]:
        assert game.make_move(game.get_current_player(), row, col) is True
    assert game.get_winner() is None
    assert game.get_board().is_full() is True
    assert game.get_game_state() is GameState.DRAW

def test_player_win_on_anti_diagonal(game):
    game.make_move("X", 2, 0)
    game.make_move("O", 2, 2)
    game.make_move("X", 0, 2)
    game.make_move("O", 1, 0)
    result = game.make_move("X", 1, 1)

    assert game.get_game_state() is GameState.WON
    assert result is True
    assert game.get_winner() == "X"

@pytest.mark.parametrize("row, col", [(-3, 1), (1, -3), (5, 2), (2, 5), (-1, 4)])
def test_off_board_move_is_rejected_and_player_turn_does_not_change(game, row, col):
    result = game.make_move("X", row, col)

    assert len(game.get_board().empty_cells()) == 9
    assert result is False
    assert game.get_current_player() == "X"

def test_player_win_on_main_diagonal(game):
    game.make_move("X", 2, 2)
    game.make_move("O", 0, 1)
    game.make_move("X", 0, 0)
    game.make_move("O", 1, 0)
    result = game.make_move("X", 1, 1)

    assert game.get_game_state() is GameState.WON
    assert game.get_winner() == "X"
    assert result is True

def test_player_win_down_a_column(game):
    game.make_move("X", 0, 2)
    game.make_move("O", 0, 0)
    game.make_move("X", 1, 2)
    game.make_move("O", 1, 0)
    result = game.make_move("X", 2, 2)

    assert result is True
    assert game.get_game_state() is GameState.WON
    assert game.get_winner() == "X"

def test_valid_move_places_mark_and_switches_player(game):
    result = game.make_move("X", 2, 1)

    assert game.get_game_state() is GameState.IN_PROGRESS
    assert result is True
    assert game.get_board().cell(2, 1) == "X"
    assert game.get_current_player() == "O"

@pytest.mark.parametrize("row, col", [(0, 0), (0, 1), (0, 2),(1, 0), (1, 1), (1, 2),(2, 0), (2, 1), (2, 2),
])
def test_on_board_move_is_accepted_and_turn_switches(game, row, col):
    result = game.make_move("X", row, col)

    assert len(game.get_board().empty_cells()) == 8
    assert result is True
    assert game.get_current_player() == "O"
    assert game.get_board().cell(row, col) == "X"

def test_player_win_across_a_row(game):
    game.make_move("X", 1, 0)
    game.make_move("O", 0, 0)
    game.make_move("X", 1, 1)
    game.make_move("O", 0, 1)
    result = game.make_move("X", 1, 2)

    assert game.get_winner() == "X"
    assert result is True
    assert game.get_game_state() is GameState.WON