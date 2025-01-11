class Group:
    name = None
    color = None

# Инициализация групп предприятий


class AutomotiveGroup(Group):
    name = "Автомобильное производство"
    color = (0, 255, 255)


class HotelGroup(Group):
    name  = "Гостиницы"
    color = (255, 0, 255)


class GroceryGroup(Group):
    name  = "Магазины продуктов"
    color = (255, 255, 0)
