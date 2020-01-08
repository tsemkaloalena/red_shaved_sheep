import pygame
import os


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
screen.fill((255, 255, 255))

clock = pygame.time.Clock()
w, h = 100, 100

all_sprites = pygame.sprite.Group()
sprite = pygame.sprite.Sprite()
sprite.image = pygame.transform.scale(load_image("raw_chicken.png", -1), (w, h))
sprite.rect = sprite.image.get_rect()
all_sprites.add(sprite)
sprite.rect.x = 0
sprite.rect.y = 0

move = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and sprite.rect.x <= event.pos[0] <= sprite.rect.x + w and sprite.rect.y <= event.pos[1] <= sprite.rect.y + h:
            move = True
            dx = sprite.rect.x - event.pos[0]
            dy = sprite.rect.y - event.pos[1]
        if event.type == pygame.MOUSEBUTTONUP:
            move = False
        if event.type == pygame.MOUSEMOTION and move:
            sprite.rect.x = event.pos[0] + dx
            sprite.rect.y = event.pos[1] + dy
    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()
