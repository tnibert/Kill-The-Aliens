from gamestrategy import Strategy
from enemy import Enemy
from gamemap import GameMap
from statusmodifiers import OneUp, Bomb, SpeedUp, MoreGuns
from utilfuncs import switch
from timer import Timer
from textelement import TextElement
from endgamesignal import EndLevel
from loadstaticres import oneupimg, moregunsimg, speedupimg, bombimg
from constants import NEW_SAUCER_IVAL, SAUCER_THRESHOLD, SCREENW, SCREENH, VAL_TEXT_SIZE, BOSSHEALTH, VAL_X_LOC, VAL_FONT, VAL_Y_LOC_START, TEXTCOLOR, INITIAL_SAUCERS, LVL_START_FONT, LVL_START_TIME
import random


class Level(Strategy):
    """
    Strategy for managing progression of typical game level
    """
    def __init__(self, scene, mixer, config, universal):
        """
        Declare and assign variables
        :param scene: Scene object to manipulate
        :param mixer: pygame.mixer object
        :param config: dictionary of level specific resources
        :param universal: dictionary of objects that stay in use between levels
        """

        super().__init__(scene)
        self.mixer = mixer
        self.config = config

        # set up player
        self.ship = universal["ship"]

        # set up map
        self.game_map = GameMap(self.config["background"].convert())

        # add health and score labels
        self.health_label = universal["health_label"]
        self.score_label = universal["score_label"]
        self.boss_health_label = TextElement(VAL_X_LOC, VAL_Y_LOC_START+VAL_TEXT_SIZE*2,
                                             VAL_FONT, TEXTCOLOR, "Boss: {}", BOSSHEALTH)
        self.level_start_label = TextElement(SCREENW/4, SCREENH/4, LVL_START_FONT, TEXTCOLOR, self.config["start_text"])

        self.start_text_timer = Timer()

        self.saucers = []

        self.saucer_timer = Timer()

    def setup(self):
        """
        Attach objects to scene and set up subscriptions
        """
        # clear relevant subscriptions on shared objects from previous levels
        self.ship.remove_event("fire")
        self.ship.remove_event("player_respawn")

        # load up music
        self.mixer.music.load(self.config["bg_music_fname"])

        # enable firing of bullets
        self.ship.subscribe("fire", lambda ev: self.scene.attach(ev.kwargs.get("bullet")))

        # so that map speed up resets on player death
        self.ship.subscribe("player_respawn", self.game_map.reset_speed)

        self.saucer_timer.subscribe("timeout", self.add_saucer)

        self.start_text_timer.subscribe("timeout", self.remove_start_text)

        # create initial enemies
        for x in range(0, INITIAL_SAUCERS):
            newsaucer = Enemy(self.config["enemy_image"])
            newsaucer.subscribe("score_up", self.score_label.update_value)
            self.saucers.append(newsaucer)
            self.scene.attach(newsaucer)

        self.scene.attach(self.ship)
        self.scene.attach(self.game_map)
        self.scene.attach(self.health_label)
        self.scene.attach(self.score_label)
        self.scene.attach(self.level_start_label)

        self.saucer_timer.startwatch(NEW_SAUCER_IVAL)
        self.start_text_timer.startwatch(LVL_START_TIME)

    def run_game(self):
        try:
            if not self.mixer.music.get_busy():
                # start music on endless loop
                self.mixer.music.play(-1)

            if self.start_text_timer.is_timing():
                self.start_text_timer.tick()

            self.saucer_timer.tick()

            # determine if we should have a status modifier
            # so apparently there's no switch/case in python >_>
            # choose a random number, determine which powerup based on number
            for case in switch(random.randrange(0, 10000)):
                statmod = None
                if case(1):
                    statmod = OneUp(oneupimg)
                elif case(90):
                    statmod = Bomb(bombimg)
                elif case(1337):
                    statmod = SpeedUp(speedupimg)
                    statmod.subscribe("collision", self.game_map.increase_speed)
                elif case(511):
                    statmod = MoreGuns(moregunsimg)
                if statmod is not None:
                    self.scene.attach(statmod)

            super().run_game()

        # intercept the EndLevel signal, stop music, and attach score
        except EndLevel as e:
            self.mixer.music.stop()
            info = e.args[0]
            info['score'] = self.score_label.get_value()
            raise EndLevel(info)

    def remove_start_text(self, event):
        self.scene.remove(self.level_start_label)

    def add_saucer(self, event):
        """
        Event handler for saucer add timeout
        :param event:
        :return:
        """
        if len(self.saucers) < SAUCER_THRESHOLD:
            newsaucer = Enemy(self.config["enemy_image"])
            newsaucer.subscribe("score_up", self.score_label.update_value)
            self.saucers.append(newsaucer)
            self.scene.attach(newsaucer)
            self.saucer_timer.startwatch(NEW_SAUCER_IVAL)
        else:
            # clear out the saucers and enter the boss
            self.clear_saucers()
            boss = self.config["boss_class"](SCREENW/2-self.config["boss_image"].get_width()/2,
                                             -1200,
                                             self.config["boss_image"],
                                             self.ship)
            boss.subscribe("health_down", self.boss_health_label.update_value)
            boss.subscribe("fire", lambda ev: self.scene.attach(ev.kwargs.get("bullet")))
            self.scene.attach(boss)
            self.scene.attach(self.boss_health_label)

    def clear_saucers(self):
        for s in self.saucers:
            s.leave()
        self.saucers.clear()
