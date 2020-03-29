from observe import Observable, Event
import time


class Timer(Observable):
    def __init__(self):
        Observable.__init__(self)
        # for general tick
        self.prevtime = time.time()
        # for stopwatch timing
        self.start = None
        self.threshold = None

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
                self.notify(Event("timeout"))
                self.start = None
                self.threshold = None

        return diff
