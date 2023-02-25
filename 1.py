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
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
icon = pygame.image.load("data/icon.png")
pygame.display.set_icon(icon)
pygame.mixer.music.load("data/Fon_music.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)
button_sound = pygame.mixer.Sound("data/mouse-click.mp3")
Map_name = ''
fullscreen = False


def start_game():
    global player1, player2
    pygame.display.set_caption("Tanks")
    player1, player2, level_x, level_y = generate_level(load_level(f'{Map_name}.txt'))
    size = (level_x + 1) * tile_width, (level_y + 1) * tile_height
    screen = pygame.display.set_mode(size)
    move = False
    last_event = None
    running = True
    while running:
        for i in leaf_wall_group.sprites():
            screen.fill((50, 50, 50), i.rect)
        all_sprites.update()
        all_sprites.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                move = True
                last_event = event
            if event.type == pygame.KEYUP:
                move = True
                last_event = event
            tanks_sprites.update(event)
        if move:
            tanks_sprites.update(last_event)
        tanks_sprites.draw(screen)
        bullet_sprites.update()
        bullet_sprites.draw(screen)
        leaf_wall_group.draw(screen)
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


def maps_menu():
    fon = pygame.transform.scale(load_image('menu_fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    show = True
    while show:
        pygame.display.set_caption("Menu")
        map1 = Button(150, 150, (255, 0, 0), (150, 0, 0))
        map2 = Button(150, 150, (255, 0, 0), (150, 0, 0))
        map3 = Button(150, 150, (255, 0, 0), (150, 0, 0))
        map4 = Button(150, 150, (255, 0, 0), (150, 0, 0))
        map5 = Button(150, 150, (255, 0, 0), (150, 0, 0))
        menu = pygame.Surface(size)
        screen.blit(menu, (0, 0))
        map1.draw(100, 100, 'Map1', start_game)
        map2.draw(300, 100, 'Map2', start_game)
        map3.draw(500, 100, 'Map3', start_game)
        map4.draw(100, 300, 'Map4', start_game)
        map5.draw(300, 300, 'Map5', start_game)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                show = False
                pygame.quit()
                quit()


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
    'indestructible_wall': load_image('iron_cell.png'),
    'water_wall': load_image('water_cell.png'),
    'leaf_wall': load_image('leaf_cell.png')
}

tile_width = tile_height = 25


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        if tile_type == 'wall':
            self.add(wall_group)
        if tile_type == 'indestructible_wall':
            self.add(indestructible_wall_group)
        if tile_type == 'water_wall':
            self.add(water_wall_group)
        if tile_type == 'leaf_wall':
            self.add(leaf_wall_group)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Button:
    def __init__(self, width, height, color, active_color):
        self.width = width
        self.height = height
        self.color = color
        self.active_color = active_color

    def draw(self, x, y, massage, action=None):
        global Map_name
        Map_name = massage
        mouse_clicked = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if x < mouse_pos[0] < (x + self.width) and y < mouse_pos[1] < (y + self.height):
            pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))
            if mouse_clicked[0] == 1:
                if action is not None:
                    pygame.mixer.Sound.play(button_sound)
                    action()
        else:
            pygame.draw.rect(screen, self.color, (x, y, self.width, self.height))
        print_text(massage, x - len(massage) * 7 + self.width // 2, y + self.height // 3)


class Tank_2_pdrl(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, x_pos, y_pos):
        super().__init__(tanks_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.create_mask()
        self.rect = self.rect.move(x, y)
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.tick_time = 0
        self.bullet_delay = 0
        self.count_shot = 0

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

    def count_live(self):
        self.count_shot += 1
        if self.count_shot == 3:
            self.Tank_kill()

    def Tank_kill(self):
        self.kill()
        end_screen("Yellow_win")

    def update(self, *args):
        get_tick = pygame.time.get_ticks()
        if args and args[0].type in [pygame.KEYDOWN, pygame.KEYUP]:
            if pygame.key.get_pressed()[pygame.K_UP]:
                self.cur_frame = 0
                self.create_mask()
                self.image = self.frames[self.cur_frame]
                if self.rect.y > 0 and not pygame.sprite.spritecollideany(player2, wall_group) \
                        and not pygame.sprite.spritecollideany(player2, indestructible_wall_group) \
                        and not pygame.sprite.spritecollideany(player2, water_wall_group):
                    self.rect.y -= 1
                    if pygame.sprite.spritecollideany(player2, wall_group) \
                            or pygame.sprite.spritecollideany(player2, indestructible_wall_group) \
                            or pygame.sprite.spritecollideany(player2, water_wall_group):
                        self.rect.y += 1
            elif pygame.key.get_pressed()[pygame.K_DOWN]:
                self.cur_frame = 1
                self.create_mask()
                self.image = self.frames[self.cur_frame]
                if self.rect.y < 550 and not pygame.sprite.spritecollideany(player2, wall_group) \
                        and not pygame.sprite.spritecollideany(player2, indestructible_wall_group) \
                        and not pygame.sprite.spritecollideany(player2, water_wall_group):
                    self.rect.y += 1
                    if pygame.sprite.spritecollideany(player2, wall_group) \
                            or pygame.sprite.spritecollideany(player2, indestructible_wall_group) \
                            or pygame.sprite.spritecollideany(player2, water_wall_group):
                        self.rect.y -= 1
            elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                self.cur_frame = 2
                self.create_mask()
                self.image = self.frames[self.cur_frame]
                if self.rect.x < 550 and not pygame.sprite.spritecollideany(player2, wall_group) \
                        and not pygame.sprite.spritecollideany(player2, indestructible_wall_group) \
                        and not pygame.sprite.spritecollideany(player2, water_wall_group):
                    self.rect.x += 1
                    if pygame.sprite.spritecollideany(player2, wall_group) \
                            or pygame.sprite.spritecollideany(player2, indestructible_wall_group) \
                            or pygame.sprite.spritecollideany(player2, water_wall_group):
                        self.rect.x -= 1
            elif pygame.key.get_pressed()[pygame.K_LEFT]:
                self.cur_frame = 3
                self.create_mask()
                self.image = self.frames[self.cur_frame]
                if self.rect.x > 0 and not pygame.sprite.spritecollideany(player2, wall_group) \
                        and not pygame.sprite.spritecollideany(player2, indestructible_wall_group) \
                        and not pygame.sprite.spritecollideany(player2, water_wall_group):
                    self.rect.x -= 1
                    if pygame.sprite.spritecollideany(player2, wall_group) \
                            or pygame.sprite.spritecollideany(player2, indestructible_wall_group) \
                            or pygame.sprite.spritecollideany(player2, water_wall_group):
                        self.rect.x += 1
            if pygame.key.get_pressed()[pygame.K_KP0]:
                if get_tick - self.bullet_delay >= 750:
                    self.bullet_delay = get_tick
                    if self.cur_frame == 0:
                        Shot(load_image("shot_sprite.png"), 6, 4, self.rect.x + 11, self.rect.y - 28, self.cur_frame)
                        Bullet(load_image("Bullet_sprite.png"), 4, 1,
                               self.rect.x + 18, self.rect.y - 14 - 5, self.cur_frame)
                    elif self.cur_frame == 1:
                        Shot(load_image("shot_sprite.png"), 6, 4, self.rect.x + 11, self.rect.y + 50, self.cur_frame)
                        Bullet(load_image("Bullet_sprite.png"), 4, 1,
                               self.rect.x + 18, self.rect.y + 50 + 5, self.cur_frame)
                    elif self.cur_frame == 2:
                        Shot(load_image("shot_sprite.png"), 6, 4, self.rect.x + 50, self.rect.y + 11, self.cur_frame)
                        Bullet(load_image("Bullet_sprite.png"), 4, 1,
                               self.rect.x + 50 + 5, self.rect.y + 18, self.cur_frame)
                    elif self.cur_frame == 3:
                        Shot(load_image("shot_sprite.png"), 6, 4, self.rect.x - 28, self.rect.y + 11, self.cur_frame)
                        Bullet(load_image("Bullet_sprite.png"), 4, 1,
                               self.rect.x - 14 - 5, self.rect.y + 18, self.cur_frame)


class Tank_WASD(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, x_pos, y_pos):
        super().__init__(tanks_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.create_mask()
        self.rect = self.rect.move(x, y)
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.tick_time = 0
        self.bullet_delay = 0
        self.count_shot = 0

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

    def count_live(self):
        self.count_shot += 1
        if self.count_shot == 3:
            self.Tank_kill()

    def Tank_kill(self):
        self.kill()
        end_screen("Green_win")

    def update(self, *args):
        get_tick = pygame.time.get_ticks()
        if args and args[0].type in [pygame.KEYDOWN, pygame.KEYUP]:
            self.tick_time += 1
            if self.tick_time % 10 == 1:
                self.tick_time %= 10
            if pygame.key.get_pressed()[pygame.K_w]:
                self.cur_frame = 0
                self.create_mask()
                self.image = self.frames[self.cur_frame]
                if self.rect.y > 0 and not pygame.sprite.spritecollideany(player1, wall_group) \
                        and not pygame.sprite.spritecollideany(player1, indestructible_wall_group) \
                        and not pygame.sprite.spritecollideany(player1, water_wall_group):
                    self.rect.y -= 1
                    if pygame.sprite.spritecollideany(player1, wall_group) \
                            or pygame.sprite.spritecollideany(player1, indestructible_wall_group) \
                            or pygame.sprite.spritecollideany(player1, water_wall_group):
                        self.rect.y += 1
            elif pygame.key.get_pressed()[pygame.K_s]:
                self.cur_frame = 1
                self.create_mask()
                self.image = self.frames[self.cur_frame]
                if self.rect.y < 550 and not pygame.sprite.spritecollideany(player1, wall_group) \
                        and not pygame.sprite.spritecollideany(player1, indestructible_wall_group) \
                        and not pygame.sprite.spritecollideany(player1, water_wall_group):
                    self.rect.y += 1
                    if pygame.sprite.spritecollideany(player1, wall_group) \
                            or pygame.sprite.spritecollideany(player1, indestructible_wall_group) \
                            or pygame.sprite.spritecollideany(player1, water_wall_group):
                        self.rect.y -= 1
            elif pygame.key.get_pressed()[pygame.K_d]:
                self.cur_frame = 2
                self.create_mask()
                self.image = self.frames[self.cur_frame]
                if self.rect.x < 550 and not pygame.sprite.spritecollideany(player1, wall_group) \
                        and not pygame.sprite.spritecollideany(player1, indestructible_wall_group) \
                        and not pygame.sprite.spritecollideany(player1, water_wall_group):
                    self.rect.x += 1
                    if pygame.sprite.spritecollideany(player1, wall_group) \
                            or pygame.sprite.spritecollideany(player1, indestructible_wall_group) \
                            or pygame.sprite.spritecollideany(player1, water_wall_group):
                        self.rect.x -= 1
            elif pygame.key.get_pressed()[pygame.K_a]:
                self.cur_frame = 3
                self.create_mask()
                self.image = self.frames[self.cur_frame]
                if self.rect.x > 0 and not pygame.sprite.spritecollideany(player1, wall_group) \
                        and not pygame.sprite.spritecollideany(player1, indestructible_wall_group) \
                        and not pygame.sprite.spritecollideany(player1, water_wall_group):
                    self.rect.x -= 1
                    if pygame.sprite.spritecollideany(player1, wall_group) \
                            or pygame.sprite.spritecollideany(player1, indestructible_wall_group) \
                            or pygame.sprite.spritecollideany(player1, water_wall_group):
                        self.rect.x += 1
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                if get_tick - self.bullet_delay >= 750:
                    self.bullet_delay = get_tick
                    if self.cur_frame == 0:
                        Shot(load_image("shot_sprite.png"), 6, 4, self.rect.x + 11, self.rect.y - 28, self.cur_frame)
                        Bullet(load_image("Bullet_sprite.png"), 4, 1,
                               self.rect.x + 18, self.rect.y - 14 - 5, self.cur_frame)
                    elif self.cur_frame == 1:
                        Shot(load_image("shot_sprite.png"), 6, 4, self.rect.x + 11, self.rect.y + 50, self.cur_frame)
                        Bullet(load_image("Bullet_sprite.png"), 4, 1,
                               self.rect.x + 18, self.rect.y + 50 + 5, self.cur_frame)
                    elif self.cur_frame == 2:
                        Shot(load_image("shot_sprite.png"), 6, 4, self.rect.x + 50, self.rect.y + 11, self.cur_frame)
                        Bullet(load_image("Bullet_sprite.png"), 4, 1,
                               self.rect.x + 50 + 5, self.rect.y + 18, self.cur_frame)
                    elif self.cur_frame == 3:
                        Shot(load_image("shot_sprite.png"), 6, 4, self.rect.x - 28, self.rect.y + 11, self.cur_frame)
                        Bullet(load_image("Bullet_sprite.png"), 4, 1,
                               self.rect.x - 14 - 5, self.rect.y + 18, self.cur_frame)


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

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, *args):
        gets_git_ind_wall = pygame.sprite.spritecollide(self, indestructible_wall_group, False)
        if gets_git_ind_wall:
            for i in gets_git_ind_wall:
                if pygame.sprite.collide_mask(self, i):
                    self.kill()
        gets_git_wall_gr = pygame.sprite.spritecollide(self, wall_group, False)
        if gets_git_wall_gr:
            for i in gets_git_wall_gr:
                if pygame.sprite.collide_mask(self, i):
                    self.kill()
                    Tile('empty', i.rect.x // 25, i.rect.y // 25)
                    i.kill()
        if not self.rect.colliderect(screen_rect):
            self.kill()
        elif pygame.sprite.collide_mask(self, tanks_sprites.sprites()[0]):
            self.kill()
            player1.count_live()
        elif pygame.sprite.collide_mask(self, tanks_sprites.sprites()[1]):
            self.kill()
            player2.count_live()
        # for i in wall_group.sprites():
        #     if pygame.sprite.collide_mask(self, i):
        #         self.kill()
        #         Tile('empty', i.rect.x // 25, i.rect.y // 25)
        #         i.kill()
        else:
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
        button_pvpgame.draw(300, 450, '2 Players', maps_menu)

        button_build = Button(200, 40, (255, 0, 0), (100, 0, 0))
        button_build.draw(300, 510, 'Building')

        button_exit = Button(100, 40, (0, 0, 0), (50, 50, 50))
        button_exit.draw(699, 559, 'Exit', end_game)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()


def end_screen(Tank_win):
    pygame.mixer.music.load("data/Win_music.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
    f()
    screen = pygame.display.set_mode(size)
    fon = pygame.transform.scale(load_image('End.gif'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    if Tank_win == "Yellow_win":
        WINNER = pygame.transform.scale(load_image('Yellow_Win.png'), (200, 200))
        screen.blit(WINNER, (130, 100))
        LOSER = pygame.transform.scale(load_image('Green_Win.png'), (200, 200))
        screen.blit(LOSER, (470, 100))
        print_text("Yellow - WIN", 100, 350, font_size=40, font_color=(255, 255, 0))
        print_text("Green - LOSE", 450, 350, font_size=40, font_color=(0, 255, 0))
    if Tank_win == "Green_win":
        WINNER = pygame.transform.scale(load_image('Green_Win.png'), (200, 200))
        screen.blit(WINNER, (470, 100))
        LOSER = pygame.transform.scale(load_image('Yellow_Win.png'), (200, 200))
        screen.blit(LOSER, (130, 100))
        print_text("Yellow - LOSE", 100, 350, font_size=40, font_color=(255, 255, 0))
        print_text("Green - WIN", 450, 350, font_size=40, font_color=(0, 255, 0))

    while True:
        button_return_menu = Button(200, 40, (130, 130, 130), (100, 0, 0))
        button_return_menu.draw(50, 500, 'Main menu', maps_menu)
        button_return_mainmenu = Button(200, 40, (130, 130, 130), (100, 0, 0))
        button_return_mainmenu.draw(290, 500, 'Start', start_screen)
        button_exit = Button(200, 40, (130, 130, 130), (100, 0, 0))
        button_exit.draw(540, 500, 'Exit', end_game)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
        clock.tick(FPS)


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
                tank_1 = Tank_WASD(load_image("yellow_tanks.png"), 4, 1, 50, 50, x * 25, y * 25)
            elif level[y][x] == 't':
                Tile('empty', x, y)
                tank_2 = Tank_2_pdrl(load_image("green_tanks.png"), 4, 1, 50, 50, x * 25, y * 25)
            elif level[y][x] == '2':
                Tile('indestructible_wall', x, y)
            elif level[y][x] == '3':
                Tile('water_wall', x, y)
            elif level[y][x] == '4':
                Tile('leaf_wall', x, y)
    return tank_1, tank_2, x, y


def f():
    global all_sprites, tiles_group, wall_group, indestructible_wall_group, water_wall_group, leaf_wall_group, bullet_sprites, tanks_sprites
    tiles_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    wall_group = pygame.sprite.Group()
    indestructible_wall_group = pygame.sprite.Group()
    water_wall_group = pygame.sprite.Group()
    leaf_wall_group = pygame.sprite.Group()
    bullet_sprites = pygame.sprite.Group()
    tanks_sprites = pygame.sprite.Group()


if __name__ == '__main__':
    f()
    start_screen()
    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            fullscreen = not fullscreen
            if fullscreen:
                screen = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
            else:
                screen = pygame.display.set_mode(size, pygame.RESIZABLE)
pygame.quit()
