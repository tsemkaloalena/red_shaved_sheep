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
pour_in_products = pygame.sprite.Group()
button = pygame.sprite.Group()
time = 30


class ProductToPourIn(pygame.sprite.Sprite):
    def __init__(self, product, product_x, product_y, *group):
        super().__init__(group)
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = product
        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect.x = product_x
        self.sprite.rect.y = product_y


class PourInProduct(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(pour_in_products)
        self.frames = []
        self.pouring_in = False
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))
                self.mask = pygame.mask.from_surface(sheet)

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


chicken = ProductToPourIn(pygame.transform.scale(load_image("raw_chicken.png", -1), (200, 200)), 10, 300)
product_to_pour_in = pygame.sprite.GroupSingle(chicken.sprite)
salt = PourInProduct(pygame.transform.scale(load_image("salt.png", -1), (44, 80)), 1, 1, 350, 350)

running = True
while running:
    screen.fill((0, 255, 100))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if salt.rect.collidepoint(event.pos):
                if not salt.pouring_in:
                    pour_in_products.remove(salt)
                    salt = PourInProduct(pygame.transform.scale(load_image("salt2.png", -1), (226, 180)), 2, 1, 100, 50)
                    salt.pouring_in = True
    pour_in_products.update()
    if salt.pouring_in:
        time -= 1
    if time <= 0:
        pour_in_products.remove(salt)
        salt = PourInProduct(pygame.transform.scale(load_image("salt.png", -1), (44, 80)), 1, 1, 350, 350)
        salt.pouring_in = False
        time = 30
    pour_in_products.draw(screen)
    product_to_pour_in.draw(screen)
    pygame.display.flip()
    clock.tick(10)
pygame.quit()
