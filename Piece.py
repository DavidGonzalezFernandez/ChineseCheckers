"""Represents a piece in the game (either from the player1 or the player2)"""
class Piece():
    PLAYER1_COLOR: str = "O"
    PLAYER2_COLOR: str = "X"

    def __init__(self, color: str) -> None:
        self.color: str = color
        
    def __str__(self) -> str:
        return self.get_color()
    
    def get_color(self) -> str:
        return self.color
    
    def is_player2_piece(self) -> bool:
        return self.color == Piece.PLAYER2_COLOR
        
    def is_player1_piece(self) -> bool:
        return self.color == Piece.PLAYER1_COLOR
