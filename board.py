'''

'''
import tile
from texture_enums import *
from board_config import *

class Board:
    """
    players: List of players
    tiles: List of tiles on board
    vertices:
    roads: List of edges with roads built
    resource_bank:
    development_cards
    """
    def __init__(self):
        self.players = []
        self.tiles = []
        self.vertices = []
        self.roads = []
        self.resource_bank = []
        self.development_cards = []


        self.beginner_setup()

    def beginner_setup(self):
        """ Add 19 tiles to self.tiles
        Board represented with axial coordinates where middle row has y = 0
        Top left line of hexagons has x = -2 """

        # Axial coordinates by row from top to bottom
        tile_coords = [
            # Top row
                    (0, -2), (1, -2), (2, -2),
            # Second row
                (-1, -1), (0, -1), (1, -1), (2, -1),
            # Third row
              (-2, 0), (-1, 0), (0, 0), (1, 0), (2,0),
            # Fourth row
                (-2, 1), (-1, 1), (0, 1), (1, 1),
            # Fifth row
                    (-2, 2), (-1, 2), (0, 2)
        ]

        # Generation Numbers
        tile_gen_nums = [
            10, 2, 9,
            12, 6, 4, 10,
            9, 11, 0, 3, 8,
            8, 3, 4, 5,
            5, 6, 11
        ]

        # Resources in order in beginner setup
        tile_resources = [
            Resource.ore, Resource.sheep, Resource.wood,
            Resource.wheat, Resource.brick, Resource.sheep, Resource.brick,
            Resource.wheat, Resource.wood, Resource.desert, Resource.wood, Resource.ore,
            Resource.wood, Resource.ore, Resource.wheat, Resource.sheep,
            Resource.brick, Resource.wheat, Resource.sheep
        ]

        # Vertices left to right, top to bottom

        for i in range(19):
            self.tiles.append(tile.Tile(coords=tile_coords[i], genNum=tile_gen_nums[i], resource=tile_resources[i]))


    def get_tile_at(self, coords):
        """ Returns the tile at given axial coordinates """
        for tile in self.tiles:
            if tile.coords == coords:
                return tile
    
    # check winning conditions

    # place road

    # place on vertex

    # start turn: roll die/distribute resources

    # trading

    # adding/removing cards from hand


