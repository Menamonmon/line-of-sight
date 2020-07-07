from wall import *
import time

def calc_dir(p1, p2):
    hyp = dist(p1, p2)
    xdiff = abs(p1[0] - p2[0])
    theta = mt.acos(xdiff/hyp)
    return theta 
class Center:

    def __init__(self, surface, pos, ray_count=100, autocp=True, rad=25, color=consts.BLUE):
        self.surface = surface
        self._pos = pos
        self.autocp = autocp
        if not self.autocp:
            dir_diff = 360 / ray_count
            self.rays = [Ray(*self.pos, mt.radians(dir_diff * ray)) for ray in range(ray_count)]
        else:
            self.rays = []
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

    def _calc_rays_to_edges(self, walls):
        # take the vertices of the walls and add then to the list pts
        pts = []
        for wall in walls:
            pts.append(wall.start)
            pts.append(wall.end)

        # delete repeated points 
        pts = set(pts)

        # loops throught the pts and calculates the angle between the origin (self.pos) and the vertex (pt)

        def right_from_origin(o, p):
            return p[0] > o[0]

        angles = []
        for pt in pts:
            sign = -1 if not right_from_origin(self.pos, pt) else 1
            angle = mt.atan2(sign * (pt[1] - self.pos[1]), pt[0] - self.pos[0])
            angle %= 2*mt.pi
            angles += [angle+.001, angle, angle-.001]
        self.rays = [Ray(*self.pos, angle) for angle in angles]

    def show(self, walls):
        if self.autocp:
            self._calc_rays_to_edges(walls)
        for ray in self.rays:
            ray.draw(self.surface, walls)
        if self.autocp:
            self.rays = []

        pygame.draw.circle(self.surface, self.color, self.pos, self.rad)