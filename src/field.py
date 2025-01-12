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
        self.tiles = [
            Tile(0, "Банкъ", 1000, tile_type="bank", position=(0, 0)),  # Стартовая клетка
            Tile(1, "Руссо-Балтъ", 9000, 50, group=groups.AutomotiveGroup, logo=car_factory_logo, position=(1, 0)),
            Tile(2, "Ньюпортъ", 20000, 50, position=(2, 0)),
            Tile(3, "Доходный домъ", 9000, 30, group=groups.HotelGroup, logo=hotel_logo, position=(3, 0)),
            Tile(4, "Рулѣтка", 0, tile_type="casino", position=(4, 0)),  # Казино
            Tile(5, "Гарфункѣль", 10000, 50, position=(5, 0)),
            Tile(6, "Елѣсѣѣвъ", 2000, 20, group=groups.GroceryGroup, position=(6, 0)),
            Tile(7, "Філіповъ", 1500, 20, group=groups.GroceryGroup, position=(7, 0)),
            Tile(8, "Табакь", 1000, 50, position=(8, 0)),
            Tile(9, "Трактіръ", 5000, 20, group=groups.GroceryGroup, position=(9, 0)),
            Tile(10, "Квасъ", 7000, 20, group=groups.GroceryGroup, position=(10, 0)),

            Tile(11, "Околотокъ", 10000, tile_type="jail", position=(10, 1)),  # Тюрьма

            Tile(12, "Зінгѣръ", 3000, 0, position=(10, 2)),
            Tile(13, "Сбітѣнь", 7000, 15, group=groups.GroceryGroup, position=(9, 2)),  # Обычная клетка предприятия
            Tile(14, "Извозъ", 2000, 0, group=groups.AutomotiveGroup, position=(8, 2)),  # Событие
            Tile(15, "Лѣпажъ", 12000, 50, position=(7, 2)),
            Tile(16, "Братія Райтъ", 20000, 30, position=(6, 2)),
            Tile(17, "Банкъ", 2000, tile_type="bank", position=(5, 2)),
            Tile(18, "Махорка", 5000, 15, position=(4, 2)),  # Обычная клетка предприятия
            Tile(19, "Фордъ", 8000, 0, group=groups.AutomotiveGroup, tile_type="event", position=(3, 2)),  # Событие
            Tile(20, "Голландъ-Голландъ", 2000, 20, position=(2, 2)),  # Обычная клетка предприятия
            Tile(21, "Рулѣтка", 0, 0, tile_type="casino", position=(1, 2)),  # Казино
            Tile(22, "Бобровъ и Ко", 2000, 15, position=(0, 2)),  # Обычная клетка предприятия

            Tile(23, "Околотокъ", 8000, 0, tile_type="jail", position=(0, 3)),  # Тюрьма

            Tile(24, "Крупъ", 50000, 50, position=(0, 4)),
            Tile(25, "Савой", 15000, 30, group=groups.HotelGroup, logo=hotel_logo, position=(1, 4)),
            Tile(26, "Остінъ", 10000, 50, group=groups.AutomotiveGroup, logo=car_factory_logo, position=(2, 4)),
            Tile(27, "Сытінъ", 3000, 20, group=groups.GroceryGroup, position=(3, 4)),
            Tile(28, "Банкъ", 2000, tile_type="bank", position=(4, 4)),
            Tile(29, "Фіатъ", 20000, 50, position=(5, 4)),
            Tile(30, "Рулѣтка", 0, tile_type="casino", position=(6, 4)),  # Казино
            Tile(31, "Мѣха", 7000, 50, position=(7, 4)),
            Tile(32, "Ціркъ", 7000, 50, position=(8, 4)),
            Tile(33, "Зауэръ", 2000, 20, position=(9, 4)),
            Tile(34, "Медъ", 7000, 20, group=groups.GroceryGroup, position=(10, 4)),

            Tile(35, "Околотокъ", 0, 0, tile_type="jail", position=(10, 5)),  # Тюрьма

            Tile(36, "Асторія", 2000, 30, group=groups.HotelGroup, logo=hotel_logo, position=(10, 6)),
            Tile(37, "Банкъ", 2000, tile_type="bank", position=(9, 6)),
            Tile(38, "Яхта", 3000, 15, position=(8, 6)),  # Обычная клетка предприятия
            Tile(39, "Кофій", 4000, 15, group=groups.GroceryGroup, position=(7, 6)),  # Обычная клетка предприятия
            Tile(40, "Дагѣръ", 9000, 15, position=(6, 6)),  # Обычная клетка предприятия
            Tile(41, "Салонъ", 8000, 15, position=(5, 6)),  # Обычная клетка предприятия
            Tile(42, "Кольтъ", 3000, 15, position=(4, 6)),  # Обычная клетка предприятия
            Tile(43, "Данхілъ", 5000, 15, position=(3, 6)),  # Обычная клетка предприятия
            Tile(44, "Бѣнтли", 10000, 0, group=groups.AutomotiveGroup, tile_type="event", position=(2, 6)),  # Событие
            Tile(45, "Чай", 7000, 15, group=groups.GroceryGroup, position=(1, 6)),  # Обычная клетка предприятия
            Tile(46, "Тула", 4000, 20, position=(0, 6)),  # Обычная клетка предприятия

            # Tile(24, "Событие", 0, 0, tile_type="event", position=(0, 4)),  # Событие
            # Tile(25, "Автозавод", 500, 50, group=groups.AutomotiveGroup, logo=car_factory_logo, position=(1, 4)),
            # Tile(26, "Гостиница", 300, 30, group=groups.HotelGroup, logo=hotel_logo, position=(2, 4)),
            # Tile(27, "Магазин продуктов", 200, 20, group=groups.GroceryGroup, position=(3, 4)),
            # Tile(28, "Аптека", 150, 15, position=(4, 4)),  # Обычная клетка предприятия
            # Tile(29, "Событие", 0, 0, tile_type="event", position=(5, 4)),  # Событие

            # Tile(47, "Околотокъ", 0, 0, tile_type="jail", position=(10, 5)),  # Тюрьма
        ]

    def get_sorted(self):
        rows = {}
        for tile in self.tiles:
            x, y = tile.position
            row = rows.get(y)
            if row is None:
                row = {}
            row[x] = tile
            rows[y] = row

        for j in sorted(rows.keys()):
            for i in sorted(rows[j].keys()):
                yield rows[j][i]

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
        for tile in self.get_sorted():
            tile.draw_tile(screen, tile.position, offset, players)
