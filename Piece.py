"""Represents a piece in the game (either from the computer or the person)"""
class Piece():
    COMPUTER_COLOR: str = "X"
    PERSON_COLOR: str = "O"

    def __init__(self, color: str) -> None:
        self.color: str = color
        
    def __str__(self) -> str:
        assert isinstance(self.get_color(), str)
        return self.get_color()
    
    def get_color(self) -> str:
        assert self.color is not None
        return self.color
    
    def is_computer_piece(self) -> bool:
        assert (self.color == Piece.PERSON_COLOR) ^ (self.color == Piece.COMPUTER_COLOR)
        return self.color == Piece.COMPUTER_COLOR
        
    def is_person_piece(self) -> bool:
        assert (self.color == Piece.PERSON_COLOR) ^ (self.color == Piece.COMPUTER_COLOR)
        return self.color == Piece.PERSON_COLOR
        
    """
    def get_score(self) -> int:
        assert self.get_tile().get_distance_from_top_vertex()  >= 0
        assert self.get_tile().get_distance_from_bottom_vertex() >= 0

        if self.is_computer_piece():
            return self.get_tile().get_distance_from_top_vertex()
        else:
            return self.get_tile().get_distance_from_bottom_vertex()"""