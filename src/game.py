#! /usr/bin/python
import logging
import pygame
import random
import colors
import config
from button import Button
from buy_window import BuyWindow
from field import Field
from player import Player
from sprite_loader import load_logos, load_tokens


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
        self.field = None
        self.turn = 1
        self.next_turn = False

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

        # Создаем список клеток для игрового поля
        self.field = Field(logos)

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

        self.field.draw(self.screen, self.players)

    def on_buy(self):
        # Игрок покупает предприятие
        player_pos = self.current_player.token_position
        tile = self.field.get_tile(player_pos)
        if self.current_player.balance >= tile.price:
            tile.set_owner(self.current_player_id)
            self.current_player.balance -= tile.price

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
        self.current_player.move_token(roll, len(self.field))
        player_pos = self.current_player.token_position
        tile = self.field.get_tile(player_pos)
        if not tile.is_owned():
            # Клетка свободна, предложение купить
            self.window = BuyWindow(self.screen, self.button_font, tile, self.on_buy)
        else:
            # Клетка занята, оплата аренды
            owner = tile.owner
            if owner != player:
                rent = tile.rent
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

            # if pygame.key.get_pressed()[pygame.K_SPACE]:
            #     self.handle_turn(self.current_player_id)

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

            self.field.update(event)

    def update(self):
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
