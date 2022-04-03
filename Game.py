from Board import Board
from random import choice
from Tile import Tile
from Players import Player_Computer, Player_Person

def create_players():
    player1, player2 = None, None
    while player1 is None:
        res = input("Is player1 a person? (y/n): ").strip().lower()
        if res == "y"  or  res == "yes":
            player1 = Player_Person("player1")
        elif res == "n"  or  res == "no":
            player1 = Player_Computer("player1")
    
    print()

    while player2 is None:
        res = input("Is player2 a person? (y/n): ").strip().lower()
        if res == "y"  or  res == "yes":
            player2 = Player_Person("player2")
        elif res == "n"  or  res == "no":
            player2 = Player_Computer("player2")

    return player1, player2

def get_heuristic(b: Board, turn1: bool):
    return lambda tile_origin, tile_destination: turn1 ^ board.board_tiles.index(tile_destination) < board.board_tiles.index(tile_origin)
    
# -----------------------------------------------------------------------------------

if __name__ == "__main__":
    board = Board()
    players = create_players()

    current_player_index = choice([0, 1])
    print(f"{players[current_player_index].get_name()} starts\n")

    while not board.has_game_ended():
        player = players[current_player_index]
        tile_origin, tile_destination = player.get_move(board, get_heuristic(board, player.is_player1()))
        if current_player_index == 0:
            assert player.is_player1()
            assert tile_origin.get_piece().is_player1_piece()
        else:
            assert not player.is_player1()
            assert tile_origin.get_piece().is_player2_piece()

        assert tile_destination.is_empty()
        board.move_piece_to_tile(tile_origin, tile_destination)
        board.print_board()
        current_player_index = (current_player_index+1) % len(players)
    
    if board.has_player1_won():
        assert not board.has_player2_won()
        print("Player1 has won")
    else:
        assert board.has_player2_won()
        print("Player2 has won")