#! /usr/bin/python
import logging
import pygame
import random
import config
from tile import Tile


# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GOLD = (255, 215, 0)


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

        # Игровые параметры
        self.player_balance = [1000, 1000]  # Балансы игроков
        self.current_player = 0  # Индекс текущего игрока
        self.tiles = []

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

        # Шрифты
        self.FONT = pygame.font.Font(None, 36)

        # Игровые параметры
        self.player_balance = [1000, 1000]  # Балансы игроков
        self.current_player = 0  # Индекс текущего игрока

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
            Tile(5, "Фабрика", 200, 20),  # Обычная клетка предприятия
            Tile(6, "Казино", 0, 0, tile_type="casino"),  # Казино
            Tile(7, "Тюрьма", 0, 0, tile_type="jail"),  # Тюрьма
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
            color = GRAY if self.tiles[i].is_owned() else GOLD
            pygame.draw.rect(self.screen, color, (x, y, 60, 60))
            text = self.FONT.render(f"{self.tiles[i].price}₽", True, BLACK)
            self.screen.blit(text, (x + 5, y + 5))
            if self.tiles[i].is_owned():
                owner_text = self.FONT.render(f"P{self.tiles[i].owner + 1}", True, BLACK)
                self.screen.blit(owner_text, (x + 5, y + 30))

    # Обработка хода
    def handle_turn(self, player):
        player_pos = random.randint(0, 9)  # Игрок "попадает" на случайную клетку
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

    def update(self):
        # Логика игры
        if pygame.key.get_pressed()[pygame.K_SPACE]:
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

        # self.screen.fill(self.background_color)
        # self.sprites.draw(self.screen)

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

        self.quit()


if __name__ == "__main__":
    game = Game()
    game()
