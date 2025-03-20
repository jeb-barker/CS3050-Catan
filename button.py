import math

class Button:
    """
    Class to represent a button with either a point-radius (circle) or a bounding box (rectangle)
    """
    def __init__(self, is_circle: bool, center: tuple[int,int], radius=0, width=0, height=0):
        self.is_circle = is_circle
        self.center = center
        # if the button is a circle...
        if is_circle:
            self.radius = radius
        else:
            # set bounding box based on width, height, and center
            self.top_left = (center[0] - width/2, center[1] - height/2)
            self.bottom_right = (center[0] + width/2, center[1] + height/2)
    
    def contains(self, point: tuple[int,int]) -> bool:
        x = point[0]
        y = point[1]
        if self.is_circle:
            # pythagorean distance between the two points
            distance = math.sqrt((self.center[0] - x)**2 + (self.center[1] - y)**2)
            # a point is within the circle if it is less than a radius away from the center
            return distance < self.radius
        else:
            # return whether the point is within the bounding box
            return self.top_left[0] < x and self.bottom_right[0] < x and self.top_left[1] > y and self.bottom_right[1] < y
