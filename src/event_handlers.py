import logging
from game_events import GameEvent
from game_resources import GameResources
from windows.buy_window import BuyWindow
from windows.roll_window import RollWindow


logger = logging.getLogger('event')


def map_events(game, event):
    player = game.get_player(event.player_id)
    player_name = player.name if player is not None else None

    if event.event_code == 'START':
        pass
    elif event.event_code == 'ROLL':
        roll = event.payload.get('roll', 0)
        logger.debug(f"Бросок {roll} игрока {player_name}")
    elif event.event_code == 'CLOSE_ROLL_WINDOW':
        pass
    elif event.event_code == 'OFFER_PROPERTY':
        logger.debug(f"Предложение покупки для игрока {player_name}")
    elif event.event_code == 'CLICK_END_TURN':
        logger.debug(f"Нажатие конца хода игрока {player_name}")
    elif event.event_code == 'END_TURN':
        logger.debug(f"Конец хода игрока {player_name}")
    else:
        logger.debug(f"Неизвестное событие {event.event_code} для игрока {player_name}")


def current_player_event(f):
    def wrapper(game, event):
        player = game.get_player(event.player_id)

        if event.player_id != game.current_player_id:
            map_events(game, event)
            return

        f(game, event)

    return wrapper


def event_start(game, event):
    logger.debug("Начало игры")


@current_player_event
def event_roll(game, event):
    roll = event.payload.get('roll', 0)

    logger.debug(f"Бросок {roll}")

    game.current_player.move_token(roll, len(game.field))

    game.window = RollWindow(
        game.screen,
        roll,
    )


def event_close_roll_window(game, event):
    logger.debug("Закрыто окно броска")

    player_pos = game.current_player.token_position
    tile = game.field.get_tile(player_pos)
    if tile.tile_type == "property":
        if not tile.is_owned():
            # Клетка свободна, предложение купить
            GameEvent.send('OFFER_PROPERTY', game.current_player_id, {'tile': tile})
        else:
            # Клетка занята, оплата аренды
            if tile.owner != game.current_player:
                if game.current_player.balance >= tile.rent:
                    game.current_player.pay_rent(tile.owner, tile.rent)
    else:
        GameEvent.send(
            'UNUSUAL_TILE',
            game.current_player_id,
            {
                'tile_type': tile.tile_type,
                'tile': tile,
            },
        )


@current_player_event
def event_offer_property(game, event):
    logger.debug(f"Предложение покупки {event.payload}")

    player_pos = game.current_player.token_position
    tile = game.field.get_tile(player_pos)
    if tile.tile_type != "property":
        return
    if tile.is_owned():
        return

    # Клетка свободна, предложение купить
    game.window = BuyWindow(
        game.screen,
        GameResources.get('small_font'),
        tile,
        game.on_buy,
    )


@current_player_event
def event_click_end_turn(game, event):
    game.current_player.end_turn()


@current_player_event
def event_end_turn(game, event):
    logger.debug("Конец хода")

    # Переход хода
    if game.current_player_id is None:
        new_player_id = 0
    else:
        new_player_id = (game.current_player_id + 1) % 2

    game.current_player_id = new_player_id
    game.current_player.start_turn()


def default_event_handler(game, event):
    player = game.get_player(event.player_id)
    player_name = player.name if player is not None else None
    event_code = event.event_code if event is not None else None
    logger.debug(f"Неизвестное событие {event_code} для игрока {player_name}")


EVENT_HANDLERS = {
    'START': event_start,
    'ROLL': event_roll,
    'CLOSE_ROLL_WINDOW': event_close_roll_window,
    'OFFER_PROPERTY': event_offer_property,
    'CLICK_END_TURN': event_click_end_turn,
    'END_TURN': event_end_turn,
}


def get_event_handler(event):
    if event is None:
        logger.debug(f"Пустое событие {event}")
        return default_event_handler

    return EVENT_HANDLERS.get(event.event_code, default_event_handler)
