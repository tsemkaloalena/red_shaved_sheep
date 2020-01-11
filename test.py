import pygame
import os
import random
from PIL import Image
import csv

pygame.init()
width, height = 500, 500
size = width, height
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
screen_rect = (0, 0, width, height)
all_sprites = pygame.sprite.Group()
GRAVITY = 0.1
pygame.display.set_caption("SSB kitchen")
pygame.display.set_icon(pygame.image.load("data/sheep.png"))


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


def load_level(filename):
    filename = "data/levels/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    a = []
    b = []
    aFlag = True
    for i in level_map:
        if i == '-':
            aFlag = True
        elif aFlag:
            aFlag = False
            a.append(i)
            b.append([])
        else:
            b[-1].append(i)
    return a, b


def info_from_csv(fname):
    with open(fname, encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        pictures = list(map(lambda x: ''.join(x) + '.png', reader))[1:]
        blocked = list(filter(lambda x: x[0] == '1', pictures))
        blocked = list(map(lambda x: int(x[1:3]), blocked))
        return pictures, len(pictures), blocked


def merge_images(pictures):
    images = []
    for file in pictures:
        image = Image.open(os.path.join('data', file))
        images.append(image)
    width, height = images[0].size
    result_height = height * len(images)
    result = Image.new('RGBA', (width, result_height))
    for image in enumerate(images):
        result.paste(image[1], (0, height * image[0]), image[1].convert('RGBA'))
    result.save(os.path.join('data', 'menu_levels.png'), "PNG")


class Particle(pygame.sprite.Sprite):
    fire = [load_image("star.png", -1)]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos

        self.gravity = GRAVITY

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position):
    particle_count = 40
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


class ProductToCut(pygame.sprite.Sprite):
    def __init__(self, product, lines, cut_product, size_x, size_y, x, y, *group):
        super().__init__(group)
        self.drawing = False
        self.start_to_cut = False
        self.x, self.y = x, y
        self.img_size = size_x, size_y
        self.product = pygame.sprite.Group()  # сам предмет, который мы собиаремся резать
        self.lines = pygame.sprite.Group()  # линии, по которым нужно резать
        self.already_cut = pygame.sprite.Group()  # линии, которые остаются, чтобы было видно, где мы уже отрезали

        self.name = product
        self.image = load_image(self.name, -1)
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
        self.spritecut.rect = self.spritecut.image.get_rect()
        self.already_cut.add(self.spritecut)
        self.spritecut.rect.x = self.x
        self.spritecut.rect.y = self.y
        self.spritecut.mask = pygame.mask.from_surface(self.spritecut.image)

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
                self.name = 'cut_' + self.name
                self.drawing = False
                return True
            return False

    def update(self):
        pass


class Oven(pygame.sprite.Sprite):
    def __init__(self, product):
        super().__init__()
        self.pr = product
        self.level_done = 0
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
            if self.ovenon and not (self.ovenopen):
                self.ovenon = False
                self.ovensprite.image = pygame.transform.scale(self.closedoven, [500, 500])
                self.buttonsprite.image = self.buttonoff
                if self.slide:
                    self.sprite.rect.x = 170
                    self.sprite.rect.y = 170
            elif not (self.ovenon) and not (self.ovenopen):
                self.ovenon = True
                self.ovensprite.image = pygame.transform.scale(self.workingoven, [500, 500])
                self.buttonsprite.image = self.buttonon
                if self.slide:
                    self.pr = self.pr[0:-4] + '_done.png'
                    self.sprite.image = pygame.transform.scale(load_image(self.pr, -1),
                                                               [150, 150])
        if type == 2:
            if not self.slide and self.ovenopen:
                self.slide = True
                self.sprite.rect.x = 170
                self.sprite.rect.y = 170

        else:
            if self.ovenopen and not self.ovenon:
                self.ovenopen = False
                self.ovensprite.image = pygame.transform.scale(self.closedoven, [500, 500])
                if self.slide:
                    self.sprite.rect.x = -150
                    self.sprite.rect.y = -150
            elif not self.ovenopen and not self.ovenon:
                self.ovenopen = True
                self.ovensprite.image = pygame.transform.scale(self.openoven, [500, 500])
                if self.slide:
                    self.sprite.rect.x = 170
                    self.sprite.rect.y = 170
                if self.slide and '_done.png' in self.pr:
                    print('DONE!')
                    self.next_level()

    def next_level(self):
        self.level_done = 1
        # Здесь будет извещение о завершении уровня, полученные баллы (от времени) и предложение перейти к дальнейшему оформлению блюда


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
    def __init__(self, product, product_min_w, product_min_h, product_max_w, product_max_h, product_x, product_y,
                 *group):
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
                        break


