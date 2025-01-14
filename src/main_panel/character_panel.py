from controls.panel import Panel


class CharacterPanel(Panel):
    width = 137
    height = 589

    def update(self):
        self.image.fill((0, 255, 0, 32))
        self.controls.update()
        super().update()
