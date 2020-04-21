from gamestrategy import Strategy
from gameobject import GameObject
from constants import SCREENH
from endgamesignal import EndLevel


class SplashPage(Strategy):
    def __init__(self, scene, inputqueue, image, trigger_key):
        super().__init__(scene)
        self.inputqueue = inputqueue
        self.trigger_key = trigger_key
        splash = GameObject(0, SCREENH/2 - image.get_height()/2, image)
        self.scene.attach(splash)

    def run_game(self):
        # read for trigger key
        while not self.inputqueue.empty():
            event = self.inputqueue.get_nowait()
            if event.key == self.trigger_key:
                raise EndLevel({"state": "continue"})

        super().run_game()
