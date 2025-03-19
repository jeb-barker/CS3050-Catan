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
        self.resource_cards = []
        self.dev_cards = []

   def has_resources(self, type, quantity):
       pass
