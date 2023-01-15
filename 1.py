import pygame
import os
import sys

# or (300 < pygame.mouse.get_pos()[0] < 500 and 460 < pygame.mouse.get_pos()[1] < 500)
# (300 < pygame.mouse.get_pos()[0] < 500 and 390 < pygame.mouse.get_pos()[1] < 450)
FPS = 100
size = WIDTH, HEIGHT = 800, 600
screen_rect = (0, 0, WIDTH, HEIGHT)
clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode(size)


def start_game():
    global tanks_sprites, bullet_sprites
    pygame.display.set_caption("Tanks")
    player1, player2, level_x, level_y = generate_level(load_level('level01.txt'))
    size = (level_x + 1) * tile_width, (level_y + 1) * tile_height
    screen = pygame.display.set_mode(size)
    move = False
    last_event = None
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                move = True
                last_event = event
            if event.type == pygame.KEYUP:
                move = False
            tanks_sprites.update(event)
        screen.fill((110, 110, 110))
        if move:
            tanks_sprites.update(last_event)
        tanks_sprites.draw(screen)
        bullet_sprites.update()
        bullet_sprites.draw(screen)
        all_sprites.update()
        screen.fill((255, 255, 255))
        all_sprites.draw(screen)
        tanks_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
        pygame.display.flip()


def end_game():
    pygame.quit()
    quit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def print_text(massage, x, y, font_color=(255, 255, 255), font_type='data/PINGPONG.TTF', font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(massage, True, font_color)
    screen.blit(text, (x, y))


def cards_menu():
    fon = pygame.transform.scale(load_image('menu_fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    show = True
    while show:
        pygame.display.set_caption("Menu")
        card1 = Button(150, 150, (255, 0, 0), (150, 0, 0))
        card2 = Button(150, 150, (255, 0, 0), (150, 0, 0))
        card3 = Button(150, 150, (255, 0, 0), (150, 0, 0))
        card4 = Button(150, 150, (255, 0, 0), (150, 0, 0))
        card5 = Button(150, 150, (255, 0, 0), (150, 0, 0))
        menu = pygame.Surface(size)
        screen.blit(menu, (0, 0))
        card1.draw(100, 100, 'Card1', start_game)
        card2.draw(300, 100, 'Card2', start_game)
        card3.draw(500, 100, 'Card3', start_game)
        card4.draw(100, 300, 'Card4', start_game)
        card5.draw(300, 300, 'Card5', start_game)
        # print(card_sprites.sprites())
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                show = False
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and \
                    (0 < pygame.mouse.get_pos()[0] < 800 and 460 < pygame.mouse.get_pos()[1] < 500):
                return


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '0'), level_map))


