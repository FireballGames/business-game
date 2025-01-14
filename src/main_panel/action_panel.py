from controls.panel import Panel


class ActionPanel(Panel):
    width = 1250
    height = 227

    def update(self):
        self.image.fill((255, 0, 0, 32))
        self.controls.update()
        super().update()
