from boundary import *
import time

class Center:

    def __init__(self, surface, pos, ray_count=500, rad=25, color=consts.BLUE):
        self.surface = surface
        self._pos = pos
        dir_diff = 360 / ray_count
        self.rays = [Ray(*self.pos, dir_diff * ray) for ray in range(ray_count)]
        self.rad = rad
        self.color = color

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, pos):
        self._pos = pos
        for ray in self.rays:
            ray.start = self.pos

    def show(self, walls):
        for ray in self.rays:
            ray.draw(self.surface, walls)
        pygame.draw.circle(self.surface, self.color, self.pos, self.rad)
        