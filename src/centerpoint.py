from wall import *
import time

def angle_between(o, pt):
    y, x = pt[1] - o[1], pt[0] - o[0]
    on_right = pt[0] > o[0]
    s = -1 if not on_right else 1
    rads = mt.atan2(s * y, x)
    rads %= 2  * mt.pi
    return rads

class Center:

    def __init__(self, surface, pos, ray_count=100, autocp=True, rad=5, color=consts.BLUE):
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
    def flat_rays(self):
        if isinstance(self.rays[0], tuple) or isinstance(self.rays[0], list):
            return sum(self.rays, [])
        return self.rays

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, pos):
        self._pos = pos
        for ray in self.rays:
            ray.start = self.pos

    def _calc_rays_to_edges(self, wall, walls):
        s, e = wall.start, wall.end
        sa, ea = angle_between(self.pos, s), angle_between(self.pos, e)
        s_angles = [sa + .001, sa, sa - .001]
        e_angles = [ea + .001, ea, ea - .001]
        s_r, e_r = [Ray(*self.pos, angle) for angle in s_angles], [Ray(*self.pos, angle) for angle in e_angles] 
        intersections = wall.get_intersections(walls)
        i_r = []
        if intersections:
            i_r = [Ray(*self.pos, angle_between(self.pos, pt)) for pt in intersections]
        self.rays += s_r + e_r + i_r
        return s_r, e_r

    def _sort_rays(self):
        q1 = [ray for ray in self.flat_rays if 270 <= mt.degrees(ray.dir) <= 360]
        q2 = [ray for ray in self.flat_rays if 0 <= mt.degrees(ray.dir) <= 90]
        q3 = [ray for ray in self.flat_rays if 180 <= mt.degrees(ray.dir) <= 270]
        q4 = [ray for ray in self.flat_rays if 90 <= mt.degrees(ray.dir) <= 180]
        k = lambda x: x.dir
        q1 = sorted(q1, key=k) 
        q2 = sorted(q2, key=k) 
        q3 = sorted(q3, key=k) 
        q4 = sorted(q4, key=k) 
        q3.reverse(); q4.reverse()
        self.rays = q1 + q2 + q3 + q4

    def _pts_meeting_corner(self, pt1, pt2):
        max_side = self.suface.get_height()
        
    
    def show(self, walls):
        if self.autocp:
            for wall in walls:
                self._calc_rays_to_edges(wall, walls)

        self._sort_rays()
        verticies = []
        for ray in self.rays:
            end_vertex = ray.draw(self.surface, walls, only_endpt=True) 
            if self.autocp:
                verticies.append(end_vertex)

        
        if self.autocp:
            rects = []
            self.rays = []

            for i in range(len(verticies) - 1):
                ends = verticies[i], verticies[i + 1], self.pos
                if not None in ends:
                    pygame.draw.polygon(self.surface, consts.LIGHT_RED, ends)

            # filling the last triangle
            if len(verticies):
                ends = (self.pos, verticies[0], verticies[-1])
                if None not in ends:
                    # if len(self.rays) and not self._are_ends_encompassing(self.rays):

                    pygame.draw.polygon(self.surface, consts.LIGHT_RED, ends)

        pygame.draw.circle(self.surface, self.color, self.pos, self.rad)