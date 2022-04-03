from random import choice
from Board import Board
from Players import Player_Computer, Player_Person

"""Asks the user if the players are people, or instead the computer is going to play.
Creates the players and returns them"""
def create_players() -> tuple[Player_Computer|Player_Person, Player_Computer|Player_Person]:
    player1, player2 = None, None

    # Player 1
    while player1 is None:
        res = input("Is player1 a person? (y/n): ").strip().lower()
        if res == "y"  or  res == "yes":
            player1 = Player_Person("player1")
        elif res == "n"  or  res == "no":
            player1 = Player_Computer("player1")
    
    print()

    # Player 2
    while player2 is None:
        res = input("Is player2 a person? (y/n): ").strip().lower()
        if res == "y"  or  res == "yes":
            player2 = Player_Person("player2")
        elif res == "n"  or  res == "no":
            player2 = Player_Computer("player2")

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
    players = create_players()

    current_player_index = choice([0, 1])
    print(f"{players[current_player_index].get_name()} starts\n")

    while not board.has_game_ended():
        player = players[current_player_index]
        tile_origin, tile_destination = player.get_move(board, get_heuristic(board, player.is_player1()))
        board.move_piece_to_tile(tile_origin, tile_destination)
        board.print_board()
        current_player_index = (current_player_index+1) % len(players)
    
    if board.has_player1_won():
        print("Player1 has won")
    else:
        print("Player2 has won")
