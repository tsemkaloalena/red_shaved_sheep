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


class ProductToGrate(pygame.sprite.Sprite):
    def __init__(self, grater, grated_product, product_size_x, product_size_y, product_x, product_y, grater_size,
                 grater_x, grater_y, number_of_swipes, result, result_size, result_xy,  *group):
        super().__init__(group)
        self.grated = pygame.sprite.Group()
        self.grater = pygame.sprite.Group()

        self.gr = load_image(grater, -1)
        self.gr = pygame.transform.scale(self.gr, grater_size)
        self.gratersprite = pygame.sprite.Sprite()
        self.gratersprite.image = self.gr
        self.gratersprite.rect = self.gratersprite.image.get_rect()
        self.grater.add(self.gratersprite)
        self.gratersprite.rect.x = grater_x
        self.gratersprite.rect.y = grater_y

        self.ch_w, self.ch_h = product_size_x, product_size_y
        self.image = load_image(grated_product, -1)
        self.image = pygame.transform.scale(self.image, (self.ch_w, self.ch_h))
        self.cheese = pygame.sprite.Sprite()
        self.cheese.image = self.image
        self.cheese.rect = self.cheese.image.get_rect()
        self.grated.add(self.cheese)
        self.cheese.rect.x = product_x
        self.cheese.rect.y = product_y
        self.number_of_swipes = number_of_swipes

        self.result = result
        self.result_size = result_size
        self.result_xy = result_xy

    def end_of_game(self):
        self.cheese.kill()
        self.gratersprite.kill()
        self.image_gr_ch = load_image(self.result, -1)
        self.image_gr_ch = pygame.transform.scale(self.image_gr_ch, self.result_size)
        self.gr_ch = pygame.sprite.Sprite()
        self.gr_ch.image = self.image_gr_ch
        self.gr_ch.rect = self.gr_ch.image.get_rect()
        self.grated.add(self.gr_ch)
        self.gr_ch.rect.x = self.result_xy[0]
        self.gr_ch.rect.y = self.result_xy[1]

    def check_grate(self):
        if pygame.sprite.spritecollideany(self.cheese, self.grater, collided=pygame.sprite.collide_rect_ratio(0.5)):
            self.number_of_swipes -= 1
            if self.number_of_swipes == 0:
                self.end_of_game()
            elif self.number_of_swipes % 10 == 0:
                self.ch_w -= 3
                self.ch_h -= 3
                self.cheese.image = pygame.transform.scale(self.image, (self.ch_w, self.ch_h))


running = True
moving = False
collision = []
grate = ProductToGrate('grater.png', "cheese.png", 180, 180, 80, 120, (250, 250), 170, 120, 259, "grch.png",
                       (270, 270), (100, 100))

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
            grate.check_grate()
            x, y = pygame.mouse.get_pos()
            grate.cheese.rect.x = x - 50
            grate.cheese.rect.y = y - 50
    grate.grater.draw(screen)
    grate.grated.draw(screen)
    pygame.display.flip()
    clock.tick(50)
pygame.quit()
