import pygame


def load_logos_from_spritesheet(spritesheet_path, tile_width, tile_height, rows, cols):
    """
    Загружает логотипы из спрайтлиста.

    :param spritesheet_path: Путь к изображению спрайтлиста.
    :param tile_width: Ширина одного логотипа.
    :param tile_height: Высота одного логотипа.
    :param rows: Количество строк в спрайтлисте.
    :param cols: Количество колонок в спрайтлисте.
    :return: Список загруженных логотипов.
    """
    # Загружаем изображение спрайтлиста
    spritesheet = pygame.image.load(spritesheet_path).convert_alpha()

    # Список для логотипов
    logos = []

    # Извлечение каждого логотипа
    for row in range(rows):
        for col in range(cols):
            x = col * tile_width
            y = row * tile_height
            rect = pygame.Rect(x, y, tile_width, tile_height)
            logo = spritesheet.subsurface(rect)
            logos.append(logo)

    return logos
