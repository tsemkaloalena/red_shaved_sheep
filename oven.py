import pygame
import os
import random


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


pygame.init()
width, height = 500, 500
size = width, height
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
screen_rect = (0, 0, width, height)
all_sprites = pygame.sprite.Group()
GRAVITY = 0.1
time = 100


class Particle(pygame.sprite.Sprite):
    fire = [load_image("star.png", -1)]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos

        self.gravity = GRAVITY

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position):
    particle_count = 40
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


class Oven(pygame.sprite.Sprite):
    def __init__(self, product):
        super().__init__()
        self.pr = product
        self.level_done = 0
        self.ovengroup = pygame.sprite.Group()
        self.buttongroup = pygame.sprite.Group()
        self.product = pygame.sprite.Group()

        self.ovenon = False
        self.ovenopen = False
        self.slide = False

        self.closedoven = load_image("closedoven.png", -1)
        self.workingoven = load_image("workingoven.png", -1)
        self.openoven = load_image("openoven.png", -1)

        self.oven = pygame.transform.scale(self.closedoven, [500, 500])
        self.ovensprite = pygame.sprite.Sprite()
        self.ovensprite.image = self.oven
        self.ovensprite.rect = self.ovensprite.image.get_rect()
        self.ovengroup.add(self.ovensprite)
        self.ovensprite.rect.x = 0
        self.ovensprite.rect.y = 0

        self.image = load_image(product, -1)
        self.image = pygame.transform.scale(self.image, [150, 150])
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = self.image
        self.sprite.mask = pygame.mask.from_surface(self.sprite.image)
        self.sprite.rect = self.sprite.image.get_rect()
        self.product.add(self.sprite)
        self.sprite.rect.x = 170
        self.sprite.rect.y = 350

        self.buttonoff = load_image("off.png", -1)
        self.buttonon = load_image("on.png", -1)
        self.buttonoff = pygame.transform.scale(self.buttonoff, [20, 20])
        self.buttonon = pygame.transform.scale(self.buttonon, [20, 20])
        self.buttonsprite = pygame.sprite.Sprite()
        self.buttonsprite.image = self.buttonoff
        self.buttonsprite.rect = self.buttonsprite.image.get_rect()
        self.buttongroup.add(self.buttonsprite)
        self.buttonsprite.rect.x = 240
        self.buttonsprite.rect.y = 60

    def update(self, type):
        if type == 1:
            if self.ovenon and not (self.ovenopen):
                self.ovenon = False
                self.ovensprite.image = pygame.transform.scale(self.closedoven, [500, 500])
                self.buttonsprite.image = self.buttonoff
                if self.slide:
                    self.sprite.rect.x = 170
                    self.sprite.rect.y = 170
                print(self.ovenopen)
            elif not (oven.ovenon) and not (oven.ovenopen):
                self.ovenon = True
                self.ovensprite.image = pygame.transform.scale(self.workingoven, [500, 500])
                self.buttonsprite.image = self.buttonon
                if self.slide:
                    self.pr = self.pr[0:-4] + '_done.png'
                    self.sprite.image = pygame.transform.scale(load_image(self.pr, -1),
                                                               [150, 150])
        if type == 2:
            if not self.slide and self.ovenopen:
                self.slide = True
                self.sprite.rect.x = 170
                self.sprite.rect.y = 170

        else:
            if self.ovenopen and not self.ovenon:
                self.ovenopen = False
                self.ovensprite.image = pygame.transform.scale(self.closedoven, [500, 500])
                if self.slide:
                    self.sprite.rect.x = -150
                    self.sprite.rect.y = -150
            elif not self.ovenopen and not self.ovenon:
                self.ovenopen = True
                self.ovensprite.image = pygame.transform.scale(self.openoven, [500, 500])
                if self.slide:
                    self.sprite.rect.x = 170
                    self.sprite.rect.y = 170
                    print(self.ovenopen)
                if self.slide and '_done.png' in self.pr:
                    print('DONE!')
                    self.next_level()

    def next_level(self):
        self.level_done = 1
        # Здесь будет извещение о завершении уровня, полученные баллы (от времени) и предложение перейти к дальнейшему оформлению блюда


oven = Oven("turkey.png")
running = True
font = pygame.font.SysFont('verdana', 20)
string_rendered = font.render('', 1, (255, 255, 255))
intro_rect = string_rendered.get_rect()
intro_rect.x = 10
intro_rect.y = 200

timetext = font.render(str(time), 1, (255, 255, 255))
time_rect = timetext.get_rect()
time_rect.x = 470
time_rect.y = 5

while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if oven.sprite.rect.collidepoint(event.pos):
                oven.update(2)
            elif oven.buttonsprite.rect.collidepoint(event.pos):
                oven.update(1)
            elif oven.ovensprite.rect.collidepoint(event.pos):
                oven.update(0)
    if oven.level_done == 1:
        create_particles((250, 0))
        font = pygame.font.SysFont('verdana', 20)
        string_rendered = font.render('Перейти к следующему шагу', 1, (255, 255, 255))
        intro_rect = string_rendered.get_rect()
        intro_rect.x = 5
        intro_rect.y = 470
        oven.level_done = 2

    timetext = font.render(str(time), 1, (255, 255, 255))
    time_rect = timetext.get_rect()
    time_rect.x = 470
    time_rect.y = 5
    if oven.level_done == 0:
        time -= 1
    all_sprites.update()
    screen.fill((0, 0, 0))
    oven.ovengroup.draw(screen)
    oven.buttongroup.draw(screen)
    oven.product.draw(screen)
    all_sprites.draw(screen)
    screen.blit(string_rendered, intro_rect)
    screen.blit(timetext, time_rect)
    pygame.display.flip()
    clock.tick(10)
pygame.quit()
