from gameobject import GameObject
from constants import TEXT_LAYER, SCREENW


class TextElement(GameObject):
    def __init__(self, x, y, font, color, text, val=None):
        """
        GameObject to show text on the screen.
        Used to display labels with values (e.g. score, health, etc)
        :param x: x position
        :param y: y position
        :param font: mygame.font object
        :param color: tuple of (r,g,b) ints 0 to 255
        :param text: the label with {} formatting for insertion
        :param val: optional numeric value to track
        """
        self.value = val
        self.defaulttext = text
        self.text = self.defaulttext.format(self.value)

        self.color = color
        self.font = font

        super().__init__(x, y, self.font.render(self.text, 1, self.color), layer=TEXT_LAYER)

    def update_value(self, event):
        """
        Event handler to change the displayed value
        :param event: event object containing kwarg key "value"
                      which is a positive or negative number to change self.value
        """
        if event.kwargs.get("value") is not None:
            self.value += event.kwargs.get("value")
            self.text = self.defaulttext.format(self.value)
            self.image = self.font.render(self.text, 1, self.color)

    def get_value(self):
        return self.value

    def center(self):
        self.x = SCREENW / 2 - self.image.get_width() / 2
