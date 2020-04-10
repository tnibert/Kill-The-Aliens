from gamestrategy import Strategy
from enemy import Enemy
from gamemap import GameMap
from statusmodifiers import OneUp, Bomb, SpeedUp, MoreGuns
from utilfuncs import switch
from timer import Timer
from textelement import TextElement
from player import Player
from boss import Boss
from loadstaticres import *
from constants import NEW_SAUCER_IVAL, SAUCER_THRESHOLD, SCREENW, TEXT_SIZE
import random


class Level(Strategy):
    def __init__(self, scene, inputqueue):
        super().__init__(scene)

        # set up player
        self.ship = Player(shipimg, inputqueue)
        self.scene.attach(self.ship)
        # enable firing of bullets
        self.ship.subscribe("fire", lambda ev: self.scene.attach(ev.kwargs.get("bullet")))

        # set up map
        map_bg = background.convert()
        self.game_map = GameMap(map_bg)
        self.scene.attach(self.game_map)

        # create initial enemies
        self.saucers = []
        for x in range(0, 3):
            newsaucer = Enemy(saucerimg)
            self.saucers.append(newsaucer)
            self.scene.attach(newsaucer)

        self.saucer_timer = Timer()
        self.saucer_timer.subscribe("timeout", self.add_saucer)
        self.saucer_timer.startwatch(NEW_SAUCER_IVAL)

        # setup labels
        gamefont = pygame.font.SysFont("monospace", TEXT_SIZE)
        textcolor = (255, 255, 0)
        text_x_loc = SCREENW - 130
        text_y_loc_start = 20

        # add health and score labels
        self.health_label = TextElement(text_x_loc, text_y_loc_start, gamefont, textcolor, "Health: {}", self.ship.health)
        self.score_label = TextElement(text_x_loc, text_y_loc_start+TEXT_SIZE, gamefont, textcolor, "Score: {}", 0)

        self.ship.subscribe("death", self.health_label.update_value)

        self.scene.attach(self.health_label)
        self.scene.attach(self.score_label)

    def run_game(self):
        self.saucer_timer.tick()

        # determine if we should have a status modifier
        # so apparently there's no switch/case in python >_>
        # choose a random number, determine which powerup based on number, if not 1 - 6 just continue on w/ no stat mod
        for case in switch(random.randrange(0, 10000)):
            statmod = None
            if case(1):
                statmod = OneUp(oneupimg)
            elif case(90):
                statmod = Bomb(bombimg)
            elif case(1337):
                statmod = SpeedUp(speedupimg)
                statmod.subscribe("collision", self.game_map.receive_signals)
            elif case(511):
                statmod = MoreGuns(moregunsimg)
            if statmod is not None:
                # todo: make the receiving function more specific
                print("statmod created")
                statmod.subscribe("collision", self.ship.on_collide)
                self.scene.attach(statmod)

        super().run_game()

    def add_saucer(self, event):
        """
        Event handler for saucer add timeout
        :param event:
        :return:
        """
        if len(self.saucers) < SAUCER_THRESHOLD:
            newsaucer = Enemy(saucerimg)
            self.saucers.append(newsaucer)
            self.scene.attach(newsaucer)
            self.saucer_timer.startwatch(NEW_SAUCER_IVAL)
        else:
            # clear out the saucers and enter the boss
            self.clear_saucers()
            self.scene.attach(Boss(SCREENW/2-bossimg.get_width()/2, -1200, bossimg, self.ship))

    def clear_saucers(self):
        for s in self.saucers:
            s.leave()
        self.saucers.clear()
