# tests/test_board.py
import pytest

from board import EMPTY, Board


@pytest.fixture
def board():
    """A fresh, empty 3x3 board for each test."""
    return Board(3)

def test_win_across_a_row(board):
    board.place_mark(1, 1, "X")
    board.place_mark(1, 0, "X")
    board.place_mark(1, 2, "X")

    assert board.has_won("X") is True

def test_new_board_is_empty(board):
    assert len(board.empty_cells()) == 9
    assert board.is_full() is False
    assert board.cell(1, 2) == EMPTY

def test_place_mark_puts_mark_on_board_cell(board):
    result = board.place_mark(1, 0, "X")

    assert result is True
    assert (1, 0) not in board.empty_cells()
    assert board.cell(1, 0) == "X"

@pytest.mark.parametrize("row, col", [(-2, 1), (1, -2), (4, 1), (1, 4), (-2, -2), (4, 4)])
def test_off_boundry_board_moves_are_rejected(board, row, col):
    result = board.place_mark(row, col, "O")

    assert result is False
    assert len(board.empty_cells()) == 9

def test_board_smaller_than_three_is_invalid():
    with pytest.raises(ValueError, match="at least 3"):
        Board(2)

@pytest.mark.parametrize("row, col", [(0, 0), (0, 1), (0, 2),(1, 0), (1, 1), (1, 2),(2, 0), (2, 1), (2, 2)])
def test_on_board_valid_moves_are_accepted(board, row, col):
    result = board.place_mark(row, col, "X")

    assert (row, col) not in board.empty_cells()
    assert board.cell(row, col) == "X"
    assert result is True

def test_win_down_a_column(board):
    board.place_mark(1, 0, "O")
    board.place_mark(2, 0, "O")
    board.place_mark(0, 0, "O")

    assert board.has_won("O") is True

def test_copy_is_independent_of_original(board):
    board.place_mark(0, 2, "X")
    clone = board.copy()
    clone.place_mark(1, 0, "O")

    assert clone.cell(0, 2) == "X"
    assert board.cell(1, 0) == EMPTY
    assert clone.cell(1, 0) == "O"

def test_cannot_place_mark_on_taken_cell(board):
    board.place_mark(2, 1, "X")
    result = board.place_mark(2, 1, "O")

    assert result is False
    assert board.cell(2, 1) == "X"
    
def test_win_on_main_diagonal(board):
    board.place_mark(1, 1, "X")
    board.place_mark(0, 0, "X")
    board.place_mark(2, 2, "X")

    assert board.has_won("X") is True

def test_win_on_anti_diagonal(board):
    board.place_mark(2, 0, "O")
    board.place_mark(0, 2, "O")
    board.place_mark(1, 1, "O")

    assert board.has_won("O") is True

def test_full_board_with_no_winner_is_a_draw(board):
    for row, col, mark in [
        (0, 0, "X"), (0, 1, "O"), (0, 2, "X"),
        (1, 0, "X"), (1, 1, "O"), (1, 2, "O"),
        (2, 0, "O"), (2, 1, "X"), (2, 2, "X"),
    ]:
        assert board.place_mark(row, col, mark) is True

    assert board.is_full() is True
    assert board.has_won("X") is False
    assert board.empty_cells() == []
    assert board.has_won("O") is False

def test_partial_line_is_not_a_win(board):
    board.place_mark(2, 1, "X")
    board.place_mark(2, 0, "X")

    assert board.has_won("X") is False