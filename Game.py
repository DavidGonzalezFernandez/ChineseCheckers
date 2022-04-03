from Board import Board
from Tile import Tile
from Piece import Piece
from random import choice

CHARACTERS = "123456789ABCDEFGHJKLMNPQRSTUVWXYZ"

def ask_person_for_piece(board: Board, is_player1: bool) -> Tile:
    tiles_with_movable_pieces: list[Tile] = list(filter(
        lambda t: any(board.get_all_valid_moves(t)), board.get_player1_tiles() if is_player1 else board.get_player2_tiles()
    ))
    board.print_board(tiles_with_movable_pieces, "".join(CHARACTERS))

    while True:
        n = input(f"Select a piece ({CHARACTERS[0]} - {CHARACTERS[len(tiles_with_movable_pieces)-1]})").strip().upper()
        if len(n) != 1:
            continue
        if n in CHARACTERS[ : len(tiles_with_movable_pieces)]:
            selected_tile = tiles_with_movable_pieces[CHARACTERS.index(n)]
            return selected_tile

def ask_person_for_tile_destination(board: Board, tile_origin: Tile) -> Tile:
    assert board is not None
    assert isinstance(tile_origin, Tile)

    available_tile_destinations: list[Tile] = [tile for tile in board.get_all_valid_moves(tile_origin)]

    board.print_board(available_tile_destinations, CHARACTERS)

    while True:
        n = input(f"Select a tile to move to ({CHARACTERS[0]} - {CHARACTERS[len(available_tile_destinations)-1]})").strip().upper()
        if len(n) != 1:
            continue
        if n in CHARACTERS[ : 1+len(available_tile_destinations)]:
            destination_tile = available_tile_destinations[ CHARACTERS.index(n) ]
            assert destination_tile is not None
            assert isinstance(destination_tile, Tile)
            assert destination_tile.is_empty()
            return destination_tile

def minimax_pruning(board: Board, depth: int, is_player1_turn: bool, maximizing: bool = True, alpha: int = -1_000_000_000, beta: int = 1_000_000_000) -> tuple[int, Tile, Tile]:
    if depth==0:
        return board.get_score(is_player1_turn), None, None

    if board.has_game_ended():
        # We add the depth as an incentive to choose the branch that is shorter
        return board.get_score(is_player1_turn)+depth, None, None
    
    if maximizing:
        max_points, better_origin, better_destination = float('-inf'), None, None
        for tile_origin in board.get_player1_tiles() if is_player1_turn else board.get_player2_tiles():
            for tile_destination in board.get_all_valid_moves(tile_origin):
                board.move_piece_to_tile(tile_origin, tile_destination)
                res_points, _1, _2 = minimax_pruning(board, depth-1, is_player1_turn, not maximizing, alpha, beta)
                board.move_piece_to_tile(tile_destination, tile_origin)

                if res_points > max_points:
                    max_points, better_origin, better_destination = res_points, tile_origin, tile_destination
                alpha = max(alpha, res_points)
                if beta <= alpha:
                    break

            if beta <= alpha:
                break

        return max_points, better_origin, better_destination
    
    else:
        min_points, better_origin, better_destination = float('inf'), None, None
        for tile_origin in board.get_player2_tiles() if is_player1_turn else board.get_player1_tiles():
            for tile_destination in board.get_all_valid_moves(tile_origin):
                board.move_piece_to_tile(tile_origin, tile_destination)
                res_points, _1, _2 = minimax_pruning(board, depth-1, is_player1_turn, not maximizing, alpha, beta)
                board.move_piece_to_tile(tile_destination, tile_origin)

                if res_points < min_points:
                    min_points, better_origin, better_destination = res_points, tile_origin, tile_destination
                beta = min(beta, res_points)
                if beta <= alpha:
                    break
            
            if beta <= alpha:
                break
        return min_points, better_origin, better_destination

class Player():
    def __init__(self, name: str) -> None:
        self.name = name
    
    def get_name(self):
        return self.name
    
    def is_player1(self):
        return "1" in self.get_name()

class Player_Computer(Player):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def get_move(self, board: Board) -> tuple[Tile, Tile]:
        _, tile_origin, tile_destination = minimax_pruning(board, 3, self.is_player1())

        return (tile_origin, tile_destination)

class Player_Person(Player):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def get_move(self, board: Board) -> tuple[Tile, Tile]:
        # Select piece from all it pieces available
        tile_origin: Tile = ask_person_for_piece(board, "1" in self.get_name())

        # Select the destination tile for the selected piece
        tile_destination: Tile = ask_person_for_tile_destination(board, tile_origin)

        return (tile_origin, tile_destination)
        

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


if __name__ == "__main__":
    board = Board()
    players = create_players()

    current_player_index = choice([0, 1])
    print(f"{players[current_player_index].get_name()} starts\n")

    while not board.has_game_ended():
        tile_origin, tile_destination = players[current_player_index].get_move(board)
        if current_player_index == 0:
            assert tile_origin.get_piece().is_player1_piece()
        else:
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