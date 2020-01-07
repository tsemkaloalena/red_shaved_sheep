import pygame
import os
from PIL import Image
import csv

def info_from_csv(fname):
    with open(fname, encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        pictures = list(map(lambda x: ''.join(x) + '.png', reader))[1:]
        blocked = list(filter(lambda x: x[0] == '1', pictures))
        blocked = list(map(lambda x: int(x[1:3]), blocked))
        return pictures, len(pictures), blocked


def merge_images(pictures):
    images = []
    for file in pictures:
        image = Image.open(os.path.join('data', file))
        images.append(image)
    width, height = images[0].size
    result_height = height * len(images)
    result = Image.new('RGBA', (width, result_height))
    for image in enumerate(images):
        result.paste(image[1], (0, height * image[0]), image[1].convert('RGBA'))
    result.save(os.path.join('data', 'menu_levels.png'), "PNG")


fname = 'menu_info.csv'
menu, dish_amount, blocked = info_from_csv(os.path.join('data', fname))
merge_images(menu)
pygame.init()

screen = pygame.display.set_mode((500, 500))
image = pygame.image.load(os.path.join('data', 'menu.png'))
level_pic = pygame.image.load(os.path.join('data', 'menu_levels.png')).convert_alpha()
top = pygame.image.load(os.path.join('data', 'menutop.png'))
bottom = pygame.image.load(os.path.join('data', 'menubot.png'))
clock = pygame.time.Clock()
running = True

scroll_y = 180

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos_y = pygame.mouse.get_pos()[1]
                if 160 < pos_y < 420:
                    dish_number = abs(scroll_y - pos_y) // 60
                    if dish_number in blocked:
                        print('choose another')
                    else:
                        print(dish_number)
            if event.button == 4:
                scroll_y = min(scroll_y + 15, 178)
            if event.button == 5:
                scroll_y = max(scroll_y - 15, - 60 * (dish_amount - 4) + 180)
    screen.blit(image, (0, 0))
    screen.blit(level_pic, (0, scroll_y))
    screen.blit(top, (0, 0))
    screen.blit(bottom, (0, 429))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
