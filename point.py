class Point:
    """
    A 2d vector for an easy lookup of the obstacles
    """
    def __init__(self, x = 0, y = 0, obstacle = None):
        self.x = x
        self.y = y
        self.obstacle = obstacle
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y 

    def __lt__(self, other):
        """
        Comparison follows the documented rules:
        - compare the x's
        - if the x's are equal, compare the y's
        """
        if self.x == other.x:
            return self.y < other.y
        else:
            return self.x < other.x
    
    def __repr__(self):
        return f"({self.x, self.y})"