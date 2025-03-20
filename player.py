from texture_enums import *

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

    # Returns boolean based on if player has certain quantity of a given resource
    def has_resources(self, type, quantity):
        sum = 0
        for i in self.resources:
            if i == type:
                sum += 1

        if sum >= quantity:
            return True
        return False

    def remove_resource(self, resource):
        """Removes an instance of a resource from the player's hand if available."""
        if resource in self.resources:
            self.resources.remove(resource)
            return True
        return False
