import pygame
import os


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)

    return image


pygame.init()
width, height = 500, 500
size = width, height
screen = pygame.display.set_mode(size)
screen.fill((0, 0, 0))
clock = pygame.time.Clock()


class Oil(pygame.sprite.Sprite):
    def __init__(self, size, x, y, *group):
        super().__init__(group)
        self.bowls = pygame.sprite.Group()
        self.brush = pygame.sprite.Group()
        self.bowl_size = size, size
        self.bowl_image = pygame.transform.scale(load_image('oil_with_brush.png', -1), self.bowl_size)
        self.bowl = pygame.sprite.Sprite(self.bowls)
        self.bowl.image = self.bowl_image
        self.bowl.rect = self.bowl.image.get_rect()
        self.bowl.rect.x = x
        self.bowl.rect.y = y

        self.cursor_image = load_image('brush.png', -1)
        self.cursor_image = pygame.transform.scale(self.cursor_image, (20, 100))
        self.cursor = pygame.sprite.Sprite(self.brush)
        self.cursor.image = self.cursor_image
        self.cursor.rect = self.cursor.image.get_rect()

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


oil = Oil(100, 300, 300)
oiling = False
running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            oil.change_cursor()
        if event.type == pygame.MOUSEBUTTONDOWN and oil.bowl.rect.collidepoint(event.pos):
            if oiling:
                oiling = False
                oil.change_bowl()
            else:
                oiling = True
                oil.change_bowl()
    oil.bowls.update()
    oil.bowls.draw(screen)
    if pygame.mouse.get_focused() and oiling:
        oil.brush.draw(screen)
    oil.brush.update()
    pygame.display.flip()
pygame.quit()
