from controls.panel import Panel


class FieldPanel(Panel):
    width = 1109
    height = 589

    def __init__(self, *groups, rect=None, field=None):
        super().__init__(*groups, rect=None)
        self.players = None
        self.field = field

    def process_event(self, event):
        self.field.update(event)

    def update_data(self, players):
        self.players = players

    def update(self):
        self.image.fill((0, 0, 0, 128))
        self.controls.update()
        super().update()
        if self.field is not None:
            # Отрисовка игрового поля
            self.field.draw(self.image, self.players)
