from centerpoint import *
from threading import Thread

class Grid:

	def __init__(self, surface):
		self.surface = surface
		self.walls = []
		cen_pos = int(self.surface.get_height()/2), int(self.surface.get_width()/2)
		self.center = Center(self.surface, cen_pos)
		self.making_walls = False
		self.running = True
		self.make_side_walls()
		self.start_update_loop()

	def close(self):
		self.running = False

	def make_side_walls(self):
		upper_wall = Wall(0, 0, self.surface.get_width(), 0)
		lower_wall = Wall(0, self.surface.get_height(), self.surface.get_width(), self.surface.get_height())
		left_wall = Wall(0, 0, 0, self.surface.get_height())
		right_wall = Wall(self.surface.get_width(), 0, self.surface.get_width(), self.surface.get_height())
		self.walls += [upper_wall, lower_wall, left_wall, right_wall]

	def take_wall_posits(self):
		t = Thread(target=self.__take_wall_posits)
		t.start()

	def __take_wall_posits(self):
		self.making_walls = True
		while not pygame.mouse.get_pressed()[0]:
			continue
		start = pygame.mouse.get_pos()
		if not pygame.mouse.get_pressed()[0]:
			return
		while pygame.mouse.get_pressed()[0]:
			pygame.draw.aaline(self.surface, consts.GREY, start, pygame.mouse.get_pos())
		end = pygame.mouse.get_pos()
		self.walls.append(Wall(*start, *end))
		time.sleep(2)
		self.making_walls = False

	def start_update_loop(self):
		update_thread = Thread(target=self.__update)
		update_thread.start()

	def __update(self):
		while self.running:
			while not self.making_walls:
				# continue
				self.center.pos = pygame.mouse.get_pos()

	def draw(self):
		for wall in self.walls:
			wall.draw(self.surface)

		self.center.show(self.walls)
		
def test():
	surface = pygame.display.set_mode((600, 600))
	grid = Grid(surface)
	running = True
	clock = pygame.time.Clock()

	while running:
		e = pygame.event.poll()
		if e.type == pygame.QUIT:
			running = False
			grid.close()
			pygame.quit()
			quit()
		elif e.type == pygame.KEYDOWN:
			if e.key == pygame.K_SPACE:
				grid.take_wall_posits()
			elif e.key == pygame.K_d:
				grid.walls = grid.walls[:4]

		surface.fill(consts.WHITE)
		grid.draw()
		clock.tick(60)
		pygame.display.update()

if __name__ == "__main__":
	test()