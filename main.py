from game import GameState, Game


def print_game_board(game):
    print()
    print(game.get_board())
    print()

def process_player_input(txt):
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
    while True:
        row, col = read_input(game)
        player = game.get_current_player()
        if game.make_move(player,row,col):
            print_game_board(game)
            return
        print("Invalid location or the cell is already taken. Please try again!")
        print_game_board(game)

def print_game_result(game):
    state = game.get_game_state()
    if state is GameState.WON:
        print(f"Player {game.get_winner()} wins!")
    elif state is GameState.DRAW:
        print("It's a draw!")

def main():
    print("Lets play the Tic-Tac-Toe Game")
    game = Game("X","O")
    print_game_board(game)
    while game.get_game_state() is GameState.IN_PROGRESS:
        play_turn(game)
    print_game_result(game)


if __name__ == "__main__":
    main()