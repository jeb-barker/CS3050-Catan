import pyglet
from pyglet.gl import *
import math

class Tile:
    """
    index (int index in the tile array)
    neighbors (int[] contains ids of neighboring Hexagons)
    genNum (int the dice roll that causes this to generate resources)
    resource (the resource (i.e. sheep, wheat, ore, brick, wood) that this tile generates)
    resourceTexture (the image shown on the tile)
    vertices (int[] contains ids of the vertices on this hexagon)
    edges (int[] the index in the edges array)
    """
    def __init__(self, index= -1, neighbors=[], vertices=[], edges=[], genNum= -1, resource="", resourceTexture= ""):
        self.index = index
        self.neighbors = neighbors
        self.vertices = vertices
        self.edges = edges
        self.genNum = genNum
        self.resource = resource
        self.resourceTexture = resourceTexture
    
    # Returns a list of vertices in a hexagon
    def create_hexagon(self, x, y, size):
        return [(x + size * math.cos(math.radians(60 * i)), 
                y + size * math.sin(math.radians(60 * i))) for i in range(6)]
    
    # returns a pyglet Polygon
    def draw_tile(self, x, y, radius) -> pyglet.shapes.Polygon:
        hexagon = pyglet.shapes.Polygon(*self.create_hexagon(x, y, radius), color=(0, 255, 0))
        hexagon.draw()
    

