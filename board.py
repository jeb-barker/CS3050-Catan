'''

'''
import road
import tile
from texture_enums import *
from board_config import *
from road import *
import random

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
        self.resource_bank = {} # maps resource enum values (i.e. Resource.wheat) to a list of cards 
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
            self.tiles.append(tile.Tile(coords=tile_coords[i], gen_num=tile_gen_nums[i], resource=tile_resources[i]))
        
        # Set up the resource bank
        for resource in [Resource.brick, Resource.ore, Resource.sheep, Resource.wheat, Resource.wood]:
            # Add 19 of each resource type to the board's bank
            self.resource_bank[resource] = [Card(resource.value) for _ in range(19)]


    def get_tile_at(self, coords):
        """ Returns the tile at given axial coordinates """
        for tile in self.tiles:
            if tile.coords == coords:
                return tile
    

    # place road
    def place_road(self, owner, vertex1, vertex2):
        """ Place road between two vertices. Returns true if successful
         and returns false if a road already exists in that location """
        # Check if road exists between two vertices already
        for road in self.roads:
            if road.vertex1 == vertex1 and road.vertex2 == vertex2:
                return False
            elif road.vertex1 == vertex2 and road.vertex2 == vertex1:
                return False
            elif vertex1 == vertex2:
                return False
            else:
                if vertex2 in VERTEX_ADJACENCY[road.vertex1]:
                    self.roads.append(Road(owner=owner, vertex1=vertex1, vertex2=vertex2))
                    return True

    # place building at the given vertex_index
    # returns False if there's an error or the placement is invalid otherwise, returns True
    def place_building(self, building, owner, vertex_index):
        vertex = self.vertices[vertex_index]
        if self.is_valid_settle_spot(vertex_index):
            # case if placing a settlement or city
            if building == Building.settlement or building == Building.city:
                self.vertices[vertex_index].owner = owner
                self.vertices[vertex_index].building = building
                return True
            else:
                return False
        else:
            return False
        
        
    # Is the given vertex_index a valid place for a settlement
    def is_valid_settle_spot(self, vertex_index):
        vertex = self.vertices[vertex_index]
        # check if city or settlement is there already:
        if vertex.building != Building.none:
            return False
        # check if city or settlement is one vertex away (see catan rules for more info)
        for neighbor_vertex_index in VERTEX_ADJACENCY[vertex]:
            if self.vertices[neighbor_vertex_index].building != Building.none:
                return False
        return True
    
    # Is the given edge a valid place for a player to place a road
    # Is the given vertex_index a valid place for a settlement
    def is_valid_road_spot(self, vertex_index):
        pass

    # start turn: roll die/distribute resources
    def start_turn(self, player):
        """
        - Turn for whichever player's turn it is
        - Roll dice and distribute resources
        - Option to trade resources with other players or maritime trade
        - Option to build roads, settlements or cities and/or buy development cards
        - Option to play one development card at any time during turn
        """
        # Roll dice first
        die1 = random.randint(1,6)
        die2 = random.randint(1,6)
        roll = die1, die2

        # Distribute resources
        for player in self.players:
            pass



    # trading

    # adding/removing cards from hand -> maybe move to Player class
    def add_resources(self, player, resources: list[Resource]):
        drawn_cards = self.draw_resources(resources)
        for card in drawn_cards:
            player.resources.append(card)


    def draw_resources(self, resources: list[Resource]) -> list[Card]:
        hand = []
        for resource in resources:
            if len(self.resource_bank[resource.value]) > 0:
                hand.append(self.resource_bank[resource.value].pop())
        return hand
            

    def draw_development_card(self, player, card):
        if len(self.development_cards) > 0:
            player.development_cards.append(self.development_cards.pop())
        else:
            return None
        

    def remove_resources(self, player, resources: list[Resource]):
        for resource in resources:
            pass
    # check winning conditions



