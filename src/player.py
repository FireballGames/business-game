"""Объявление класса Player."""
import random
from game_events import GameEvent


class Player:
    """Данные игрока."""

    # TODO: Fix this lint warnings
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-positional-arguments

    def __init__(
        self,
        player_id,
        name: str,
        color,
        token_position=0,
        balance=60000,
        token=None,
        avatar=None,
        properties=None,
        in_jail=False,
        turns_in_jail=0,
        inventory=None,
    ):
        """
        Инициализация игрока.

        :param name: Имя игрока.
        :param color: Цвет игрока (например, для отображения фишки).
        :param token_position: Текущая позиция игрока на поле.
        :param balance: Сумма денег у игрока.
        :param properties: Список предприятий, принадлежащих игроку.
        :param in_jail: Флаг, указывающий, находится ли игрок в тюрьме.
        :param turns_in_jail: Количество ходов, оставшихся до выхода из тюрьмы.
        :param inventory: Дополнительные элементы инвентаря, например, карточки казино.
        """
        self.player_id = player_id
        self.name = name
        self.color = color
        self.token_position = token_position
        self.balance = balance
        self.avatar = avatar
        self.token = token
        self.properties = properties if properties else []
        self.in_jail = in_jail
        self.turns_in_jail = turns_in_jail
        self.inventory = inventory if inventory else []

        self.turn = 0

        self.has_rolled = False

        self.last_event_id = None
        self.event_log = []

    def move_token(self, steps, board_size):
        """
        Переместить фишку на указанное количество клеток.

        :param steps: Количество клеток для перемещения.
        :param board_size: Размер игрового поля.
        """
        self.token_position = (self.token_position + steps) % board_size

    def adjust_balance(self, amount):
        """
        Изменить баланс игрока.

        :param amount: Сумма изменения (может быть положительной или отрицательной).
        """
        self.balance += amount

    def buy_property(self, property_cell):
        """
        Купить предприятие и добавить его в список собственности игрока.

        :param property_cell: Клетка с информацией о предприятии.
        """
        if self.balance >= property_cell.price:
            self.adjust_balance(-property_cell.price)
            self.properties.append(property_cell)
            # property_cell.owner = self
            property_cell.set_owner(self)
        else:
            raise ValueError("Недостаточно средств для покупки.")

    def pay_rent(self, owner, amount):
        """
        Оплатить ренту владельцу клетки.

        :param owner: Игрок, которому должна быть выплачена рента.
        :param amount: Сумма ренты.
        """
        if self.balance >= amount:
            self.adjust_balance(-amount)
            owner.adjust_balance(amount)
        else:
            raise ValueError("Недостаточно средств для оплаты ренты.")

    def go_to_jail(self):
        """
        Отправить игрока в тюрьму.
        """
        self.in_jail = True
        self.turns_in_jail = 3

    def release_from_jail(self):
        """
        Выпустить игрока из тюрьмы.
        """
        self.in_jail = False
        self.turns_in_jail = 0

    def start_turn(self):
        self.turn += 1
        self.has_rolled = False

    def do_roll(self):
        if self.has_rolled:
            return

        roll = random.randint(1, 6)  # Игрок "попадает" на случайную клетку
        GameEvent.send(
            'ROLL',
            self.player_id,
            {
                'turn': self.turn,
                'roll': roll,
            },
        )
        self.has_rolled = True

    def end_turn(self):
        if not self.has_rolled:
            return

        GameEvent.send('END_TURN', self.player_id)

    def __repr__(self):
        return f"Player(name={self.name}, balance={self.balance}, " \
            + f"position={self.token_position}, properties={len(self.properties)})"
