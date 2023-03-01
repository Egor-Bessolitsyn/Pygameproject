import pygame
import os
import sys
from sys import setrecursionlimit
import sqlite3

setrecursionlimit(5000)
FPS = 100
size = WIDTH, HEIGHT = 800, 600
screen_rect = (0, 0, WIDTH, HEIGHT)
clock = pygame.time.Clock()
pygame.init()
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
width = screen.get_width()
height = screen.get_height()
pygame.display.set_caption("Танчики")
icon = pygame.image.load("data/icon.png")
pygame.display.set_icon(icon)
button_sound = pygame.mixer.Sound("data/mouse-click.mp3")
Map_name = ''
green_count = 0
yellow_count = 0
fullscreen = False


def start_game():
    global player1, player2, Last_map
    player1, player2, level_x, level_y = generate_level(load_level(f'{Map_name}.txt'))
    size = (level_x + 1) * tile_width, (level_y + 1) * tile_height
    screen = pygame.display.set_mode(size)
    move = False
    move_shot = False
    last_event = None
    last_shot = None
    running = True
    pygame.event.clear()
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
            if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
                move_shot = True
                last_shot = event
            if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
                move = True
                last_event = event
        if move_shot:
            tanks_sprites.update(last_shot)
            move_shot = False
        if move:
            tanks_sprites.update(last_event)
        tanks_sprites.draw(screen)
        bullet_sprites.update()
        bullet_sprites.draw(screen)
        leaf_wall_group.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()


def restart():
    global Map_name
    Last_map = Map_name
    Map_name = Last_map
    start_game()


