import pygame
import sys

# Инициализация PyGame
pygame.init()
WIDTH, HEIGHT = 1000, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D-платформер")
clock = pygame.time.Clock()

# Загрузка материалов (фото, звуки)
player_images = {
    "player1": {
        "idle": pygame.image.load("images/person1/персонаж.png"),
        "left": pygame.image.load("images/person1/влево.png"),
        "right": pygame.image.load("images/person1/вправо.png"),
        "jump_right": pygame.image.load("images/person1/прыжок_вправо.png"),
        "jump_left": pygame.image.load("images/person1/прыжок_влево.png"),
    },
    "player2": {
        "idle": pygame.image.load("images/person2/персонаж2.png"),
        "left": pygame.image.load("images/person2/влево2.png"),
        "right": pygame.image.load("images/person2/вправо2.png"),
        "jump_right": pygame.image.load("images/person2/прыжок_вправо2.png"),
        "jump_left": pygame.image.load("images/person2/прыжок_влево2.png"),
    },
    "player3": {
        "idle": pygame.image.load("images/person3/персонаж3.png"),
        "left": pygame.image.load("images/person3/влево3.png"),
        "right": pygame.image.load("images/person3/вправо3.png"),
        "jump_right": pygame.image.load("images/person3/прыжок_вправо3.png"),
        "jump_left": pygame.image.load("images/person3/прыжок_влево3.png"),
    },
}
coin_image = pygame.image.load("images/монета.png")
spike_image = pygame.image.load("images/шипы.png")
background_image = pygame.image.load("images/фон1.png")  # Загрузите фоновое изображение

pygame.mixer.music.load("sounds/12cfb941f3a5f50.mp3")
pygame.mixer.music.play(-1)

jump_sound = pygame.mixer.Sound("sounds/прыжок1.wav")
coin_sound = pygame.mixer.Sound("sounds/монета.mp3")

# Создание класса персонажа
class Player:
    def __init__(self, x, y, character="player1"):
        self.images = player_images[character]
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


# Остальные классы (Platform, Coin, Spike, MovingPlatform) остаются без изменений

# Функция для отображения главного меню
def main_menu():
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 50)
    title_text = font.render("Alien Ascent", True, (30,30,30))
    start_text = font.render("START", True, (255, 255, 255))
    settings_text = font.render("OPTION", True, (255, 255, 255))
    exit_text = font.render("EXIT", True, (255, 255, 255))

    selected_character = "player1"  # По умолчанию выбран первый персонаж

    while True:
        screen.blit(background_image, (0, 0))  # Отображение фонового изображения
        screen.blit(title_text, (WIDTH // 2 - 150, 100))

        # Координаты и размеры кнопок
        button_width, button_height = 300, 80
        start_button = pygame.Rect(WIDTH // 2 - 150, 300, button_width, button_height)
        settings_button = pygame.Rect(WIDTH // 2 - 150, 400, button_width, button_height)
        exit_button = pygame.Rect(WIDTH // 2 - 150, 500, button_width, button_height)

        # Отрисовка кнопок с выделением
        mouse_pos = pygame.mouse.get_pos()
        for button, text in zip([start_button, settings_button, exit_button], [start_text, settings_text, exit_text]):
            if button.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (100, 100, 100), button)  # Выделение кнопки
            else:
                pygame.draw.rect(screen, (50, 50, 50), button)
            screen.blit(text, (button.x + 50, button.y + 20))

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(mouse_pos):
                    return "start", selected_character
                elif settings_button.collidepoint(mouse_pos):
                    selected_character = settings_menu()
                elif exit_button.collidepoint(mouse_pos):
                    return "exit", selected_character

        pygame.display.flip()
        clock.tick(60)

# Функция для отображения меню настроек
def settings_menu():
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 50)
    title_text = font.render("Выберите персонажа", True, (30, 30, 30))
    player1_text = small_font.render("Персонаж 1", True, (255, 255, 255))
    player2_text = small_font.render("Персонаж 2", True, (255, 255, 255))
    player3_text = small_font.render("Персонаж 3", True, (255, 255, 255))

    selected_character = "player1"

    while True:
        screen.blit(background_image, (0, 0))  # Отображение фонового изображения
        screen.blit(title_text, (WIDTH // 2 - 200, 100))

        # Координаты и размеры кнопок
        button_width, button_height = 300, 80
        player1_button = pygame.Rect(WIDTH // 2 - 150, 250, button_width, button_height)
        player2_button = pygame.Rect(WIDTH // 2 - 150, 350, button_width, button_height)
        player3_button = pygame.Rect(WIDTH // 2 - 150, 450, button_width, button_height)

        # Отрисовка кнопок с выделением
        mouse_pos = pygame.mouse.get_pos()
        for button, text in zip([player1_button, player2_button, player3_button], [player1_text, player2_text, player3_text]):
            if button.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (100, 100, 100), button)  # Выделение кнопки
            else:
                pygame.draw.rect(screen, (50, 50, 50), button)
            screen.blit(text, (button.x + 50, button.y + 20))

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player1_button.collidepoint(mouse_pos):
                    return "player1"
                elif player2_button.collidepoint(mouse_pos):
                    return "player2"
                elif player3_button.collidepoint(mouse_pos):
                    return "player3"

        pygame.display.flip()
        clock.tick(60)

# Определение классов для платформ, монет и шипов
class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.rect)

class Coin:
    def __init__(self, x, y):
        self.image = coin_image
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# Определение уровней
levels = {
        "platforms": [
            Platform(0, HEIGHT - 40, WIDTH, 40),  # Нижняя платформа
            Platform(100, HEIGHT - 200, 200, 20),  # Платформа на высоте 200
            Platform(400, HEIGHT - 300, 200, 20),  # Платформа на высоте 300
        ],
        "coins": [
            Coin(150, HEIGHT - 220),
            Coin(450, HEIGHT - 320),
        ],
        "spikes": [
            Spike(300, HEIGHT - 40),
            Spike(600, HEIGHT - 40),
        ],
        "moving_platforms": [
            MovingPlatform(200, HEIGHT - 150, 100, 20, 2, (100, 300)),
        ],
    },
    # Добавьте другие уровни здесь

# Основной игровой цикл
def game_loop(level, character):
    player = Player(100, HEIGHT - 100, character)
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
selected_character = "player1"
while True:
    choice, selected_character = main_menu()
    if choice == "start":
        result = game_loop(levels[current_level], selected_character)
        if result == "restart":
            current_level = 0
        else:
            current_level = (current_level + 1) % len(levels)
    elif choice == "exit":
        pygame.quit()
        sys.exit()