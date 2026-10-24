import pytest

from game import Game, GameState
from main import (process_player_input, print_game_result, print_game_board, play_turn, main)

def test_print_game_board_shows_board(capsys):
    game = Game("X", "O")
    game.make_move("X", 2, 2)
    print_game_board(game)

    out = capsys.readouterr().out
    assert "X" in out

def test_process_player_input_accepts_negative_numbers_as_coordinates():
    assert process_player_input("-1 2") == (-2, 1)

def test_print_game_result_silent_when_game_in_progress(capsys):
    game = Game("X", "O")
    print_game_result(game)
    out = capsys.readouterr().out

    assert out == ""

def test_print_game_result_announces_winner(capsys):
    game = Game("X", "O")
    game.make_move("X", 1, 0)
    game.make_move("O", 0, 0)
    game.make_move("X", 1, 1)
    game.make_move("O", 0, 1)
    game.make_move("X", 1, 2)
    print_game_result(game)

    out = capsys.readouterr().out
    assert "wins" in out.lower()
    assert "X" in out

def test_print_game_result_announces_draw(capsys):
    game = Game("X", "O")
    for row, col in [
        (0, 1), (0, 0), (1, 0),
        (0, 2), (1, 1), (1, 2),
        (2, 0), (2, 1), (2, 2),
    ]:
        game.make_move(game.get_current_player(), row, col)

    assert game.get_game_state() is GameState.DRAW
    print_game_result(game)
    out = capsys.readouterr().out
    assert "draw" in out.lower()

def test_play_turn_places_mark_and_switches_player(monkeypatch):
    game = Game("X", "O")
    monkeypatch.setattr("builtins.input", lambda _: "3 1")
    play_turn(game)

    assert game.get_current_player() == "O"
    assert game.get_board().cell(2, 0) == "X"

def test_play_turn_retries_after_non_numeric_input(monkeypatch):
    game = Game("X", "O")
    answers = iter(["nope", "3 3"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    play_turn(game)

    assert game.get_current_player() == "O"
    assert game.get_board().cell(2, 2) == "X"

@pytest.mark.parametrize(
    "text",
    ["hello", "3", "1 2 3", "x y", "2 x", "x 2", "2.0 1", "\t"]
)
def test_process_player_input_rejects_invalid_text(text):
    assert process_player_input(text) is None

def test_process_player_input_allows_extra_spaces():
    assert process_player_input("  3   1  ") == (2, 0)

def test_play_turn_retries_after_taken_cell_mark(monkeypatch):
    game = Game("X", "O")
    game.make_move("X", 2, 1) 
    answers = iter(["3 2", "2 1"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    play_turn(game)

    assert game.get_current_player() == "X"
    assert game.get_board().cell(1, 0) == "O"
    assert game.get_board().cell(2, 1) == "X"

@pytest.mark.parametrize(
    "text, expected",
    [("3 2", (2, 1)), ("1 2", (0, 1)), ("2 1", (1, 0)), ("3 1", (2, 0)), ("2 2", (1, 1))]
)
def test_process_player_input_converts_one_based_to_zero_based(text, expected):
    assert process_player_input(text) == expected

def test_main_announces_player_win(monkeypatch, capsys):
    answers = iter(["1 3", "1 1", "2 3", "2 1", "3 3"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    main()

    out = capsys.readouterr().out
    assert "X" in out
    assert "wins" in out.lower()

def test_main_announces_draw(monkeypatch, capsys):
    answers = iter([
        "1 2", "1 1", "2 1",
        "1 3", "2 2", "2 3",
        "3 1", "3 2", "3 3",
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    main()

    out = capsys.readouterr().out
    assert "draw" in out.lower()

def test_play_turn_retries_multiple_bad_inputs_then_succeeds(monkeypatch):
    game = Game("X", "O")
    answers = iter(["abc", "9 9", "2 2"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    play_turn(game)

    assert game.get_current_player() == "O"
    assert game.get_board().cell(1, 1) == "X"

def test_main_announces_O_wins(monkeypatch, capsys):
    answers = iter(["1 1", "1 2", "1 3", "2 2", "3 3", "3 2"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    main()

    out = capsys.readouterr().out
    assert "wins" in out.lower()
    assert "O" in out

def test_play_turn_retries_after_off_board_move(monkeypatch):
    game = Game("X", "O")
    answers = iter(["5 5", "1 3"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    play_turn(game)

    assert game.get_current_player() == "O"
    assert game.get_board().cell(0, 2) == "X"