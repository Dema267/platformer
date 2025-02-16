#Инициализация PyGame
import pygame

pygame.init()
WIDTH, HEIGHT = 1100, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D-платформер")
clock = pygame.time.Clock()

#Создание игрового цикла
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # Очистка экрана
    pygame.display.flip()    # Обновление экрана
    clock.tick(60)           # Ограничение FPS

#Загрузка материалов (фото, видео)
player_image = pygame.image.load("images/персонаж.png")
coin_image = pygame.image.load("images/монета.png")
background_music = pygame.mixer.Sound("sounds/меню игры.mp3")

pygame.mixer.music.load("sounds/12cfb941f3a5f50.mp3")
pygame.mixer.music.play(-1)

jump_sound = pygame.mixer.Sound("sounds/прыжок.mp3")
coin_sound = pygame.mixer.Sound("sounds/монета.mp3")

#Создание класса персонажа
class Player:
    def __init__(self, x, y):
        self.image = player_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity_y = 0
        self.on_ground = False

    def update(self):
        # Гравитация
        self.velocity_y += 1
        self.rect.y += self.velocity_y

        # Ограничение падения
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.on_ground = True
            self.velocity_y = 0

    def jump(self):
        if self.on_ground:
            self.velocity_y = -15
            self.on_ground = False

#Управление персонажем
player = Player(100, HEIGHT - 100)

while running:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.rect.x -= 5
    if keys[pygame.K_d]:
        player.rect.x += 5
    if keys[pygame.K_SPACE]:
        player.jump()

    player.update()
    screen.blit(player.image, player.rect)

#Создание платформ и препятствий
class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.rect)

#Добавление плаатформ на уровень
platforms = [
    Platform(0, HEIGHT - 50, WIDTH, 50),
    Platform(200, 400, 200, 20),
    Platform(500, 300, 150, 20),
]

#Взаимодействие платформы и персонажа
def check_collision(player, platforms):
    for platform in platforms:
        if player.rect.colliderect(platform.rect):
            if player.velocity_y > 0:
                player.rect.bottom = platform.rect.top
                player.on_ground = True
                player.velocity_y = 0

#Добавление предметов и счета
class Coin:
    def __init__(self, x, y):
        self.image = coin_image
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

#Сбор предметов
coins = [Coin(250, 350), Coin(550, 250)]
score = 0

for coin in coins:
    if player.rect.colliderect(coin.rect):
        coins.remove(coin)
        score += 1

#Создание уровней
levels = [
    [Platform(0, HEIGHT - 50, WIDTH, 50), Coin(250, 350)],
    [Platform(0, HEIGHT - 50, WIDTH, 50), Platform(200, 400, 200, 20), Coin(550, 250)],
]

