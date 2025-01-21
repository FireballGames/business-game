import pygame


def align_left(bounds, rect):
    rect.topleft = bounds.topleft
    rect.height = bounds.height

    bounds.width -= rect.width
    bounds.left += rect.width

    return rect, bounds


def align_right(bounds, rect):
    rect.topright = bounds.topright
    rect.height = bounds.height

    bounds.width -= rect.width

    return bounds, rect


def align_top(bounds, rect):
    rect.topleft = bounds.topleft
    rect.width = bounds.width

    bounds.height -= rect.height
    bounds.top += rect.height

    return rect, bounds


def align_bottom(bounds, rect):
    rect.bottomleft = bounds.bottomleft
    rect.width = bounds.width

    bounds.height -= rect.height

    return bounds, rect


def horyzontal(bounds, left=None, right=None):
    if left is not None:
        for rect in left:
            align_left(bounds, rect)
            yield rect

    yield bounds

    if right is not None:
        for rect in right:
            align_right(bounds, rect)
            yield rect


def vertical(bounds, top=None, bottom=None):
    if top is not None:
        for rect in top:
            align_top(bounds, rect)
            yield rect

    yield bounds

    if bottom is not None:
        for rect in bottom:
            align_bottom(bounds, rect)
            yield rect

