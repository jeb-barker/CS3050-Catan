

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

    def add_resource_card(self, type):
        pass

    def remove_resource_card(self, type):
        pass

    def add_development_card(self, type):
        pass

    def remove_development_card(self, type):
        pass