tile_images = {
    'wall': load_image('brick_cell.png'),
    'empty': load_image('null_cell.png'),
    'indestructible_wall': load_image('iron_cell.png')
}

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        if tile_type == 'wall':
            self.add(wall_group)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Button:
    def __init__(self, width, height, color, active_color):
        self.width = width
        self.height = height
        self.color = color
        self.active_color = active_color

    def draw(self, x, y, massage, action=None):
        mouse_clicked = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if x < mouse_pos[0] < (x + self.width) and y < mouse_pos[1] < (y + self.height):
            pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))
            if mouse_clicked[0] == 1:
                if action is not None:
                    action()
        else:
            pygame.draw.rect(screen, self.color, (x, y, self.width, self.height))
        print_text(massage, x - len(massage) * 7 + self.width // 2, y + self.height // 3)


class Tank_2_pdrl(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(tanks_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.create_mask()
        self.rect = self.rect.move(x, y)
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 200
        self.tick_time = 0
        self.bullet_delay = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def create_mask(self):
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *args):
        clock = pygame.time.get_ticks()
        if args and args[0].type == pygame.KEYDOWN:
            self.tick_time += 1
            if self.tick_time % 10 == 1:
                self.tick_time %= 10
            if pygame.key.get_pressed()[pygame.K_UP]:
                self.cur_frame = 0
                self.create_mask()
                self.image = self.frames[self.cur_frame]
                self.rect.y -= 1
            elif pygame.key.get_pressed()[pygame.K_DOWN]:
                self.cur_frame = 1
                self.create_mask()
                self.image = self.frames[self.cur_frame]
                self.rect.y += 1
            elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                self.cur_frame = 2
                self.create_mask()
                self.image = self.frames[self.cur_frame]
                self.rect.x += 1
            elif pygame.key.get_pressed()[pygame.K_LEFT]:
                self.cur_frame = 3
                self.create_mask()
                self.image = self.frames[self.cur_frame]
                self.rect.x -= 1
            elif pygame.key.get_pressed()[pygame.K_KP0]:
                if clock - self.bullet_delay >= 500:
                    self.bullet_delay = clock
                    if self.cur_frame == 0:
                        Shot(load_image("shot_sprite.png"), 6, 4, self.rect.x + 11, self.rect.y - 28, self.cur_frame)
                        Bullet(load_image("Bullet_sprite.png"), 4, 1,
                               self.rect.x + 18, self.rect.y - 14, self.cur_frame)
                    elif self.cur_frame == 1:
                        Shot(load_image("shot_sprite.png"), 6, 4, self.rect.x + 11, self.rect.y + 50, self.cur_frame)
                        Bullet(load_image("Bullet_sprite.png"), 4, 1,
                               self.rect.x + 18, self.rect.y + 50, self.cur_frame)
                    elif self.cur_frame == 2:
                        Shot(load_image("shot_sprite.png"), 6, 4, self.rect.x + 50, self.rect.y + 11, self.cur_frame)
                        Bullet(load_image("Bullet_sprite.png"), 4, 1,
                               self.rect.x + 50, self.rect.y + 18, self.cur_frame)
                    elif self.cur_frame == 3:
                        Shot(load_image("shot_sprite.png"), 6, 4, self.rect.x - 28, self.rect.y + 11, self.cur_frame)
                        Bullet(load_image("Bullet_sprite.png"), 4, 1,
                               self.rect.x - 14, self.rect.y + 18, self.cur_frame)


class Tank_WASD(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(tanks_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.create_mask()
        self.rect = self.rect.move(x, y)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 150
        self.tick_time = 0
        self.bullet_delay = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def create_mask(self):
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *args):
        clock = pygame.time.get_ticks()
        if args and args[0].type == pygame.KEYDOWN:
            self.tick_time += 1
            if self.tick_time % 10 == 1:
                self.tick_time %= 10
            if pygame.key.get_pressed()[pygame.K_w]:
                self.cur_frame = 0
                self.create_mask()
                self.image = self.frames[self.cur_frame]
                self.rect.y -= 1
            elif pygame.key.get_pressed()[pygame.K_s]:
                self.cur_frame = 1
                self.create_mask()
                self.image = self.frames[self.cur_frame]
                self.rect.y += 1
            elif pygame.key.get_pressed()[pygame.K_d]:
                self.cur_frame = 2
                self.create_mask()
                self.image = self.frames[self.cur_frame]
                self.rect.x += 1
            elif pygame.key.get_pressed()[pygame.K_a]:
                self.cur_frame = 3
                self.create_mask()
                self.image = self.frames[self.cur_frame]
                self.rect.x -= 1
            elif pygame.key.get_pressed()[pygame.K_SPACE]:
                if clock - self.bullet_delay >= 500:
                    self.bullet_delay = clock
                    if self.cur_frame == 0:
                        Shot(load_image("shot_sprite.png"), 6, 4, self.rect.x + 11, self.rect.y - 28, self.cur_frame)
                        Bullet(load_image("Bullet_sprite.png"), 4, 1,
                               self.rect.x + 18, self.rect.y - 14, self.cur_frame)
                    elif self.cur_frame == 1:
                        Shot(load_image("shot_sprite.png"), 6, 4, self.rect.x + 11, self.rect.y + 50, self.cur_frame)
                        Bullet(load_image("Bullet_sprite.png"), 4, 1,
                               self.rect.x + 18, self.rect.y + 50, self.cur_frame)
                    elif self.cur_frame == 2:
                        Shot(load_image("shot_sprite.png"), 6, 4, self.rect.x + 50, self.rect.y + 11, self.cur_frame)
                        Bullet(load_image("Bullet_sprite.png"), 4, 1,
                               self.rect.x + 50, self.rect.y + 18, self.cur_frame)
                    elif self.cur_frame == 3:
                        Shot(load_image("shot_sprite.png"), 6, 4, self.rect.x - 28, self.rect.y + 11, self.cur_frame)
                        Bullet(load_image("Bullet_sprite.png"), 4, 1,
                               self.rect.x - 14, self.rect.y + 18, self.cur_frame)


class Shot(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, cur_frame):
        super().__init__(bullet_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = cur_frame
        self.cur_frame_r = 0
        self.image = self.frames[self.cur_frame][self.cur_frame_r]
        self.rect = self.rect.move(x, y)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.tick_time = 1

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            frames_rows = []
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                frames_rows.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
            self.frames.append(frames_rows)

    def update(self, *args):
        if not self.tick_time % 10:
            self.tick_time = 1
            self.cur_frame_r = (self.cur_frame_r + 1) % len(self.frames[self.cur_frame])
            self.image = self.frames[self.cur_frame][self.cur_frame_r]
            if self.cur_frame_r == 5:
                self.kill()
        else:
            self.tick_time += 1


class Bullet(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, cur_frame):
        super().__init__(bullet_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = cur_frame
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # self.tick_time = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, *args):
        if not self.rect.colliderect(screen_rect) or pygame.sprite.collide_mask(self, tanks_sprites.sprites()[0]) \
                or pygame.sprite.collide_mask(self, tanks_sprites.sprites()[1]):
            self.kill()
        else:
            #     self.tick_time += 1
            # if self.tick_time % 3 == 1:
            #     self.tick_time %= 3
            if self.cur_frame == 0:
                self.rect.y -= 2
            elif self.cur_frame == 1:
                self.rect.y += 2
            elif self.cur_frame == 2:
                self.rect.x += 2
            elif self.cur_frame == 3:
                self.rect.x -= 2


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    while True:
        button_sologame = Button(200, 40, (255, 0, 0), (100, 0, 0))
        button_sologame.draw(300, 390, '1 Player')

        button_pvpgame = Button(200, 40, (255, 0, 0), (100, 0, 0))
        button_pvpgame.draw(300, 450, '2 Players', cards_menu)

        button_build = Button(200, 40, (255, 0, 0), (100, 0, 0))
        button_build.draw(300, 510, 'Building')

        button_exit = Button(100, 40, (0, 0, 0), (50, 50, 50))
        button_exit.draw(699, 559, 'Exit', end_game)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()


def generate_level(level):
    tank_1, tank_2, x, y = None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '0':
                Tile('empty', x, y)
            elif level[y][x] == '1':
                Tile('wall', x, y)
            elif level[y][x] == 'T':
                Tile('empty', x, y)
                tank_1 = Tank_WASD(load_image("yellow_tanks.png"), 4, 1, 50, 50)
            elif level[y][x] == 't':
                Tile('empty', x, y)
                tank_2 = Tank_2_pdrl(load_image("yellow_tanks.png"), 4, 1, 50, 50)
            elif level[y][x] == '2':
                Tile('indestructible_wall', x, y)
    return tank_1, tank_2, x, y


if __name__ == '__main__':
    tiles_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    wall_group = pygame.sprite.Group()
    bullet_sprites = pygame.sprite.Group()
    tanks_sprites = pygame.sprite.Group()

    start_screen()
    cards_menu()
    start_game()
pygame.quit()
