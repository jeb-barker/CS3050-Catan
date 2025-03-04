'''

'''
import tile
class board:
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
            (-2, 2), (-1, 2), (0, 2),
            # Second row
            (-2, 1), (-1, 1), (0, 1), (1, 1),
            # Third row
            (-2, 0), (-1, 0), (0, 0), (1, 0), (2,0),
            # Fourth row
            (-1, -1), (-1, 0), (-1, 1), (-1, 2),
            # Fifth row
            (-2, 0), (-2, 1), (-2, 2)
        ]

        # Resources in order in beginner setup
        tile_resources = [
            "mountains", "pasture", "forest",
            "fields", "hills", "pasture", "hills",
            "fields", "forest", "desert", "forest", "mountains",
            "forest", "mountains", "fields", "pasture",
            "hills", "fields", "pasture"
        ]
        for i in range(19):
            self.tiles.append(tile.Tile(coords=tile_coords[i], resource=tile_resources[i]))


    def get_tile_at(self, coords):
        """ Returns the tile at given axial coordinates """
        for tile in self.tiles:
            if tile.coords == coords:
                return tile
