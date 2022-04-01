from Piece import Piece

"""Represents a tile (empty or filled) in the board"""
class Tile():
    VALID_DIRECTIONS: list[str] = ["L", "R", "UL", "UR", "DL", "DR"]
    EMPTY_TYLE_STR: str = "."
    DEFAULT_SCORE: int = -1

    def __init__(self) -> None:
        self.piece = None
        self.neighbours: dict[str, Tile] = {}
        self.score_for_person: int = Tile.DEFAULT_SCORE
        self.score_for_computer: int = Tile.DEFAULT_SCORE
    
    def __str__(self) -> str:
        return Tile.EMPTY_TYLE_STR if self.is_empty() else str(self.get_piece())
    
    def set_piece(self, new_piece: Piece) -> None:
        self.piece = new_piece
    
    def set_empty(self) -> None:
        self.set_piece(None)
        assert self.get_piece() is None
        assert self.is_empty()

    def set_score_for_person(self, new_score: int) -> bool:
        if self.score_for_person == Tile.DEFAULT_SCORE  or  (new_score > self.score_for_person):
            self.score_for_person = new_score
            return True
        return False

    def set_score_for_computer(self, new_score: int) -> bool:
        if self.score_for_computer == Tile.DEFAULT_SCORE  or  (new_score > self.score_for_computer):
            self.score_for_computer = new_score
            return True
        return False
    
    def get_score(self) -> int:
        assert self.score_for_person != Tile.DEFAULT_SCORE
        assert self.score_for_computer != Tile.DEFAULT_SCORE
        assert self.get_piece() is not None

        if self.get_piece().is_computer_piece():
            return self.get_score_for_computer()
        else:
            return self.get_score_for_person()

    def get_score_for_person(self) -> int:
        assert self.score_for_person != Tile.DEFAULT_SCORE
        assert self.score_for_person >= 0
        return self.score_for_person

    def get_score_for_computer(self) -> int:
        assert self.score_for_computer != Tile.DEFAULT_SCORE
        assert self.score_for_computer >= 0
        return self.score_for_computer
    
    def add_neighbour(self, direction: str, neighbour_tile) -> None:
        self.neighbours[direction] = neighbour_tile
        assert len(list(self.neighbours.keys())) <= 6

    def get_neighbours(self) -> dict:
        return self.neighbours
    
    def get_piece(self) -> Piece:
        return self.piece
    
    def is_empty(self) -> bool:
        return self.get_piece() is None