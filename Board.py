from Tile import Tile
from Piece import Piece

class Board():
    def __init__(self) -> None:
        self.board_row_tiles: list[list[Tile]] = self.generate_board_rows()
        self.board_tiles: list[Tile] = self.rows_to_board()

        assert Piece.PERSON_COLOR != Piece.COMPUTER_COLOR
        self.pieces: list[Piece] = self.generate_pieces()

        self.add_neighbouring_tiles()
        self.place_pieces_in_board()
        self.calculate_distances()
    
    def generate_board_rows(self) -> list[list[Tile]]:
        TILES_PER_ROW: list[int] = [1, 2, 3, 4, 13, 12, 11, 10, 9, 10, 11, 12, 13, 4, 3, 2, 1]
        board_rows: list[list[Tile]] = []
        for i in range(17):
            board_rows.append([Tile() for _ in range(TILES_PER_ROW[i])])
        return board_rows
    
    """Receives the list of rows with Tiles and outputs a list of Tiles"""
    def rows_to_board(self) -> list[Tile]:
        board: list[Tile] = []
        for row in self.board_row_tiles:
            board.extend(row)

        return board

    """Creates 10 pieces for the person and another 10 pieces for the computer.
    Returns a single list with all 20 pieces"""
    def generate_pieces(self) -> list[Piece]:
        pieces = [Piece(Piece.PERSON_COLOR) for _ in range(10)] + [Piece(Piece.COMPUTER_COLOR) for _ in range(10)]
        assert len(list(pieces)) == 20
        return pieces
    
    """Adds all the neighbours for each tile"""
    def add_neighbouring_tiles(self) -> None:
        # Add edges within the row
        for row in self.board_row_tiles:
            for i in range(0, len(row)-1):
                row[i].add_neighbour("R", row[i+1])
            for i in range(1, len(row)):
                row[i].add_neighbour("L", row[i-1])
        
        # Check that the number of edges matches the expected
        assert sum(len(list(tile.get_neighbours().values())) for row in self.board_row_tiles for tile in row) == (121 - 17) * 2

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

        edge_count = 0
        opposite_directions = {"L": "R", "R": "L", "UL": "DR", "UR": "DL", "DL": "UR", "DR": "UL"}
        for row in self.board_row_tiles:
            for tile in row:
                # Check that every Tile has between 2 and 6 edges
                assert 2 <= len(list(tile.get_neighbours().values())) <= 6
                edge_count += len(list(tile.get_neighbours().values()))
                for (neighbour_direction, neighbour_tile) in tile.get_neighbours().items():
                    # Check that there are no loops
                    assert neighbour_tile is not tile
                    # Check that the edges exist in both ways
                    assert neighbour_tile.get_neighbours()[opposite_directions[neighbour_direction]] == tile
                    pass
        
        # Check number of edges match the expected number
        assert edge_count == (121 - 17) * 2 * 3
    
    """Places the 20 pieces where they should be at the start of the game"""
    def place_pieces_in_board(self) -> None:
        i = 0
        for piece in self.get_person_pieces():
            self.board_tiles[i].set_piece(piece)
            i += 1
        assert i == 10
        
        for piece in self.get_computer_pieces():
            self.board_tiles[-i].set_piece(piece)
            i -= 1
        assert i == 0
        
        assert all(tile.is_empty() for tile in self.board_tiles[10 : -10])
        assert all(not tile.is_empty() for tile in self.board_tiles[:10]+self.board_tiles[-10:])
    
    """Returns a filter that iterates through all Pieces of the person"""
    def get_person_pieces(self):
        return filter(lambda p: p.is_person_piece(), self.pieces)

    """Returns a filter that iterates through all Pieces of the computer"""
    def get_computer_pieces(self):
        return filter(lambda p: p.is_computer_piece(), self.pieces)

    def has_computer_won(self) -> bool:
        return all(not tile.is_empty() and tile.get_piece().is_computer_piece() for tile in self.board_tiles[:10])

    def has_person_won(self) -> bool:
        return all(not tile.is_empty() and tile.get_piece().is_person_piece() for tile in self.board_tiles[-10:])
    
    """Return True if (at least) one of the player has reached the end of the board"""
    def has_game_ended(self) -> bool:
        return self.has_computer_won() or self.has_person_won()

    def get_score(self) -> int:
        if self.has_computer_won():
            return 1_000_000
        elif self.has_person_won():
            return -1_000_000
        return sum(t.get_distance_from_top_vertex() for t in self.get_computer_tiles()) - sum(t.get_distance_from_bottom_vertex() for t in self.get_person_tiles())
        
    def get_computer_tiles(self):
        return filter(lambda t: not t.is_empty()  and  t.get_piece().is_computer_piece(), self.board_tiles)

    def get_person_tiles(self):
        return filter(lambda t: not t.is_empty() and t.get_piece().is_person_piece(), self.board_tiles)
    
    """Generator that outputs all the tiles where you can move to"""
    def get_all_possible_tiles_to_move(self, tile: Tile, only_jumps = False, already_jumped_from = None, already_returned = None):
        assert tile is not None
        assert 2 <= len(list(tile.get_neighbours().values())) <= 6

        # This only happens on the first call
        if already_jumped_from is None:
            already_jumped_from = set()
            already_returned = set()
        
        # We only process the tile if we still haven't jumped from this tile
        if tile not in already_jumped_from:
            # Add the starting tile 
            already_jumped_from.add(tile)

            neighbour_direction: str
            neighbour_tile: Tile

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
                                if move not in already_returned:
                                    yield move
                                    already_returned.add(move)
                                else:
                                    assert False, "It is neccessary"
    
    def get_top_triangle_tiles(self):
        return self.board_row_tiles[0] + self.board_row_tiles[1] + self.board_row_tiles[2] + self.board_row_tiles[3]

    def get_bottom_triangle_tiles(self):
        return self.board_row_tiles[-1] + self.board_row_tiles[-2] + self.board_row_tiles[-3] + self.board_row_tiles[-4]
    
    def get_all_valid_moves(self, tile_origin: Tile):
        for move in self.get_all_possible_tiles_to_move(tile_origin):
            if tile_origin.get_piece().is_computer_piece()  and  tile_origin in self.get_top_triangle_tiles()  and   move not in self.get_top_triangle_tiles():
                continue
            elif tile_origin.get_piece().is_person_piece()  and  tile_origin in self.get_bottom_triangle_tiles()  and  move not in self.get_bottom_triangle_tiles():
                continue
            else:
                yield move

                                    
    """Moves the piece in the arguments to the tile in the paramenters. If the movement is not possible it does nothing returns False"""
    def move_piece_to_tile(self, tile_origin: Tile, destination_tile: Tile) -> bool:
        assert destination_tile is not None

        if not destination_tile.is_empty():
            # We cannot move here
            return False
        
        destination_tile.set_piece(tile_origin.get_piece())
        tile_origin.set_empty()

        assert sum(1 for tile in self.board_tiles if not tile.is_empty()) == 20
        return True

    """Calculates for all tiles in the board the distance from that tile to tiles in the top and bottom edges"""
    def calculate_distances(self) -> None:
        pending_of_exploring: list[Tile]

        # Calculate distances from top vertex
        self.board_tiles[0].set_distance_from_top_vertex(0)
        pending_of_exploring = [tile for tile in self.board_tiles[0].get_neighbours().values() if tile.set_distance_from_top_vertex(1)]
        while len(pending_of_exploring) > 0:
            exploring_tile, pending_of_exploring = pending_of_exploring[0], pending_of_exploring[1:]
            pending_of_exploring.extend( [tile for tile in exploring_tile.get_neighbours().values() if tile.set_distance_from_top_vertex(exploring_tile.get_distance_from_top_vertex() + 1)] )
        
        # Checks
        distances = [tile.get_distance_from_top_vertex() for tile in self.board_tiles]              # Used at the end to check that the distances have not changed
        assert distances[0] == 0                                                                    # Checks the distance from top for the first tile
        assert all(distance > 0 for distance in distances[1:])                                      # Checks the distance from top for the rest of tiles
        assert all(tile.distance_from_bottom_vertex == Tile.DEFAULT_DISTANCE for tile in self.board_tiles) # Checks the distance to the bottom of all tiles
        
        # Calculate distances from bottom vertex
        self.board_tiles[-1].set_distance_from_bottom_vertex(0)
        pending_of_exploring = [tile for tile in self.board_tiles[-1].get_neighbours().values() if tile.set_distance_from_bottom_vertex(1)]
        while len(pending_of_exploring) > 0:
            exploring_tile, pending_of_exploring = pending_of_exploring[0], pending_of_exploring[1:]
            pending_of_exploring.extend( [tile for tile in exploring_tile.get_neighbours().values() if tile.set_distance_from_bottom_vertex(exploring_tile.get_distance_from_bottom_vertex() + 1)] )

        # Checks
        assert [tile.get_distance_from_top_vertex() for tile in self.board_tiles] == distances     # Checks that the distance from top is still the same
        assert self.board_tiles[-1].get_distance_from_bottom_vertex() == 0                         # Checks the tile at the bottom
        assert all(tile.get_distance_from_bottom_vertex() > 0 for tile in self.board_tiles[:-1])   # Check the rest of the tiles

    """Prints the board in the command line"""
    def print_board(self, numbered_tiles=None, characters="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ") -> None:
        numbered_tiles = [] if numbered_tiles is None else list(numbered_tiles)
        
        # Calculate the lenth of the row(s) with the most tiles
        max_length: int = max( (len(row) for row in self.board_row_tiles) )

        print("CURRENT BOARD:\n")
        for row in self.board_row_tiles:
            # Print the spaces before the row
            print(" "*(max_length-len(row)), end="")
            tile: Tile
            for tile in row:
                # Print each tile
                if tile in numbered_tiles:
                    print(f"{characters[numbered_tiles.index(tile)]}", end=" ")
                else:
                    assert tile is not None
                    print(f"{str(tile)}", end=" ")
            print("")   # New line
        print("\n")
    
    def get_tile(self, piece: Piece):
        assert piece is not None
        assert isinstance(piece, Piece)
        assert piece in self.pieces
        
        return next(tile for tile in self.board_tiles if tile.get_piece() is piece)