from enum import Enum

# Values are placeholder for now, they should eventually be a reference to card textures.
class Card(Enum):
    # resource cards
    ore = 0
    wheat = 1
    sheep = 2
    brick = 3
    wood = 4
    # development cards
    knight = 5
    victory_point = 6
    road_building = 7
    year_of_plenty = 8
    monopoly = 9

# Values are placeholder for now, they should eventually be a reference to a resource hex texture.
class Resource(Enum):
    ore = 0
    wheat = 1
    sheep = 2
    brick = 3
    wood = 4
    desert = 5
