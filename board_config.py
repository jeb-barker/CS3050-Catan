"""configuration class containing helpful enums and global variables for the board"""
from enum import Enum
from texture_enums import Resource

# Adjacency List representing vertices and their neighbors
VERTEX_DEFINITION = """
        0 1 2
       3 4 5 6
       7 8 9 10
    11 12 13 14 15
    16 17 18 19 20
  21 22 23 24 25 26
  27 28 29 30 31 32
    33 34 35 36 37
    38 39 40 41 42
      43 44 45 46
      47 48 49 50
       51 52 53
"""

VERTEX_ADJACENCY = [
    [3, 4],        # Row #1
    [4, 5],
    [5, 6],
    [0, 7],     # Row 2
    [0, 1, 8],
    [1, 2,9],
    [2, 10],
    [3, 11, 12],    # Row 3
    [4, 12, 13],
    [5, 13, 14],
    [6, 14, 15],
    [7, 16],  # Row 4
    [7, 8, 17],
    [8, 9, 18],
    [9, 10, 19],
    [10, 20],
    [11, 21, 22], # Row 5
    [12, 22, 23],
    [13, 23, 24],
    [14, 24, 25],
    [15, 25, 26],
    [16, 27], # Row 6
    [16, 17, 28],
    [17, 18, 29],
    [18, 19, 30],
    [19, 20, 31],
    [20, 32],
    [21, 33], # Row 7
    [22, 33, 34],
    [23, 34, 35],
    [24, 35, 36],
    [25, 36, 37],
    [26, 37],
    [27, 28, 38], # Row 8
    [28, 29, 39],
    [29, 30, 40],
    [30, 31, 41],
    [31, 32, 42],
    [33, 43], # Row 9
    [34, 43, 44],
    [35, 44, 45],
    [36, 45, 46],
    [37, 46],
    [38, 39, 47], # Row 10
    [39, 40, 48],
    [40, 41, 49],
    [41, 42, 50],
    [43, 51], # Row 11
    [44, 51, 52],
    [45, 52, 53],
    [46, 53],
    [47, 48],     # Row 12
    [48, 49],
    [49, 50]
]

TILE_ADJACENCY = [
    [0,4,8,12,7,3],
    [1,5,9,13,8,4],
    [2,6,10,14,9,5],
    [7,12,17,22,16,11],
    [8,13,18,23,17,12],
    [9,14,19,24,18,13],
    [10,15,20,25,19,14],
    [16,22,28,33,27,21],
    [17,23,29,34,28,22],
    [18,24,30,35,29,23],
    [19,25,31,36,30,24],
    [20,26,32,37,31,25],
    [28,34,39,43,38,33],
    [29,35,40,44,39,34],
    [30,36,41,45,40,35],
    [31,37,42,46,41,36],
    [39,44,48,51,47,43],
    [40,45,49,52,48,44],
    [41,46,50,53,49,45]
]

class Building(Enum):
    """Enum representing building types"""
    NONE = 0
    SETTLEMENT = 1
    CITY = 2
    ROAD = 3

BUILDING_COSTS = {
    Building.CITY :
        [Resource.wheat, Resource.wheat, Resource.ore, Resource.ore, Resource.ore,], # 2 w, 3 o
    Building.SETTLEMENT :
        [Resource.wheat, Resource.brick, Resource.sheep, Resource.wood], # 1 w, 1 b, 1 s, 1 w
    Building.ROAD : 
        [Resource.wood, Resource.brick] # 1 wood, 1 brick
}
