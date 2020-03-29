class Event:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Observable:
    def __init__(self):
        # dicts of form {eventname: [callbacks]}
        self.callbacks = {}

    def subscribe(self, eventname, callback):
        if eventname not in self.callbacks.keys():
            self.callbacks[eventname] = [callback]
        else:
            self.callbacks[eventname].append(callback)

    def notify(self, event):
        event.source = self

        if event.name in self.callbacks.keys():
            for fn in self.callbacks[event.name]:
                fn(event)
