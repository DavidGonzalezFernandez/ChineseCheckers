from Board import Board
from Tile import Tile
from Piece import Piece
from random import choice

CHARACTERS = "1234567890ABCDEFGHJKLMNPQRSTUVWXYZ"
CHARACTERS_NO_ZERO = "123456789ABCDEFGHJKLMNPQRSTUVWXYZ"

def get_person_move(board: Board) -> tuple[Tile, Tile]:
    # Select piece from all it pieces available
    tile_origin: Tile = ask_person_for_piece(board)

    # Select the destination tile for the selected piece
    tile_destination: Tile = ask_person_for_tile_destination(board, tile_origin)

    return (tile_origin, tile_destination)

def ask_person_for_piece(board: Board) -> Tile:
    tiles_with_movable_pieces: list[Tile] = list(filter(
        lambda t: any(board.get_all_valid_moves(t)), board.get_person_tiles()
    ))
    board.print_board(tiles_with_movable_pieces, "".join(CHARACTERS))

    while True:
        n = input(f"Select a piece ({CHARACTERS[0]} - {CHARACTERS[len(tiles_with_movable_pieces)-1]})").strip().upper()
        if n in CHARACTERS[ : len(tiles_with_movable_pieces)]:
            selected_tile = tiles_with_movable_pieces[CHARACTERS.index(n)]
            assert selected_tile.get_piece().is_person_piece()
            return selected_tile

def ask_person_for_tile_destination(board: Board, tile_origin: Tile) -> Tile:
    assert board is not None
    assert isinstance(tile_origin, Tile)
    assert tile_origin.get_piece().is_person_piece()

    available_tile_destinations: list[Tile] = [tile for tile in board.get_all_valid_moves(tile_origin)]

    board.print_board(available_tile_destinations, CHARACTERS_NO_ZERO)

    while True:
        n = input(f"Select a tile to move to ({CHARACTERS_NO_ZERO[0]} - {CHARACTERS_NO_ZERO[len(available_tile_destinations)-1]})").strip().upper()
        if n in CHARACTERS_NO_ZERO[ : 1+len(available_tile_destinations)]:
            destination_tile = available_tile_destinations[ CHARACTERS_NO_ZERO.index(n) ]
            assert destination_tile is not None
            assert isinstance(destination_tile, Tile)
            assert destination_tile.is_empty()
            return destination_tile

def minimax(board: Board, depth: int, maximize_for_computer: bool = True) -> tuple[int, Tile, Tile]:
    if depth==0  or  board.has_game_ended():
        return board.get_score(), None, None
    
    if maximize_for_computer:
        max_points, better_origin, better_destination = float('-inf'), None, None
        for tile_origin in board.get_computer_tiles():
            for tile_destination in board.get_all_valid_moves(tile_origin):
                board.move_piece_to_tile(tile_origin, tile_destination)
                res_points, _1, _2 = minimax(board, depth-1, not maximize_for_computer)
                board.move_piece_to_tile(tile_destination, tile_origin)

                if res_points > max_points:
                    max_points, better_origin, better_destination = res_points, tile_origin, tile_destination
        return max_points, better_origin, better_destination
    
    else:
        min_points, better_origin, better_destination = float('inf'), None, None
        for tile_origin in board.get_person_tiles():
            for tile_destination in board.get_all_valid_moves(tile_origin):
                board.move_piece_to_tile(tile_origin, tile_destination)
                res_points, _1, _2 = minimax(board, depth-1, not maximize_for_computer)
                board.move_piece_to_tile(tile_destination, tile_origin)

                if res_points < min_points:
                    min_points, better_origin, better_destination = res_points, tile_origin, tile_destination
        return min_points, better_origin, better_destination


def get_computer_move(board: Board) -> tuple[Tile, Tile]:
    _, tile_origin, tile_destination = minimax(board, 3)

    return (tile_origin, tile_destination)


if __name__ == "__main__":
    board = Board()

    is_person_turn = choice([True, False])
    if is_person_turn:
        print("You start!\n")
    else:
        print("The computer starts\n")
    
    while not board.has_game_ended():
        if is_person_turn:
            tile_origin, tile_destination = get_person_move(board)
            assert tile_origin.get_piece().is_person_piece()
        else:
            tile_origin, tile_destination = get_computer_move(board)
            assert tile_origin.get_piece().is_computer_piece()

        assert tile_destination.is_empty()
        board.move_piece_to_tile(tile_origin, tile_destination)
        board.print_board()
        is_person_turn = not is_person_turn
    
    if board.has_person_won():
        assert not board.has_computer_won()
        print("You won!")
    else:
        assert board.has_computer_won()
        print("The computer has won :(")