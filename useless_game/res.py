import pyglet

WIN_W = 800
WIN_H = 600

HALF_WIN_W = WIN_W // 2
HALF_WIN_H = WIN_H // 2

def center_image(image):
    image.anchor_x = image.width/2
    image.anchor_y = image.height/2

pyglet.resource.path = ['resources']
pyglet.resource.reindex()

player = pyglet.resource.image("player.png")
center_image(player) 