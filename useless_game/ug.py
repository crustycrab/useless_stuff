from pyglet.gl import *
import res
from graphics import SmoothCircle, Stars
from player import Player


config = pyglet.gl.Config(double_buffer=True)
window = pyglet.window.Window(res.WIN_W, res.WIN_H, config=config)
fps_display = pyglet.clock.ClockDisplay()

radius = int((res.HALF_WIN_W**2 + res.HALF_WIN_H**2)**0.5)

background = SmoothCircle((0.2, 0.2, 0.4, 1.0), (0.0, 0.0, 0.0, 1.0), radius * 2, 10)
core       = SmoothCircle((0.0, 0.0, 0.0, 0.0), (0.4, 0.4, 0.4, 1.0), 80, 5)
stars      = Stars(radius)

main_batch = main_batch = pyglet.graphics.Batch()

player = Player(x=res.HALF_WIN_W, y=res.HALF_WIN_H, batch=main_batch)

@window.event
def on_draw():
	window.clear()
	background.draw()
	stars.draw()
	core.draw()
	main_batch.draw()
	# fps_display.draw()

def update(dt):
	background.update(dt)
	stars.update(dt)
	core.update(dt)
	player.update(dt)

def gl_init():
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	glEnable(GL_BLEND)

if __name__ == '__main__':
	gl_init()
	pyglet.clock.schedule_interval(update, 1 / 60.0)
	pyglet.app.run()