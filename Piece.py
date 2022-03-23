from Tile import Tile

"""Represents a piece in the game (either from the computer or the person)"""
class Piece():
    COMPUTER_COLOR: str = "X"
    PERSON_COLOR: str = "O"

    def __init__(self, color: str) -> None:
        self.tile: Tile = None
        self.color: str = color
        
    def __str__(self) -> str:
        return self.get_color()

    def set_tile(self, new_tile: Tile) -> None:
        self.tile = new_tile
    
    def get_tile(self) -> Tile:
        return self.tile
    
    def get_color(self) -> str:
        return self.color
    
    def is_computer_piece(self) -> bool:
        return self.color == Piece.COMPUTER_COLOR
        
    def is_person_piece(self) -> bool:
        return self.color == Piece.PERSON_COLOR

    def get_score(self) -> int:
        return self.get_tile().get_distance_from_top_vertex() if self.is_computer_piece() else self.get_tile().get_distance_from_bottom_vertex()