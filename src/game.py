#! /usr/bin/python
import logging
from lib2to3.btm_utils import tokens

import pygame
import random
import config
from Button import Button
from sprite_loader import load_logos_from_spritesheet
from tile import Tile


# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GOLD = (255, 215, 0)
DARK_GRAY = (150, 150, 150)

# Инициализация групп предприятий
automotive_group = "Автомобильное производство"
hotel_group = "Гостиницы"
grocery_group = "Магазины продуктов"

group_colors = {
    automotive_group: (0, 255, 255),
    hotel_group: (255, 0, 255),
    grocery_group: (255, 255, 0),
}

# Параметры спрайтлиста
LOGO_SPRITESHEET_PATH = "../res/logo_spritesheet.png"  # Путь к спрайтлисту
PLAYER_SPRITESHEET_PATH = "../res/player_spritesheet.png"  # Путь к спрайтлисту
TILE_WIDTH = 128  # Ширина одного логотипа
TILE_HEIGHT = 128  # Высота одного логотипа
ROWS = 4  # Количество строк
COLS = 4  # Количество колонок


class Game:
    def __init__(self):
        # Инициализация pygame
        pygame.init()

        # Параметры окна
        self.title = "Дѣло"
        self.background_color = WHITE
        # self.delay = delay # ???
        self.width = config.WINDOW_WIDTH
        self.height = config.WINDOW_HEIGHT
        # self.config = config # ???
        self.__is_running = False

        # Создаём окно
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)

        # Шрифты
        # pygame.font.init()
        self.FONT = None
        self.button_font = None

        # Создание кнопки
        self.next_turn_button = None

        # clock = pygame.time.Clock()

        # Игровые параметры
        self.player_balance = [1000, 1000]  # Балансы игроков
        self.current_player = 0  # Индекс текущего игрока
        self.owner_colors = {}
        self.player_positions = {}
        self.player_tokens = {}
        self.tiles = []

        # Игровые переменные
        self.turn = 1
        self.next_turn = False

        # ?
        # self.player_group = pygame.sprite.GroupSingle()
        # self.sprites = pygame.sprite.Group()
        # self.group = pygame.sprite.Group()

    @property
    def is_running(self):
        return self.__is_running

    @is_running.setter
    def is_running(self, value):
        self.__is_running = value

    def load(self):
        """Load game data before start."""
        logging.debug("Загрузка игровых данных")

        # Загрузка логотипов
        logos = load_logos_from_spritesheet(LOGO_SPRITESHEET_PATH, TILE_WIDTH, TILE_HEIGHT, ROWS, COLS)

        # Загрузка фишек
        tokens = load_logos_from_spritesheet(PLAYER_SPRITESHEET_PATH, TILE_WIDTH, TILE_HEIGHT, ROWS, COLS)

        # Шрифты
        self.FONT = pygame.font.Font(None, 36)
        self.button_font = pygame.font.SysFont("Arial", 24)

        # Создание кнопки
        self.next_turn_button = Button(300, 500, 200, 50, "Следующий ход", self.button_font, GRAY, DARK_GRAY, BLACK)

        # Игровые параметры
        self.player_balance = [1000, 1000]  # Балансы игроков
        self.current_player = 0  # Индекс текущего игрока

        # Игровые переменные
        self.turn = 1
        self.next_turn = False

        self.owner_colors = {
            0: (255, 0, 0),
            1: (0, 255, 0),
        }
        self.player_positions = {
            0: 0,
            1: 0,
        }
        self.player_tokens = {
            0: tokens[0],
            1: tokens[1],
        }

        # Пример создания предприятий с логотипами
        car_factory_logo = logos[0]
        hotel_logo = logos[1]

        # Создаем список клеток для игрового поля
        # properties = [None] * 10  # Клетки поля
        # property_prices = [random.randint(100, 300) for _ in range(10)]  # Цены на предприятия
        # property_rents = [price // 10 for price in property_prices]  # Аренда = 10% от цены
        self.tiles = [
            Tile(0, "Фабрика", 200, 20),  # Обычная клетка предприятия
            Tile(1, "Казино", 0, 0, tile_type="casino"),  # Казино
            Tile(2, "Тюрьма", 0, 0, tile_type="jail"),  # Тюрьма
            Tile(3, "Аптека", 150, 15),  # Обычная клетка предприятия
            Tile(4, "Событие", 0, 0, tile_type="event"),  # Событие
            Tile(5, "Автозавод", 500, 50, group=automotive_group, logo=car_factory_logo),
            Tile(6, "Гостиница", 300, 30, group=hotel_group, logo=hotel_logo),
            Tile(7, "Магазин продуктов", 200, 20, group=grocery_group),
            Tile(8, "Аптека", 150, 15),  # Обычная клетка предприятия
            Tile(9, "Событие", 0, 0, tile_type="event"),  # Событие
        ]

    def start(self):
        """Start game."""
        logging.debug("Запуск игры")
        self.is_running = True

    def stop(self):
        """Stop game."""
        logging.debug("Остановка игры")
        self.is_running = False

    @classmethod
    def quit(cls):
        """Start game."""
        logging.debug("Выход из игры")
        pygame.quit()

    # Отрисовка игрового поля
    def draw_board(self):
        self.screen.fill(self.background_color)

        for i in range(10):
            x, y = 50 + i * 70, 250
            # self.tiles[i].render(self.screen, x, y)
            self.tiles[i].draw_tile(self.screen, (i, 0), self.owner_colors, group_colors, self.player_positions, self.player_tokens)

    # Обработка хода
    def handle_turn(self, player):
        self.turn += 1

        player_pos = random.randint(0, 9)  # Игрок "попадает" на случайную клетку
        self.player_positions[player] = player_pos
        if not self.tiles[player_pos].is_owned():
            # Клетка свободна, предложение купить
            if self.player_balance[player] >= self.tiles[player_pos].price:
                self.tiles[player_pos].set_owner(player)
                self.player_balance[player] -= self.tiles[player_pos].price
        else:
            # Клетка занята, оплата аренды
            owner = self.tiles[player_pos].owner
            if owner != player:
                rent = self.tiles[player_pos].rent
                self.player_balance[player] -= rent
                self.player_balance[owner] += rent

        # Переход хода
        self.current_player = (player + 1) % 2

        self.next_turn = False

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop()

            # elif event.type == pygame.KEYDOWN:
            #     events.keys.set_pressed(event.key)
            # elif event.type == pygame.KEYUP:
            #     events.keys.unset_pressed(event.key)

            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     events.mouse.set_pressed(event.button)
            # elif event.type == pygame.MOUSEBUTTONUP:
            #     events.mouse.unset_pressed(event.button)

            # if events.keys.is_key_pressed(pygame.K_ESCAPE):
            #     self.stop()

            # Проверка нажатия кнопки мышью
            if self.next_turn_button.is_clicked(event):
                self.next_turn = True

            # Проверка нажатия клавиши (например, пробел для следующего хода)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.next_turn = True

    def update(self):
        # Логика игры
        # if pygame.key.get_pressed()[pygame.K_SPACE]:
        #     self.handle_turn(self.current_player)

        # Логика для следующего хода
        if self.next_turn:
            self.handle_turn(self.current_player)

    def draw(self):
        """Draw game screen."""
        # Отрисовка
        self.draw_board()

        # Отображение баланса
        player1_text = self.FONT.render(f"Игрок 1: {self.player_balance[0]}₽", True, BLACK)
        self.screen.blit(player1_text, (50, 50))

        player2_text = self.FONT.render(f"Игрок 2: {self.player_balance[1]}₽", True, BLACK)
        self.screen.blit(player2_text, (50, 100))

        # Отрисовка кнопки
        self.next_turn_button.draw(self.screen)

        # Отображение текущего хода
        turn_text = self.FONT.render(f"Ход: {self.turn}", True, BLACK)
        self.screen.blit(turn_text, (350, 450))

    def __call__(self, *args, **kwargs):
        self.load()
        self.start()

        # Основной игровой цикл
        while self.is_running:
            self.get_events()

            self.update()
            self.draw()

            # Обновление экрана
            pygame.display.flip()

            # clock.tick(30)

        self.quit()


if __name__ == "__main__":
    game = Game()
    game()
