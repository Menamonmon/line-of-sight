import pygame
import math as mt
import consts

class Ray:

    def __init__(self, sx, sy, direction, color=consts.WHITE, width=1):
        self.start = sx, sy
        self.dir = mt.radians(direction)
        self.color = color
        self.width = width

    @property
    def end(self):
        return self.__make_other_point(self.start, self.dir)

    def __make_other_point(self, o, theta):
        x, y = o
        dist = 5
        side1 = mt.sin(theta) * dist
        side2 = mt.sqrt((dist ** 2) - (side1 ** 2))
        nx, ny = x + side2, y + side1
        return nx, ny

    def equation(self):
        x1, y1 = self.start
        x2, y2 = self.__make_other_point(self.start)
        m = (y2 - y1) / (x2 - x1)
        b = y1 - (m * x1)
        return m, b

    def __dist(self, p1, p2):
        xdiff = (p1[0] - p2[0]) ** 2
        ydiff = (p1[1] - p2[1]) ** 2
        return mt.sqrt(xdiff + ydiff)

    def draw(self, surface, walls, update=False):
        colliding_walls = [(wall, wall.collides(self)) for wall in walls if wall.collides(self) is not None]
        if not len(colliding_walls):
            return
        if colliding_walls.count(None):
            return
        try:        
            colliding_walls = sorted(colliding_walls, key=lambda x: self.__dist(self.start, x[1]))
            colliding_point = colliding_walls[0][1]
            colliding_point = tuple(map(int, colliding_point))
            l = pygame.draw.line(surface, self.color, self.start, colliding_point, self.width)
            # c = pygame.draw.circle(surface, self.color, colliding_point, 5)
            if update:
                pygame.display.update(l)
                # pygame.display.update(c)

        except TypeError:
            print(f'The ray with the direction {mt.degrees(self.dir)} cannot be displayed.')

    