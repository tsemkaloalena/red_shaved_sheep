import pygame
import os
import random


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
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
screen.fill((0, 0, 0))


class Bomb(pygame.sprite.Sprite):
    image = load_image("bomb.png", -1)
    image = pygame.transform.scale(image, (100, 100))
    image_boom = load_image("boom.png", -1)
    image_boom = pygame.transform.scale(image_boom, (100, 100))

    def __init__(self, group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite. Это очень важно !!!
        super().__init__(group)
        self.image = Bomb.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width-100)
        self.rect.y = random.randrange(height-100)

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            self.image = self.image_boom

    def get_event(self):
        if self.rect.collidepoint(event.pos):
            self.image = self.image_boom


all_sprites = pygame.sprite.Group()

bomb_image = load_image("bomb.png", -1)
bomb_image = pygame.transform.scale(bomb_image, (100, 100))

for _ in range(20):
    Bomb(all_sprites)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for bomb in all_sprites:
                bomb.get_event()
    all_sprites.draw(screen)
    all_sprites.update()

    pygame.display.flip()
    screen.fill((0, 0, 0))
pygame.quit()