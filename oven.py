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

class Oven(pygame.sprite.Sprite):
    def __init__(self, product):
        super().__init__()
        self.pr = product
        self.all_sprites = pygame.sprite.Group()
        self.ovengroup = pygame.sprite.Group()
        self.buttongroup = pygame.sprite.Group()
        self.product = pygame.sprite.Group()

        self.ovenon = False
        self.ovenopen = False
        self.slide = False

        self.closedoven = load_image("closedoven.png", -1)
        self.workingoven = load_image("workingoven.png", -1)
        self.openoven = load_image("openoven.png", -1)

        self.oven = pygame.transform.scale(self.closedoven, [500, 500])
        self.ovensprite = pygame.sprite.Sprite()
        self.ovensprite.image = self.oven
        self.ovensprite.rect = self.ovensprite.image.get_rect()
        self.ovengroup.add(self.ovensprite)
        self.ovensprite.rect.x = 0
        self.ovensprite.rect.y = 0

        self.image = load_image(product, -1)
        self.image = pygame.transform.scale(self.image, [150, 150])
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = self.image
        self.sprite.mask = pygame.mask.from_surface(self.sprite.image)
        self.sprite.rect = self.sprite.image.get_rect()
        self.product.add(self.sprite)
        self.sprite.rect.x = 170
        self.sprite.rect.y = 350

        self.buttonoff = load_image("off.png", -1)
        self.buttonon = load_image("on.png", -1)
        self.buttonoff = pygame.transform.scale(self.buttonoff, [20, 20])
        self.buttonon = pygame.transform.scale(self.buttonon, [20, 20])
        self.buttonsprite = pygame.sprite.Sprite()
        self.buttonsprite.image = self.buttonoff
        self.buttonsprite.rect = self.buttonsprite.image.get_rect()
        self.buttongroup.add(self.buttonsprite)
        self.buttonsprite.rect.x = 240
        self.buttonsprite.rect.y = 60

    def update(self, type):
        if type == 1:
            if self.buttonsprite.rect.collidepoint(event.pos):
                if self.ovenon and not(self.ovenopen):
                    self.ovenon = False
                    self.ovensprite.image = pygame.transform.scale(self.closedoven, [500, 500])
                    self.buttonsprite.image = self.buttonoff
                    if self.slide:
                        self.sprite.rect.x = 170
                        self.sprite.rect.y = 350
                elif not(oven.ovenon) and not(oven.ovenopen):
                    self.ovenon = True
                    self.ovensprite.image = pygame.transform.scale(self.workingoven, [500, 500])
                    self.buttonsprite.image = self.buttonon
                    if self.slide:
                        self.sprite.image = pygame.transform.scale(load_image(self.pr[0:-4]+'_done.png', -1), [150, 150])
        if type == 2:
            if not(self.slide) and self.ovenopen:
                self.slide = True
                self.sprite.rect.x = 170
                self.sprite.rect.y = 170
        else:
            if self.ovenopen:
                self.ovenopen = False
                self.ovensprite.image = pygame.transform.scale(self.closedoven, [500, 500])
                if self.slide:
                    self.sprite.rect.x = -150
                    self.sprite.rect.y = -150
            elif not(self.ovenopen) and not(self.ovenon):
                self.ovenopen = True
                self.ovensprite.image = pygame.transform.scale(self.openoven, [500, 500])
                if self.slide:
                    self.sprite.rect.x = 170
                    self.sprite.rect.y = 350



oven = Oven("turkey.png")

running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if oven.sprite.rect.collidepoint(event.pos):

                oven.update(2)
            elif oven.buttonsprite.rect.collidepoint(event.pos):
                oven.update(1)
            elif oven.ovensprite.rect.collidepoint(event.pos):
                oven.update(0)
    screen.fill((0, 0, 0))
    oven.ovengroup.draw(screen)
    oven.buttongroup.draw(screen)
    oven.product.draw(screen)
    pygame.display.flip()
    clock.tick(10)
pygame.quit()
