"""represents a button. 
offers basic functionality for checking if points are within the bounds."""
import math
import pyglet

class Button:
    """
    Class to represent a button with either a point-radius (circle) or a bounding box (rectangle)
    """
    def __init__(self, is_circle: bool, center: tuple[int,int], radius=0, width=0, height=0, id=-1):
        self.is_circle = is_circle
        self.center = center
        # if the button is a circle...
        if is_circle:
            self.radius = radius
        else:
            # set bounding box based on width, height, and center
            self.top_left = (center[0] - width/2, center[1] - height/2)
            self.bottom_right = (center[0] + width/2, center[1] + height/2)
            self.rect = pyglet.shapes.Rectangle(self.top_left[0], self.top_left[1], width, height, color=(255, 0, 0))

    def contains(self, point: tuple[int,int]) -> bool:
        """returns True if the given tuple is within the bounds of the button 
        (either point-radius or bounding box)"""
        x = point[0]
        y = point[1]
        if self.is_circle:
            # pythagorean distance between the two points
            distance = math.sqrt((self.center[0] - x)**2 + (self.center[1] - y)**2)
            # a point is within the circle if it is less than a radius away from the center
            return distance < self.radius

        # return whether the point is within the bounding box
        x_within = self.top_left[0] < x and self.bottom_right[0] > x
        y_within = self.top_left[1] > y and self.bottom_right[1] < y
        return x_within and y_within
    
    def draw(self):
        self.rect.draw()
