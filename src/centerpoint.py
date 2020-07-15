from wall import *
import time
from pygame import gfxdraw as gfx

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
        q1 = [ray for ray in self.rays if 270 <= mt.degrees(ray.dir) <= 360]
        q2 = [ray for ray in self.rays if 0 <= mt.degrees(ray.dir) <= 90]
        q3 = [ray for ray in self.rays if 180 <= mt.degrees(ray.dir) <= 270]
        q4 = [ray for ray in self.rays if 90 <= mt.degrees(ray.dir) <= 180]
        k = lambda x: x.dir
        q1 = sorted(q1, key=k) 
        q2 = sorted(q2, key=k) 
        q3 = sorted(q3, key=k) 
        q4 = sorted(q4, key=k) 
        q3.reverse(); q4.reverse()
        self.rays = q1 + q2 + q3 + q4

    def _filter_rays(self, rays, dist_limit=3):
        for ray in rays:
            for other in rays:
                if ray == other or (not (ray.intersection_pt or other.intersection_pt)):
                    continue
                # assert ray.intersection_pt and other.intersection_pt
                try:
                    distance = dist(ray.intersection_pt, other.intersection_pt)
                except:
                    continue
                if distance == 0:
                    rays.remove(other)

        return rays

    def show(self, walls, triangles=True, rays=False):
        self.surface.fill(consts.WHITE)
        # calculted the rays to the verticies of all the walls
        if self.autocp:
            for wall in walls:
                self._calc_rays_to_edges(wall, walls)

        # updating the intersection_pt attribute for the rays and drawing them if the option is activated
        for ray in self.rays:
            ray.check_intersections(walls)

        
        # sorts and filters the similar rays
        self._sort_rays()
        # print("Original Num of Rays is ", len(self.rays))
        self.rays = self._filter_rays(self.rays)
        # print("New Num of Rays is ", len(self.rays)) 
        self._sort_rays()

        if rays:
            for ray in self.rays:
                ray.draw(self.surface)
        

        if triangles:
            # drawing the triangles
            if len(self.rays):
                for i in range(len(self.rays) - 1):
                    r1, r2 = self.rays[i], self.rays[i+1]
                    pt_list = (self.pos, r1.intersection_pt, r2.intersection_pt)
                    if None in pt_list:
                        self.surface.fill(consts.WHITE)
                        continue
                    gfx.aapolygon(self.surface, pt_list, consts.LIGHT_RED)
                gfx.aapolygon(self.surface, 
                (
                    self.pos,
                    self.rays[0].intersection_pt,
                    self.rays[-1].intersection_pt 
                ), consts.LIGHT_BLUE)
                pygame.display.update()
            
        if self.autocp:
            self.rays = []


        pygame.draw.circle(self.surface, self.color, self.pos, self.rad)