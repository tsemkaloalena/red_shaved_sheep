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

flag = 0
x, y = 50, 100
img_size = [200, 200]
obj = pygame.sprite.Group()  # тесто

image = load_image("dough.png", -1)
image = pygame.transform.scale(image, img_size)
sprite = pygame.sprite.Sprite()
sprite.image = image
sprite.mask = pygame.mask.from_surface(sprite.image)
sprite.rect = sprite.image.get_rect()
obj.add(sprite)
sprite.rect.x = 100
sprite.rect.y = 100

board = load_image("board.png", -1)
board = pygame.transform.scale(board, img_size)

roller = pygame.sprite.Group()
rollerimg_size = [200, 50]
roller_image = load_image("rollingpin.png", -1)
roller_image = pygame.transform.scale(roller_image, rollerimg_size)
roller_sprite = pygame.sprite.Sprite()
roller_sprite.image = roller_image
roller_sprite.mask = pygame.mask.from_surface(roller_sprite.image)
roller_sprite.rect = roller_sprite.image.get_rect()
roller.add(sprite)
roller_sprite.rect.x = 150
roller_sprite.rect.y = 150

def roll_your_fckn_dough(dir):
    global flag
    if dir == 'up' and sprite.rect.y > 0:
        sprite.rect.y -= 1
        img_size[1] = img_size[1] + 1
        sprite.image = pygame.transform.scale(image, img_size)
        roller_sprite.rect.y -= 2
        if sprite.rect.y == 0:
            flag += 1
    if dir == 'down' and img_size[1] < height:
        img_size[1] = img_size[1] + 1
        sprite.image = pygame.transform.scale(image, img_size)
        roller_sprite.rect.y += 2
        if img_size[1] == height:
            flag += 1
    if dir == 'left' and sprite.rect.x > 0:
        sprite.rect.x -= 1
        img_size[0] = img_size[0] + 1
        sprite.image = pygame.transform.scale(image, img_size)
        roller_sprite.rect.x -= 2
        if sprite.rect.x == 0:
            flag += 1
    if dir == 'right' and img_size[0] < width:
        img_size[0] = img_size[0] + 1
        sprite.image = pygame.transform.scale(image, img_size)
        roller_sprite.rect.x += 2
        if img_size[0] == width:
            flag += 1


running = True
up = False
down = False
left = False
right = False

while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                up = True
            if event.key == pygame.K_DOWN:
                down = True
            if event.key == pygame.K_LEFT:
                left = True
            if event.key == pygame.K_RIGHT:
                right = True
        if event.type == pygame.KEYUP:
            up = False
            down = False
            left = False
            right = False
    if up:
        roll_your_fckn_dough('up')
    if down:
        roll_your_fckn_dough('down')
    if left:
        roll_your_fckn_dough('left')
    if right:
        roll_your_fckn_dough('right')
    if flag == 4:
        print('DONE')
    obj.draw(screen)
    roller.draw(screen)
    pygame.display.flip()
    clock.tick(20)
pygame.quit()
