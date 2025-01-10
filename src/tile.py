import pygame


class Tile:
    def __init__(self, tile_id, name, price, rent, tile_type="property", owner=None, logo=None, group=None, **kwargs):
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
        self.rent = rent
        self.owner = owner
        self.tile_type = tile_type
        self.logo = logo  # Логотип или изображение для отрисовки
        self.group = group  # Группа, к которой относится предприятие (например, "Автомобильное производство")

        self.position = None
        self.logo_index = None

    def is_owned(self):
        """Проверяет, есть ли у клетки владелец."""
        return self.owner is not None

    def set_owner(self, owner_id):
        """Устанавливает владельца клетки."""
        self.owner = owner_id

    def reset(self):
        """Сбрасывает владельца клетки."""
        self.owner = None

    def get_group(self):
        """Возвращает группу предприятия."""
        return self.group

    def render(self, screen, x, y):
        """Отображение клетки на экране (включая логотип)."""
        if self.logo:
            # Здесь будет код для отрисовки логотипа на координатах (x, y).
            screen.blit(self.logo, (x, y))  # Псевдокод для отрисовки
        else:
            # Отображение текстового названия, если логотип не задан
            font = pygame.font.SysFont("Arial", 20)
            label = font.render(self.name, True, (0, 0, 0))
            screen.blit(label, (x, y))
