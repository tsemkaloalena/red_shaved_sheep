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
mixers = pygame.sprite.Group()
button = pygame.sprite.Group()


class Mixer(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(mixers)
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


mixer = Mixer(pygame.transform.scale(load_image("mixer_off.png", -1), (200, 200)), 1, 1, 100, 50)
mixing = False

running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mixer.rect.collidepoint(event.pos):
                if mixing:
                    mixing = False
                    mixers.remove(mixer)
                    mixer = Mixer(pygame.transform.scale(load_image("mixer_off.png", -1), (200, 200)), 1, 1, 100, 50)
                else:
                    mixing = True
                    mixers.remove(mixer)
                    mixer = Mixer(pygame.transform.scale(load_image("mixer_on.png", -1), (400, 200)), 2, 1, 100, 50)
    mixers.update()
    screen.fill((0, 0, 0))
    mixers.draw(screen)
    pygame.display.flip()
    clock.tick(10)
pygame.quit()
