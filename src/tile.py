import pygame
import colors


class Tile:
    # Размеры клетки
    TILE_WIDTH = 128
    TILE_HEIGHT = 64

    def __init__(self, tile_id, name, price, rent=None, tile_type="property", owner=None, logo=None, group=None, position=(0, 0)):
        """
        Инициализация клетки.

        :param tile_id: Уникальный идентификатор клетки.
        :param name: Название клетки (например, "Фабрика" или "Гостиница").
        :param price: Цена клетки (если применимо).
        :param rent: Арендная плата за клетку (если применимо).
        :param tile_type: Тип клетки (property, casino, jail, event).
        :param owner: Владелец клетки (None, если клетка свободна).
        :param logo: Логотип или изображение для клетки (для отрисовки).
        :param group: Группа предприятия (например, "Автомобильное производство", "Гостиницы").
        """
        self.tile_id = tile_id
        self.name = name

        self.price = price
        self.rent = 0
        if rent is not None:
            self.rent = rent
        elif tile_type == "property":
            self.rent = price // 10

        self.owner = owner
        self.tile_type = tile_type
        self.logo = logo  # Логотип или изображение для отрисовки
        self.group = group  # Группа, к которой относится предприятие (например, "Автомобильное производство")

        self.position = position
        self.logo_index = None

        self.font = pygame.font.SysFont("../res/fonts/OldStandardTT-Regular.ttf", 16)

    def is_owned(self):
        """Проверяет, есть ли у клетки владелец."""
        return self.owner is not None

    def set_owner(self, owner):
        """Устанавливает владельца клетки."""
        self.owner = owner

    def reset(self):
        """Сбрасывает владельца клетки."""
        self.owner = None

    def get_group(self):
        """Возвращает группу предприятия."""
        return self.group

    def render(self, screen, x, y):
        """Отображение клетки на экране (включая логотип)."""
        color = colors.GRAY if self.is_owned() else colors.GOLD
        pygame.draw.rect(screen, color, (x, y, 60, 60))

        if self.logo:
            # Здесь будет код для отрисовки логотипа на координатах (x, y).
            screen.blit(self.logo, (x + 2, y + 2), (0, 0, 56, 56))  # Псевдокод для отрисовки
        else:
            # Отображение текстового названия, если логотип не задан
            label = self.font.render(self.name, True, colors.BLACK)
            screen.blit(label, (x + 5, y + 30))

        text = self.font.render(f"{self.price}₽", True, colors.BLACK)
        screen.blit(text, (x + 5, y + 5))

        if self.is_owned():
            owner_text = self.font.render(self.owner.name, True, colors.BLACK)
            screen.blit(owner_text, (x + 30, y + 5))

    ####

    def draw_tile(self, screen, position, offset, players):
        """
        Отображает клетку на экране в изометрическом стиле.

        :param screen: Экран для отображения.
        :param position: Координаты клетки (x, y).
        :param offset:
        :param players:
        """

        offset_x, offset_y = offset

        # Координаты изометрической клетки
        x, y = position
        iso_x = x - y
        iso_y = x + y

        # Центр клетки
        center_x = (offset_x - self.TILE_WIDTH // 2) + iso_x * self.TILE_WIDTH // 2
        center_y = offset_y + iso_y * self.TILE_HEIGHT // 2

        # Цвет группы клетки
        group_color = self.group.color if self.group is not None else (200, 200, 200)  # Если группа не найдена, серый цвет

        # Цвет владельца
        owner_color = colors.GOLD
        if self.is_owned():
            owner_color = self.owner.color or (255, 255, 255)  # Если владелец не найден, белый цвет

        # Рисуем клетку как ромб
        points = [
            (center_x, center_y - self.TILE_HEIGHT // 2),  # Верх
            (center_x + self.TILE_WIDTH // 2, center_y),  # Право
            (center_x, center_y + self.TILE_HEIGHT // 2),  # Низ
            (center_x - self.TILE_WIDTH // 2, center_y)   # Лево
        ]
        pygame.draw.polygon(screen, group_color, points)  # Цвет по группе

        # Отображение владельца
        pygame.draw.polygon(screen, owner_color, points, 1)  # Чёрная рамка
        # pygame.draw.circle(screen, owner_color, (center_x, center_y), 10)

        # Логотип предприятия (если есть)
        if self.logo:
            # Здесь будет код для отрисовки логотипа на координатах (x, y).
            # logo_rect = self.logo.get_rect(center=(center_x, center_y))
            logo_rect = (center_x - self.TILE_WIDTH // 2, center_y - self.TILE_HEIGHT * 2)
            screen.blit(self.logo, logo_rect)  # Псевдокод для отрисовки
        else:
            # Если логотипа нет, отображаем название
            label = self.font.render(self.name, True, colors.BLACK)
            screen.blit(label, (center_x - self.TILE_WIDTH // 4, center_y - self.TILE_HEIGHT // 4))

        text = self.font.render(f"{self.price}₽", True, colors.BLACK)
        screen.blit(text, (center_x - 32, center_y + 8))

        # Отображение фишек игроков, находящихся на клетке
        for player_id, player in enumerate(players):
            if player.token_position == self.tile_id:
                # Координаты для фишки
                token_x = center_x - self.TILE_WIDTH // 2  # center_x + self.TILE_WIDTH // 4
                token_y = center_y + self.TILE_HEIGHT // 2 - 128 - player_id * 8  # center_y + self.TILE_HEIGHT // 4 + player_id * 10
                screen.blit(player.token, (token_x, token_y))
