from pyglet.gl import *
import res
import math
import random


class SmoothCircle:

	def __init__(self, outer_color, inner_color, radius, freq=10):
		self.freq = freq
		self.__up_time = 0

		self.const_o = self.__outer_color = self.__do = Color(outer_color)
		self.const_i = self.__inner_color = self.__di = Color(inner_color)
		self.shuffle_colors()

		self.radius = radius	

	def update(self, dt):
		self.__outer_color += self.__do * dt
		self.__inner_color += self.__di * dt
		if self.__up_time >= self.freq:
			self.__up_time = 0
			self.shuffle_colors()
		self.__up_time += dt

	def shuffle_colors(self):
		self.__do = (self.const_o.shuffle() - self.__outer_color) / self.freq
		self.__di = (self.const_i.shuffle() - self.__inner_color) / self.freq

	def draw(self):
		outer_color = self.__outer_color.raw()
		inner_color = self.__inner_color.raw()

		accuracy = 50
		incr = 2 * math.pi / accuracy

		# glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		# glEnable(GL_BLEND)

		glBegin(GL_TRIANGLE_FAN)

		glColor4f(*inner_color)
		glVertex2i(res.HALF_WIN_W, res.HALF_WIN_H)
		glColor4f(*outer_color)

		for i in range(accuracy):
			angle = incr * i

			x = int(math.cos(angle) * self.radius + res.HALF_WIN_W)
			y = int(math.sin(angle) * self.radius + res.HALF_WIN_H)

			glVertex2i(x, y)

		glVertex2i(self.radius + res.HALF_WIN_W, res.HALF_WIN_H)
		glEnd()


class Stars:

	def __init__(self, radius, num_stars=2048):
		self.__num_stars = num_stars
		self.__radius = radius
		self.__stars = []
		self.gen_stars()

	def draw(self):
		for star in self.__stars:
			x, y = star['cords']
			glPointSize(star['size'])
			glBegin(GL_POINTS)
			glColor3f(*star['color'])
			glVertex2i(x + res.HALF_WIN_W, y + res.HALF_WIN_H)
			glEnd()

	def update(self, dt):
		stars = self.__stars
		for i in range(self.__num_stars):
			x = int(stars[i]['radius'] * math.sin(stars[i]['angle']))
			y = int(stars[i]['radius'] * math.cos(stars[i]['angle']))
			stars[i]['cords'] = (x, y)
			stars[i]['angle'] += (stars[i]['speed'] * dt)

	def gen_stars(self):
		for _ in range(self.__num_stars):
			x, y = self.get_random_cords()
			star = {'speed': math.pi / random.randint(100, 200),
					'cords': (x, y),
					'angle': math.atan2(x, y),
					'radius': math.hypot(x, y),
					'size': random.randint(1, 2),
					'color': (random.uniform(.6, 1),) * 3}
			self.__stars.append(star)

	def get_random_cords(self):
		range_ = (-self.__radius, self.__radius)
		return (random.randint(*range_), random.randint(*range_))

	@property
	def num_stars(self):
		return self.__num_stars

	@num_stars.setter
	def num_stars(self, value):
		self.__num_stars = value
		self.gen_stars()

	@property
	def radius(self):
		return self.__radius

	@radius.setter
	def radius(self, value):
		self.__radius = value
		self.gen_stars()


class Color:

	def __init__(self, color):
		self.r, self.g, self.b, self.a = color

	def __mul__(self, value):
		return Color(tuple(map(lambda x: x * value, (self.r, self.g, self.b))) + (self.a,))

	def __truediv__(self, value):
		return Color(tuple(map(lambda x: x / value, (self.r, self.g, self.b))) + (self.a,))

	def __add__(self, other):
		return Color((self.r + other.r, self.g + other.g, self.b + other.b, self.a))

	def __sub__(self, other):
		return Color((self.r - other.r, self.g - other.g, self.b - other.b, self.a))

	def shuffle(self):
		dr = self.r / 2
		dg = self.g / 2
		db = self.b / 2

		return Color((random.uniform(self.r - dr, self.r + dr),
					  random.uniform(self.g - dg, self.g + dg),
					  random.uniform(self.b - db, self.b + db),
					  self.a))

	def raw(self):
		return (self.r, self.g, self.b, self.a)