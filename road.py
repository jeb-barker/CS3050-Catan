"""Class representing a road as two vertices and an owner"""
class Road:
    """
    owner: Player that placed the road
    vertex1: vertex on one end of road
    vertex2: vertex on other end of road
    """
    def __init__(self, owner, vertex1, vertex2):
        self.owner = owner
        self.vertex1 = vertex1
        self.vertex2 = vertex2
