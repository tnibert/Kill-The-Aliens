from gamestrategy import Strategy
from gameobject import GameObject
from constants import SCREENH
from endgamesignal import EndLevel


class SplashPage(Strategy):
    """
    A level strategy in which we display a spash page until
    a specified key is pressed.
    """

    def __init__(self, scene, inputqueue, image, trigger_key):
        """
        :param scene: Scene object
        :param inputqueue: Queue object for the input
        :param image: a static image to display
        :param trigger_key: the key the user must type to continue
        """
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
