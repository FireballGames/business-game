#! /usr/bin/python
import logging
import pygame
import random
import colors
import config
import groups
from button import Button
from buy_window import BuyWindow
from player import Player
from sprite_loader import load_logos, load_tokens
from tile import Tile


class Game:
    def __init__(self):
        # Инициализация pygame
        pygame.init()

        # Параметры окна
        self.title = "Дѣло"
        self.background_color = colors.WHITE
        # self.delay = delay # ???
        self.width = config.WINDOW_WIDTH
        self.height = config.WINDOW_HEIGHT
        # self.config = config # ???
        self.__is_running = False

        # Создаём окно
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)

        # Шрифты
        self.FONT = None
        self.button_font = None

        # Создание кнопки
        self.next_turn_button = None
        self.window = None

        # clock = pygame.time.Clock()

        # Игровые параметры
        self.players = []
        self.current_player_id = None  # Индекс текущего игрока
        self.tiles = []
        self.turn = 1
        self.next_turn = False

        self.field_offset_x = 500
        self.field_offset_y = 100

        self.dragging = False
        self.start_drag_pos = (0, 0)

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

    @property
    def current_player(self):
        return self.players[self.current_player_id]

    def load(self):
        """Load game data before start."""
        logging.debug("Загрузка игровых данных")

        # Загрузка логотипов
        logos = load_logos()

        # Загрузка фишек
        tokens = load_tokens()

        # Шрифты
        self.FONT = pygame.font.Font("res/fonts/OldStandardTT-Regular.ttf", 36)
        self.button_font = pygame.font.SysFont("res/fonts/OldStandardTT-Regular.ttf", 24)

        # Создание кнопки
        self.next_turn_button = Button(300, 500, 200, 50, "Следующий ход", self.button_font, colors.GRAY, colors.DARK_GRAY, colors.BLACK)

        # Игровые параметры
        self.players = [
            Player("Player 1", (255, 0, 0), 0, 1000, tokens[0]),
            Player("Player 2", (0, 255, 0), 0, 1000, tokens[1]),
        ]
        self.current_player_id = None  # Индекс текущего игрока
        self.turn = 1
        self.next_turn = False

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
            Tile(5, "Автозавод", 500, 50, group=groups.AutomotiveGroup, logo=car_factory_logo),
            Tile(6, "Гостиница", 300, 30, group=groups.HotelGroup, logo=hotel_logo),
            Tile(7, "Магазин продуктов", 200, 20, group=groups.GroceryGroup),
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
            # x, y = 50 + i * 70, 250
            # self.tiles[i].render(self.screen, x, y)
            offset = self.field_offset_x, self.field_offset_y
            self.tiles[i].draw_tile(self.screen, (i, 0), offset, self.players)

    def on_buy(self):
        # Игрок покупает предприятие
        player_pos = self.current_player.token_position
        if self.current_player.balance >= self.tiles[player_pos].price:
            self.tiles[player_pos].set_owner(self.current_player_id)
            self.current_player.balance -= self.tiles[player_pos].price

    # Обработка хода
    def handle_turn(self):
        # Переход хода
        if self.current_player_id is None:
            player = 0
        else:
            player = (self.current_player_id + 1) % 2
        self.current_player_id = player
        self.turn += 1

        roll = random.randint(1, 6)  # Игрок "попадает" на случайную клетку
        self.current_player.move_token(roll, len(self.tiles))
        player_pos = self.current_player.token_position
        if not self.tiles[player_pos].is_owned():
            # Клетка свободна, предложение купить
            self.window = BuyWindow(self.screen, self.button_font, self.tiles[player_pos], self.on_buy)
        else:
            # Клетка занята, оплата аренды
            owner = self.tiles[player_pos].owner
            if owner != player:
                rent = self.tiles[player_pos].rent
                self.current_player.balance -= rent
                self.players[owner].balance += rent

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

            if self.window is not None:
                self.window.update(event)
                continue

            # Проверка нажатия кнопки мышью
            if self.next_turn_button.is_clicked(event):
                self.next_turn = True

            # Проверка нажатия клавиши (например, пробел для следующего хода)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.next_turn = True

            # Нажатие мыши
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    self.dragging = True
                    self.start_drag_pos = event.pos

            # Отпускание мыши
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Левая кнопка мыши
                    self.dragging = False

            # Перемещение мыши
            if event.type == pygame.MOUSEMOTION:
                if self.dragging:
                    dx, dy = event.pos[0] - self.start_drag_pos[0], event.pos[1] - self.start_drag_pos[1]
                    self.field_offset_x += dx
                    self.field_offset_y += dy
                    self.start_drag_pos = event.pos

    def update(self):
        # Логика игры
        # if pygame.key.get_pressed()[pygame.K_SPACE]:
        #     self.handle_turn(self.current_player_id)

        # Логика для следующего хода
        if self.next_turn:
            self.handle_turn()

        if self.window is not None and not self.window.visible:
            self.window = None

    def draw(self):
        """Draw game screen."""
        # Отрисовка
        self.draw_board()

        # Отображение баланса
        player1_text = self.FONT.render(f"Игрок 1: {self.players[0].balance}₽", True, colors.BLACK)
        self.screen.blit(player1_text, (50, 50))

        player2_text = self.FONT.render(f"Игрок 2: {self.players[1].balance}₽", True, colors.BLACK)
        self.screen.blit(player2_text, (50, 100))

        # Отрисовка кнопки
        self.next_turn_button.draw(self.screen)

        # Отображение текущего хода
        turn_text = self.FONT.render(f"Ход: {self.turn}", True, colors.BLACK)
        self.screen.blit(turn_text, (350, 450))

        if self.window is not None:
            self.window.draw(self.screen)

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
