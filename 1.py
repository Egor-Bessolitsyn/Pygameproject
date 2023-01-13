import pygame
import os
import sys

# or (300 < pygame.mouse.get_pos()[0] < 500 and 460 < pygame.mouse.get_pos()[1] < 500)
# (300 < pygame.mouse.get_pos()[0] < 500 and 390 < pygame.mouse.get_pos()[1] < 450)
FPS = 50
size = WIDTH, HEIGHT = 800, 600
clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode(size)


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


def start_game():
    print(123456789)


class Button:
    def __init__(self, width, height, color):
        self.width = width
        self.height = height
        self.color = color

    def draw(self, x, y, massage, action=None):
        mouse_clicked = pygame.mouse.get_pressed()
        pygame.draw.rect(screen, self.color, (x, y, self.width, self.height))
        print_text(massage, x + 40, y + 10)
        if mouse_clicked[0] == 1:
            if action is not None:
                action()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 200
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
        if args and args[0].type == pygame.KEYDOWN:
            self.tick_time += 1
            # if self.tick_time % 10 == 1:
            #     self.tick_time %= 10
            #     self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            #     self.image = self.frames[self.cur_frame]
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


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100
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
        if args and args[0].type == pygame.KEYDOWN:
            self.tick_time += 1
            # if self.tick_time % 10 == 1:
            #     self.tick_time %= 10
            #     self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            #     self.image = self.frames[self.cur_frame]
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


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    button_sologame = Button(200, 40, (255, 0, 0))
    button_pvpgame = Button(200, 40, (255, 0, 0))
    fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    button_sologame.draw(300, 390, '1 Player')
    button_pvpgame.draw(300, 460, '2 Players')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) \
                    and ((300 < pygame.mouse.get_pos()[0] < 500 and 460 < pygame.mouse.get_pos()[1] < 500)):
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    start_screen()

    all_sprites = pygame.sprite.Group()
    tank = AnimatedSprite(load_image("yellow_tanks.png"), 4, 1, 50, 50)
    enemy = Enemy(load_image("yellow_tanks.png"), 4, 1, 50, 50)

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
            all_sprites.update(event)
        screen.fill((110, 110, 110))
        if move:
            all_sprites.update(last_event)
        all_sprites.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
