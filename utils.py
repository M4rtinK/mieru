"""various miscellaneous utility functions for Mieru"""

class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def add(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __str__(self):
        print "(%d, %d)" % (self.x, self.y)