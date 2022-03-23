from Piece import Piece

"""Represents a tile (empty or filled) in the board"""
class Tile():
    VALID_DIRECTIONS: list[str] = ["L", "R", "UL", "UR", "DL", "DR"]
    EMPTY_TYLE_STR: str = "."
    DEFAULT_DISTANCE: int = -1

    def __init__(self) -> None:
        self.piece = None
        self.neighbours: dict[str, Tile] = {}
        self.distance_from_top_vertex: int = Tile.DEFAULT_DISTANCE
        self.distance_from_bottom_vertex: int = Tile.DEFAULT_DISTANCE
    
    def __str__(self) -> str:
        return Tile.EMPTY_TYLE_STR if self.is_empty() else str(self.get_piece())
    
    def set_piece(self, new_piece: Piece) -> None:
        self.piece = new_piece
    
    def set_empty(self) -> None:
        self.set_piece(None)
    
    def set_distance_from_top_vertex(self, new_distance: int) -> bool:
        if self.distance_from_top_vertex == Tile.DEFAULT_DISTANCE  or  (new_distance < self.distance_from_top_vertex):
            self.distance_from_top_vertex = new_distance
            return True
        return False

    def set_distance_from_bottom_vertex(self, new_distance: int) -> bool:
        if self.distance_from_bottom_vertex == Tile.DEFAULT_DISTANCE  or  (new_distance < self.distance_from_bottom_vertex):
            self.distance_from_bottom_vertex = new_distance
            return True
        return False

    def get_basic_str(self) -> str:
        return Tile.EMPTY_TYLE_STR if self.is_empty() else self.get_piece().get_color()

    def get_distance_from_top_vertex(self) -> int:
        return self.distance_from_top_vertex

    def get_distance_from_bottom_vertex(self) -> int:
        return self.distance_from_bottom_vertex
    
    def add_neighbour(self, direction: str, neighbour_tile) -> None:
        self.neighbours[direction] = neighbour_tile

    def get_neighbours(self) -> dict:
        return self.neighbours
    
    def get_piece(self) -> Piece:
        return self.piece
    
    def is_empty(self) -> bool:
        return self.get_piece() is None