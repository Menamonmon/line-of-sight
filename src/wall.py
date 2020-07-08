from ray import *
from numpy import linalg, array

def collision_from_line(line1, line2):
    if line1 == line2:
        return consts.INF
    elif line1[0] == line2[0]:
        return consts.NOSOL
    
    A = array([
        [line1[0], -1],
        [line2[0], -1]
    ])
    b = array([
        [-line1[1]],
        [-line2[1]]
    ])
    full = linalg.solve(A, b)
    solx, soly = full[0][0], full[1][0]
    return solx, soly

def point_lies_on_line(sx, sy, ex, ey, x, y):
    return (sx <= x <= ex) and (sy <= y <= ey)

class Wall:

    def __init__(self, sx, sy, ex, ey, color=consts.GREY, width=1):
        self.start = sx, sy
        self.end = ex, ey
        self.color = color
        self.width = width

    def draw(self, surface):
        pygame.draw.aaline(surface, self.color, self.start, self.end, self.width)

    def equation(self):
        m = (self.start[1] - self.end[1]) / (self.start[0] - self.end[0])
        b = self.start[1] - (m * self.start[0])
        return m, b

    def collides(self, ray):
        x1, y1 = self.start
        x2, y2 = self.end
        x3, y3 = ray.start
        x4, y4 = ray.end

        left_side = 90 <= mt.degrees(ray.dir) <= 270 

        den = ((x1 - x2) * (y3 - y4)) - ((y1 - y2) * (x3 - x4))
        if den == 0:
            return

        t = (((x1 - x3) * (y3 - y4)) - ((y1 - y3) * (x3 - x4))) / den
        u = - (((x1 - x2) * (y1 - y3)) - ((y1 - y2) * (x1 - x3))) / den
        if 0 <= t <= 1 and ((left_side and u <= 0) or (not left_side and u >= 0)):
            return x1 + (t * (x2 - x1)), y1 + (t * (y2 - y1))

    def _intersects(self, other_wall):
        x1, y1 = self.start
        x2, y2 = self.end
        x3, y3 = other_wall.start
        x4, y4 = other_wall.end

        den = ((x1 - x2) * (y3 - y4)) - ((y1 - y2) * (x3 - x4))
        if den == 0:
            return

        t = (((x1 - x3) * (y3 - y4)) - ((y1 - y3) * (x3 - x4))) / den
        u = - (((x1 - x2) * (y1 - y3)) - ((y1 - y2) * (x1 - x3))) / den
        if 0 <= t <= 1 and 0 <= u <= 1:
            return x1 + (t * (x2 - x1)), y1 + (t * (y2 - y1))
    
    def get_intersections(self, other_walls):
        intersections = []
        for wall in other_walls:
            i = self._intersects(wall)
            if i != None:
                intersections.append(i)

        return intersections

        

def test():
    wall = Wall(3, 6, 6, 4)
    ray = Ray(2, 0, 70)
    print(wall.collides(ray))

if __name__ == "__main__":
    test()