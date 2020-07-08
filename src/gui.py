# for recovery

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


0.0
3.6
7.2
10.8
14.4
18.0
21.6
25.2
28.8
32.4
36.0
39.6
43.2
46.800000000000004
50.4
54.0
57.6
61.20000000000001
64.8
68.4
72.0
75.60000000000001
79.2
82.8
86.4
90.0
93.60000000000001
97.2
100.8
104.4
108.0
111.60000000000001
115.2
118.79999999999998
122.40000000000002
126.0
129.6
133.20000000000002
136.8
140.4
144.0
147.6
151.20000000000002
154.8
158.4
162.0
165.6
169.20000000000002
172.8
176.4
180.0



183.6
187.20000000000002
190.8
194.4
198.0
201.6
205.20000000000002
208.8
212.4
216.0
219.6
223.20000000000002
226.8
230.4
234.0
237.59999999999997
241.20000000000002
244.80000000000004
248.4
252.0
255.59999999999997
259.2
262.8
266.40000000000003
270.0
273.6
277.2
280.8
284.40000000000003
288.0
291.6
295.2
298.8
302.40000000000003
306.0
309.6
313.2
316.8
320.40000000000003
324.0
327.6
331.2
334.8
338.40000000000003
342.0
345.6
349.2
352.8
356.40000000000003