import pygame
import os
import sys


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
            if self.tick_time % 10 == 1:
                self.tick_time %= 10
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = self.frames[self.cur_frame]
            if pygame.key.get_pressed()[pygame.K_UP]:
                self.rect.y -= 1
            elif pygame.key.get_pressed()[pygame.K_DOWN]:
                self.rect.y += 1
            elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                self.rect.x += 1
            elif pygame.key.get_pressed()[pygame.K_LEFT]:
                self.rect.x -= 1


if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)

    all_sprites = pygame.sprite.Group()
    dragon = AnimatedSprite(load_image("dragon_sheet8x2.png"), 8, 2, 50, 50)

    fps = 100
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
        screen.fill((255, 255, 255))
        if move:
            all_sprites.update(last_event)
        all_sprites.draw(screen)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
