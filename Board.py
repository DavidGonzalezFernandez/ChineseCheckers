from Tile import Tile
from Piece import Piece

class Board():
    def __init__(self) -> None:
        # Create the tiles, an arrange them in a list of lists
        self.board_row_tiles: list[list[Tile]] = self.generate_board_rows()

        # Arrange the tiles in a single list
        self.board_tiles: list[Tile] = self.rows_to_board()

        # Generate the pieces for both players
        self.pieces: list[Piece] = self.generate_pieces()

        # Generate then links between all tiles
        self.add_neighbouring_tiles()

        # Place the pieces of both users in the board
        self.place_pieces_in_board()

        # Calculate scores for every tiles later used in evaluation function
        self.calculate_tiles_scores()
    
    """Creates and returns a lists of Tiles that represent each row in the board"""
    def generate_board_rows(self) -> list[list[Tile]]:
        TILES_PER_ROW: list[int] = [1, 2, 3, 4, 13, 12, 11, 10, 9, 10, 11, 12, 13, 4, 3, 2, 1]
        board_rows: list[list[Tile]] = []
        for i in range(len(TILES_PER_ROW)):
            board_rows.append([Tile() for _ in range(TILES_PER_ROW[i])])
        return board_rows
    
    """Receives the list of rows with Tiles and outputs a list of Tiles"""
    def rows_to_board(self) -> list[Tile]:
        board: list[Tile] = []
        for row in self.board_row_tiles:
            board.extend(row)
        return board

    """Creates 10 pieces for the player1 and another 10 pieces for the player2.
    Returns a single list with all 20 pieces"""
    def generate_pieces(self) -> list[Piece]:
        return [Piece(Piece.PLAYER1_COLOR) for _ in range(10)] + [Piece(Piece.PLAYER2_COLOR) for _ in range(10)]
    
    """Adds all the neighbours for each tile"""
    def add_neighbouring_tiles(self) -> None:
        # Add edges within the row
        for row in self.board_row_tiles:
            for i in range(0, len(row)-1):
                row[i].add_neighbour("R", row[i+1])
            for i in range(1, len(row)):
                row[i].add_neighbour("L", row[i-1])

        # Add some diagonal edges (1/4)
        for row_index in [0, 1, 2, 8, 9, 10, 11]:
            for tile_index in range(len(self.board_row_tiles[row_index])):
                self.board_row_tiles[row_index    ][tile_index    ].add_neighbour("DL", self.board_row_tiles[row_index+1][tile_index])
                self.board_row_tiles[row_index    ][tile_index    ].add_neighbour("DR", self.board_row_tiles[row_index+1][tile_index+1])
                self.board_row_tiles[row_index + 1][tile_index    ].add_neighbour("UR", self.board_row_tiles[row_index][tile_index])
                self.board_row_tiles[row_index + 1][tile_index + 1].add_neighbour("UL", self.board_row_tiles[row_index][tile_index])

        # Add more diagonal edges (2/4)
        for row_index in [5, 6, 7, 8, 14, 15, 16]:
            for tile_index in range(len(self.board_row_tiles[row_index])):
                self.board_row_tiles[row_index    ][tile_index    ].add_neighbour("UL", self.board_row_tiles[row_index - 1][tile_index])
                self.board_row_tiles[row_index    ][tile_index    ].add_neighbour("UR", self.board_row_tiles[row_index - 1][tile_index+1])
                self.board_row_tiles[row_index - 1][tile_index    ].add_neighbour("DR", self.board_row_tiles[row_index    ][tile_index])
                self.board_row_tiles[row_index - 1][tile_index + 1].add_neighbour("DL", self.board_row_tiles[row_index    ][tile_index])

        # Add more diagonal edges (3/4)
        for tile_index in range(len(self.board_row_tiles[3])):
            self.board_row_tiles[3][tile_index    ].add_neighbour("DL", self.board_row_tiles[4][tile_index + 4])
            self.board_row_tiles[3][tile_index    ].add_neighbour("DR", self.board_row_tiles[4][tile_index + 5])
            self.board_row_tiles[4][tile_index + 4].add_neighbour("UR", self.board_row_tiles[3][tile_index])
            self.board_row_tiles[4][tile_index + 5].add_neighbour("UL", self.board_row_tiles[3][tile_index])

        # Add last diagonal edges (4/4)
        for tile_index in range(len(self.board_row_tiles[13])):
            self.board_row_tiles[13][tile_index    ].add_neighbour("UL", self.board_row_tiles[12][tile_index + 4])
            self.board_row_tiles[13][tile_index    ].add_neighbour("UR", self.board_row_tiles[12][tile_index + 5])
            self.board_row_tiles[12][tile_index + 4].add_neighbour("DR", self.board_row_tiles[13][tile_index])
            self.board_row_tiles[12][tile_index + 5].add_neighbour("DL", self.board_row_tiles[13][tile_index])
    
    """Places the 20 pieces where they should be at the start of the game"""
    def place_pieces_in_board(self) -> None:
        i = 0
        for piece in self.get_player1_pieces():
            self.board_tiles[i].set_piece(piece)
            i += 1
        
        for piece in self.get_player2_pieces():
            self.board_tiles[-i].set_piece(piece)
            i -= 1

    """Returns all the tiles that contain pieces from the player1"""
    def get_player1_tiles(self):
        return filter(lambda t: not t.is_empty()  and  t.get_piece().is_player1_piece(), self.board_tiles)

    """Returns all the tiles that contain pieces from the player2"""
    def get_player2_tiles(self):
        return filter(lambda t: not t.is_empty()  and  t.get_piece().is_player2_piece(), self.board_tiles)
        
    """Returns a filter that iterates through all Pieces of the player1"""
    def get_player1_pieces(self):
        return filter(lambda p: p.is_player1_piece(), self.pieces)

    """Returns a filter that iterates through all Pieces of the player2"""
    def get_player2_pieces(self):
        return filter(lambda p: p.is_player2_piece(), self.pieces)

    """Check if triangle destination for player1 is filled with player1 Tiles"""
    def has_player1_reached_destination(self) -> bool:
        return all(not tile.is_empty() for tile in self.get_bottom_triangle_tiles())  and  any(tile.get_piece().is_player1_piece() for tile in self.get_bottom_triangle_tiles())

    """Check if triangle destination for player2 is filled with player2 Tiles"""
    def has_player2_reached_destination(self) -> bool:
        return all(not tile.is_empty() for tile in self.get_top_triangle_tiles())  and  any(tile.get_piece().is_player2_piece() for tile in self.get_top_triangle_tiles())

    """Check if player1 can move"""
    def can_player1_move(self) -> bool:
        return any(filter(lambda t: any(self.get_all_valid_moves(t)), self.get_player1_tiles()))

    """Check if player2 can move"""
    def can_player2_move(self) -> bool:
        return any(filter(lambda t: any(self.get_all_valid_moves(t)), self.get_player2_tiles()))

    """Check if the player1 has won"""
    def has_player1_won(self) -> bool:
        # Has won if has reached destination 
        return self.has_player1_reached_destination()

    """Check if the player2 has won"""
    def has_player2_won(self) -> bool:
        # Has won if has reached destination
        return self.has_player2_reached_destination()

    """Return True if (at least) one of the player has reached the end of the board"""
    def has_game_ended(self) -> bool:
        return self.has_player2_won() or self.has_player1_won()

    """Return the score for the current state of the board"""
    def get_score(self, is_player1_turn: bool, use_eval_func_1: bool) -> int:
        if (is_player1_turn  and  self.has_player1_won())  or  (not is_player1_turn  and  self.has_player2_won()):
            return 1_000_000
        if (is_player1_turn  and  self.has_player2_won())  or  (not is_player1_turn  and  self.has_player1_won()):
            return -1_000_000
         
        if use_eval_func_1:
            # Evaluation function 1
            score_player_1 = sum(t.get_score1() for t in self.get_player1_tiles()) * (1 if is_player1_turn else -1)
            score_player_2 = sum(t.get_score1() for t in self.get_player2_tiles()) * (-1 if is_player1_turn else 1)
            return score_player_1 + score_player_2
        else:
            # Evaluation function 2
            score_player_1 = sum(t.get_score2() for t in self.get_player1_tiles()) * (1 if is_player1_turn else -1)
            score_player_2 = sum(t.get_score2() for t in self.get_player2_tiles()) * (-1 if is_player1_turn else 1)
            return score_player_1 + score_player_2
    
    """Generator that outputs all the tiles where you can move to"""
    def get_all_possible_tiles_to_move(self, tile: Tile, only_jumps = False, already_jumped_from = None, already_returned = None):
        # This only happens on the first call
        if already_jumped_from is None:
            already_jumped_from = set()
            already_returned = set()
        
        # We only process the tile if we still haven't jumped from this tile
        if tile not in already_jumped_from:
            # Add the starting tile 
            already_jumped_from.add(tile)

            for (neighbour_direction, neighbour_tile) in tile.get_neighbours().items():
                if neighbour_tile.is_empty():
                    # A neighbouring tile is empty, we can move to that it directly but we cannot jump it
                    if not only_jumps:
                        # Only return the result if it is the first move (if it is a recursive call only_jumps is set to True)
                        yield neighbour_tile
                else:
                    # Neighbour is not empty, maybe we can jump
                    neighbours_neighbour: Tile = neighbour_tile.get_neighbours().get(neighbour_direction, None)
                    if neighbours_neighbour is not None:
                        # The neighbour exists
                        if neighbours_neighbour.is_empty():
                            # It exists and it is empty, we can jump to it
                            if neighbours_neighbour not in already_returned:
                                yield neighbours_neighbour
                                already_returned.add(neighbours_neighbour)
                            for move in self.get_all_possible_tiles_to_move(neighbours_neighbour, True, already_jumped_from, already_returned):
                                # Maybe we can keep on jumping
                                yield move
                                already_returned.add(move)
    
    """Return the tiles that are part of the triangle in the top"""
    def get_top_triangle_tiles(self):
        return self.board_tiles[:10]

    """Return the tiles that are part of the triangle in the bottom"""
    def get_bottom_triangle_tiles(self):
        return self.board_tiles[-10:]
    
    """Generates all the valid moves from the piece in the argument"""
    def get_all_valid_moves(self, tile_origin: Tile):
        for move in self.get_all_possible_tiles_to_move(tile_origin):
            # Moves that are not valid: move a piece that already rests in its target triangle out of that triangle
            if tile_origin.get_piece().is_player2_piece()  and  tile_origin in self.get_top_triangle_tiles()  and   move not in self.get_top_triangle_tiles():
                continue
            elif tile_origin.get_piece().is_player1_piece()  and  tile_origin in self.get_bottom_triangle_tiles()  and  move not in self.get_bottom_triangle_tiles():
                continue
            else:
                yield move
    
    """Generates all valid moves that satisfy the heuristic function"""
    def get_all_valid_logical_moves(self, tile_origin: Tile, heuristic_function):
        for tile_destination in self.get_all_valid_moves(tile_origin):
            if heuristic_function(tile_origin, tile_destination):
                yield tile_destination

                                    
    """Moves the piece in the arguments to the tile in the paramenters. If the movement is not possible it does nothing returns False"""
    def move_piece_to_tile(self, tile_origin: Tile, destination_tile: Tile) -> bool:
        if not destination_tile.is_empty():
            # We cannot move here, do not do anythin
            return False
        
        destination_tile.set_piece(tile_origin.get_piece())
        tile_origin.set_empty()

        return True

    """Calculates for all tiles in the board the distance from that tile to tiles in the top and bottom edges"""
    def calculate_tiles_scores(self) -> None:
        pending_of_exploring: list[Tile]

        # Evaluation function 1
        # Calculate scores for player1 player
        pending_of_exploring = [self.board_tiles[-1]]
        pending_of_exploring[0].set_score1_for_player1(16)
        while any(pending_of_exploring):
            exploring_tile, pending_of_exploring = pending_of_exploring[0], pending_of_exploring[1:]
            pending_of_exploring.extend( [tile for tile in exploring_tile.get_neighbours().values() if tile.set_score1_for_player1(exploring_tile.get_score1_for_player1() - 1)] )
        for tile in self.get_bottom_triangle_tiles():
            tile.set_score1_for_player1(5 + tile.get_score1_for_player1())
        
        # Calculate scores for player2 player
        pending_of_exploring = [self.board_tiles[0]]
        pending_of_exploring[0].set_score1_for_player2(16)
        while any(pending_of_exploring):
            exploring_tile, pending_of_exploring = pending_of_exploring[0], pending_of_exploring[1:]
            pending_of_exploring.extend( [tile for tile in exploring_tile.get_neighbours().values() if tile.set_score1_for_player2(exploring_tile.get_score1_for_player2() - 1)] )
        for tile in self.get_top_triangle_tiles():
            tile.set_score1_for_player2(5 + tile.get_score1_for_player2())

        # Evaluation function 2
        # Player 1
        for i in range(len(self.board_row_tiles)):
            row = self.board_row_tiles[i]
            for j in range(len(row)):
                if len(row) % 2 == 0:
                    row[j].set_score2_for_player1(1*10 - abs(int((len(row)-1)/2 - j)))
                else:
                    row[j].set_score2_for_player1(i*10 - abs(len(row)//2 - j))
        for tile in self.get_bottom_triangle_tiles():
            tile.set_score2_for_player1(tile.get_score2_for_player1() + 50)
        # Player2
        for i in range(len(self.board_row_tiles)):
            row = self.board_row_tiles[i]
            for j in range(len(row)):
                if len(row) % 2 == 0:
                    row[j].set_score2_for_player2((16-i)*10 - abs(int((len(row)-1)/2 - j)))
                else:
                    row[j].set_score2_for_player2((16-i)*10 - abs(len(row)//2 - j))
        for tile in self.get_top_triangle_tiles():
            tile.set_score2_for_player2(tile.get_score2_for_player2() + 50)

    """Prints the board in the command line"""
    def print_board(self, numbered_tiles=None, characters="123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ") -> None:
        print(self.to_string(numbered_tiles, characters))

    def to_string(self, numbered_tiles=None, characters="123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ") -> str:
        res = ""
        numbered_tiles = [] if numbered_tiles is None else list(numbered_tiles)
        
        # Calculate the lenth of the row(s) with the most tiles
        max_length: int = max( (len(row) for row in self.board_row_tiles) )

        res += "CURRENT BOARD:\n"
        for row in self.board_row_tiles:
            # Print the spaces before the row
            res += " "*(max_length-len(row))
            tile: Tile
            for tile in row:
                # Print each tile
                if tile in numbered_tiles:
                    res += f"{characters[numbered_tiles.index(tile)]} "
                else:
                    res += f"{str(tile)} "
            res += "\n"
        res += "\n"

        return res

    
    """Returns if both tiles are in the same row"""
    def get_row_index(self, tile: Tile) -> int:
        for i in range(len(self.board_row_tiles)):
            if tile in self.board_row_tiles[i]:
                return i
    
    """Returns the tile that contain the piece in the argument"""
    def get_tile(self, piece: Piece):
        return next(tile for tile in self.board_tiles if tile.get_piece() is piece)
