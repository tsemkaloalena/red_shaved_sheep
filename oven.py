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
ovensprite = pygame.sprite.Group()
buttongroup = pygame.sprite.Group()


class Oven(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(ovensprite)
        self.frames = []
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


oven = Oven(pygame.transform.scale(load_image("closedoven.png", -1), (500, 500)), 1, 1, 0, 0)
ovenon = False
ovenopen = False

buttonoff = load_image("off.png", -1)
buttonon = load_image("on.png", -1)
buttonoff = pygame.transform.scale(buttonoff, [20, 20])
buttonon = pygame.transform.scale(buttonon, [20, 20])
buttonsprite = pygame.sprite.Sprite()
buttonsprite.image = buttonoff
buttonsprite.rect = buttonsprite.image.get_rect()
buttongroup.add(buttonsprite)
buttonsprite.rect.x = 240
buttonsprite.rect.y = 65

running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if buttonsprite.rect.collidepoint(event.pos):
                if ovenon and not(ovenopen):
                    ovenon = False
                    ovensprite.remove(oven)
                    oven = Oven(pygame.transform.scale(load_image("closedoven.png", -1), (500, 500)), 1, 1, 0, 0)
                    buttonsprite.image = buttonoff
                elif not(ovenon) and not(ovenopen):
                    ovenon = True
                    ovensprite.remove(oven)
                    oven = Oven(pygame.transform.scale(load_image("workingoven.png", -1), (500, 500)), 1, 1, 0, 0)
                    buttonsprite.image = buttonon
            elif oven.rect.collidepoint(event.pos):
                if ovenopen:
                    ovenopen = False
                    ovensprite.remove(oven)
                    oven = Oven(pygame.transform.scale(load_image("closedoven.png", -1), (500, 500)), 1, 1, 0, 0)
                elif not(ovenopen) and not(ovenon):
                    ovenopen = True
                    ovensprite.remove(oven)
                    oven = Oven(pygame.transform.scale(load_image("openoven.png", -1), (500, 500)), 1, 1, 0, 0)
    ovensprite.update()
    screen.fill((0, 0, 0))
    ovensprite.draw(screen)
    buttongroup.draw(screen)
    pygame.display.flip()
    clock.tick(10)
pygame.quit()