class ProductToPourIn(pygame.sprite.Sprite):
    def __init__(self, product, product_x, product_y, *group):
        super().__init__(group)
        self.sprite = pygame.sprite.Sprite()
        self.image = product
        self.sprite.image = product
        self.sprite.rect = self.sprite.image.get_rect()
        self.rect = self.sprite.image.get_rect()
        self.sprite.rect.x = product_x
        self.sprite.rect.y = product_y


class PourInProduct(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, pour_in_products, *k):
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


running = True


def cut_stage(things_to_place):
    global running, maxscore, score, game_running, start_running
    cut_running = True
    font = pygame.font.SysFont('verdana', 20)
    string_rendered = font.render('', 1, (255, 255, 255))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = 10
    intro_rect.y = 200

    recepy = font.render('Нарежь продукты', 1, (255, 0, 0))
    recepy_rect = recepy.get_rect()
    recepy_rect.x = 10
    recepy_rect.y = 5

    startpos = 30
    everything = []
    positions = []
    for i in things_to_place:
        st = i.split()
        product = ProductToCut(st[0] + '.png', st[0] + '_lines.png', "cut_" + st[0] + ".png", int(st[1]), int(st[2]), 0,
                               startpos)
        positions.append(startpos)
        startpos += int(st[2]) + 10
        everything.append(product)

    time = 300 * len(everything)
    maxscore += time
    fon = pygame.transform.scale(load_image('table.jpg'), [500, 500])

    timetext = font.render(str(time), 1, (255, 255, 255))
    time_rect = timetext.get_rect()
    time_rect.x = 470
    time_rect.y = 51

    temp_product = -1
    check_done = 0

    while cut_running:
        if check_done < 4:
            check_done = 0
        screen.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cut_running = False
                running = False
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if check_done >= 4:
                    if intro_rect.collidepoint(event.pos):
                        return True
                if temp_product == -1:
                    for i in range(len(everything)):
                        if everything[i].sprite.rect.collidepoint(event.pos):
                            if 'cut_' not in everything[temp_product].name:
                                everything[i].sprite.rect.x = 230
                                everything[i].sprite.rect.y = 200
                                everything[i].spriteline.rect.x = 230
                                everything[i].spriteline.rect.y = 200
                                everything[i].spritecut.rect.x = 230
                                everything[i].spritecut.rect.y = 200
                                everything[i].x, everything[i].y = 230, 200
                                everything[i].start_to_cut = True
                                everything[i].drawing = True
                                temp_product = i
                            break
                else:
                    if everything[temp_product].drawing:
                        everything[temp_product].start_to_cut = True
                    elif everything[temp_product].sprite.rect.collidepoint(event.pos) and 'cut_' in everything[
                        temp_product].name:
                        everything[temp_product].sprite.rect.x = 0
                        everything[temp_product].sprite.rect.y = positions[temp_product]
                        everything[temp_product].start_to_cut = False
                        everything[temp_product].drawing = False
                        temp_product = -1

            if event.type == pygame.MOUSEBUTTONUP:
                if temp_product != -1:
                    if everything[temp_product].drawing:
                        everything[temp_product].start_to_cut = False
                        everything[temp_product].spritecut.image = everything[temp_product].board
                        everything[temp_product].spritecut.mask = pygame.mask.from_surface(
                            everything[temp_product].spritecut.image)
                        everything[temp_product].check_cut()

            if event.type == pygame.MOUSEMOTION and everything[temp_product] != -1:
                if everything[temp_product].drawing:
                    if everything[temp_product].start_to_cut:
                        pygame.draw.circle(everything[temp_product].board, (0, 0, 255), (
                            event.pos[0] - everything[temp_product].x, event.pos[1] - everything[temp_product].y),
                                           5)
                        everything[temp_product].spritecut.image = everything[temp_product].board

        timetext = font.render(str(time).split('.')[0], 1, (255, 255, 255))
        time_rect = timetext.get_rect()
        time_rect.x = 450
        time_rect.y = 5
        screen.blit(string_rendered, intro_rect)
        screen.blit(timetext, time_rect)
        screen.blit(recepy, recepy_rect)
        for product in everything:
            product.product.draw(screen)
            if 'cut' in product.name:
                check_done += 1
            if product.drawing:
                product.lines.draw(screen)
                product.already_cut.draw(screen)
        all_sprites.update()
        all_sprites.draw(screen)
        if check_done >= len(everything):
            if check_done == len(everything):
                create_particles((250, 0))
                score += time
            font = pygame.font.SysFont('verdana', 20)
            string_rendered = font.render('Перейти к следующему шагу', 1, (255, 255, 255))
            intro_rect = string_rendered.get_rect()
            intro_rect.x = 5
            intro_rect.y = 470
            check_done = len(everything) + 1
        if check_done < len(everything):
            time -= 0.1
        if time <= 0:
            cut_running = False
            start_running = True
            game_running = False
            lose()
            return False
        pygame.display.flip()
        clock.tick(50)


