import pygame
import sys

# Инициализация PyGame
pygame.init()
WIDTH, HEIGHT = 1100, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D-платформер")
clock = pygame.time.Clock()

# Загрузка материалов (фото, звуки)
player_images = {
    'idle': pygame.image.load("images/персонаж.png"),
    'walk': [pygame.image.load("images/персонаж_walk1.png"), pygame.image.load("images/персонаж_walk2.png")],
    'jump': pygame.image.load("images/персонаж_jump.png")
}
coin_image = pygame.image.load("images/монета.png")
spike_image = pygame.image.load("images/шипы.png")

pygame.mixer.music.load("sounds/12cfb941f3a5f50.mp3")
pygame.mixer.music.play(-1)

# Класс главного меню
class MainMenu:
    def __init__(self):
        self.font = pygame.font.Font(None, 74)
        self.start_text = self.font.render("Начать игру", True, (255, 255, 255))
        self.exit_text = self.font.render("Выход", True, (255, 255, 255))
        self.start_rect = self.start_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        self.exit_rect = self.exit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    def draw(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.start_text, self.start_rect)
        screen.blit(self.exit_text, self.exit_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_rect.collidepoint(event.pos):
                return 'start'
            elif self.exit_rect.collidepoint(event.pos):
                return 'exit'
        return None


# Создание класса персонажа
class Player:
    def __init__(self, x, y):
        self.images = player_images
        self.image = self.images['idle']
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity_y = 0
        self.on_ground = False
        self.walk_index = 0

    def update(self, moving_left, moving_right):
        # Анимация
        if not self.on_ground:
            self.image = self.images['jump']
        elif moving_left or moving_right:
            self.walk_index += 0.1
            if self.walk_index >= len(self.images['walk']):
                self.walk_index = 0
            self.image = self.images['walk'][int(self.walk_index)]
        else:
            self.image = self

.images['idle']

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


# Функция для проверки коллизий с платформами
def check_collision(player, platforms):
    for platform in platforms:
        if player.rect.colliderect(platform.rect):
            if player.velocity_y > 0:
                player.rect.bottom = platform.rect.top
                player.on_ground = True
                player.velocity_y = 0


# Функция для проверки коллизий с шипами
def check_spike_collision(player, spikes):
    for spike in spikes:
        if player.rect.colliderect(spike.rect):
            return True
    return False


# Функция для загрузки уровня
def load_level(level):
    if level == 1:
        platforms = [
            Platform(0, HEIGHT - 50, WIDTH, 50),
            Platform(200, 400, 200, 20),
            Platform(500, 300, 150, 20),
        ]
        coins = [Coin(250, 350), Coin(550, 250)]
        spikes = [Spike(700, HEIGHT - 50 - spike_image.get_height())]
    elif level == 2:
        platforms = [
            Platform(0, HEIGHT - 50, WIDTH, 50),
            Platform(300, 500, 150, 20),
            Platform(600, 400, 150, 20),
        ]
        coins = [Coin(350, 450), Coin(620, 350)]
        spikes = [Spike(800, HEIGHT - 50 - spike_image.get_height())]
    else:
        platforms = []
        coins = []
        spikes = []
    return platforms, coins, spikes


# Основной игровой цикл
def main():
    main_menu = MainMenu()
    player = Player(100, HEIGHT - 100)
    current_level = 1
    platforms, coins, spikes = load_level(current_level)
    score = 0

    running = True
    in_game = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


if not in_game:
    action = main_menu.handle_event(event)
    if action == 'start':
        in_game = True
    elif action == 'exit':
        running = False

if not in_game:
    main_menu.draw(screen)
else:
    # Управление персонажем
    keys = pygame.key.get_pressed()
    moving_left = keys[pygame.K_a]
    moving_right = keys[pygame.K_d]

    if moving_left:
        player.rect.x -= 5
    if moving_right:
        player.rect.x += 5
    if keys[pygame.K_SPACE]:
        player.jump()

    # Обновление игровых объектов
    player.update(moving_left, moving_right)
    check_collision(player, platforms)

    # Проверка сбора монет
    for coin in coins[:]:
        if player.rect.colliderect(coin.rect):
            coins.remove(coin)
            score += 1
            coin_sound.play()

    # Проверка коллизий с шипами
    if check_spike_collision(player, spikes):
        print("Вы проиграли!")
        running = False

    # Переход на следующий уровень
    if not coins and current_level < 2:
        current_level += 1
        platforms, coins, spikes = load_level(current_level)
        player.rect.topleft = (100, HEIGHT - 100)

    # Отрисовка
    screen.fill((0, 0, 0))  # Очистка экрана

    # Отрисовка платформ
    for platform in platforms:
        platform.draw(screen)

    # Отрисовка монет
    for coin in coins:
        coin.draw(screen)

    # Отрисовка шипов
    for spike in spikes:
        spike.draw(screen)

    # Отрисовка персонажа
    screen.blit(player.image, player.rect)

    # Отображение счета
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Счет: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Обновление экрана
pygame.display.flip()
clock.tick(60)  # Ограничение FPS

# Завершение игры
pygame.quit()
sys.exit()

main()