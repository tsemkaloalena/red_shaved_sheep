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
                return True


running = True
orange = ProductToCut("orange.png", "orange_lines.png", "cut_orange.png", 300, 189, 50, 100)

while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            orange.start_to_cut = True
        if event.type == pygame.MOUSEBUTTONUP:
            orange.start_to_cut = False
            orange.spritecut.image = orange.board
            orange.spritecut.mask = pygame.mask.from_surface(orange.spritecut.image)
            orange.check_cut()
        if orange.start_to_cut and event.type == pygame.MOUSEMOTION:
            pygame.draw.circle(orange.board, (0, 0, 255), (event.pos[0] - orange.x, event.pos[1] - orange.y), 5)
            orange.spritecut.image = orange.board
    orange.product.draw(screen)
    if orange.drawing:
        orange.lines.draw(screen)
        orange.already_cut.draw(screen)
    pygame.display.flip()
    clock.tick(90)
pygame.quit()
