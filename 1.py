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
    clock = pygame.time.Clock()
    move = False
    last_event = None
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
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
        clock.tick(FPS)
        pygame.display.flip()


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
        card1 = Button(100, 100, (255, 0, 0), (150, 0, 0))
        menu = pygame.Surface(size)
        screen.blit(menu, (0, 0))
        card1.draw(100, 100, 'Card1', start_game)
        # print(card_sprites.sprites())
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                show = False
            if event.type == pygame.MOUSEBUTTONDOWN and \
                    (0 < pygame.mouse.get_pos()[0] < 800 and 460 < pygame.mouse.get_pos()[1] < 500):
                show = False
                return


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
        self.mask = pygame.mask.from_surface(self.image)
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

    def update(self, *args):
        clock = pygame.time.get_ticks()
        if args and args[0].type == pygame.KEYDOWN:
            self.tick_time += 1
            if self.tick_time % 10 == 1:
                self.tick_time %= 10
            if pygame.key.get_pressed()[pygame.K_UP]:
                self.cur_frame = 0
                self.image = self.frames[self.cur_frame]
                self.rect.y -= 1
            elif pygame.key.get_pressed()[pygame.K_DOWN]:
                self.cur_frame = 1
                self.image = self.frames[self.cur_frame]
                self.rect.y += 1
            elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                self.cur_frame = 2
                self.image = self.frames[self.cur_frame]
                self.rect.x += 1
            elif pygame.key.get_pressed()[pygame.K_LEFT]:
                self.cur_frame = 3
                self.image = self.frames[self.cur_frame]
                self.rect.x -= 1
            elif pygame.key.get_pressed()[pygame.K_KP0]:
                if clock - self.bullet_delay >= 500:
                    self.bullet_delay = clock
                    if self.cur_frame == 0:
                        Bullet(load_image("Bullet_sprite.png"), 4, 1, self.rect.x + 18, self.rect.y - 14,
                               self.cur_frame, self.rect)
                    elif self.cur_frame == 1:
                        Bullet(load_image("Bullet_sprite.png"), 4, 1, self.rect.x + 18, self.rect.y + 50,
                               self.cur_frame, self.rect)
                    elif self.cur_frame == 2:
                        Bullet(load_image("Bullet_sprite.png"), 4, 1, self.rect.x + 50, self.rect.y + 18,
                               self.cur_frame, self.rect)
                    elif self.cur_frame == 3:
                        Bullet(load_image("Bullet_sprite.png"), 4, 1, self.rect.x - 14, self.rect.y + 18,
                               self.cur_frame, self.rect)


class Tank_WASD(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(tanks_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.rect.move(x, y)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100
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

    def update(self, *args):
        clock = pygame.time.get_ticks()
        if args and args[0].type == pygame.KEYDOWN:
            self.tick_time += 1
            if self.tick_time % 10 == 1:
                self.tick_time %= 10
            if pygame.key.get_pressed()[pygame.K_w]:
                self.cur_frame = 0
                self.image = self.frames[self.cur_frame]
                self.rect.y -= 1
            elif pygame.key.get_pressed()[pygame.K_s]:
                self.cur_frame = 1
                self.image = self.frames[self.cur_frame]
                self.rect.y += 1
            elif pygame.key.get_pressed()[pygame.K_d]:
                self.cur_frame = 2
                self.image = self.frames[self.cur_frame]
                self.rect.x += 1
            elif pygame.key.get_pressed()[pygame.K_a]:
                self.cur_frame = 3
                self.image = self.frames[self.cur_frame]
                self.rect.x -= 1
            elif pygame.key.get_pressed()[pygame.K_SPACE]:
                if clock - self.bullet_delay >= 500:
                    self.bullet_delay = clock
                    if self.cur_frame == 0:
                        Bullet(load_image("Bullet_sprite.png"), 4, 1, self.rect.x + 18, self.rect.y - 14,
                               self.cur_frame, self.rect)
                    elif self.cur_frame == 1:
                        Bullet(load_image("Bullet_sprite.png"), 4, 1, self.rect.x + 18, self.rect.y + 50,
                               self.cur_frame, self.rect)
                    elif self.cur_frame == 2:
                        Bullet(load_image("Bullet_sprite.png"), 4, 1, self.rect.x + 50, self.rect.y + 18,
                               self.cur_frame, self.rect)
                    elif self.cur_frame == 3:
                        Bullet(load_image("Bullet_sprite.png"), 4, 1, self.rect.x - 14, self.rect.y + 18,
                               self.cur_frame, self.rect)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, cur_frame, animatedSprite_rect):
        super().__init__(bullet_sprites)
        self.animatedSprite_rect = animatedSprite_rect
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = cur_frame
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.tick_time = 0

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
            self.tick_time += 1
            if self.tick_time % 3 == 1:
                self.tick_time %= 3
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
        button_exit.draw(699, 559, 'Exit')

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.MOUSEBUTTONDOWN and
                                             (700 < pygame.mouse.get_pos()[0] < 800 and 550 < pygame.mouse.get_pos()[
                                                 1] < 600)):
                terminate()
        pygame.display.flip()


if __name__ == '__main__':
    start_screen()
    cards_menu()
    start_game()

    card_sprites = pygame.sprite.Group()
    bullet_sprites = pygame.sprite.Group()
    tanks_sprites = pygame.sprite.Group()

    tank_1 = Tank_WASD(load_image("yellow_tanks.png"), 4, 1, 50, 50)
    tank_2 = Tank_2_pdrl(load_image("yellow_tanks.png"), 4, 1, 50, 50)

pygame.quit()
