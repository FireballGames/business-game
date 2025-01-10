import pygame
import random
from tile import Tile

# Инициализация pygame
pygame.init()

# Параметры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Имперские магнаты")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GOLD = (255, 215, 0)

# Шрифты
FONT = pygame.font.Font(None, 36)

# Игровые параметры
player_balance = [1000, 1000]  # Балансы игроков
current_player = 0  # Индекс текущего игрока

# Создаем список клеток для игрового поля
# properties = [None] * 10  # Клетки поля
# property_prices = [random.randint(100, 300) for _ in range(10)]  # Цены на предприятия
# property_rents = [price // 10 for price in property_prices]  # Аренда = 10% от цены
tiles = [
    Tile(0, "Фабрика", 200, 20),  # Обычная клетка предприятия
    Tile(1, "Казино", 0, 0, tile_type="casino"),  # Казино
    Tile(2, "Тюрьма", 0, 0, tile_type="jail"),  # Тюрьма
    Tile(3, "Аптека", 150, 15),  # Обычная клетка предприятия
    Tile(4, "Событие", 0, 0, tile_type="event"),  # Событие
    Tile(5, "Фабрика", 200, 20),  # Обычная клетка предприятия
    Tile(6, "Казино", 0, 0, tile_type="casino"),  # Казино
    Tile(7, "Тюрьма", 0, 0, tile_type="jail"),  # Тюрьма
    Tile(8, "Аптека", 150, 15),  # Обычная клетка предприятия
    Tile(9, "Событие", 0, 0, tile_type="event"),  # Событие
]

game_running = True

# Отрисовка игрового поля
def draw_board():
    screen.fill(WHITE)
    for i in range(10):
        x, y = 50 + i * 70, 250
        color = GRAY if tiles[i].is_owned() else GOLD
        pygame.draw.rect(screen, color, (x, y, 60, 60))
        text = FONT.render(f"{tiles[i].price}₽", True, BLACK)
        screen.blit(text, (x + 5, y + 5))
        if tiles[i].is_owned():
            owner_text = FONT.render(f"P{tiles[i].owner + 1}", True, BLACK)
            screen.blit(owner_text, (x + 5, y + 30))

# Обработка хода
def handle_turn(player):
    global current_player
    player_pos = random.randint(0, 9)  # Игрок "попадает" на случайную клетку
    if not tiles[player_pos].is_owned():
        # Клетка свободна, предложение купить
        if player_balance[player] >= tiles[player_pos].price:
            tiles[player_pos].set_owner(player)
            player_balance[player] -= tiles[player_pos].price
    else:
        # Клетка занята, оплата аренды
        owner = tiles[player_pos].owner
        if owner != player:
            rent = tiles[player_pos].rent
            player_balance[player] -= rent
            player_balance[owner] += rent
    # Переход хода
    current_player = (current_player + 1) % 2

# Основной игровой цикл
while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    # Логика игры
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        handle_turn(current_player)

    # Отрисовка
    draw_board()

    # Отображение баланса
    player1_text = FONT.render(f"Игрок 1: {player_balance[0]}₽", True, BLACK)
    player2_text = FONT.render(f"Игрок 2: {player_balance[1]}₽", True, BLACK)
    screen.blit(player1_text, (50, 50))
    screen.blit(player2_text, (50, 100))

    # Обновление экрана
    pygame.display.flip()

pygame.quit()
