from random import choice
from Board import Board
from Players import Player_Computer, Player_Person

"""Asks the user if the players are people, or instead the computer is going to play.
Creates the players and returns them"""

def create_computer_player(board: Board, name: str) -> Player_Computer:
    res = input("\tUse evaluation function 1 or 2? (1/2): ").strip().lower()
    while res not in ["1", "2"]:
        res = input("\tUse evaluation function 1 or 2? (1/2): ").strip()
    eval_func = int(res)

    res = input("\tWhich depth? (1-9): ").strip().lower()
    while res not in "1 2 3 4 5 6 7 8 9".split(" "):
        res = input("\tWhich depth? (1-9): ").strip().lower()
    depth = int(res)
    
    player = Player_Computer(name, eval_func, depth)

    res = input("\tDo you want the computer to use an heuristic? (y/n): ").strip().lower()
    while res not in ["y", "yes", "n", "no"]:
        res = input("\tDo you want the computer to use an heuristic? (y/n): ").strip()
    if res in ["yes", "y"]:
        player.set_heuristic( get_heuristic(board, player.is_player1()) )

    return player


def create_players(board: Board) -> tuple[Player_Computer|Player_Person, Player_Computer|Player_Person]:
    player1, player2 = None, None

    # Player 1
    while player1 is None:
        res = input("Is player1 a person? (y/n): ").strip().lower()
        if res == "y"  or  res == "yes":
            player1 = Player_Person("Player1")
        elif res == "n"  or  res == "no":
            player1 = create_computer_player(board, "Player1")
    
    print()

    # Player 2
    while player2 is None:
        res = input("Is player2 a person? (y/n): ").strip().lower()
        if res == "y"  or  res == "yes":
            player2 = Player_Person("Player2")
        elif res == "n"  or  res == "no":
            player2 = create_computer_player(board, "Player2")

    return player1, player2

"""The implemented heuristic for the game"""
def get_heuristic(b: Board, turn1: bool):
    def h1(tile_origin, tile_destination) -> bool:
        if turn1:
            return board.get_row_index(tile_destination) >= board.get_row_index(tile_origin)
        else:
            return board.get_row_index(tile_destination) <= board.get_row_index(tile_origin)

    return h1

# -----------------------------------------------------------------------------------

if __name__ == "__main__":
    board = Board()
    players = create_players(board)

    current_player_index = choice([0, 1])
    print("\n----------------------------------------------------")
    print(f"{players[current_player_index].get_name()} starts\n")

    while not board.has_game_ended():
        player = players[current_player_index]
        tile_origin, tile_destination = player.get_move(board)
        board.move_piece_to_tile(tile_origin, tile_destination)
        board.print_board()
        current_player_index = (current_player_index+1) % len(players)
    
    if board.has_player1_won():
        print("Player1 has won")
    else:
        print("Player2 has won")