def oven_stage(things_to_place):
    global running, start_running, game_running, maxscore, score
    oven = Oven(things_to_place[0].split()[0] + '.png')
    oven_running = True
    font = pygame.font.SysFont('verdana', 20)
    string_rendered = font.render('', 1, (255, 255, 255))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = 10
    intro_rect.y = 200
    time = 100
    maxscore += time

    recepy = font.render('Приготовь блюдо в духовке', 1, (255, 0, 0))
    recepy_rect = recepy.get_rect()
    recepy_rect.x = 10
    recepy_rect.y = 5

    timetext = font.render(str(time), 1, (255, 255, 255))
    time_rect = timetext.get_rect()
    time_rect.x = 470
    time_rect.y = 5
    while oven_running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                oven_running = False
                running = False
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if oven.level_done >= 1:
                    if intro_rect.collidepoint(event.pos):
                        return True
                if oven.sprite.rect.collidepoint(event.pos):
                    oven.update(2)
                elif oven.buttonsprite.rect.collidepoint(event.pos):
                    oven.update(1)
                elif oven.ovensprite.rect.collidepoint(event.pos):
                    oven.update(0)
        if oven.level_done == 1:
            create_particles((250, 0))
            font = pygame.font.SysFont('verdana', 20)
            string_rendered = font.render('Перейти к следующему шагу', 1, (255, 255, 255))
            intro_rect = string_rendered.get_rect()
            score += time
            intro_rect.x = 5
            intro_rect.y = 470
            oven.level_done = 2
        timetext = font.render(str(time).split('.')[0], 1, (255, 255, 255))
        time_rect = timetext.get_rect()
        time_rect.x = 460
        time_rect.y = 5
        if oven.level_done == 0:
            time -= 0.1
        if time <= 0:
            oven_running = False
            start_running = True
            game_running = False
            lose()
            return False
        all_sprites.update()
        screen.fill((0, 0, 0))
        oven.ovengroup.draw(screen)
        oven.buttongroup.draw(screen)
        oven.product.draw(screen)
        all_sprites.draw(screen)
        screen.blit(string_rendered, intro_rect)
        screen.blit(timetext, time_rect)
        screen.blit(recepy, recepy_rect)
        pygame.display.flip()
        clock.tick(50)


def stuffing_stage(things_to_place):
    global running, start_running, game_running, maxscore, score, stuff_running
    stuff_running = True

    tostuff = things_to_place[0]
    stuffs = things_to_place[1::]

    chicken = ProductToStuff(tostuff.split()[0] + ".png", 200, 200, 300, 300, 240, 150)

    font = pygame.font.SysFont('verdana', 20)
    string_rendered = font.render('', 1, (255, 255, 255))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = 10
    intro_rect.y = 200

    recepy = font.render('Нафаршируй своё блюдо', 1, (255, 0, 0))
    recepy_rect = recepy.get_rect()
    recepy_rect.x = 10
    recepy_rect.y = 5

    startpos = 30
    everything = []
    done = 0

    for i in stuffs:
        st = i.split()
        product = Stuffing(st[0] + '.png', int(st[1]), int(st[2]), 0, startpos, chicken)
        startpos += int(st[2]) + 10
        everything.append(product)

    time = 20 * len(everything)
    maxscore += time
    fon = pygame.transform.scale(load_image('table.jpg'), [500, 500])

    timetext = font.render(str(time), 1, (255, 255, 255))
    time_rect = timetext.get_rect()
    time_rect.x = 470
    time_rect.y = 51

    while stuff_running:
        screen.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and done > 0:
                if intro_rect.collidepoint(event.pos):
                    return True
            if done == 1:
                create_particles((250, 0))
            chicken.check_event(event)

        timetext = font.render(str(time).split('.')[0], 1, (255, 255, 255))
        time_rect = timetext.get_rect()
        time_rect.x = 460
        time_rect.y = 5
        if done == 0:
            time -= 0.1
        if time <= 0:
            stuff_running = False
            start_running = True
            game_running = False
            lose()
            return False

        if len(chicken.list) == 0:
            done += 1
            if done == 1:
                score += time
                print(score)
            font = pygame.font.SysFont('verdana', 20)
            string_rendered = font.render('Перейти к следующему шагу', 1, (255, 255, 255))
            intro_rect = string_rendered.get_rect()
            intro_rect.x = 5
            intro_rect.y = 470
        screen.blit(string_rendered, intro_rect)
        screen.blit(timetext, time_rect)
        screen.blit(recepy, recepy_rect)
        chicken.draw_on_screen()
        pygame.display.flip()
        clock.tick(50)


