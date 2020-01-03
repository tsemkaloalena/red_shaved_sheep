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


class ProductToCut(pygame.sprite.Sprite):
    def __init__(self, product, lines, cut_product, size_x, size_y, x, y, *group):
        super().__init__(group)
        self.drawing = True
        self.start_to_cut = False
        self.x, self.y = x, y
        self.img_size = size_x, size_y
        self.product = pygame.sprite.Group()  # сам предмет, который мы собиаремся резать
        self.lines = pygame.sprite.Group()  # линии, по которым нужно резать
        self.already_cut = pygame.sprite.Group()  # линии, которые остаются, чтобы было видно, где мы уже отрезали

        self.image = load_image(product, -1)
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
        self.spritecut.mask = pygame.mask.from_surface(self.spritecut.image)
        self.spritecut.rect = self.spritecut.image.get_rect()
        self.spritecut.rect.x = self.x
        self.spritecut.rect.y = self.y
        self.already_cut.add(self.spritecut)

        self.cut_product = cut_product

    def check_cut(self):
        if pygame.sprite.collide_mask(self.spriteline, self.spritecut):
            m1 = self.spriteline.mask
            m2 = self.spritecut.mask
            m = m1.overlap_mask(m2, (0, 0))
            if m.count() > m1.count() - 50:
                '''
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
                self.drawing = False
                '''
                return True
            return False

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

products = pygame.sprite.Group()
name = 'carrot.png'
image = load_image(name, -1)
image = pygame.transform.scale(image, [200, 54])
product = pygame.sprite.Sprite()
product.image = image
product.rect = product.image.get_rect()
products.add(product)
product.rect.x = 10
product.rect.y = 400
cutting = False

while running:
    screen.blit(fon, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT or time == 0:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if cutting:
                product.start_to_cut = True
            else:
                if product.rect.collidepoint(event.pos) and 'cut_' not in name:
                    product = ProductToCut("carrot.png", "carrot_lines.png", "cut_carrot.png", 300, 80, 200, 200)
                    product.start_to_cut = True
                    cutting = True
                elif product.rect.collidepoint(event.pos) and 'cut_' in name:
                    image = pygame.transform.scale(image, [200, 54])
                    product.image = image
                    product.rect.x = 10
                    product.rect.y = 400
                    time = 500

        if event.type == pygame.MOUSEBUTTONUP:
            if cutting:
                product.start_to_cut = False
                product.spritecut.image = product.board
                product.spritecut.mask = pygame.mask.from_surface(product.spritecut.image)
                if product.check_cut():
                    cutting = False
                    products = pygame.sprite.Group()
                    name = "cut_" + name
                    image = load_image(name, -1)
                    image = pygame.transform.scale(image, [300, 80])
                    product.image = image
                    product.rect = product.image.get_rect()
                    product.rect.x = 200
                    product.rect.y = 200
                    products.add(product)

        if event.type == pygame.MOUSEMOTION and cutting:
            if product.start_to_cut:
                pygame.draw.circle(product.board, (0, 0, 255), (event.pos[0] - product.x, event.pos[1] - product.y),
                                   5)
                product.spritecut.image = product.board
    timetext = font.render(str(time), 1, (255, 255, 255))
    time_rect = timetext.get_rect()
    time_rect.x = 450
    time_rect.y = 5
    time -= 1
    screen.blit(string_rendered, intro_rect)
    screen.blit(timetext, time_rect)
    if not (cutting):
        products.draw(screen)
    elif cutting:
        product.product.draw(screen)
        if product.drawing:
            product.lines.draw(screen)
            product.already_cut.draw(screen)
    pygame.display.flip()
    clock.tick(10)
pygame.quit()