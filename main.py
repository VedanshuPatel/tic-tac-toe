from game import GameState, Game
from ai import EasyAI, HardAI
import random

def print_game_board(game):
    """Print the current board"""
    print()
    print(game.get_board())
    print()

def process_player_input(txt):
    """Convert 'row col' (1-based) to (row, col) (0-based), or None if invalid"""
    input_lst = txt.split()
    if len(input_lst) != 2:
        return None
    try:
        row = int(input_lst[0]) - 1
        col = int(input_lst[1]) - 1
    except ValueError:
        return None
    return row,col

def read_input(game):
    """Prompt until the player enters valid input for a move."""
    mark = game.get_current_player()
    while True:
        player_move = input(f"Player {mark} please enter the row and column to mark the board: ").strip()
        processed_player_move = process_player_input(player_move)
        if processed_player_move is None:
            print("Invalid input. Please try again")
            print_game_board(game)
            continue
        return processed_player_move

def play_turn(game):
    """Ask for a move until Game accepts it, print the board after each try"""
    while True:
        row, col = read_input(game)
        player = game.get_current_player()
        if game.make_move(player,row,col):
            print_game_board(game)
            return
        print("Invalid location or the cell is already taken. Please try again!")
        print_game_board(game)

def print_game_result(game):
    """Print the win or draw message for a finished game"""
    state = game.get_game_state()
    if state is GameState.WON:
        print(f"Player {game.get_winner()} wins!")
    elif state is GameState.DRAW:
        print("It's a draw!")

def play_ai_turn(game, ai):
    """Let the AI choose and play a move, then print the board"""
    mark = game.get_current_player()
    row, col = ai.choose_move(game.get_board(), mark)
    game.make_move(mark, row, col)
    print(f"AI {mark} plays {row+1} {col+1}")
    print_game_board(game)

def choose_game_mode():
    """Ask for two-player or AI mode, return 'two_player' or 'ai_opponent'"""
    while True:
        print("Choose a game mode to begin:")
        print("1. 2 Players")
        print("2. AI Opponent")
        choice = input("Enter 1 or 2: ").strip()
        if choice == "1":
            return "two_player"
        if choice == "2":
            return "ai_opponent"
        print("Please choose a valid game mode (1 or 2)")

def choose_ai_difficulty():
    """Ask for Easy or Hard level and return an EasyAI or HardAI instance"""
    while True:
        print("Choose AI difficulty level:")
        print("1. Easy")
        print("2. Hard")
        choice = input("Enter 1 or 2: ").strip()
        rng = random.Random()
        if choice == "1":
            return EasyAI(rng)
        if choice == "2":
            return HardAI(rng)
        print("Please choose a valid difficulty level mode (1 or 2)")

def run_two_player():
    """Run a two-player game"""
    game = Game("X", "O")
    print_game_board(game)
    while game.get_game_state() is GameState.IN_PROGRESS:
        play_turn(game)
    print_game_result(game)

def run_human_versus_ai(ai):
    """Run a game of human (X) versus the given AI (O)"""
    game = Game("X", "O")
    print("You are X. AI is O.")
    print_game_board(game)
    while game.get_game_state() is GameState.IN_PROGRESS:
        if game.get_current_player() == "X":
            play_turn(game)
        else:
            play_ai_turn(game, ai)
    print_game_result(game)

def main():
    """Start the game, then play two-player or versus AI"""

    print("Lets play the Tic-Tac-Toe Game")
    mode = choose_game_mode()
    if mode == "two_player":
        run_two_player()
    else:
        ai = choose_ai_difficulty()
        run_human_versus_ai(ai)

if __name__ == "__main__":
    main()