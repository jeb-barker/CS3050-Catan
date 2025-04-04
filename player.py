"""Class that represents a player in the Catan game"""
import copy

from texture_enums import Resource

class Player:
    """
    player_id: unique int
    color: unique color
    resource_cards: list of resource cards
    dev_cards: list of development cards
    """
    def __init__(self, player_id, color):
        self.player_id = player_id
        self.color = color
        self.resources = []
        self.dev_cards = []
        self.vps = 0
        self.numRoads = 15
        self.numCities = 4
        self.numSettlements = 5

    def has_resources(self, resources: list[Resource]):
        """Returns true if the player has the resources in the quantities supplied"""
        availible = copy.deepcopy(self.resources)
        for resource in resources:
            if resource in availible:
                availible.remove(resource)
            else:
                return False
 
        return True

    def remove_resource(self, resource):
        """Removes an instance of a resource from the player's hand if available."""
        if resource in self.resources:
            self.resources.remove(resource)
            return True
        return False
