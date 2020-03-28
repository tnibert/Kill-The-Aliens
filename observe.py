class Event:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Observable:
    def __init__(self):
        self.callbacks = []

    def subscribe(self, callback):
        self.callbacks.append(callback)

    def notify(self, event):
        event.source = self
        # change to string to avoid circular imports
        # something like "<class 'player.Player'>"
        event.sourcestr = str(type(self))
        for fn in self.callbacks:
            fn(event)
