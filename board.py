'''
Class that represents the board in the Catan game
Handles game logic
'''
import random
from tile import Tile
from texture_enums import Resource, Card, Color
from board_config import VERTEX_ADJACENCY, TILE_ADJACENCY, Building, BUILDING_COSTS
from road import Road
from game_state import GameState
from vertex import Vertex
from player import Player


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
        self.vertices = [Vertex() for _ in range(54)]
        self.roads = []
        self.resource_bank = {} # maps resource enum values (i.e. Resource.wheat) to a list of cards
        self.development_cards = []
        self.game_state = GameState(self.players)

        self.beginner_setup()
        self.die_roll = (1, 1)
        # add a robber_tile field to track where the robber is currently placed
        self.robber_tile = None

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
            self.tiles.append(Tile(coords=tile_coords[i],
                                   gen_num=tile_gen_nums[i],
                                   resource=tile_resources[i]))

        # Set up the resource bank
        for resource in [Resource.brick, Resource.ore,
                         Resource.sheep, Resource.wheat, Resource.wood]:
            # Add 19 of each resource type to the board's bank
            self.resource_bank[resource] = [Card(resource.value) for _ in range(19)]

        # Set the robber up on the desert tile
        for tile in self.tiles:
            if tile.resource == Resource.desert:
                self.robber_tile = tile
                break

        # Initiate 4 players
        # First player is the user
        self.players.append(Player(0, Color.red, True))

        # Player 2-4 are AI
        self.players.append(Player(1, Color.green, False))
        self.players.append(Player(2, Color.blue, False))
        self.players.append(Player(3, Color.black, False))

        # Start game state at "before roll" and user player's turn


    def get_tile_at(self, coords):
        """ Returns the tile at given axial coordinates """
        for tile in self.tiles:
            if tile.coords == coords:
                return tile


    # Place a road, checking if it connects to an existing road, city or settlement
    # owned by that player, that they have roads left and there isn't already
    # a road at specified location
    def place_road(self, owner, vertex_index1, vertex_index2):
        """ Place road between two vertices. Returns true if successful
         and returns false if unable to place road """

        vertex1 = self.vertices[vertex_index1]
        vertex2 = self.vertices[vertex_index2]
        # Check if player has less than 15 roads
        if owner.numRoads == 0:
            return False

        # Check if the player can afford a road
        if not owner.has_resources(BUILDING_COSTS[Building.ROAD]):
            return False

        # Bool indicating whether road is allowed
        allowed = False

        # Check if player has a road or city or settlement there already
        # Check buildings first
        if vertex1.owner == owner or vertex2.owner == owner:
            if vertex1.building == Building.CITY or vertex1.building == Building.SETTLEMENT:
                allowed = True
            elif vertex2.building == Building.CITY or vertex2.building == Building.SETTLEMENT:
                allowed = True

        # Check for adjacent roads
        for road in self.roads:
            if road.owner == owner:
                if road.vertex1 == vertex_index1 or road.vertex2 == vertex_index1:
                    allowed = True
                    break
                elif road.vertex2 == vertex_index1 or road.vertex2 == vertex_index2:
                    allowed = True
                    break

        # check if vertices are adjacent to each other:
        if vertex_index2 not in VERTEX_ADJACENCY[vertex_index1]:
            allowed = False
        if vertex_index1 not in VERTEX_ADJACENCY[vertex_index2]:
            allowed = False
        if vertex_index2 == vertex_index1:
            allowed = False

        # Abort or allow to proceed based on allowed value
        if allowed is False:
            return False

        # Check if road exists between two vertices already
        for road in self.roads:
            if road.vertex1 == vertex_index1 and road.vertex2 == vertex_index2:
                return False
            elif road.vertex1 == vertex_index2 and road.vertex2 == vertex_index1:
                return False
            elif vertex_index1 == vertex_index2:
                return False
            else:
                if vertex_index2 in VERTEX_ADJACENCY[road.vertex1]:
                    self.roads.append(Road(owner=owner,
                                           vertex1=vertex_index1,
                                           vertex2=vertex_index2))
                    self.remove_resources(owner, BUILDING_COSTS[Building.ROAD])
                    owner.numRoads -= 1
                    return True
        self.roads.append(Road(owner=owner, vertex1=vertex_index1, vertex2=vertex_index2))
        self.remove_resources(owner, BUILDING_COSTS[Building.ROAD])
        owner.numRoads -= 1
        return True

    def place_building(self, building, owner, vertex_index):
        """place building at the given vertex_index
           returns False if there's an error or the placement is invalid otherwise, returns True"""
        # Check that player has settlements left in pool
        if building == Building.CITY:
            if owner.numCities == 0:
                return False

        # if the owner can't afford the building, don't let them.
        # special case is during the start phase, when the first 2 settlements are free
        if not owner.has_resources(BUILDING_COSTS[building]):
            return False


        if building == Building.SETTLEMENT:
            if owner.numSettlements == 0:
                return False

        vertex = self.vertices[vertex_index]
        if building == Building.SETTLEMENT:
            if self.is_valid_settle_spot(owner, vertex_index):
                # case if placing a settlement or city
                vertex.owner = owner
                vertex.building = building
                owner.numSettlements -= 1
                # remove the cost of the settlement from the player's hand
                self.remove_resources(owner, BUILDING_COSTS[building])
                # update tags
                self.game_state.tags['settlements_placed_turn'] += 1
                self.game_state.tags['settlements_placed'] += 1
                return True
        elif building == Building.CITY:
            if self.is_valid_city_spot(owner, vertex_index):
                vertex.owner = owner
                vertex.building = building
                owner.numCities -= 1
                # the owner gets the settlement that they upgraded back
                owner.numSettlements += 1
                # remove the cost of the city from the player's hand
                self.remove_resources(owner, BUILDING_COSTS[building])
                return True

        return False


    def is_valid_settle_spot(self, owner, vertex_index):
        """Is the given vertex_index a valid place for a settlement"""
        vertex = self.vertices[vertex_index]
        # check if player can afford a settlement
        if not self.game_state.is_start_phase() and not owner.has_resources(BUILDING_COSTS[Building.SETTLEMENT]):
            return False
        # check if city or settlement is there already:
        if vertex.building != Building.NONE:
            return False
        # check if city or settlement is one vertex away (see catan rules for more info)
        for neighbor_vertex_index in VERTEX_ADJACENCY[vertex_index]:
            if self.vertices[neighbor_vertex_index].building != Building.NONE:
                return False

        # If we are in the start phase, these checks are sufficient
        if self.game_state.is_start_phase():
            return True
        # If we are in the main phase of the game, 
        # Look for a road that starts/stops on the given vertex
        for road in self.roads:
            # if vertex is on the end of a road owned by the given owner, return True
            if vertex_index in [road.vertex1, road.vertex2] and road.owner is owner:
                return True
        return False

    def is_valid_city_spot(self, player, vertex_index):
        """Is the given vertex_index a valid place for a city owned by the given player"""
        vertex = self.vertices[vertex_index]
        # Check if player can afford a city
        if not self.game_state.is_start_phase() and not player.has_resources(BUILDING_COSTS[Building.CITY]):
            return False
        # Cities can only be placed on existing settlements owned by the player
        if vertex.building == Building.SETTLEMENT and vertex.owner == player:
            return True
        return False


    # Is the given edge a valid place for a player to place a road
    # Is the given vertex_index a valid place for a settlement
    def is_valid_road_spot(self, owner, vertex_index1, vertex_index2):
        """TODO: Check if the given vertex is a valid spot for a road. Possibly Duplicate."""
        vertex1 = self.vertices[vertex_index1]
        vertex2 = self.vertices[vertex_index2]
        # Check if player has less than 15 roads
        if owner.numRoads == 0:
            return False
        
        # Check if player has enough to afford a road (in regular phase)
        if not self.game_state.is_start_phase() and not owner.has_resources(BUILDING_COSTS[Building.ROAD]):
            return False

        # Bool indicating whether road is allowed
        allowed = False

        # Check if player has a road or city or settlement there already
        # Check buildings first
        if vertex1.owner == owner or vertex2.owner == owner:
            if vertex1.building == Building.CITY or vertex1.building == Building.SETTLEMENT:
                allowed = True
            elif vertex2.building == Building.CITY or vertex2.building == Building.SETTLEMENT:
                allowed = True

        # Check for adjacent roads
        for road in self.roads:
            if road.owner == owner:
                if road.vertex1 == vertex_index1 or road.vertex2 == vertex_index1:
                    allowed = True
                    break
                elif road.vertex2 == vertex_index1 or road.vertex2 == vertex_index2:
                    allowed = True
                    break

        # check if vertices are adjacent to each other:
        if vertex_index2 not in VERTEX_ADJACENCY[vertex_index1]:
            allowed = False
        if vertex_index1 not in VERTEX_ADJACENCY[vertex_index2]:
            allowed = False
        if vertex_index2 == vertex_index1:
            allowed = False

        # In the start phase...
        # Roads must be adjacent to the settlement placed
        if self.game_state.is_start_phase():
            settle_index = self.game_state.tags['settlement_pos']
            if vertex_index2 != settle_index and vertex_index1 != settle_index:
                allowed = False
            if vertex_index2 == vertex_index1:
                allowed = False

        # Abort or allow to proceed based on allowed value
        if allowed is False:
            return False

        # Check if road exists between two vertices already
        for road in self.roads:
            if road.vertex1 == vertex_index1 and road.vertex2 == vertex_index2:
                return False
            elif road.vertex1 == vertex_index2 and road.vertex2 == vertex_index1:
                return False
            elif vertex_index1 == vertex_index2:
                return False
            else:
                if vertex_index2 in VERTEX_ADJACENCY[road.vertex1]:
                    return True
        return True

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
        roll = die1 + die2
        self.die_roll = (die1, die2)

        # Iterate through tiles
        for i, tile in enumerate(self.tiles):
            # First: Check if tile's gen num matches most recent roll
            if self.tiles[i].gen_num == roll:
                # new_resource_tiles.append(tile)
                for vertex_index in TILE_ADJACENCY[i]:
                    # Next check for players with settlements placed on its nearby vertices
                    vertex = self.vertices[vertex_index]
                    if vertex.building != Building.NONE:
                        # Distribute resources (if not a desert)
                        if tile.resource is not Resource.desert:
                            self.add_resources(vertex.owner, [tile.resource])

        # If roll == 7
        if roll == 7:
            # Each player with more than 7 resources discards half their hand (round down)
            players_to_discard = []
            for player in self.players:
                if len(player.resources) >= 7:
                    players_to_discard.append(player)

            # Discard cards at random
            for player in players_to_discard:
                num_to_discard = len(player.resources) // 2
                indices_to_discard = []
                # Choose random indices in player's hand to discard
                for i in range(num_to_discard):
                    temp = random.randint(0, len(player.resources))
                    while temp in indices_to_discard:
                        temp += 1
                        temp = temp % (len(player.resources) - 1)
                    indices_to_discard.append(temp)
                # Find what resources they are
                resources_to_discard = []
                for index in indices_to_discard:
                    resources_to_discard.append(player.resources[index])
                self.remove_resources(player, resources_to_discard)

        
        # trading

    def add_resources(self, player, resources: list[Resource]):
        """adding/removing cards from hand -> maybe move to Player class"""
        drawn_cards = self.draw_resources(resources)
        for card in drawn_cards:
            player.resources.append(card)


    def draw_resources(self, resources: list[Resource]) -> list[Card]:
        """Draw resources from the bank and return a list of returned resources"""
        hand = []
        for resource in resources:
            if len(self.resource_bank[resource]) > 0:
                hand.append(self.resource_bank[resource].pop())
        return hand


    def draw_development_card(self, player):
        """Draw a development card from the bank and give it to the given player"""
        if len(self.development_cards) > 0:
            player.development_cards.append(self.development_cards.pop())
        else:
            return None


    def remove_resources(self, player, resources: list[Resource]):
        """Remove the given resources from the player's hand. returns truthy value based on success"""
        removed_resources = []
        allowed = True
        for resource in resources:
            if Card(resource.value) in player.resources:
                res_index = player.resources.index(Card(resource.value))
                player.resources.pop(res_index)
                removed_resources.append(Card(resource.value))
            else:
                allowed = False
        if allowed:
            for card in removed_resources:
                self.resource_bank[Resource(card.value)].append(card)
            return True
        else:
            for card in removed_resources:
                player.resources.append(card)
            return False
        
    def get_resources_from_vertex(self, vertex_index):
        """retuns a list of Resources from the surrounding tiles from the vertex"""
        resources = []
        for tile_index, tile in enumerate(self.tiles):
            if vertex_index in TILE_ADJACENCY[tile_index]:
                if tile.resource is not Resource.desert:
                    resources.append(tile.resource)
        return resources

    # check winning conditions

    def calculate_player_longest_road(self, player) -> int:
        """Returns the length of the given player's longest road."""
        player_roads = [road if road.owner == player else None for road in self.roads]
        road_graph = {}
        for road in player_roads:
            if road is not None:
                # ensure vertices are in the graph
                if road.vertex1 not in road_graph.keys():
                    road_graph[road.vertex1] = []
                if road.vertex2 not in road_graph.keys():
                    road_graph[road.vertex2] = []
                # add two edges to make the graph undirected
                road_graph[road.vertex1].append(road.vertex2)
                road_graph[road.vertex2].append(road.vertex1)

        # road_graph is now an adjacency list
        # connecting vertices that have the given player's roads between them.
        # We can perform a search (essentially) on this graph to get the longest path, 
        # and return the length of the longest one.
        def graph_search(graph,curr,visited) -> int:
            # only on the first iteration
            if visited is None: 
                visited = []

            visited.append(curr)

            path_lengths = [0]
            # check if a different player's settlement is built on this vertex.
            if self.vertices[curr].owner not in [player, None]:
                # if it is, then don't traverse and return the length as 0
                return 0

            for neighbor in graph[curr]:
                # check if we've visited the neighbor
                if neighbor not in visited:
                    # add one to represent traversing the graph
                    path_lengths.append(1 + graph_search(graph, neighbor, visited[:]))
            return max(path_lengths)

        road_lengths = [0]
        for vertice in road_graph.keys():
            # for each vertice in the road graph...
            # graph search returns the length of the segment that the given vertice is on
            road_lengths.append(graph_search(road_graph, vertice, None))

        # return the maximum road segment length found
        return max(road_lengths)
