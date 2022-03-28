from Board import Board
from Tile import Tile
from Piece import Piece
from random import choice

def get_person_move(board: Board) -> tuple[Piece, Tile]:
    # Select piece from all it pieces available
    piece_to_move: Piece = None         #TODO: implement

    # Select the destination tile for the selected piece
    tile_destination: Tile = None       #TODO: implement

    return (piece_to_move, tile_destination)


def get_computer_move(board: Board) -> tuple[Piece, Tile]:
    piece_to_move, tile_destination = None, None    #TODO: implement

    return (piece_to_move, tile_destination)


if __name__ == "__main__":
    board = Board()
    board.print_board()

    is_person_turn = choice([True, False])
    if is_person_turn:
        print("You start!\n")
    else:
        print("The computer starts\n")
    
    while not board.has_game_ended():
        if is_person_turn:
            piece_to_move, tile_destination = get_person_move(board)
            assert piece_to_move.is_person_piece()
            assert tile_destination.is_empty()
        else:
            piece_to_move, tile_destination = get_computer_move(board)
            assert piece_to_move.is_computer_piece()
            assert tile_destination.is_empty()

        board.move_piece_to_tile(piece_to_move, tile_destination)
        is_person_turn = not is_person_turn
    
    if board.has_person_won():
        assert not board.has_computer_won()
        print("You won!")
    else:
        assert board.has_computer_won()
        print("The computer has won :(")