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


class ProductToOil(pygame.sprite.Sprite):
    def __init__(self, product, oiled_product, product_size_x, product_size_y, product_x, product_y, bowl_size, bowl_x,
                 bowl_y, *group):
        super().__init__(group)
        self.bowls = pygame.sprite.Group()
        self.brush = pygame.sprite.Group()
        self.bowl_size = bowl_size, bowl_size
        self.bowl_image = pygame.transform.scale(load_image('oil_with_brush.png', -1), self.bowl_size)
        self.bowl = pygame.sprite.Sprite(self.bowls)
        self.bowl.image = self.bowl_image
        self.bowl.rect = self.bowl.image.get_rect()
        self.bowl.rect.x = bowl_x
        self.bowl.rect.y = bowl_y

        self.cursor_image = pygame.transform.scale(load_image('brush.png', -1), (20, 100))
        self.cursor = pygame.sprite.Sprite(self.brush)
        self.cursor.image = self.cursor_image
        self.cursor.rect = self.cursor.image.get_rect()

        self.drawing = True
        self.start_to_oil = False
        self.x, self.y = product_x, product_y
        self.img_size = product_size_x, product_size_y
        self.product = pygame.sprite.Group()  # сам предмет
        self.already_oil = pygame.sprite.Group()  # линии, которые остаются, чтобы было видно, где мы уже намазали масло

        self.image = load_image(product, -1)
        self.image = pygame.transform.scale(self.image, self.img_size)
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = self.image
        self.sprite.mask = pygame.mask.from_surface(self.sprite.image)
        self.sprite.rect = self.sprite.image.get_rect()
        self.product.add(self.sprite)
        self.sprite.rect.x = product_x
        self.sprite.rect.y = product_y

        self.board = load_image("board.png", -1)
        self.board = pygame.transform.scale(self.board, self.img_size)
        self.oiled = pygame.sprite.Sprite()
        self.oiled.image = self.board
        self.oiled.mask = pygame.mask.from_surface(self.oiled.image)
        self.oiled.rect = self.oiled.image.get_rect()
        self.oiled.rect.x = self.x
        self.oiled.rect.y = self.y
        self.already_oil.add(self.oiled)

        self.oiled_product = load_image(oiled_product, -1)
        self.oiled_product = pygame.transform.scale(self.oiled_product, self.img_size)

    def check_oil(self):
        if pygame.sprite.collide_mask(self.sprite, self.oiled):
            m1 = self.sprite.mask
            m2 = self.oiled.mask
            m = m1.overlap_mask(m2, (0, 0))
            if m.count() > (m1.count() - m.count()) // 2:
                self.product.remove(self.sprite)
                self.sprite = pygame.sprite.Sprite()
                self.sprite.image = self.oiled_product
                self.sprite.mask = pygame.mask.from_surface(self.sprite.image)
                self.sprite.rect = self.sprite.image.get_rect()
                self.sprite.rect.x = self.x
                self.sprite.rect.y = self.y
                self.product.add(self.sprite)
                self.drawing = False
                return True

    def change_cursor(self):
        if oiling:
            pygame.mouse.set_visible(False)
            self.cursor.rect.bottomleft = event.pos
        else:
            pygame.mouse.set_visible(True)

    def change_bowl(self):
        if oiling:
            x = self.bowl.rect.x
            y = self.bowl.rect.y
            self.bowls.remove(self.bowl)
            self.bowl_image = pygame.transform.scale(load_image('oil.png', -1), self.bowl_size)
            self.bowl = pygame.sprite.Sprite(self.bowls)
            self.bowl.image = self.bowl_image
            self.bowl.rect = self.bowl.image.get_rect()
            self.bowl.rect.x = x
            self.bowl.rect.y = y
        else:
            x = self.bowl.rect.x
            y = self.bowl.rect.y
            self.bowls.remove(self.bowl)
            self.bowl_image = pygame.transform.scale(load_image('oil_with_brush.png', -1), self.bowl_size)
            self.bowl = pygame.sprite.Sprite(self.bowls)
            self.bowl.image = self.bowl_image
            self.bowl.rect = self.bowl.image.get_rect()
            self.bowl.rect.x = x
            self.bowl.rect.y = y


running = True
oiling = False
oil = ProductToOil("orange.png", "oiled_orange.png", 300, 189, 50, 100, 100, 300, 300)

while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if oiling:
                oil.start_to_oil = True
        if event.type == pygame.MOUSEBUTTONUP:
            oil.start_to_oil = False
            oil.oiled.image = oil.board
            oil.oiled.mask = pygame.mask.from_surface(oil.oiled.image)
            oil.check_oil()
        if oil.start_to_oil and event.type == pygame.MOUSEMOTION:
            pygame.draw.circle(oil.board, (255, 255, 0), (event.pos[0] - oil.x, event.pos[1] - oil.y), 15)
            oil.oiled.image = oil.board

        if event.type == pygame.MOUSEMOTION:
            oil.change_cursor()
        if event.type == pygame.MOUSEBUTTONDOWN and oil.bowl.rect.collidepoint(event.pos):
            if oiling:
                oiling = False
                oil.change_bowl()
            else:
                oiling = True
                oil.change_bowl()
    oil.product.draw(screen)
    if oil.drawing:
        oil.already_oil.draw(screen)
    oil.bowls.update()
    oil.bowls.draw(screen)
    if pygame.mouse.get_focused() and oiling:
        oil.brush.draw(screen)
    oil.brush.update()
    pygame.display.flip()
    clock.tick(90)
pygame.quit()