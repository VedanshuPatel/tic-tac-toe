import random
import pytest
from ai import AIPlayer, EasyAI, HardAI
from board import Board


def test_choose_move_leaves_the_board_unchanged_hard_ai():
    board = Board()
    board.place_mark(0, 2, "X")
    board.place_mark(2, 0, "O")
    before = _cells(board)
    HardAI(random.Random(9)).choose_move(board, "X")

    assert _cells(board) == before

def test_easy_ai_always_returns_an_empty_cell():
    board = Board()
    board.place_mark(2, 0, "X")
    board.place_mark(2, 1, "O")
    board.place_mark(1, 2, "X")

    for seed in range(40):
        move = EasyAI(random.Random(seed)).choose_move(board, "O")
        assert move in board.empty_cells()

def test_easy_ai_with_same_seed_is_deterministic():
    board = Board()
    a = EasyAI(random.Random(99)).choose_move(board, "O")
    b = EasyAI(random.Random(99)).choose_move(board, "O")

    assert a == b

def test_ai_player_cannot_be_created_with_AIPlayer_directly():
    with pytest.raises(TypeError):
        AIPlayer(random.Random(3))

def test_hard_ai_blocks_opponent_win():
    board = Board()
    board.place_mark(0, 0, "X")
    board.place_mark(0, 1, "X")
    board.place_mark(1, 1, "O")
    move = HardAI(random.Random(4)).choose_move(board, "O")

    assert move == (0, 2)

def test_hard_ai_never_loses_on_3x3_board():
    ai = HardAI(random.Random(11))

    def explore(board):
        if board.has_won("X"):
            pytest.fail("Hard lost on 3x3 while playing second")
        if board.has_won("O") or board.is_full():
            return

        for row, col in list(board.empty_cells()):
            board.place_mark(row, col, "X")
            if board.has_won("X"):
                board.remove_mark(row, col)
                pytest.fail("Hard lost on 3x3 while playing second")
            if not board.is_full():
                o_row, o_col = ai.choose_move(board, "O")
                assert (o_row, o_col) in board.empty_cells()
                board.place_mark(o_row, o_col, "O")
                explore(board)
                board.remove_mark(o_row, o_col)
            board.remove_mark(row, col)

    explore(Board())

def test_hard_ai_returns_an_empty_cell():
    board = Board()
    board.place_mark(1, 0, "X")
    move = HardAI(random.Random(8)).choose_move(board, "O")
    assert move in board.empty_cells()

def _cells(board):
    return [[board.cell(r, c) for c in range(3)] for r in range(3)]

def test_choose_move_leaves_the_board_unchanged_easy_ai():
    board = Board()
    board.place_mark(2, 2, "O")
    before = _cells(board)
    EasyAI(random.Random(9)).choose_move(board, "X")

    assert _cells(board) == before

def test_hard_ai_takes_a_winning_move_when_one_exists():
    board = Board()
    board.place_mark(0, 0, "O")
    board.place_mark(0, 1, "O")
    board.place_mark(1, 0, "X")
    board.place_mark(1, 1, "X")
    move = HardAI(random.Random(2)).choose_move(board, "O")

    assert move == (0, 2)