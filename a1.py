import pygame
import sys
import os

FPS = 50

clock = pygame.time.Clock()
WINDOW_SIZE = WIDTH, HEIGHT = 30 * 50, 6 * 50
screen = pygame.display.set_mode(WINDOW_SIZE)
lvl = 1


def level_name(level):
    return 'levels/lvl' + str(level) + '.txt'


level = level_name(lvl)


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
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


# основной персонаж
player = None

tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('sky.png'),
    'grass': load_image('grass.png'),
    'finish': load_image('flag.png'),
    'fire': load_image('fire.png'),
    'candy': load_image('candy.png')
}
player_image = load_image('cat.png')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = tile_images[tile_type]
        self.type = tile_type
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def get_tile_type(self):
        return self.type

    def get_tile_pos(self):
        return self.pos_x, self.pos_y


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - 50 // 2)
        self.dy = 0


camera = Camera()


class Fire(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = load_image('fire.png')
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        '''
        fire_sprite = pygame.sprite.Sprite()
        fire_sprite.image = load_image("fire.png")
        # и размеры
        fire_sprite.rect = fire_sprite.image.get_rect()
        # добавим спрайт в группу
        all_sprites.add(fire_sprite)
        '''


class Candy_gained(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = load_image('grass.png')
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Candy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = load_image('candy.png')
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Score:
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

    def show_score(self, ochki):
        line = 'SCORE: ' + str(ochki)
        font = pygame.font.Font(None, 30)
        string_rendered = font.render(line, 1, (199, 21, 133))
        intro_rect = string_rendered.get_rect()
        intro_rect.x = self.pos_x
        intro_rect.y = self.pos_y
        screen.blit(string_rendered, intro_rect)


def show_level(level, pos_x, pos_y):
    line = 'LEVEL: ' + str(level)
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(line, 1, (199, 21, 133))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = pos_x
    intro_rect.y = pos_y
    screen.blit(string_rendered, intro_rect)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'a':
                Tile('empty', x, y)
            elif level[y][x] == '.':
                Tile('grass', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == 'F':
                Tile('finish', x, y)
            elif level[y][x] == '!':
                Tile('candy', x, y)
            elif level[y][x] == '@':
                Tile('grass', x, y)
                new_player = Player(x, y)

    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def show_win():
    screen = pygame.display.set_mode((1500, 300))
    scr = pygame.transform.scale(load_image('win.jpg'), (1500, 300))
    screen.blit(scr, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    screen = pygame.display.set_mode((450, 450))

    intro_text = ["КОТОШИЗА", "",
                  "Чтобы пройти уровень,",
                  "нужно собрать все сердечки на поле",
                  "и дойти до радуги.",
                  "Будьте осторожны на своем пути",
                  "и остерегайтесь тумана и луж,",
                  "ведь всем известно,",
                  "что кошки не любят воду."]

    fon = pygame.transform.scale(load_image('fon.jpg'), (450, 450))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    big_font=pygame.font.Font(None, 40)
    text_coord = 50

    for line in intro_text:
        if line=='КОТОШИЗА':
            string_rendered = big_font.render(line, 1, (255, 255, 0))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = 55
            intro_rect.x = 10
            screen.blit(string_rendered, intro_rect)

            continue
        string_rendered = font.render(line, 1, (255, 255, 0))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
#pyinstaller --onefile --noconsole a1.py
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def get_image(self):
        return self.image

    def get_rect(self):
        return self.rect

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


cat = AnimatedSprite(load_image("cat.png"), 2, 1, 50, 50)
player_image = cat.get_image()

pygame.init()
start_screen()
screen = pygame.display.set_mode(WINDOW_SIZE)
loaded_level = load_level(level)
max_score = 0
height = 6
for i in range(6):
    for j in range(30):
        if loaded_level[i][j] == '!':
            max_score += 1
for i in range(6):
    if 'a' in loaded_level[i]:
        height -= 1
screen.fill((0, 0, 0))
player, level_x, level_y = generate_level(loaded_level)
running = True
player_x = 0
time = pygame.time.get_ticks()
start_fire = -3
fire = [Fire(start_fire, x) for x in range(6)]
minus_time = 0
ochki = 0
gained_candy = []
temp = 0
background = pygame.Surface((1500, 300))
while running:
    for el in gained_candy:
        x, y = el
        candy = Candy_gained(x, y)
        if x <= (pygame.time.get_ticks() - minus_time) // 400 - time // 1000 + start_fire:
            candy = Fire(x, y)
        if ochki == 0:
            candy = Candy(x, y)
            if gained_candy.index(el) == len(gained_candy) - 1:
                gained_candy = []
        if player.rect.x // 50 == x and player.rect.y // 50 == y:
            player_on_grass = Player(x, y)
            clock.tick(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            a, b = player.rect.x // 50, player.rect.y // 50
            grass_on_player = Candy_gained(a, b)
            player = Player(player.rect.x // 50, player.rect.y // 50)
            if event.key == pygame.K_RIGHT:
                player_x += 50
                if player.rect.x + tile_width < 50 * 30:
                    player.rect.x += tile_width
                    if pygame.sprite.spritecollide(player, tiles_group, False)[0].get_tile_type() == 'wall':
                        all_sprites = pygame.sprite.Group()
                        tiles_group = pygame.sprite.Group()
                        player_group = pygame.sprite.Group()
                        player, level_x, level_y = generate_level(loaded_level)
                        ochki = 0
                    elif pygame.sprite.spritecollide(player, tiles_group, False)[0].get_tile_type() == 'candy':
                        gained_candy += [pygame.sprite.spritecollide(player, tiles_group, False)[0].get_tile_pos()]
                        ochki += 1
                    elif pygame.sprite.spritecollide(player, tiles_group, False)[
                        0].get_tile_type() == 'finish' and ochki == max_score:
                        if lvl == 6:
                            show_win()
                            running = False
                        ochki = 0
                        lvl += 1
                        level = level_name(lvl)
                        loaded_level = load_level(level)
                        height = 6
                        for i in range(6):
                            if 'a' in loaded_level[i]:
                                height -= 1
                        max_score = 0
                        for i in range(6):
                            for j in range(30):
                                if loaded_level[i][j] == '!':
                                    max_score += 1
                        player, level_x, level_y = generate_level(loaded_level)
            if event.key == pygame.K_UP:
                if player.rect.y - tile_width >= 50 * (6 - height):
                    player.rect.y -= tile_width
                    if pygame.sprite.spritecollide(player, tiles_group, False)[0].get_tile_type() == 'wall':
                        all_sprites = pygame.sprite.Group()
                        tiles_group = pygame.sprite.Group()
                        player_group = pygame.sprite.Group()
                        player, level_x, level_y = generate_level(loaded_level)
                        ochki = 0
                    elif pygame.sprite.spritecollide(player, tiles_group, False)[0].get_tile_type() == 'candy':
                        gained_candy += [pygame.sprite.spritecollide(player, tiles_group, False)[0].get_tile_pos()]
                        ochki += 1
                    elif pygame.sprite.spritecollide(player, tiles_group, False)[
                        0].get_tile_type() == 'finish' and ochki == max_score:
                        if lvl == 6:
                            show_win()
                            running = False
                        ochki = 0
                        lvl += 1
                        level = level_name(lvl)
                        loaded_level = load_level(level)
                        max_score = 0
                        for i in range(6):
                            for j in range(30):
                                if loaded_level[i][j] == '!':
                                    max_score += 1
                        player, level_x, level_y = generate_level(loaded_level)
            if event.key == pygame.K_DOWN:
                if player.rect.y + tile_width < 50 * 6:
                    player.rect.y += tile_width
                    if pygame.sprite.spritecollide(player, tiles_group, False)[0].get_tile_type() == 'wall':
                        all_sprites = pygame.sprite.Group()
                        tiles_group = pygame.sprite.Group()
                        player_group = pygame.sprite.Group()
                        player, level_x, level_y = generate_level(loaded_level)
                        ochki = 0
                    elif pygame.sprite.spritecollide(player, tiles_group, False)[0].get_tile_type() == 'candy':
                        gained_candy += [pygame.sprite.spritecollide(player, tiles_group, False)[0].get_tile_pos()]
                        ochki += 1
                    elif pygame.sprite.spritecollide(player, tiles_group, False)[
                        0].get_tile_type() == 'finish' and ochki == max_score:
                        if lvl == 6:
                            show_win()
                            running = False
                        ochki = 0
                        lvl += 1
                        level = level_name(lvl)
                        loaded_level = load_level(level)
                        max_score = 0
                        for i in range(6):
                            for j in range(30):
                                if loaded_level[i][j] == '!':
                                    max_score += 1
                        player, level_x, level_y = generate_level(loaded_level)
            if event.key == pygame.K_LEFT:
                if player.rect.x > 0:
                    player.rect.x -= tile_width
                    if pygame.sprite.spritecollide(player, tiles_group, False)[0].get_tile_type() == 'wall':
                        all_sprites = pygame.sprite.Group()
                        tiles_group = pygame.sprite.Group()
                        player_group = pygame.sprite.Group()
                        player, level_x, level_y = generate_level(loaded_level)
                        ochki = 0
                    elif pygame.sprite.spritecollide(player, tiles_group, False)[0].get_tile_type() == 'candy':
                        gained_candy += [pygame.sprite.spritecollide(player, tiles_group, False)[0].get_tile_pos()]
                        ochki += 1
                    elif pygame.sprite.spritecollide(player, tiles_group, False)[
                        0].get_tile_type() == 'finish' and ochki == max_score:
                        ochki = 0
                        lvl += 1
                        level = level_name(lvl)
                        loaded_level = load_level(level)
                        max_score = 0
                        for i in range(6):
                            for j in range(30):
                                if loaded_level[i][j] == '!':
                                    max_score += 1
                        player, level_x, level_y = generate_level(loaded_level)
    if player.rect.x // 50 < (pygame.time.get_ticks() - minus_time) // 400 - time // 1000 + start_fire:
        minus_time = pygame.time.get_ticks()
        start_fire = -3
        fire = [Fire(start_fire, x) for x in range(6)]
        fire += [Fire(player.rect.x // 50, player.rect.y // 50)]
        all_sprites = pygame.sprite.Group()
        tiles_group = pygame.sprite.Group()
        player_group = pygame.sprite.Group()
        player, level_x, level_y = generate_level(loaded_level)
        ochki = 0

    cat.update()
    player_image = cat.get_image()

    all_sprites.draw(screen)
    tiles_group.draw(screen)
    player_group.draw(screen)
    if temp != (pygame.time.get_ticks() - minus_time) // 400 - time // 1000 + start_fire:
        fire = [Fire((pygame.time.get_ticks() - minus_time) // 400 - time // 1000 + start_fire, x) for x in range(6)]
    else:
        fire = []
    temp = (pygame.time.get_ticks() - minus_time) // 400 - time // 1000 + start_fire
    load_level(level)
    score = Score(25 * 50, 20)
    score.show_score(ochki)
    show_level(lvl, 28 * 50, 20)
    pygame.display.flip()
    clock.tick(FPS)

pygame.QUIT
