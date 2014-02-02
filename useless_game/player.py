import pyglet
import res

class Player(pyglet.sprite.Sprite):

	def __init__(self, *args, **kwargs):
		super(Player, self).__init__(img=res.player, *args, **kwargs)

	def update(self, dt):
		pass