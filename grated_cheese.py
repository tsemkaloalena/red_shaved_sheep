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
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()

x, y = 50, 100

cheese = pygame.sprite.Group()
grater = pygame.sprite.Group()
help_line = pygame.sprite.Group()

line = load_image('grater.png', -1)
line = pygame.transform.scale(line, (250, 250))
gratersprite = pygame.sprite.Sprite()
gratersprite.image = line
gratersprite.rect = gratersprite.image.get_rect()
grater.add(gratersprite)
gratersprite.rect.x = 170
gratersprite.rect.y = 120

ch_w, ch_h = 180, 180
image = load_image("cheese.png", -1)
image = pygame.transform.scale(image, (180, 180))
sprite = pygame.sprite.Sprite()
sprite.image = image
sprite.rect = sprite.image.get_rect()
cheese.add(sprite)
sprite.rect.x = 80
sprite.rect.y = 120
number_of_swipes = 100


def end_of_game():
    sprite.kill()
    gratersprite.kill()
    image_gr_ch = load_image("grch.png", -1)
    image_gr_ch = pygame.transform.scale(image_gr_ch, (300, 300))
    gr_ch = pygame.sprite.Sprite()
    gr_ch.image = image_gr_ch
    gr_ch.rect = sprite.image.get_rect()
    cheese.add(gr_ch)
    gr_ch.rect.x = 100
    gr_ch.rect.y = 100


def check_grate():
    global number_of_swipes
    if pygame.sprite.spritecollideany(sprite, grater, collided=pygame.sprite.collide_rect_ratio(0.5)):
        number_of_swipes -= 1
    if number_of_swipes == 0:
        end_of_game()
    if number_of_swipes % 10 == 0:
        sprite.image = pygame.transform.scale(image, (ch_w - 5, ch_h - 5))
    print(number_of_swipes)



running = True
moving = False
collision = []

while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            moving = True
        if event.type == pygame.MOUSEBUTTONUP:
            moving = False
        if event.type == pygame.MOUSEMOTION and moving:
            check_grate()
            x, y = pygame.mouse.get_pos()
            sprite.rect.x = x - 50
            sprite.rect.y = y - 50
    grater.draw(screen)
    cheese.draw(screen)
    pygame.display.flip()
    clock.tick(50)
pygame.quit()