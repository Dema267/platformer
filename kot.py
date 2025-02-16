import pygame
import sys

# Инициализация PyGame
pygame.init()
WIDTH, HEIGHT = 1100, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D-платформер")
clock = pygame.time.Clock()

# Загрузка материалов (фото, звуки)
player_image = pygame.image.load("images/персонаж.png")
coin_image = pygame.image.load("images/монета.png")
spike_image = pygame.image.load("images/шипы.png")  # Загрузите изображение шипов

pygame.mixer.music.load("sounds/меню игры.mp3")
pygame.mixer.music.play(-1)

jump_sound = pygame.mixer.Sound("sounds/прыжок1.wav")
coin_sound = pygame.mixer.Sound("sounds/монета.mp3")

# Создание класса персонажа
class Player:
    def __init__(self, x, y):
        self.images = {
            "idle": pygame.image.load("images/персонаж.png"),
            "left": pygame.image.load("images/влево.png"),
            "right": pygame.image.load("images/вправо.png"),
            "jump_right": pygame.image.load("images/прыжок_вправо.png"),
            "jump_left": pygame.image.load("images/прыжок_влево.png"),
        }
        self.image = self.images["idle"]  # Начальное изображение
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity_y = 0
        self.on_ground = False
        self.direction = "idle"  # Направление персонажа

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
            jump_sound.play()

    def draw(self, screen):
        screen.blit(self.image, self.rect)


# Создание класса платформ
class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.rect)

# Создание класса монет
class Coin:
    def __init__(self, x, y):
        self.image = coin_image
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# Создание класса шипов
class Spike:
    def __init__(self, x, y):
        self.image = spike_image
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# Создание класса движущейся платформы
class MovingPlatform:
    def __init__(self, x, y, width, height, speed, range_x):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.range_x = range_x
        self.direction = 1  # 1 - вправо, -1 - влево

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.x <= self.range_x[0] or self.rect.x >= self.range_x[1]:
            self.direction *= -1

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 255), self.rect)

# Функция для проверки коллизий с платформами
def check_collision(player, platforms):
    for platform in platforms:
        if player.rect.colliderect(platform.rect):
            if player.velocity_y > 0:
                player.rect.bottom = platform.rect.top
                player.on_ground = True
                player.velocity_y = 0

# Функция для отображения главного меню
def main_menu():
    font = pygame.font.Font(None, 74)
    title_text = font.render("2D-платформер", True, (255, 255, 255))
    start_text = font.render("Начать игру", True, (255, 255, 255))
    exit_text = font.render("Выход", True, (255, 255, 255))

    while True:
        screen.fill((0, 0, 0))
        screen.blit(title_text, (WIDTH // 2 - 150, 100))
        screen.blit(start_text, (WIDTH // 2 - 100, 300))
        screen.blit(exit_text, (WIDTH // 2 - 50, 400))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        # Проверка нажатия на кнопки
        if WIDTH // 2 - 100 <= mouse_pos[0] <= WIDTH // 2 + 100 and 300 <= mouse_pos[1] <= 350:
            if mouse_click[0]:
                return "start"
        if WIDTH // 2 - 50 <= mouse_pos[0] <= WIDTH // 2 + 50 and 400 <= mouse_pos[1] <= 450:
            if mouse_click[0]:
                return "exit"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(60)

# Инициализация уровней
levels = [
    {
        "platforms": [
            Platform(0, HEIGHT - 50, WIDTH, 50),
            Platform(200, 400, 200, 20),
            Platform(500, 300, 150, 20),
        ],
        "coins": [Coin(250, 350), Coin(550, 250)],
        "spikes": [Spike(400, HEIGHT - 100)],
        "moving_platforms": [MovingPlatform(300, 200, 100, 20, 2, [300, 500])],
    },
    {
        "platforms": [
            Platform(0, HEIGHT - 50, WIDTH, 50),
            Platform(100, 500, 150, 20),
            Platform(400, 400, 150, 20),
        ],
        "coins": [Coin(150, 450), Coin(450, 350)],
        "spikes": [Spike(600, HEIGHT - 100)],
        "moving_platforms": [MovingPlatform(200, 300, 100, 20, 3, [200, 600])],
    },
]




# Основной игровой цикл
def game_loop(level):
    player = Player(100, HEIGHT - 100)
    platforms = level["platforms"]
    coins = level["coins"]
    spikes = level["spikes"]
    moving_platforms = level["moving_platforms"]
    score = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Управление персонажем
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player.rect.x -= 5
            player.image = player.images["left"]
            player.direction = "left"
        if keys[pygame.K_d]:
            player.rect.x += 5
            player.image = player.images["right"]
            player.direction = "right"
        if keys[pygame.K_SPACE]:
            player.jump()
            if player.direction == "right":
                player.image = player.images["jump_right"]
            elif player.direction == "left":
                player.image = player.images["jump_left"]

        # Обновление игровых объектов
        player.update()
        check_collision(player, platforms)
        for platform in moving_platforms:
            platform.update()
            check_collision(player, [platform])

        # Проверка сбора монет
        for coin in coins[:]:
            if player.rect.colliderect(coin.rect):
                coins.remove(coin)
                score += 1
                coin_sound.play()

        # Проверка столкновения с шипами
        for spike in spikes:
            if player.rect.colliderect(spike.rect):
                print("Игрок погиб!")
                return "restart"

        # Отрисовка
        screen.fill((0, 0, 0))  # Очистка экрана

        # Отрисовка платформ
        for platform in platforms:
            platform.draw(screen)

        # Отрисовка движущихся платформ
        for platform in moving_platforms:
            platform.draw(screen)

        # Отрисовка монет
        for coin in coins:
            coin.draw(screen)

        # Отрисовка шипов
        for spike in spikes:
            spike.draw(screen)

        # Отрисовка персонажа
        player.draw(screen)

        # Отображение счета
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Счет: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        # Обновление экрана
        pygame.display.flip()
        clock.tick(60)  # Ограничение FPS

# Запуск игры
current_level = 0
while True:
    choice = main_menu()
    if choice == "start":
        result = game_loop(levels[current_level])
        if result == "restart":
            current_level = 0
        else:
            current_level = (current_level + 1) % len(levels)
    elif choice == "exit":
        pygame.quit()
        sys.exit()