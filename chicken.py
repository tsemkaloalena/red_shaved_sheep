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


class Stuffing(pygame.sprite.Sprite):
    def __init__(self, product, product_w, product_h, product_x, product_y, group, *k):
        super().__init__(k)
        self.move = False
        self.dx = 0
        self.dy = 0
        self.img_size = product_w, product_h
        self.image = load_image(product, -1)
        self.image = pygame.transform.scale(self.image, self.img_size)
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = self.image
        self.sprite.mask = pygame.mask.from_surface(self.sprite.image)
        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect.x = product_x
        self.sprite.rect.y = product_y
        group.stuffings.add(self.sprite)
        group.list.append(self)


class ProductToStuff(pygame.sprite.Sprite):
    def __init__(self, product, product_min_w, product_min_h, product_max_w, product_max_h, product_x, product_y, *group):
        super().__init__(group)
        self.sprite_group = pygame.sprite.Group()
        self.stuffings = pygame.sprite.Group()
        self.list = []
        self.product_max_w = product_max_w
        self.product_max_h = product_max_h

        self.product_image = load_image(product, -1)
        self.product_size = product_min_w, product_min_h
        self.product = pygame.sprite.Sprite()
        self.product.image = pygame.transform.scale(self.product_image, self.product_size)
        self.product.mask = pygame.mask.from_surface(self.product.image)
        self.product.rect = self.product.image.get_rect()
        self.product.rect.x = product_x
        self.product.rect.y = product_y
        self.sprite_group.add(self.product)

    def add_stuff(self, stuffing):
        product_x = self.product.rect.x
        product_y = self.product.rect.y
        k = len(self.stuffings.sprites())
        self.stuffings.remove(stuffing.sprite)
        self.list.remove(stuffing)
        dx = (self.product_max_w - self.product_size[0]) // k
        dy = (self.product_max_h - self.product_size[1]) // k
        self.product_size = self.product_size[0] + dx, self.product_size[1] + dy
        self.sprite_group.remove(self.product)
        self.product = pygame.sprite.Sprite()
        self.product.image = pygame.transform.scale(self.product_image, self.product_size)
        self.product.mask = pygame.mask.from_surface(self.product.image)
        self.product.rect = self.product.image.get_rect()
        self.product.rect.x = product_x
        self.product.rect.y = product_y
        self.sprite_group.add(self.product)

    def draw_on_screen(self):
        self.stuffings.draw(screen)
        self.stuffings.update()
        self.sprite_group.draw(screen)
        self.sprite_group.update()

    def check_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(self.list)):
                prod = self.list[i]
                if prod.sprite.rect.x <= event.pos[
                    0] <= prod.sprite.rect.x + prod.sprite.rect.w and prod.sprite.rect.y <= event.pos[
                    1] <= prod.sprite.rect.y + prod.sprite.rect.h:
                    prod.move = True
                    prod.dx = prod.sprite.rect.x - event.pos[0]
                    prod.dy = prod.sprite.rect.y - event.pos[1]
        if event.type == pygame.MOUSEBUTTONUP:
            for i in range(len(self.list)):
                prod = self.list[i]
                if prod.sprite.rect.x <= event.pos[
                    0] <= prod.sprite.rect.x + prod.sprite.rect.w and prod.sprite.rect.y <= event.pos[
                    1] <= prod.sprite.rect.y + prod.sprite.rect.h:
                    prod.move = False
        if event.type == pygame.MOUSEMOTION:
            for i in range(len(self.list)):
                prod = self.list[i]
                if prod.move:
                    prod.sprite.rect.x = event.pos[0] + prod.dx
                    prod.sprite.rect.y = event.pos[1] + prod.dy
                    if pygame.sprite.collide_mask(prod.sprite, self.product):
                        self.add_stuff(prod)


running = True
chicken = ProductToStuff("raw_chicken.png", 50, 50, 250, 250, 10, 10)
carrot = Stuffing("cut_orange.png", 50, 50, 400, 400, chicken)
apple = Stuffing("cut_apple.png", 50, 50, 300, 300, chicken)

while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        chicken.check_event(event)
    chicken.draw_on_screen()
    pygame.display.flip()
    clock.tick(50)
pygame.quit()
