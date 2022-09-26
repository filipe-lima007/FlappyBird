import pygame
import os
import random
import neat
from time import sleep
# player = int(input('Who will play? [1] - AI or [2] - Human: '))

# if player == 1:
#     ai_playing = True
# else:
#    ai_playing = False
ai_playing = False

generation = 0

SCREEN_W = 550
SCREEN_H = 800

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 200, 0)

C_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
G_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
BG_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
B_IMAGES = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png')))
]

pygame.font.init()
SCORE_SOURCE = pygame.font.SysFont('arial', 30, True)
pygame.display.set_caption('Flappy bird')


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
        return pygame.mask.from_surface(self.image)


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
            self.x0 = self.x1 + self.WIDTH
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x0 + self.WIDTH

    def draw(self, screen):
        screen.blit(self.IMAGE, (self.x0, self.y))
        screen.blit(self.IMAGE, (self.x1, self.y))


def draw_screen(screen, birds, canos, ground, points):
    screen.blit(BG_IMAGE, (0, 0))
    for bird in birds:
        bird.drawn(screen)
    for cano in canos:
        cano.draw(screen)

    text = SCORE_SOURCE.render(f'SCORE: {points}', 1, (0, 0, 255))
    screen.blit(text, (SCREEN_W - 10 - text.get_width(), 10))

    if ai_playing:
        text = SCORE_SOURCE.render(f'GENERATION: {generation}', 1, (255, 0, 0))
        screen.blit(text, (10, 10))
        
    ground.draw(screen)
    pygame.display.update()


def main(gens, config):
    global generation
    generation += 1

    if ai_playing:
        networks = []
        gen_list = []
        birds = []
        for _, gen in gens:
            network = neat.nn.FeedForwardNetwork.create(gen, config)
            networks.append(network)
            gen.fitness = 0
            gen_list.append(gen)
            birds.append(Bird(230, 350))
    else:
        birds = [Bird(230, 350)]
    ground = Ground(730)
    canos = [Cano(700)]
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    scores = 0
    watch = pygame.time.Clock()

    running = True
    while running:
        watch.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            if not ai_playing:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        for bird in birds:
                            bird.jump()

        cano_index = 0
        if len(birds) > 0:
            if len(canos) > 1 and birds[0].x > (canos[0].x + canos[0].TOP_CANO.get_width()):
                cano_index = 1
        else:
            running = False
            break

        for i, bird in enumerate(birds):
            bird.move()
            if ai_playing:
                gen_list[i].fitness += 0.1
                output = networks[i].activate((bird.y,
                                               abs(bird.y - canos[cano_index].height),
                                               abs(bird.y - canos[cano_index].base_pos)))
                if output[0] > 0.5:
                    bird.jump()
        ground.move()

        add_cano = False
        removed_canos = []
        for cano in canos:
            for i, bird in enumerate(birds):
                if cano.colition(bird):
                    birds.pop(i)
                    if not ai_playing:
                        game_over('Game over', screen)
                    if ai_playing:
                        gen_list[i].fitness -= 1
                        gen_list.pop(i)
                        networks.pop(i)
                if not cano.passed and bird.x > cano.x:
                    cano.passed = True
                    add_cano = True
            cano.move()
            if cano.x + cano.TOP_CANO.get_width() < 0:
                removed_canos.append(cano)

        if add_cano:
            scores += 1
            canos.append(Cano(600))
            if ai_playing:
                for gen in gen_list:
                    gen.fitness += 5
        for cano in removed_canos:
            canos.remove(cano)

        for i, bird in enumerate(birds):
            if (bird.y + bird.image.get_height()) > ground.y or bird.y < 0:
                birds.pop(i)
                if not ai_playing:
                    game_over('Game over', screen)
                if ai_playing:
                    gen_list.pop(i)
                    networks.pop(i)

        into(screen)
        draw_screen(screen, birds, canos, ground, scores)


def into(screen):
    text = 'Flappy bird'
    clock = pygame.time.Clock()
    intro = True

    while intro:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(BG_IMAGE, (0, 0))
        large_text = pygame.font.Font('freesansbold.ttf', 100)
        text_surf, text_rect = text_objects(text, large_text)
        text_rect.center = ((SCREEN_W / 2), (SCREEN_H / 2))
        screen.blit(text_surf, text_rect)

        pygame.draw.rect(screen, green, (SCREEN_W/9, SCREEN_H/10, SCREEN_W/3, SCREEN_H/10))
        pygame.draw.rect(screen, green, (5*(SCREEN_W/9), SCREEN_H/10, SCREEN_W/3, SCREEN_H/10))
        pygame.draw.rect(screen, red, ((1/3)*SCREEN_W, SCREEN_H/4, SCREEN_W/3, SCREEN_H/10))

        pygame.display.update()
        clock.tick(15)



def running(config_route):
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_route)
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())

    if ai_playing:
        population.run(main, 50)
    else:
        main(None, None)


def game_over(text, screen):
    message_display(text, screen)


def message_display(text, screen):
    large_text = pygame.font.Font('freesansbold.ttf', 100)
    text_surf, text_rect = text_objects(text, large_text)
    text_rect.center = ((SCREEN_W/2), (SCREEN_H/2))
    screen.blit(text_surf, text_rect)

    pygame.display.update()
    sleep(2)
    pygame.quit()
    quit()


def text_objects(text, font):
    text_surface = font.render(text, True, black)
    return text_surface, text_surface.get_rect()


if __name__ == '__main__':
    route = os.path.dirname(__file__)
    config_route = os.path.join(route, 'config.txt')
    running(config_route)
