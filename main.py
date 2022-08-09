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

    def drawn(self, screen):
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

        if self.angle < -80:
            self.image = self.IMGS[1]
            self.image_cont = self.ANIMATION_TIME*2

        image_rotationed = pygame.transform.rotate(self.image, self.angle)
        image_center_pos = self.image.get_rect(topleft=(self.x, self.y)).center
        rectangle = image_rotationed.get_rect(center=image_center_pos)
        screen.blit(image_rotationed, rectangle.topleft)

    def get_mask(self):
        pygame.mask.from_surface(self.image)


class Cano:
    DISTANCE = 200
    SPEED = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top_pos = 0
        self.base_pos = 0
        self.TOP_CANO = pygame.transform.flip(C_IMAGE, False, True)
        self.BASE_CANO = C_IMAGE
        self.passed = False
        self.define_height()

    def define_height(self):
        self.height = random.randrange(50, 450)
        self.top_pos = self.height - self.TOP_CANO.get_height()
        self.base_pos = self.height + self.DISTANCE

    def move(self):
        self.x -= self.SPEED

    def draw(self, screen):
        screen.blit(self.TOP_CANO, (self.x, self.top_pos))
        screen.blit(self.BASE_CANO, (self.x, self.base_pos))

    def colition(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.TOP_CANO)
        base_mask = pygame.mask.from_surface(self.BASE_CANO)

        top_distance = (self.x - bird.x, self.top_pos - round(bird.y))
        base_distance = (self.x - bird.x, self.base_pos - round(bird.y))

        top_point = bird_mask.overlap(top_mask, top_distance)
        base_point = bird_mask.overlap(base_mask, base_distance)

        if top_point or base_point:
            return True
        else:
            return False


class Ground:
    SPEED = 5
    WIDTH = G_IMAGE.get_width()
    IMAGE = G_IMAGE

    def __init__(self, y):
        self.y = y
        self.x0 = 0
        self.x1 = self.WIDTH

    def move(self):
        self.x0 -= self.SPEED
        self.x1 -= self.SPEED

        if self.x0 + self.WIDTH < 0:
            self.x0 = self.x0 + self.WIDTH
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x1 + self.WIDTH

    def draw(self, screen):
        screen.blit(self.IMAGE, (self.x0, self.y))
        screen.blit(self.IMAGE, (self.x1, self.y))


def draw_screen(screen, birds, canos, ground, points):
    screen.blit(BG_IMAGE, (0, 0))
    for bird in birds:
        bird.drawn(screen)
    for cano in canos:
        cano.draw(screen)

    text = SCORE_SOURCE.render(f'SCORE: {points}')
