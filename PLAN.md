# Tic-Tac-Toe Plan

## Goal
This is a terminal-based Tic-Tac-Toe game played on a 3x3 grid. It supports two modes: local two player or single player against an AI opponent with adjustable Easy and Hard difficulty levels. The application is written in Python.

## Requirements


| ID | Requirement | Type | Priority | How verified |
|---|---|---|---|---|
| R1 | A newly created board is an empty 3x3 grid, which returns all 9 empty positions. | Functional | Must | confirm a new board has 9 empty cells and no winner |
| R2 | X takes the first turn, and the active player changes only when a move is valid. | Functional | Must | confirm `Game` starts with X and switches to O after one valid move |
| R3 | The game accepts player moves as row and column coordinates numbered from 1 to 3, corresponding to the positions on the 3×3 board. | Functional | Must | Verify that inputs such as 1 1, 2 3, and 3 3 select the correct cells on the board.
| R4 | Attempting to play in an occupied cell returns `False`, preserves the existing mark, and does not advance the turn. | Functional | Must | place X at (0,0), then attempt O at (0,0), confirm the move returns `False`, X remains in the cell, and it is still O's turn |
| R5 | Moves outside the board boundaries, including negative coordinates, return `False` without advancing the turn. | Functional | Must | Parametrized test using (-1,0), (0,-1), (3,0), and (0,3) |
| R6 | Invalid input, including non-numeric values, blank input, or coordinates outside the valid range, displays an error message and prompts the same player to try again. | Functional | Must | Test the input parser with "a b", "", "2", and "4 4"|
| R7 | The game correctly identifies wins in every row, column, and diagonal direction. | Functional | Must | Parametrized test covering all possible winning lines |
| R8 | A completely filled board with no winning line is recognized as a draw. | Functional | Must | Verify that a known draw board is identified as full and that neither X nor O has a winning line |
| R9 | `AIPlayer` is an abstract class and cannot be instantiated directly. | Non-functional | Must | verify that attempting to instantiate `AIPlayer` raises `TypeError` |
| R10 | In versus-computer mode, the human plays as X and the computer plays as O. | Functional | Must | Verify that the human moves first as X and the computer responds as O. |
| R11 | At the start of the game, the player can choose between two-player mode and versus-computer mode | Functional | Must | Verify with tests that both game modes are offered and can be selected |
| R12 | The Hard AI uses the minimax algorithm to select moves and guarantees that X cannot win when X plays first and Hard plays second on a 3×3 board | Functional | Must | Explore every possible sequence of X moves against Hard and confirm that X never wins and that Hard selects moves using the minimax algorithm |
| R13 | Calling `choose_move` must not modify the current board state, regardless of which AI difficulty is used. | Non-functional| Must | compare every cell before and after calling `choose_move` for both Easy and Hard |
| R14 | All console input and output operations are confined to `main.py`; `board.py`, `ai.py`, and `game.py` contain no calls to `print()` or `input()`. | Non-functional | Must | automated test checks that `board.py`, `ai.py`, and `game.py` contain no `print()` or `input()` |
| R15 | Automated tests run on every pull request and every push to the main branch, and all required checks must pass before changes are merged. | Non-functional | Should | Verify that CI checks pass for pull requests and pushes to the main branch |
| R16 | The current board is printed after every move, whether the move is valid or invalid. | functional | Must | Verify during manual play that the board is displayed after each move attempt. |
| R17 | In versus-computer mode, the player can select either Easy or Hard AI difficulty | functional | Must | Verify that both difficulty options are offered and can be selected |
| R18 | The Easy AI randomly selects an empty cell from the available positions on the board. | Functional | Must | Test multiple board configurations and verify that each selected move is an empty cell. |

## Components


| Name | Responsibility | File |
|---|---|---|
| Board | Maintains the 3×3 grid and provides methods to access and evaluate the board state. | `board.py` |
| AIPlayer | Defines an abstract base class specifying the `choose_move(board, mark)` method for all AI players. | `ai.py` |
| EasyAI | Randomly selects an empty cell using the provided `random.Random` instance. | `ai.py` |
| HardAI | Selects the optimal move using the minimax algorithm. | `ai.py` |
| Game | Manages turn order, game modes, and win or draw detection without handling input or output. | `game.py` |
| Main | Handles menus, user prompts, converts 1-based coordinates to 0-based indices, and prints the board. | `main.py` |
| Tests | Contains pytest tests to verify that the requirements are met. | `tests/` |
| CI Workflow | Runs pytest on every pull request and every push to the `main` branch. | `ci.yml` |

## Decisions

| Decision | Options considered | Chosen | Reason |
|---|---|---|---|
| How the game communicates with the AI | Pass a difficulty string and use `if` statements in `Game`, or pass an `AIPlayer` instance | Pass an `AIPlayer` instance | This separates game logic from AI difficulty, reduces conditional statements, and allows tests to use an AI configured with a fixed random seed. |
| How to structure AI behavior | Implement all AI strategies in one class with conditional checks, or use a parent class with separate subclasses | Parent class with subclasses | Polymorphism lets each AI implement its own move-selection logic, keeping the code organized and avoiding lengthy conditional chains. |
| How to test that Hard AI never loses | Run multiple games with different random seeds, or test every possible sequence of X's moves | Test every possible sequence | Exhaustively checking all possible move sequences provides a reliable, repeatable way to verify that Hard AI cannot be defeated on a 3×3 board. |
| How to represent the board | Use a dictionary keyed by position, or a list of lists | List of lists within a `Board` class | A list of lists naturally represents the 3×3 grid, while the `Board` class encapsulates the grid and controls how it is accessed. |


## What changed

