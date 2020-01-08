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

    # def draw_on_screen(self):
    #     self.product.draw(screen)
    #     if self.drawing:
    #         self.already_oil.draw(screen)
    #     self.bowls.update()
    #     self.bowls.draw(screen)
    #     if pygame.mouse.get_focused() and self.oiling:
    #         self.brush.draw(screen)
    #     self.brush.update()

    def check_event(self, event):
        pass


running = True
chicken = ProductToStuff("raw_chicken.png", 50, 50, 300, 300, 10, 10)
carrot = Stuffing("cut_orange.png", 50, 50, 400, 400, chicken)
apple = Stuffing("cut_apple.png", 50, 50, 300, 300, chicken)

while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(chicken.list)):
                prod = chicken.list[i]
                if prod.sprite.rect.x <= event.pos[0] <= prod.sprite.rect.x + prod.sprite.rect.w and prod.sprite.rect.y <= event.pos[1] <= prod.sprite.rect.y + prod.sprite.rect.h:
                    prod.move = True
                    prod.dx = prod.sprite.rect.x - event.pos[0]
                    prod.dy = prod.sprite.rect.y - event.pos[1]
        if event.type == pygame.MOUSEBUTTONUP:
            for i in range(len(chicken.list)):
                prod = chicken.list[i]
                if prod.sprite.rect.x <= event.pos[0] <= prod.sprite.rect.x + prod.sprite.rect.w and prod.sprite.rect.y <= event.pos[1] <= prod.sprite.rect.y + prod.sprite.rect.h:
                    prod.move = False
        if event.type == pygame.MOUSEMOTION:
            for i in range(len(chicken.list)):
                prod = chicken.list[i]
                if prod.move:
                    prod.sprite.rect.x = event.pos[0] + prod.dx
                    prod.sprite.rect.y = event.pos[1] + prod.dy
                    if pygame.sprite.collide_mask(prod.sprite, chicken.product):
                        print(1)
                        chicken.add_stuff(prod)

    chicken.stuffings.draw(screen)
    chicken.stuffings.update()
    chicken.sprite_group.draw(screen)
    chicken.sprite_group.update()

    pygame.display.flip()
    clock.tick(50)
pygame.quit()
