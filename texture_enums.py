"""Enums used throughout the project"""
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
    road_building = 6
    year_of_plenty = 7
    monopoly = 8
    # single victory point cards
    library = 9
    market = 10
    chapel = 11
    university = 12
    palace = 13
    # double victory point cards
    longest_road = 14
    largest_army = 15


# Values are placeholder for now, they should eventually be a reference to a resource hex texture.
class Resource(Enum):
    ore = 0
    wheat = 1
    sheep = 2
    brick = 3
    wood = 4
    desert = 5

class Color(Enum):
    red = (176, 51, 47)
    green = (63, 101, 33)
    blue = (52, 92, 143)
    black = (0, 0, 0)
    white = (255, 255, 255)
    grey = (128, 128, 128)
