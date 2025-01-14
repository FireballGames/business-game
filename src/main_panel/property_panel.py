from controls.panel import Panel


class PropertyPanel(Panel):
    width = 1250
    height = 172

    def update(self):
        self.image.fill((0, 0, 255, 32))
        self.controls.update()
        super().update()
