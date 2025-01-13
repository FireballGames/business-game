"""Данные о группах предприятий."""

class Group:
    """Базовая группа."""

    def __init__(self, name, color=(255, 255, 255)):
        self.name = name
        self.color = color

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"Group({self.name})"

# Инициализация групп предприятий

automotive_group = Group(
    name="Автомобильное производство",
    color=(0, 255, 255),
)

hotel_group = Group(
    name="Гостиницы",
    color=(255, 0, 255),
)

grocery_group = Group(
    name="Магазины продуктов",
    color=(255, 255, 0),
)
