import pygame
import groups
from tile import Tile


class Field:
    def __init__(self, logos):
        # Пример создания предприятий с логотипами
        car_factory_logo = logos[0]
        hotel_logo = logos[1]

        self.offset_x = 500
        self.offset_y = 100

        self.dragging = False
        self.start_drag_pos = (0, 0)

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
            Tile(10, "Фабрика", 200, 20),  # Обычная клетка предприятия
            Tile(11, "Казино", 0, 0, tile_type="casino"),  # Казино
            Tile(12, "Тюрьма", 0, 0, tile_type="jail"),  # Тюрьма
            Tile(13, "Аптека", 150, 15),  # Обычная клетка предприятия
            Tile(14, "Событие", 0, 0, tile_type="event"),  # Событие
            Tile(15, "Автозавод", 500, 50, group=groups.AutomotiveGroup, logo=car_factory_logo),
            Tile(16, "Гостиница", 300, 30, group=groups.HotelGroup, logo=hotel_logo),
            Tile(17, "Магазин продуктов", 200, 20, group=groups.GroceryGroup),
            Tile(18, "Аптека", 150, 15),  # Обычная клетка предприятия
            Tile(19, "Событие", 0, 0, tile_type="event"),  # Событие
            Tile(20, "Фабрика", 200, 20),  # Обычная клетка предприятия
            Tile(21, "Казино", 0, 0, tile_type="casino"),  # Казино
            Tile(22, "Тюрьма", 0, 0, tile_type="jail"),  # Тюрьма
            Tile(23, "Аптека", 150, 15),  # Обычная клетка предприятия
            Tile(24, "Событие", 0, 0, tile_type="event"),  # Событие
            Tile(25, "Автозавод", 500, 50, group=groups.AutomotiveGroup, logo=car_factory_logo),
            Tile(26, "Гостиница", 300, 30, group=groups.HotelGroup, logo=hotel_logo),
            Tile(27, "Магазин продуктов", 200, 20, group=groups.GroceryGroup),
            Tile(28, "Аптека", 150, 15),  # Обычная клетка предприятия
            Tile(29, "Событие", 0, 0, tile_type="event"),  # Событие
        ]

    def __len__(self):
        return len(self.tiles)

    def get_tile(self, tile_id):
        return self.tiles[tile_id]


    def update(self, event):
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
                self.offset_x += dx
                self.offset_y += dy
                self.start_drag_pos = event.pos

    # Отрисовка игрового поля
    def draw(self, screen, players):
        offset = self.offset_x, self.offset_y
        starter_tile_id = 0
        j = 0
        while starter_tile_id < len(self.tiles):
            for i in range(11):
                # x, y = 50 + i * 70, 250
                # self.tiles[i].render(self.screen, x, y)
                tile_id = starter_tile_id + i
                if tile_id < len(self.tiles):
                    self.tiles[tile_id].draw_tile(screen, (i, j), offset, players)

            tile_id = starter_tile_id + 11
            if tile_id < len(self.tiles):
                self.tiles[tile_id].draw_tile(screen, (10, j + 1), offset, players)

            for i in range(11):
                # x, y = 50 + i * 70, 250
                # self.tiles[i].render(self.screen, x, y)
                tile_id = starter_tile_id + 22 - i
                if tile_id < len(self.tiles):
                    self.tiles[tile_id].draw_tile(screen, (i, j + 2), offset, players)

            tile_id = starter_tile_id + 23
            if tile_id < len(self.tiles):
                self.tiles[tile_id].draw_tile(screen, (0, j + 3), offset, players)

            starter_tile_id += 24
            j += 4
