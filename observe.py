class Event:
    """
    Object sent by the Observable.notify() call
    This will be passed to callables being notified
    """
    def __init__(self, name, source, kw):
        """
        :param name: The event being fired
        :param source: the source of the event (Observable object)
        :param kw: a dictionary to attach data
        """
        self.name = name
        self.source = source
        self.kwargs = kw

    def __str__(self):
        return self.name


class Observable:
    def __init__(self):
        # dicts of form {eventname: [callbacks]}
        self.callbacks = {}

    def remove_event(self, eventname):
        """
        Removes an event
        Will just do nothing if event is not already a key in callbacks
        :param eventname: the name of the vent to remove
        :return:
        """
        self.callbacks.pop(eventname, None)

    def subscribe(self, eventname, callback):
        """
        Add a callback to an event
        :param eventname: the event name to add a callback for (string)
        :param callback: a callable to be run when notify() is called, must take only one required argument
        """
        if eventname not in self.callbacks.keys():
            self.callbacks[eventname] = [callback]
        else:
            self.callbacks[eventname].append(callback)

    def unsubscribe(self, eventname, callback):
        """
        Unsubscribe a callback from an event
        NB: If a callback has been subscribed twice, only one instance will be removed
        :param eventname: the event to remove from (string)
        :param callback: the callable to remove
        """
        if eventname in self.callbacks.keys():
            if callback in self.callbacks[eventname]:
                self.callbacks[eventname].remove(callback)

    def notify(self, eventname, **kwargs):
        """
        Call all callbacks for the given events
        :param eventname: the event to notify for (string)
        :param kwargs: keyword args to pass with the event object
        """
        event = Event(eventname, self, kwargs)

        if event.name in self.callbacks.keys():
            for fn in self.callbacks[event.name][:]:
                fn(event)