def BD(text):
    global yellow_count, green_count
    con = sqlite3.connect('data/Score.db')
    cur = con.cursor()
    if text == 'Yellow_tank':
        cur.execute(("""
                    UPDATE Winstrick
                    SET Win_count = ?
                    WHERE Tank_name = ?
                    """), (yellow_count, 'Yellow_tank'))
        print(yellow_count)
    if text == 'Green_tank':
        cur.execute(("""
            UPDATE Winstrick
            SET Win_count = ?
            WHERE Tank_name = ?
            """), (green_count, 'Green_tank'))
        print(green_count)
    con.commit()
    con.close()


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
    pygame.mixer.music.load("data/Fon_music.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
    fon = pygame.transform.scale(load_image('menu_fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    show = True
    while show:
        map1 = Button(150, 150, (255, 0, 0), (150, 0, 0))
        map2 = Button(150, 150, (255, 0, 0), (150, 0, 0))
        map3 = Button(150, 150, (255, 0, 0), (150, 0, 0))
        map4 = Button(150, 150, (255, 0, 0), (150, 0, 0))
        map5 = Button(150, 150, (255, 0, 0), (150, 0, 0))
        map6 = Button(150, 150, (255, 0, 0), (150, 0, 0))
        menu = pygame.Surface(size)
        screen.blit(menu, (0, 0))
        map1.draw(100, 100, 'Map1', start_game)
        Map1 = pygame.transform.scale(load_image('Map1.png'), (150, 150))
        screen.blit(Map1, (100, 100))
        print_text("Map1", 140, 60, font_color=(255, 255, 100), font_size=35)
        map2.draw(300, 100, 'Map6', start_game)
        Map2 = pygame.transform.scale(load_image('Map6.png'), (150, 150))
        screen.blit(Map2, (300, 100))
        print_text("Map2", 340, 60, font_color=(255, 255, 100), font_size=35)
        map3.draw(500, 100, 'Map7', start_game)
        Map3 = pygame.transform.scale(load_image('Map7.png'), (150, 150))
        screen.blit(Map3, (500, 100))
        print_text("Map3", 540, 60, font_color=(255, 255, 100), font_size=35)
        map4.draw(100, 320, 'Map8', start_game)
        Map4 = pygame.transform.scale(load_image('Map8.png'), (150, 150))
        screen.blit(Map4, (100, 320))
        print_text("Map4", 140, 280, font_color=(255, 255, 100), font_size=35)
        map5.draw(300, 320, 'Map9', start_game)
        Map5 = pygame.transform.scale(load_image('Map9.png'), (150, 150))
        screen.blit(Map5, (300, 320))
        print_text("Map5", 340, 280, font_color=(255, 255, 100), font_size=35)
        map6.draw(500, 320, 'Map10', start_game)
        Map6 = pygame.transform.scale(load_image('Map10.png'), (150, 150))
        screen.blit(Map6, (500, 320))
        print_text("Map6", 540, 280, font_color=(255, 255, 100), font_size=35)
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


def Finding_Path(start, end):
    a = [[0 for i in range(24)] for _ in range(24)]
    for sprt in wall_group.sprites():
        a[sprt.rect[1] // 25][sprt.rect[0] // 25] = 1
    for sprt in indestructible_wall_group.sprites():
        a[sprt.rect[1] // 25][sprt.rect[0] // 25] = 1
    for sprt in water_wall_group.sprites():
        a[sprt.rect[1] // 25][sprt.rect[0] // 25] = 1

    m = [[0 for i in range(24)] for _ in range(24)]
    start = start
    m[start[0]][start[1]] = 1
    end = end
    visited_old = [(start)]
    visited_new = []

    def make_step(k):
        for cell in visited_old:
            i, j = cell[0], cell[1]
            if m[i][j] == k:
                if i > 0 and j < len(m[i]) - 1 and m[i - 1][j] == 0 and a[i - 1][j] == 0 and not a[i - 1][j + 1]:
                    # if j < 23 and m[i - 1][j + 1] == 0 and a[i - 1][j + 1] == 0:
                    m[i - 1][j] = k + 1
                    visited_new.append((i - 1, j))
                    # m[i - 1][j + 1] = k + 1
                if j > 0 and i < 23 and m[i][j - 1] == 0 and a[i][j - 1] == 0 and not a[i + 1][j - 1]:
                    # if i < 23 and m[i + 1][j - 1] == 0 and a[i + 1][j - 1] == 0:
                    m[i][j - 1] = k + 1
                    visited_new.append((i, j - 1))
                    # m[i + 1][j - 1] = k + 1
                if i < len(m) - 2 and j < 23 and m[i + 1][j] == 0 and a[i + 1][j] == 0 and not a[i + 2][j] and not \
                        a[i + 1][j + 1] and not a[i + 2][j + 1]:
                    # if j < 22 and m[i + 1][j + 1] == 0 and a[i + 1][j + 1] == 0 and not a[i + 2][j + 1]:
                    m[i + 1][j] = k + 1
                    visited_new.append((i + 1, j))
                    # m[i + 1][j + 1] = k + 1
                if j < len(m[i]) - 2 and i < 23 and m[i][j + 1] == 0 and a[i][j + 1] == 0 and not a[i][j + 2] and not \
                        a[i + 1][j + 1] and not a[i + 1][j + 2]:
                    # if i < 22 and m[i + 1][j + 1] <= k + 1 and a[i + 1][j + 1] == 0 and not a[i + 1][j + 2]:
                    m[i][j + 1] = k + 1
                    visited_new.append((i, j + 1))
                    # m[i + 1][j + 1] = k + 1

    k = 0
    while m[end[0]][end[1]] == 0:
        k += 1
        make_step(k)
        visited_old = visited_new[:]
        visited_new = []

    i, j = end
    k = m[i][j]
    path = [(i, j)]
    while k > 1:
        if i > 0 and j < 23 and m[i - 1][j] == k - 1:
            i, j = i - 1, j
            path.append((i, j))
            k -= 1
        elif j > 0 and i < 23 and m[i][j - 1] == k - 1:
            i, j = i, j - 1
            path.append((i, j))
            k -= 1
        elif i < len(m) - 1 and m[i + 1][j] == k - 1:
            i, j = i + 1, j
            path.append((i, j))
            k -= 1
        elif j < len(m[i]) - 1 and m[i][j + 1] == k - 1:
            i, j = i, j + 1
            path.append((i, j))
            k -= 1
    return path[::-1]


def prepare_start(pos_tank, end_pos, class_tank, last_event):
    if pos_tank[0] < end_pos[0]:
        class_tank.rect.x += 1
        class_tank.cur_frame = 2
        class_tank.image = class_tank.frames[class_tank.cur_frame]
    elif pos_tank[0] > end_pos[0]:
        class_tank.rect.x -= 1
        class_tank.cur_frame = 3
        class_tank.image = class_tank.frames[class_tank.cur_frame]
    elif pos_tank[1] < end_pos[1]:
        class_tank.rect.y += 1
        class_tank.cur_frame = 1
        class_tank.image = class_tank.frames[class_tank.cur_frame]
    elif pos_tank[1] > end_pos[1]:
        class_tank.rect.y -= 1
        class_tank.cur_frame = 0
        class_tank.image = class_tank.frames[class_tank.cur_frame]
    class_tank.mouse_path = True
    all_sprites.draw(screen)
    tanks_sprites.draw(screen)
    bullet_sprites.update()
    bullet_sprites.draw(screen)
    leaf_wall_group.draw(screen)
    pygame.display.flip()
    class_tank.update(last_event)


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
        self.mouse_path = False
        self.start = 0, 0
        self.numb = 0

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
        if self.count_shot != 3:
            hit_sound = pygame.mixer.Sound("data/Есть пробитие.mp3")
            pygame.mixer.Sound.play(hit_sound)
        if self.count_shot == 3:
            kill_sound = pygame.mixer.Sound("data/Готов.mp3")
            pygame.mixer.Sound.play(kill_sound)
            self.Tank_kill()

    def Tank_kill(self):
        global yellow_count
        self.kill()
        yellow_count += 1
        BD('Yellow_tank')
        pygame.time.delay(1000)
        end_screen("Yellow_win")

    def update(self, *args):
        get_tick = pygame.time.get_ticks()
        if args and args[0].type in [pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP,
                                     pygame.MOUSEMOTION]:
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
            if args[0].type == pygame.MOUSEBUTTONDOWN:
                if player2.rect.collidepoint(args[0].pos):
                    self.mouse_path = True
                    self.start = (player2.rect[1] // 25 + (player2.rect[1] % 25 // 15),
                                  player2.rect[0] // 25 + (player2.rect[0] % 25 // 15))
                    self.numb = 0
                # else:
                #     self.bullet_delay_mouse = get_tick
            if self.mouse_path and args[0].type == pygame.MOUSEBUTTONUP:
                self.mouse_path = False
                the_path = Finding_Path(self.start, (args[0].pos[1] // 25, args[0].pos[0] // 25))
                if player2.rect[:2] != [the_path[self.numb][1] * 25, the_path[self.numb][0] * 25]:
                    prepare_start(player2.rect[:2], [the_path[self.numb][1] * 25, the_path[self.numb][0] * 25], player2,
                                  args[0])
                elif player2.rect[:2] == [the_path[self.numb][1] * 25, the_path[self.numb][0] * 25]:
                    self.numb += 1
                    self.mouse_path = True
                    if player2.rect[:2] == [(args[0].pos[0] // 25) * 25, (args[0].pos[1] // 25) * 25]:
                        self.numb = 0
                        self.mouse_path = False
                    self.update(args[0])


            elif pygame.key.get_pressed()[pygame.K_KP0] \
                    or (args[0].type == pygame.MOUSEBUTTONUP and args[0].button == 3):
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
        self.mouse_path = False
        self.start = 0, 0

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
        if self.count_shot != 3:
            hit_sound = pygame.mixer.Sound("data/Есть пробитие.mp3")
            pygame.mixer.Sound.play(hit_sound)
        if self.count_shot == 3:
            kill_sound = pygame.mixer.Sound("data/Готов.mp3")
            pygame.mixer.Sound.play(kill_sound)
            self.Tank_kill()

    def Tank_kill(self):
        global green_count
        self.kill()
        green_count += 1
        BD('Green_tank')
        pygame.time.delay(1000)
        end_screen("Green_win")

    def update(self, *args):
        get_tick = pygame.time.get_ticks()
        if args and args[0].type in [pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP,
                                     pygame.MOUSEMOTION]:
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
            if args[0].type == pygame.MOUSEBUTTONDOWN:
                if player1.rect.collidepoint(args[0].pos):
                    self.mouse_path = True
                    self.start = (player1.rect[1] // 25 + (player1.rect[1] % 25 // 15),
                                  player1.rect[0] // 25 + (player1.rect[0] % 25 // 15))
                # else:
                #     self.bullet_delay_mouse = get_tick
            if self.mouse_path and args[0].type == pygame.MOUSEBUTTONUP:
                self.mouse_path = False
                # print(The_Path(self.start, (args[0].pos[1] // 25, args[0].pos[0] // 25)))
            elif pygame.key.get_pressed()[pygame.K_SPACE] or (
                    args[0].type == pygame.MOUSEBUTTONUP and args[0].button == 1):
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
    global width, height
    pygame.mixer.music.load("data/Fon_music.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)

    fon = pygame.transform.scale(load_image('new.png'), (width, height))
    screen.blit(fon, (0, 0))

    while True:
        fon = pygame.transform.scale(load_image('new.png'), (width, height))
        screen.blit(fon, (0, 0))
        width = screen.get_width()
        height = screen.get_height()
        # button_sologame = Button(200, 40, (255, 0, 0), (100, 0, 0))
        # button_sologame.draw(300, 390, '1 Player')
        button_pvpgame = Button(200, 40, (255, 0, 0), (100, 0, 0))
        button_pvpgame.draw(width // 2 - 100, height - height // 3 + 70, '2 Players', maps_menu)
        # button_build = Button(200, 40, (255, 0, 0), (100, 0, 0))
        # button_build.draw(300, 510, 'Building')

        button_exit = Button(100, 40, (0, 0, 0), (50, 50, 50))
        button_exit.draw(width - 100, height - 40, 'Exit', end_game)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()


def resert_score():
    global yellow_count, green_count
    yellow_count, green_count = 0, 0
    update_sprite()
    screen = pygame.display.set_mode(size)
    fon = pygame.transform.scale(load_image('End.gif'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    print_text(f'Winstrick: {yellow_count}', 60, 40, font_size=50, font_color=(255, 0, 0))
    print_text(f'Winstrick: {green_count}', 410, 40, font_size=50, font_color=(255, 0, 0))
    WINNER = pygame.transform.scale(load_image('Yellow_Win.png'), (200, 200))
    screen.blit(WINNER, (130, 200))
    LO0SER = pygame.transform.scale(load_image('Green_Win.png'), (200, 200))
    screen.blit(LO0SER, (470, 200))

    while True:
        button_return_menu = Button(200, 40, (130, 130, 130), (100, 0, 0))
        button_return_menu.draw(50, 500, 'Restart', restart)
        button_return_mainmenu = Button(200, 40, (130, 130, 130), (100, 0, 0))
        button_return_mainmenu.draw(290, 500, 'Main menu', start_screen)
        button_exit = Button(200, 40, (130, 130, 130), (100, 0, 0))
        button_exit.draw(540, 500, 'Exit', end_game)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
        clock.tick(FPS)


def end_screen(Tank_win):
    global yellow_count, green_count
    pygame.mixer.music.load("data/Win_music.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
    update_sprite()
    screen = pygame.display.set_mode(size)
    fon = pygame.transform.scale(load_image('End.gif'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    print_text(f'Winstrick: {yellow_count}', 60, 40, font_size=50, font_color=(255, 0, 0))
    print_text(f'Winstrick: {green_count}', 410, 40, font_size=50, font_color=(255, 0, 0))
    if Tank_win == "Yellow_win":
        WINNER = pygame.transform.scale(load_image('Yellow_Win.png'), (200, 200))
        screen.blit(WINNER, (130, 100))
        LO0SER = pygame.transform.scale(load_image('Green_Win.png'), (200, 200))
        screen.blit(LO0SER, (470, 100))
        print_text("Yellow - WIN", 100, 350, font_size=40, font_color=(255, 255, 0))
        print_text("Green - LOSE", 450, 350, font_size=40, font_color=(0, 255, 0))
    if Tank_win == "Green_win":
        WINNER = pygame.transform.scale(load_image('Green_Win.png'), (200, 200))
        screen.blit(WINNER, (470, 100))
        LO0SER = pygame.transform.scale(load_image('Yellow_Win.png'), (200, 200))
        screen.blit(LO0SER, (130, 100))
        print_text("Yellow - LOSE", 100, 350, font_size=40, font_color=(255, 255, 0))
        print_text("Green - WIN", 450, 350, font_size=40, font_color=(0, 255, 0))

    while True:
        button_return_menu = Button(200, 40, (130, 130, 130), (100, 0, 0))
        button_return_menu.draw(50, 500, 'Restart', maps_menu)
        button_return_mainmenu = Button(200, 40, (130, 130, 130), (100, 0, 0))
        button_return_mainmenu.draw(290, 500, 'Main menu', start_screen)
        button_exit = Button(200, 40, (130, 130, 130), (100, 0, 0))
        button_exit.draw(540, 500, 'Exit', end_game)
        button_resert_score = Button(200, 35, (0, 0, 0), (100, 0, 0))
        button_resert_score.draw(280, 0, 'Resert score', resert_score)
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


def update_sprite():
    global all_sprites, tiles_group, wall_group, indestructible_wall_group
    global water_wall_group, leaf_wall_group, bullet_sprites, tanks_sprites
    tiles_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    wall_group = pygame.sprite.Group()
    indestructible_wall_group = pygame.sprite.Group()
    water_wall_group = pygame.sprite.Group()
    leaf_wall_group = pygame.sprite.Group()
    bullet_sprites = pygame.sprite.Group()
    tanks_sprites = pygame.sprite.Group()


if __name__ == '__main__':
    update_sprite()
    start_screen()
    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            fullscreen = not fullscreen
            if fullscreen:
                screen = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
            else:
                screen = pygame.display.set_mode(size, pygame.RESIZABLE)
pygame.quit()
