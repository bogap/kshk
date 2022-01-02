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

level=level_name(lvl)

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
        string_rendered = font.render(line, 1, pygame.Color('pink'))
        intro_rect = string_rendered.get_rect()
        intro_rect.x = self.pos_x
        intro_rect.y = self.pos_y
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


def start_screen():
    screen = pygame.display.set_mode((450, 450))
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (450, 450))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

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

pygame.init()
start_screen()
screen = pygame.display.set_mode(WINDOW_SIZE)
loaded_level = load_level(level)
max_score = 0
for i in range(6):
    for j in range(30):
        if loaded_level[i][j] == '!':
            max_score += 1
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

while running:
    for el in gained_candy:
        x, y = el
        candy = Candy_gained(x, y)
        if x <= (pygame.time.get_ticks() - minus_time) // 350 - time // 1000 + start_fire:
            candy = Fire(x, y)
        if ochki == 0:
            candy = Candy(x, y)
            if gained_candy.index(el) == len(gained_candy) - 1:
                gained_candy = []
        if player.rect.x // 50 == x and player.rect.y // 50 == y:
            player_on_grass = Player(x, y)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
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
                        print('pobeda')
                        ochki = 0
            if event.key == pygame.K_UP:
                if player.rect.y - tile_width >= 50 * 3:
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
                        print('pobeda')
                        ochki = 0
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
                        print('pobeda')
                        ochki = 0
    if player.rect.x // 50 < (pygame.time.get_ticks() - minus_time) // 350 - time // 1000 + start_fire:
        minus_time = pygame.time.get_ticks()
        start_fire = -3
        fire = [Fire(start_fire, x) for x in range(6)]
        all_sprites = pygame.sprite.Group()
        tiles_group = pygame.sprite.Group()
        player_group = pygame.sprite.Group()
        player, level_x, level_y = generate_level(loaded_level)
        ochki = 0

    all_sprites.draw(screen)
    tiles_group.draw(screen)
    player_group.draw(screen)
    fire += [Fire((pygame.time.get_ticks() - minus_time) // 350 - time // 1000 + start_fire, x) for x in range(6)]

    score = Score(14 * 50, 1 * 50)
    score.show_score(ochki)

    pygame.display.flip()
    clock.tick(FPS)
pygame.QUIT
