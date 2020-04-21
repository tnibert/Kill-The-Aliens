from gamestrategy import Strategy
from enemy import Enemy
from gamemap import GameMap
from statusmodifiers import OneUp, Bomb, SpeedUp, MoreGuns
from utilfuncs import switch
from timer import Timer
from textelement import TextElement
from player import Player
from endgamesignal import EndLevel
from loadstaticres import shipimg, oneupimg, moregunsimg, speedupimg, bombimg
from constants import NEW_SAUCER_IVAL, SAUCER_THRESHOLD, SCREENW, TEXT_SIZE, BOSSHEALTH
import random
import pygame


class Level(Strategy):
    """
    Strategy for managing progression of typical game level
    """
    def __init__(self, scene, inputqueue, mixer, config):
        """
        :param scene: Scene object to manipulate
        :param inputqueue: Queue object to receive input from
        :param mixer: pygame.mixer object
        :param config: dictionary of level specific resources
        """
        super().__init__(scene)
        self.mixer = mixer
        self.config = config

        # load up music
        self.mixer.music.load(self.config["bg_music_fname"])

        # set up player
        self.ship = Player(shipimg, inputqueue)
        self.scene.attach(self.ship)
        # enable firing of bullets
        self.ship.subscribe("fire", lambda ev: self.scene.attach(ev.kwargs.get("bullet")))

        # set up map
        map_bg = self.config["background"].convert()
        self.game_map = GameMap(map_bg)
        self.scene.attach(self.game_map)

        # so that map speed up resets on player death
        self.ship.subscribe("player_respawn", self.game_map.reset_speed)

        # setup labels
        # todo: improve font and color
        gamefont = pygame.font.SysFont("monospace", TEXT_SIZE)
        textcolor = (255, 255, 0)
        text_x_loc = SCREENW - 180
        text_y_loc_start = 20

        # add health and score labels
        self.health_label = TextElement(text_x_loc, text_y_loc_start, gamefont,
                                        textcolor, "Health: {}", self.ship.health)
        self.score_label = TextElement(text_x_loc, text_y_loc_start+TEXT_SIZE, gamefont, textcolor, "Score: {}", 0)
        self.boss_health_label = TextElement(text_x_loc, text_y_loc_start+TEXT_SIZE*2,
                                             gamefont, textcolor, "Boss: {}", BOSSHEALTH)

        self.ship.subscribe("alterhealth", self.health_label.update_value)

        self.scene.attach(self.health_label)
        self.scene.attach(self.score_label)

        # create initial enemies
        self.saucers = []
        for x in range(0, 3):
            newsaucer = Enemy(self.config["enemy_image"])
            newsaucer.subscribe("score_up", self.score_label.update_value)
            self.saucers.append(newsaucer)
            self.scene.attach(newsaucer)

        self.saucer_timer = Timer()
        self.saucer_timer.subscribe("timeout", self.add_saucer)
        self.saucer_timer.startwatch(NEW_SAUCER_IVAL)

    def run_game(self):
        try:
            if not self.mixer.music.get_busy():
                # start music on endless loop
                self.mixer.music.play(-1)

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