def pour_in_stage(things_to_place):
    global running, maxscore, score, game_running, start_running
    pour_in_running = True
    font = pygame.font.SysFont('verdana', 20)
    string_rendered = font.render('', 1, (255, 255, 255))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = 10
    intro_rect.y = 200

    st = things_to_place[0].split()
    if st[5] == 'salt':
        recepy = font.render('Посоли курицу', 1, (255, 0, 0))
    elif st[5] == 'pepper':
        recepy = font.render('Поперчи курицу', 1, (255, 0, 0))
    recepy_rect = recepy.get_rect()
    recepy_rect.x = 10
    recepy_rect.y = 5

    pour_in_products = pygame.sprite.Group()
    time = 300

    startpos = 30
    everything = []
    positions = []

    pour_in_time = 30
    product = ProductToPourIn(pygame.transform.scale(load_image(st[0] + '.png', -1), (int(st[1]), int(st[2]))),
                              int(st[3]), int(st[4]))
    product_to_pour_in = pygame.sprite.GroupSingle(product.sprite)
    pour_in = PourInProduct(pygame.transform.scale(load_image(st[5] + '.png', -1), (44, 80)), 1, 1, int(st[6]),
                            int(st[7]), pour_in_products)

    everything.append(product)

    maxscore += time
    fon = pygame.transform.scale(load_image('table.jpg'), [500, 500])

    timetext = font.render(str(time), 1, (255, 255, 255))
    time_rect = timetext.get_rect()
    time_rect.x = 470
    time_rect.y = 51

    temp_product = -1
    check_done = 0

    while pour_in_running:
        if check_done < 4:
            check_done = 0
        screen.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pour_in_running = False
                running = False
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pour_in.rect.collidepoint(event.pos):
                    if not pour_in.pouring_in:
                        pour_in_products.remove(pour_in)
                        pour_in = PourInProduct(
                            pygame.transform.scale(load_image(st[5] + '2' + '.png', -1), (226, 180)), 2, 1,
                            int(st[3]) + int(st[1]) // 2 - 50, int(st[4]) - 120, pour_in_products)
                        pour_in.pouring_in = True
        pour_in_products.update()
        if pour_in.pouring_in:
            pour_in_time -= 1
        if pour_in_time <= 0:
            pour_in_products.remove(pour_in)
            pour_in = PourInProduct(pygame.transform.scale(load_image(st[5] + '.png', -1), (44, 80)), 1, 1, int(st[6]),
                                    int(st[7]), pour_in_products)
            pour_in.pouring_in = False
            pour_in_time = 30

        timetext = font.render(str(time).split('.')[0], 1, (255, 255, 255))
        time_rect = timetext.get_rect()
        time_rect.x = 450
        time_rect.y = 5
        screen.blit(string_rendered, intro_rect)
        screen.blit(timetext, time_rect)
        screen.blit(recepy, recepy_rect)

        pour_in_products.draw(screen)
        product_to_pour_in.draw(screen)

        all_sprites.update()
        # all_sprites.draw(screen)
        if check_done >= len(everything):
            if check_done == len(everything):
                create_particles((250, 0))
                score += time
            font = pygame.font.SysFont('verdana', 20)
            string_rendered = font.render('Перейти к следующему шагу', 1, (255, 255, 255))
            intro_rect = string_rendered.get_rect()
            intro_rect.x = 5
            intro_rect.y = 470
            check_done = len(everything) + 1
        if check_done < len(everything):
            time -= 0.1
        if time <= 0:
            pour_in_running = False
            start_running = True
            game_running = False
            lose()
            return False
        pygame.display.flip()
        clock.tick(50)


def start_screen():
    global running, start_running, rules_running, menu_running
    fon = pygame.transform.scale(load_image('main_wall.png'), (500, 500))

    buttongroup = pygame.sprite.Group()

    rules_button = load_image('rules.png', -1)
    rules_button = pygame.transform.scale(rules_button, [150, 70])
    rulesbuttonsprite = pygame.sprite.Sprite()
    rulesbuttonsprite.image = rules_button
    rulesbuttonsprite.rect = rulesbuttonsprite.image.get_rect()
    buttongroup.add(rulesbuttonsprite)
    rulesbuttonsprite.rect.x = 10
    rulesbuttonsprite.rect.y = 300

    menu_button = load_image('menu.png', -1)
    menu_button = pygame.transform.scale(menu_button, [120, 60])
    menubuttonsprite = pygame.sprite.Sprite()
    menubuttonsprite.image = menu_button
    menubuttonsprite.rect = menubuttonsprite.image.get_rect()
    buttongroup.add(menubuttonsprite)
    menubuttonsprite.rect.x = 10
    menubuttonsprite.rect.y = 370

    start_running = True
    while start_running:
        screen.blit(fon, (0, 0))
        buttongroup.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start_running = False
                running = False
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if rulesbuttonsprite.rect.collidepoint(event.pos):
                    start_running = False
                    rules_running = True
                    return False
                elif menubuttonsprite.rect.collidepoint(event.pos):
                    start_running = False
                    menu_running = True
                    return False
        pygame.display.flip()
        clock.tick(50)
    return True


def rules():
    global running, start_running, rules_running

    fon = pygame.transform.scale(load_image('rules.jpg'), (500, 500))
    screen.blit(fon, (0, 0))

    buttongroup = pygame.sprite.Group()

    main_button = load_image('main.png', -1)
    main_button = pygame.transform.scale(main_button, [150, 50])
    mainbuttonsprite = pygame.sprite.Sprite()
    mainbuttonsprite.image = main_button
    mainbuttonsprite.rect = mainbuttonsprite.image.get_rect()
    buttongroup.add(mainbuttonsprite)
    mainbuttonsprite.rect.x = 10
    mainbuttonsprite.rect.y = 450
    buttongroup.draw(screen)

    while rules_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rules_running = False
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mainbuttonsprite.rect.collidepoint(event.pos):
                    start_running = True
                    rules_running = False
                    return False
        pygame.display.flip()
        clock.tick(50)


def menu():
    global running, start_running, menu_running, game_running
    fname = 'menu_info.csv'
    menu, dish_amount, blocked = info_from_csv(os.path.join('data', fname))
    merge_images(menu)

    image = pygame.image.load(os.path.join('data', 'menupage.png'))
    level_pic = pygame.image.load(os.path.join('data', 'menu_levels.png')).convert_alpha()
    top = pygame.image.load(os.path.join('data', 'menutop.png'))
    bottom = pygame.image.load(os.path.join('data', 'menubot.png'))
    scroll_y = 180

    buttongroup = pygame.sprite.Group()

    main_button = load_image('main.png', -1)
    main_button = pygame.transform.scale(main_button, [150, 50])
    mainbuttonsprite = pygame.sprite.Sprite()
    mainbuttonsprite.image = main_button
    mainbuttonsprite.rect = mainbuttonsprite.image.get_rect()
    buttongroup.add(mainbuttonsprite)
    mainbuttonsprite.rect.x = 10
    mainbuttonsprite.rect.y = 450

    while menu_running:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                menu_running = False
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mainbuttonsprite.rect.collidepoint(event.pos):
                    start_running = True
                    menu_running = False
                    game_running = False
                    return False
                if event.button == 1:
                    pos_y = pygame.mouse.get_pos()[1]
                    if 160 < pos_y < 420:
                        dish_number = abs(scroll_y - pos_y) // 60
                        if dish_number in blocked:
                            print('choose another')
                        else:
                            start_running = False
                            menu_running = False
                            game_running = True
                            return dish_number
                if event.button == 4:
                    scroll_y = min(scroll_y + 15, 178)
                if event.button == 5:
                    scroll_y = max(scroll_y - 15, - 60 * (dish_amount - 4) + 180)

        screen.blit(image, (0, 0))
        screen.blit(level_pic, (0, scroll_y))
        screen.blit(top, (0, 0))
        screen.blit(bottom, (0, 429))
        buttongroup.draw(screen)
        pygame.display.flip()
        clock.tick(50)


def ending():
    global running, start_running, namelevel, maxscore, score

    fon = pygame.transform.scale(load_image('win.jpg'), (500, 500))
    dish = pygame.transform.scale(load_image(str(namelevel) + 'result.png', -1), (250, 250))

    screen.blit(fon, (0, 0))
    screen.blit(dish, (110, 100))

    font = pygame.font.SysFont('verdana', 20)
    string_rendered = font.render('Cчёт: {}/{}'.format(str(score).split('.')[0], str(maxscore).split('.')[0]), 1,
                                  (255, 255, 255))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = 170
    intro_rect.y = 100

    res_score = score / maxscore
    if res_score >= 0.75:
        pass
    elif res_score > 0.5 and res_score < 0.75:
        pass
    else:
        pass

    screen.blit(string_rendered, intro_rect)

    buttongroup = pygame.sprite.Group()

    end_running = True

    main_button = load_image('main.png', -1)
    main_button = pygame.transform.scale(main_button, [150, 50])
    mainbuttonsprite = pygame.sprite.Sprite()
    mainbuttonsprite.image = main_button
    mainbuttonsprite.rect = mainbuttonsprite.image.get_rect()
    buttongroup.add(mainbuttonsprite)
    mainbuttonsprite.rect.x = 10
    mainbuttonsprite.rect.y = 450
    buttongroup.draw(screen)

    while end_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_running = False
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mainbuttonsprite.rect.collidepoint(event.pos):
                    pygame.mixer.music.load('data/rhapsody.mp3')
                    pygame.mixer.music.set_volume(0.4)
                    pygame.mixer.music.play(loops=-1)
                    namelevel = ''
                    start_running = True
                    end_running = False
                    return False
        pygame.display.flip()
        clock.tick(50)


def lose():
    global running, start_running, namelevel

    fon = pygame.transform.scale(load_image('lose.jpg'), (500, 500))
    screen.blit(fon, (0, 0))

    pygame.mixer.music.load('data/directedby.mp3')
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(loops=-1)

    buttongroup = pygame.sprite.Group()

    end_running = True

    main_button = load_image('main.png', -1)
    main_button = pygame.transform.scale(main_button, [150, 50])
    mainbuttonsprite = pygame.sprite.Sprite()
    mainbuttonsprite.image = main_button
    mainbuttonsprite.rect = mainbuttonsprite.image.get_rect()
    buttongroup.add(mainbuttonsprite)
    mainbuttonsprite.rect.x = 10
    mainbuttonsprite.rect.y = 450
    buttongroup.draw(screen)

    while end_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_running = False
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mainbuttonsprite.rect.collidepoint(event.pos):
                    pygame.mixer.music.load('data/rhapsody.mp3')
                    pygame.mixer.music.set_volume(0.4)
                    pygame.mixer.music.play(loops=-1)
                    namelevel = ''
                    start_running = True
                    end_running = False
                    return False
        pygame.display.flip()
        clock.tick(50)


pygame.mixer.music.load('data/rhapsody.mp3')
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(loops=-1)
start_running = True
rules_running = False
menu_running = False
game_running = False
stuff_running = False
level_number = -1
namelevel = ''

maxscore = 0
score = 0

while running:
    if start_running:
        start_screen()
        continue
    if rules_running:
        rules()
        continue
    if menu_running:
        a = menu()
        if game_running:
            namelevel = a
        continue
    if game_running:
        pygame.mixer.music.load('data/vitas.mp3')
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(loops=-1)
        stage, things_to_place = load_level(str(namelevel) + '.txt')
        for i in range(len(stage)):
            if stage[i] == 'cut':
                if not cut_stage(things_to_place[i]):
                    break
            if stage[i] == 'oven':
                if not oven_stage(things_to_place[i]):
                    break
            if stage[i] == 'stuff':
                if not stuffing_stage(things_to_place[i]):
                    break
            if stage[i] == 'pour_in':
                if not pour_in_stage(things_to_place[i]):
                    break
            if stage[i] == 'end':
                game_running = False
                ending()
pygame.quit()
