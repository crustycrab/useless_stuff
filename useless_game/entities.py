import pygame
import res


class Enity(pyglet.sprite.Sprite):

    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(img=res.player, *args, **kwargs)
