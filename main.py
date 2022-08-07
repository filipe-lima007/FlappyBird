import pygame
import os
import random

SCREEN_W = 500
SCREEN_H = 800

C_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
G_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
BG_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
B_IMAGES = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png')))
]

pygame.font.init()
SCORE_SOURCE = pygame.font.SysFont('arial', 50)


class Bird:
    IMGS = B_IMAGES
    # Rotation animations
    MAX_ROTATION = 25
    SPEED_ROTATION = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.height = self.y
        self.time = 0
        self.image_cont = 0
        self.image = self.IMGS[0]

    def jump(self):
        self.speed = -10.5
        self.time = 0
        self.height = self.y

    def move(self):
        self.time += 1
        distance = 1.5*(self.time**2)+self.speed*self.time
        if distance > 16:
            distance = 16
        elif distance < 0:
            distance -= 2
        self.y += distance
        if distance < 0 or self.y < (self.height + 50):
            if self.angle < self.MAX_ROTATION:
                self.angle = self.MAX_ROTATION
        elif self.angle < -90:
            self.angle -= self.SPEED_ROTATION

    def drawn(self):
        self.image_cont += 1
        if self.image_cont < self.ANIMATION_TIME:
            self.image = self.IMGS[0]
        elif self.image_cont < self.ANIMATION_TIME*2:
            self.image = self.IMGS[1]
        elif self.image_cont < self.ANIMATION_TIME*3:
            self.image = self.IMGS[2]
        elif self.image_cont < self.ANIMATION_TIME*4:
            self.image = self.IMGS[1]
        elif self.image_cont >= self.ANIMATION_TIME*4+1:
            self.image = self.IMGS[0]
            self.image_cont = 0


class Cano():
    pass


class Ground():
    pass
