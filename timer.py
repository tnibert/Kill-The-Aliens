from observe import Observable, Event
import time


class Timer(Observable):
    def __init__(self, owner=None):
        """

        :param owner: An optional Observable to send the timeout event from
        """
        Observable.__init__(self)
        # for general tick
        self.prevtime = time.time()
        # for stopwatch timing
        self.start = None
        self.threshold = None
        self.owner = owner

    def startwatch(self, seconds):
        self.start = time.time()
        self.threshold = seconds

    def tick(self):
        curtime = time.time()

        diff = curtime - self.prevtime
        self.prevtime = curtime

        # if stop watch is running
        if self.start:
            if (curtime - self.start) > self.threshold:

                # allows the callback to start another timer
                self.start = None
                self.threshold = None

                if self.owner is not None:
                    self.owner.notify(Event("timeout"))
                else:
                    self.notify(Event("timeout"))

        return diff
