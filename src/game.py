#! /usr/bin/python
"""Main game module."""

import logging
import random
import pygame
import colors
import config
from controls.button import Button
from buy_window import BuyWindow
from field import Field
from player import Player
from player_panel import PlayerPanel
from sprite_loader import load_logos, load_portraits


class GameResources:
    def __init__(self):
        self.__resources = {
            # Images
            'main-screen': pygame.image.load("res/main-screen.png").convert_alpha(),
            # Spritesheets
            'logos': load_logos(),
            'portraits': load_portraits(),
            # Fonts
            'big_font': pygame.font.Font("res/fonts/OldStandardTT-Regular.ttf", 36),
            'small_font': pygame.font.Font("res/fonts/OldStandardTT-Regular.ttf", 24),
        }

    def get(self, resource_id):
        return self.__resources.get(resource_id)


class Game:
    """Game main class."""

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

        # Resources
        self.resources = {}

        # Спрайты
        self.background_image = None
        self.player_panel = None

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

        # Load resources
        self.resources = GameResources()

        # Load sprites
        if config.NO_BACKGROUND:
            self.background_image = pygame.Surface(self.width, self.height)
            self.background_image.fill(self.background_color)
        else:
            self.background_image = self.resources.get('main-screen')

        self.player_panel = PlayerPanel(rect=pygame.Rect(1, 18, 274, 992))

        # Создание кнопки
        self.next_turn_button = Button(
            rect=pygame.Rect(300, 500, 200, 50),
            text="Следующий ход",
        )
        self.next_turn_button.label.font = self.resources.get('small_font')
        self.next_turn_button.label.render()
        self.next_turn_button.on_click = self.on_next_turn_button_click

        # Игровые параметры
        self.players = [
            Player(
                "Игрок 1",
                (255, 0, 0),
                # 0,
                # 1000,
                token=pygame.transform.scale(self.resources.get('portraits')[0], (64, 64)),
                avatar=self.resources.get('portraits')[0],
            ),
            Player(
                "Игрок 2",
                (0, 255, 0),
                # 0,
                # 1000,
                token=pygame.transform.scale(self.resources.get('portraits')[1], (64, 64)),
                avatar=self.resources.get('portraits')[1],
            ),
        ]
        self.current_player_id = None  # Индекс текущего игрока
        self.turn = 1
        self.next_turn = True

        # Создаем список клеток для игрового поля
        self.field = Field(self.resources.get('logos'))

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

    def on_buy(self):
        # Игрок покупает предприятие
        player_pos = self.current_player.token_position
        tile = self.field.get_tile(player_pos)
        if self.current_player.balance >= tile.price:
            self.current_player.buy_property(tile)

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
        if tile.tile_type == "property":
            if not tile.is_owned():
                # Клетка свободна, предложение купить
                self.window = BuyWindow(
                    self.screen,
                    self.resources.get('small_font'),
                    tile,
                    self.on_buy,
                )
            else:
                # Клетка занята, оплата аренды
                owner = tile.owner
                if owner != self.current_player:
                    if self.current_player.balance >= tile.rent:
                        self.current_player.pay_rent(owner, tile.rent)

        self.next_turn = False

    def on_next_turn_button_click(self):
        self.next_turn = True

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop()

            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
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
            self.next_turn_button.process_event(event)

            # Проверка нажатия клавиши (например, пробел для следующего хода)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.on_next_turn_button_click()

            self.field.update(event)

    def update(self):
        # Логика для следующего хода
        if self.next_turn:
            self.handle_turn()

        if self.window is not None and not self.window.visible:
            self.window = None

        if self.current_player_id is not None:
            self.player_panel.render(self.current_player, self.turn, self.players)

    def draw(self):
        """Draw game screen."""
        # Отрисовка
        # self.screen.fill(self.background_color)
        self.screen.blit(self.background_image, (0, 0))

        # Отрисовка игрового поля
        self.field.draw(self.screen, self.players)

        self.screen.blit(self.player_panel.image, self.player_panel.rect)

        # Отрисовка кнопки
        next_turn_button_group = pygame.sprite.Group(self.next_turn_button)
        self.next_turn_button.render()
        next_turn_button_group.draw(self.screen)

        # Отображение текущего хода
        turn_text_font = self.resources.get('big_font')
        turn_text = turn_text_font.render(f"Ход: {self.turn}", True, colors.BLACK)
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
