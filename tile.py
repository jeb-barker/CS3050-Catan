import pyglet
from pyglet.gl import *
import math

class Tile:
    """
    coords (axial coordinate of the Tile in the board)
    neighbors (int[] contains ids of neighboring Hexagons)
    genNum (int the dice roll that causes this to generate resources)
    resource (the resource (i.e. sheep, wheat, ore, brick, wood) that this tile generates)
    resourceTexture (the image shown on the tile)
    vertices (int[] contains ids of the vertices on this hexagon)
    edges (int[] the index in the edges array)
    """
    def __init__(self, coords, vertices=[], edges=[], genNum= -1, resource="", resourceTexture= ""):
        # Ensure that given coordinate is within the catan board.
        assert abs(coords.x + coords.y) <= 2
        
        self.coords = coords
        self.neighbors = get_neighbors_from_coordinate(coords)
        self.vertices = vertices
        self.edges = edges
        self.genNum = genNum
        self.resource = resource
        self.resourceTexture = resourceTexture
    
    # Returns a list of vertices in a hexagon
    def create_hexagon(self, x, y, size):
        return [(x + size * math.cos(math.radians(60 * i)), 
                y + size * math.sin(math.radians(60 * i))) for i in range(6)]
    
    # TODO: move rendering functions to another file
    # returns a pyglet Polygon
    def draw_tile(self, x, y, radius) -> pyglet.shapes.Polygon:
        hexagon = pyglet.shapes.Polygon(*self.create_hexagon(x, y, radius), color=(0, 255, 0))
        hexagon.draw()
    
# returns the neighbors of an axial coordinate that are within the catan board (hexagonal grid with radius 2).
def get_neighbors_from_coordinate(coords: tuple[int,int]) -> list[tuple[int,int]]:
    neighbors = []
    # left, up-left, up-right, right, down-right, down-left
    directions = [(-1, 0), (0, -1), (1, -1), (1, 0), (0, 1), (-1, 1)]
    for direction in directions:
        neighbor_x = coords.x + directions.x
        neighbor_y = coords.y + directions.y
        # if the new coordinate is within the hexagonal grid...
        if abs(neighbor_x + neighbor_y) <= 2:
            # add the new coordinates to neighbors
            neighbors.append((neighbor_x, neighbor_y))