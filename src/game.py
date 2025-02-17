#! /usr/bin/python
"""Main game module."""

import logging
import random
import pygame
import colors
import config
from event_handlers import get_event_handler
from game_events import GameEvent
from game_resources import GameResources
from controls.button import Button
from sprite_groups.main_gui import MainGUI
from field import Field
from player import Player
from main_panel import MainPanel
from windows.buy_window import BuyWindow
from windows.rent_window import RentWindow
from windows.roll_window import RollWindow


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

        # Спрайты
        self.background_image = None
        self.main_gui = MainGUI()
        self.player_panel = None
        self.main_panel = None
        self.tile_panel = None

        # Создание кнопки
        self.next_turn_button = None
        self.buy_property_button = None

        self.window = None

        # clock = pygame.time.Clock()

        # Игровые параметры
        self.players = []
        self.current_player_id = None  # Индекс текущего игрока
        self.field = None

    @property
    def is_running(self):
        return self.__is_running

    @is_running.setter
    def is_running(self, value):
        self.__is_running = value

    @property
    def current_player(self):
        return self.get_player(self.current_player_id)

    def get_player(self, player_id):
        if player_id is None:
            return None

        return self.players[player_id]

    def load(self):
        """Load game data before start."""
        logging.debug("Загрузка игровых данных")

        # Load resources
        GameResources.load()

        # Load sprites
        if config.NO_BACKGROUND:
            self.background_image = pygame.Surface(self.width, self.height)
            self.background_image.fill(self.background_color)
        else:
            self.background_image = GameResources.get('main-screen')

        # Игровые параметры
        self.players = [
            Player(
                0,
                "Игрок 1",
                (255, 0, 0),
                # 0,
                # 1000,
                token=pygame.transform.scale(GameResources.get('portraits')[0], (64, 64)),
                avatar=GameResources.get('portraits')[0],
            ),
            Player(
                1,
                "Игрок 2",
                (0, 255, 0),
                # 0,
                # 1000,
                token=pygame.transform.scale(GameResources.get('portraits')[1], (64, 64)),
                avatar=GameResources.get('portraits')[1],
            ),
        ]
        self.current_player_id = None  # Индекс текущего игрока

        # Создаем список клеток для игрового поля
        self.field = Field(GameResources.get('logos'))

        self.player_panel = self.main_gui.player_panel
        self.tile_panel = self.main_gui.tile_panel

        self.main_panel = MainPanel(
            self.main_gui,
            field=self.field,
        )
        self.main_gui.main_panel = self.main_panel

        # Создание кнопки
        self.next_turn_button = self.main_panel.turn_panel_group.next_turn_button
        self.next_turn_button.on_click = self.on_next_turn_button_click

        self.buy_property_button = self.main_panel.action_panel_group.buy_button
        self.buy_property_button.on_click = self.offer_property

        GameEvent.send('START')

        self.current_player_id = 0
        self.current_player.start_turn()

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

    def on_next_turn_button_click(self):
        GameEvent.send('CLICK_END_TURN', self.current_player_id)

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
                self.window.process_event(event)
                continue

            # Проверка нажатия кнопки мышью
            self.next_turn_button.process_event(event)

            # Проверка нажатия клавиши (например, пробел для следующего хода)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.on_next_turn_button_click()

            self.main_panel.process_event(event)

    def process_event(self, event):
        current_player = self.current_player

        event_logger = logging.getLogger('event')

        event_logger.debug(f"Обрабатываем событие {event} для игрока {current_player.name}")

        if event is None:
            event_logger.debug(f"Пустое событие {event}")
            return

        handler = get_event_handler(event)
        handler(self, event)

        event_logger.debug(f"Сохраняем событие #{event.event_id} для игрока {current_player.name}")
        current_player.event_log.append(event)
        current_player.last_event_id = event.event_id

    def update(self):
        if self.window is not None and not self.window.visible:
            self.window = None

        if self.current_player is not None:
            self.main_panel.update_data(self.current_player, self.players)
            self.player_panel.render(self.current_player)
            self.tile_panel.render(self.current_player.turn, self.players)

            for e in GameEvent.load(self.current_player.last_event_id):
                self.process_event(e)

        self.main_gui.rect = self.screen.get_rect().inflate(0, -18)

    def draw(self):
        """Draw game screen."""
        # Отрисовка
        # self.screen.fill(self.background_color)
        self.screen.blit(self.background_image, (0, 0))

        # Отрисовка игрового поля
        self.main_gui.update()
        self.main_gui.draw(self.screen)
        self.main_panel.draw_panels(self.screen)

        if self.window is not None:
            self.window.update()
            self.window.draw(self.screen)

    # Window event

    def close_roll_window(self):
        logging.debug("Закрыто окно броска")

        player_pos = self.current_player.token_position
        tile = self.field.get_tile(player_pos)

        if tile is None:
            return

        payload = {
            'tile_id': tile.tile_id,
            'tile_type': tile.tile_type,
            'tile': tile,
        }
        if tile.tile_type == "property":
            if not tile.is_owned():
                # Клетка свободна, предложение купить
                GameEvent.send('OFFER_PROPERTY', self.current_player_id, payload)
            else:
                # Клетка занята, оплата аренды
                GameEvent.send('PAY_RENT', self.current_player_id, payload)
        else:
            GameEvent.send('UNUSUAL_TILE', self.current_player_id, payload)

    def on_buy(self):
        # Игрок покупает предприятие
        player_pos = self.current_player.token_position
        tile = self.field.get_tile(player_pos)

        if self.current_player.balance < tile.price:
            return

        self.current_player.buy_property(tile)

    def on_pay_rent(self):
        # Игрок покупает предприятие
        player_pos = self.current_player.token_position
        tile = self.field.get_tile(player_pos)

        if self.current_player.balance < tile.price:
            return

        self.current_player.pay_rent(tile.owner, tile.rent)

    # Game events

    def move_player(self, roll):
        self.current_player.move_token(roll, len(self.field))

        self.window = RollWindow(
            self.screen,
            roll,
            on_close=self.close_roll_window,
        )

    def offer_property(self):
        player_pos = self.current_player.token_position
        tile = self.field.get_tile(player_pos)

        if tile.tile_type != "property":
            return

        if tile.is_owned():
            return

        # Клетка свободна, предложение купить
        self.window = BuyWindow(
            self.screen,
            GameResources.get('small_font'),
            tile,
            self.on_buy,
        )

    def pay_rent(self):
        player_pos = self.current_player.token_position
        tile = self.field.get_tile(player_pos)

        if tile.tile_type != "property":
            return

        if not tile.is_owned():
            return

        if tile.owner == self.current_player:
            return

        # Клетка занята, оплата аренды
        self.window = RentWindow(
            self.screen,
            tile,
            on_close=self.on_pay_rent,
        )

    # Run game

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
