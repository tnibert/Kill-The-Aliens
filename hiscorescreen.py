from splashpage import SplashPage
from constants import SCORE_FILE, SCREENH, LVL_START_FONT, TEXTCOLOR_WHITE, VAL_FONT, TEXTCOLOR, LEVEL_START_TEXT_SIZE
from textelement import TextElement


class HiScoreScreen(SplashPage):
    def __init__(self, scene, input_queue, image, trigger_key, score):
        super().__init__(scene, input_queue, image, trigger_key)
        self.error = None

        self.finalscore = TextElement(0, 0, LVL_START_FONT, TEXTCOLOR_WHITE, "SCORE: {}", val=score)
        self.finalscore.center()
        self.newhigh = TextElement(0, 0, LVL_START_FONT, TEXTCOLOR_WHITE, "NEW HISCORE")
        self.newhigh.center()

        try:
            top_score = self.read_score()
            if top_score < score:
                # new high score
                self.scene.attach(self.newhigh)
                top_score = score
                self.write_score()
            else:
                self.scene.attach(self.finalscore)

        except IOError:
            try:
                top_score = self.write_score()
                self.scene.attach(self.newhigh)
            except IOError as e:
                # present error to the user if we have failed here
                self.error = TextElement(0, 0, VAL_FONT, TEXTCOLOR, "Error: {}", val=str(e))
                self.scene.attach(self.error)
                top_score = score

        self.highscore = TextElement(0, SCREENH - LEVEL_START_TEXT_SIZE * 1.5,
                                     LVL_START_FONT, TEXTCOLOR_WHITE, "HISCORE: {}", val=top_score)
        self.highscore.center()

        self.scene.attach(self.highscore)

    def read_score(self):
        with open(SCORE_FILE, "r") as fi:
            value = int(fi.read())
            return value

    def write_score(self):
        with open(SCORE_FILE, "w") as fi:
            fi.write(str(self.finalscore.get_value()))
        return self.finalscore.get_value()
