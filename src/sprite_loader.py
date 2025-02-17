"""Загрузки спратлистов из файлов."""

import pygame


def __load_from_spritesheet(spritesheet_path, tile_width, tile_height, rows, cols):
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

    # Извлечение каждого логотипа
    for row in range(rows):
        for col in range(cols):
            x = col * tile_width
            y = row * tile_height
            rect = pygame.Rect(x, y, tile_width, tile_height)
            yield spritesheet.subsurface(rect)


def load_logos():
    """Загружает логотипы компаний.

    Returns:
        List[pygame.Surface]: список изображений логотипов.
    """
    # Параметры спрайтлиста
    path = "res/logo_spritesheet.png"  # Путь к спрайтлисту
    images = __load_from_spritesheet(path, 128, 128, 4, 4)
    return list(images)


def load_tokens():
    """Загружает фишки игроков.

    Returns:
        List[pygame.Surface]: список изображений фишек.
    """
    # Параметры спрайтлиста
    path = "res/player_spritesheet.png"  # Путь к спрайтлисту
    images = __load_from_spritesheet(path, 128, 128, 4, 4)
    return list(images)


def load_portraits():
    """Загружает портреты игроков.

    Returns:
        List[pygame.Surface]: список портретов.
    """
    # Параметры спрайтлиста
    path = "res/characters.png"  # Путь к спрайтлисту
    images = __load_from_spritesheet(path, 210, 210, 4, 4)
    return list(images)
