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

all_sprites = pygame.sprite.Group()

x, y = 50, 100
img_size = 200, 200
smth = pygame.sprite.Group()  # сам предмет, который мы собиаремся резать
lines = pygame.sprite.Group()  # линии, по которым нужно резать
cut = pygame.sprite.Group()  # линии, которые остаются, чтобы было видно, где мы уже отрезали

image = load_image("carrot.png", -1)
image = pygame.transform.scale(image, img_size)
sprite = pygame.sprite.Sprite()
sprite.image = image
sprite.mask = pygame.mask.from_surface(sprite.image)
sprite.rect = sprite.image.get_rect()
smth.add(sprite)
sprite.rect.x = 0
sprite.rect.y = 0

line = load_image('carrot_lines.png', -1)
line = pygame.transform.scale(line, img_size)
spriteline = pygame.sprite.Sprite()
spriteline.image = line
spriteline.mask = pygame.mask.from_surface(spriteline.image)
spriteline.rect = spriteline.image.get_rect()
lines.add(spriteline)
spriteline.rect.x = sprite.rect.x
spriteline.rect.y = sprite.rect.y

board = load_image("board.png", -1)
board = pygame.transform.scale(board, img_size)
spritecut = pygame.sprite.Sprite()
spritecut.image = board
spritecut.mask = pygame.mask.from_surface(spritecut.image)
spritecut.rect = spritecut.image.get_rect()
cut.add(spritecut)


def check_cut():
    if pygame.sprite.collide_mask(spriteline, spritecut):
        print(1)


start_to_cut = False
running = True

while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            start_to_cut = True
        if event.type == pygame.MOUSEBUTTONUP:
            start_to_cut = False
            spritecut.image = board
            spritecut.mask = pygame.mask.from_surface(spritecut.image)
            check_cut()
        if start_to_cut and event.type == pygame.MOUSEMOTION:
            pygame.draw.circle(board, (0, 0, 255), (event.pos[0], event.pos[1]), 5)
            spritecut.image = board

    smth.draw(screen)
    lines.draw(screen)
    cut.draw(screen)
    pygame.display.flip()
    clock.tick(50)
pygame.quit()
