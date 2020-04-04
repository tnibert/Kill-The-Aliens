class Event:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Observable:
    # todo: unit test
    def __init__(self):
        # dicts of form {eventname: [callbacks]}
        self.callbacks = {}

    def subscribe(self, eventname, callback):
        if eventname not in self.callbacks.keys():
            self.callbacks[eventname] = [callback]
        else:
            self.callbacks[eventname].append(callback)

    def unsubscribe(self, eventname, callback):
        if eventname in self.callbacks.keys():
            if callback in self.callbacks[eventname]:
                self.callbacks[eventname].remove(callback)
                print("callback removed from {}".format(eventname))

    def notify(self, eventname, **kwargs):
        event = Event(eventname)
        event.source = self
        event.kwargs = kwargs

        if event.name in self.callbacks.keys():
            for fn in self.callbacks[event.name][:]:
                fn(event)
