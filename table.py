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


def load_level(filename):
    filename = "data/levels/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    return level_map[0], level_map[1::]


class ProductToCut(pygame.sprite.Sprite):
    def __init__(self, product, lines, cut_product, size_x, size_y, x, y, *group):
        super().__init__(group)
        self.drawing = False
        self.start_to_cut = False
        self.x, self.y = x, y
        self.img_size = size_x, size_y
        self.product = pygame.sprite.Group()  # сам предмет, который мы собиаремся резать
        self.lines = pygame.sprite.Group()  # линии, по которым нужно резать
        self.already_cut = pygame.sprite.Group()  # линии, которые остаются, чтобы было видно, где мы уже отрезали

        self.name = product
        self.image = load_image(self.name, -1)
        self.image = pygame.transform.scale(self.image, self.img_size)
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = self.image
        self.sprite.mask = pygame.mask.from_surface(self.sprite.image)
        self.sprite.rect = self.sprite.image.get_rect()
        self.product.add(self.sprite)
        self.sprite.rect.x = x
        self.sprite.rect.y = y

        self.line = load_image(lines, -1)
        self.line = pygame.transform.scale(self.line, self.img_size)
        self.spriteline = pygame.sprite.Sprite()
        self.spriteline.image = self.line
        self.spriteline.mask = pygame.mask.from_surface(self.spriteline.image)
        self.spriteline.rect = self.spriteline.image.get_rect()
        self.lines.add(self.spriteline)
        self.spriteline.rect.x = self.x
        self.spriteline.rect.y = self.y

        self.board = load_image("board.png", -1)
        self.board = pygame.transform.scale(self.board, self.img_size)
        self.spritecut = pygame.sprite.Sprite()
        self.spritecut.image = self.board
        self.spritecut.rect = self.spritecut.image.get_rect()
        self.already_cut.add(self.spritecut)
        self.spritecut.rect.x = self.x
        self.spritecut.rect.y = self.y
        self.spritecut.mask = pygame.mask.from_surface(self.spritecut.image)

        self.cut_product = cut_product

    def check_cut(self):
        global time
        if pygame.sprite.collide_mask(self.spriteline, self.spritecut):
            m1 = self.spriteline.mask
            m2 = self.spritecut.mask
            m = m1.overlap_mask(m2, (0, 0))
            if m.count() > m1.count() - 50:
                self.product.remove(self.sprite)
                self.image = load_image(self.cut_product, -1)
                self.image = pygame.transform.scale(self.image, self.img_size)
                self.sprite = pygame.sprite.Sprite()
                self.sprite.image = self.image
                self.sprite.mask = pygame.mask.from_surface(self.sprite.image)
                self.sprite.rect = self.sprite.image.get_rect()
                self.sprite.rect.x = self.x
                self.sprite.rect.y = self.y
                self.product.add(self.sprite)
                self.name = 'cut_' + self.name
                self.drawing = False
                time = 500
                return True
            return False

    def update(self):
        pass


pygame.init()
width, height = 500, 500
size = width, height
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
screen_rect = (0, 0, width, height)
all_sprites = pygame.sprite.Group()
time = 500
pygame.display.set_caption("RSS kitchen")

running = True
font = pygame.font.SysFont('verdana', 20)
string_rendered = font.render('', 1, (255, 255, 255))
intro_rect = string_rendered.get_rect()
intro_rect.x = 10
intro_rect.y = 200

fon = pygame.transform.scale(load_image('table.jpg'), [500, 500])

timetext = font.render(str(time), 1, (255, 255, 255))
time_rect = timetext.get_rect()
time_rect.x = 470
time_rect.y = 51

stage, things_to_place = load_level('1.txt')  # стадия, на которой мы находимся, нужна будет при сборке всей игры
startpos = 0
everything = []
positions = []
for i in things_to_place:
    st = i.split()
    product = ProductToCut(st[0] + '.png', st[0] + '_lines.png', "cut_" + st[0] + ".png", int(st[1]), int(st[2]), 0,
                           startpos)
    positions.append(startpos)
    startpos += int(st[2]) + 10
    everything.append(product)

temp_product = -1
while running:
    screen.blit(fon, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT or time == 0:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if temp_product == -1:
                for i in range(len(everything)):
                    if everything[i].sprite.rect.collidepoint(event.pos):
                        if 'cut_' not in everything[temp_product].name:
                            everything[i].sprite.rect.x = 230
                            everything[i].sprite.rect.y = 200
                            everything[i].spriteline.rect.x = 230
                            everything[i].spriteline.rect.y = 200
                            everything[i].spritecut.rect.x = 230
                            everything[i].spritecut.rect.y = 200
                            everything[i].x, everything[i].y = 230, 200
                            everything[i].start_to_cut = True
                            everything[i].drawing = True
                            temp_product = i
                        break
            else:
                if everything[temp_product].drawing:
                    everything[temp_product].start_to_cut = True
                elif everything[temp_product].sprite.rect.collidepoint(event.pos) and 'cut_' in everything[
                    temp_product].name:
                    everything[temp_product].sprite.rect.x = 0
                    everything[temp_product].sprite.rect.y = positions[temp_product]
                    everything[temp_product].start_to_cut = False
                    everything[temp_product].drawing = False
                    temp_product = -1

        if event.type == pygame.MOUSEBUTTONUP:
            if temp_product != -1:
                if everything[temp_product].drawing:
                    everything[temp_product].start_to_cut = False
                    everything[temp_product].spritecut.image = everything[temp_product].board
                    everything[temp_product].spritecut.mask = pygame.mask.from_surface(
                        everything[temp_product].spritecut.image)
                    everything[temp_product].check_cut()

        if event.type == pygame.MOUSEMOTION and everything[temp_product] != -1:
            if everything[temp_product].drawing:
                if everything[temp_product].start_to_cut:
                    pygame.draw.circle(everything[temp_product].board, (0, 0, 255), (
                        event.pos[0] - everything[temp_product].x, event.pos[1] - everything[temp_product].y),
                                       5)
                    everything[temp_product].spritecut.image = everything[temp_product].board

    timetext = font.render(str(time), 1, (255, 255, 255))
    time_rect = timetext.get_rect()
    time_rect.x = 450
    time_rect.y = 5
    time -= 1
    screen.blit(string_rendered, intro_rect)
    screen.blit(timetext, time_rect)
    for product in everything:
        product.product.draw(screen)
        if product.drawing:
            product.lines.draw(screen)
            product.already_cut.draw(screen)
    pygame.display.flip()
    clock.tick(10)
pygame.quit()
