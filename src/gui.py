from grid import *
import time

pygame.font.init()

def replace_color(image, old, new):
	w, h = image.get_size()
	dr, dg, db = old
	r, g, b = new
	for x in range(w):
		for y in range(h):
			cr, cg, cb, a = image.get_at((x, y))
			if (cr, cg, cb) == old:
				image.set_at((x, y), (r, g, b, a))

class PygameWidget:

	def __init__(self, pos, width, height, color):
		self.pos = pos
		self.width, self.height = width, height
		self.color = color
		self.click_time = None
	
	def place(self, surf):
		pass

	def get_clicked(self, btn=0):
		# this checks whether there is a time difference 
		# between the last time the button was clicked and the current time
		if self.click_time != None:
			if abs(self.click_time - time.time()) < .4:
				return False
		if not pygame.mouse.get_pressed()[btn]:
			return False
		p = pygame.mouse.get_pos()
		if self.pos[0] <= p[0] <= self.pos[0] + self.width and self.pos[1] <= p[1] <= self.pos[1] + self.height:
			self.click_time = time.time()
			return True


class PygameButton(PygameWidget):

	def __init__(self, pos, text, color=consts.BLUE, font_color=consts.WHITE, width=100, height=25):
		super().__init__(pos, width, height, color)
		self.text = text
		self.color = color
		self.font_color = font_color
		font_size = int(self.height / 2)
		self.font = pygame.font.Font('./../fonts/Candara.ttf', font_size)
		self.command = None
		self.command_args = None

	def place(self, surf):
		pygame.draw.rect(surf, self.color, pygame.Rect(self.pos, (self.width, self.height)))
		font_surf = self.render_text()
		y_padding = int((self.height - font_surf.get_height()) / 2)
		x_padding = int((self.width - font_surf.get_width()) / 2)
		font_pos = (self.pos[0] + x_padding, self.pos[1] + y_padding)
		surf.blit(font_surf, font_pos)

	def render_text(self):
		font_surface = self.font.render(self.text, True, self.font_color)
		return font_surface


class PygameCheckBtn(PygameWidget):

	def __init__(self, pos, size=50, color=consts.LIGHT_BLUE):
		super().__init__(pos, size, size, color)
		self.chosen = True
		self.load_images()

	def load_images(self):
		self.checked_image = pygame.image.load('./../images/checkbtn/1.png')
		self.unchecked_image = pygame.image.load('./../images/checkbtn/0.png')
		self.checked_image = pygame.transform.scale(self.checked_image, (self.width, self.height))
		self.unchecked_image = pygame.transform.scale(self.unchecked_image, (self.width, self.height))
		replace_color(self.checked_image, consts.BLACK, self.color)
		replace_color(self.unchecked_image, consts.BLACK, self.color)

	def place(self, surf):
		img = self.checked_image if self.chosen else self.unchecked_image
		surf.blit(img, self.pos)

	def check(self):
		self.chosen = True

	def uncheck(self):
		self.chosen = False

	def reverse(self):
		self.chosen = not self.chosen
		

class PygameScrollBar(PygameWidget):

	class Slider:

		def __init__(self, pos, color, rad, val=0):
			self.pos = pos
			self.color = color
			self.rad = rad
			self.val = val

		def draw(self, surf):
			pygame.draw.circle(surf, self.color, self.pos + (self.rad * self.val), self.rad)

	def __init__(self, pos, length=100, _min=0, _max=10, color1=consts.BLACK, color2=consts.RED):
		self.min, self.max = _min, _max
		diff = abs(self.max - self.min)
		self.rad = int(length/(diff * 2))
		super().__init__(pos, length, self.rad * 2, color1)
		self.slider = PygameScrollBar.Slider((self.pos[0], self.pos[1] + self.rad), color2, self.rad, self.min)

	def place(self, surf):
		l_start = (self.pos[0], self.pos[1] + self.rad)
		l_end = (self.pos[0] + self.width, self.pos[1] + self.rad)
		pygame.draw.line(surf, self.color, l_start, l_end, 5)
		self.slider.draw(surf)

	def increase(self):
		self.slider.val += 1

def test_button():
	surf = pygame.display.set_mode((600, 600))
	btn = PygameButton((100, 100), "Click Me")
	checkbtn = PygameCheckBtn((150, 150))

	bar = PygameScrollBar((100, 150))

	while True:
		event = pygame.event.poll()
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()
		elif event.type == pygame.KEYDOWN:
			bar.increase()
		if checkbtn.get_clicked():
			checkbtn.reverse()
		

		surf.fill(consts.WHITE)
		bar.place(surf)
		btn.place(surf)
		checkbtn.place(surf)
		pygame.display.update()
	
if __name__ == "__main__":
	test_button()
	