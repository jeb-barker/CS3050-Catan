'''

'''

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
    def __intit__(index=-1: int, neighbors=[]: List[int], vertices=[]: List[int], edges=[]: List[int], genNum=-1: int, resource: Resource, resourceTexture="": string):
        this.index = index
        this.neighbors = neighbors
        this.vertices = vertices
        this.edges = edges
        this.genNum = genNum
        this.resource = resource
        this.resourceTexture = resourceTexture