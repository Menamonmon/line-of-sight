import pygame
import math as mt
import consts

def dist(p1, p2):
    xdiff = (p1[0] - p2[0]) ** 2
    ydiff = (p1[1] - p2[1]) ** 2
    return mt.sqrt(xdiff + ydiff)
class Ray:

    def __init__(self, sx, sy, direction, color=consts.RED, width=1):
        self.start = [sx, sy]
        self.dir = direction
        self.color = color
        self.width = width
        self.intersection_pt = None

    @property
    def end(self):
        return self.__make_other_point(self.start, self.dir)

    @property
    def intersection_pt(self):
        return self._intersection_pt

    @intersection_pt.setter
    def intersection_pt(self, new):
        self._intersection_pt = new

    def check_intersections(self, walls):
        colliding_walls = []
        for wall in walls:
            collision = wall.collides(self)
            if collision:
                colliding_walls.append(collision)

        if not len(colliding_walls) or None in colliding_walls:
            self.intersection_pt = None
            return

        colliding_walls = sorted(colliding_walls, key=lambda x: dist(self.start, x))
        colliding_point = colliding_walls[0]
        colliding_point = tuple(map(int, colliding_point))
        self.intersection_pt = colliding_point


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

    def draw(self, surface, update=False, show_collide_pt=False):
        if not self.intersection_pt:
            return
        l = pygame.draw.aaline(surface, self.color, self.start, self.intersection_pt, self.width)
        if show_collide_pt:
            c = pygame.draw.circle(surface, self.color, self.intersection_pt, 3)
        if update:
            pygame.display.update(l)
            if show_collide_pt:
                pygame.display.update(c)
    